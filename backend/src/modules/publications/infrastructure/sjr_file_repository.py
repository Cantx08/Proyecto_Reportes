from functools import lru_cache
import unicodedata
import logging
import pandas as pd
from typing import Dict, Tuple, List
from collections import defaultdict

from ..domain.sjr_repository import ISJRRepository

logger = logging.getLogger(__name__)

class SJRFileRepository(ISJRRepository):
    """
    Repositorio de datos SJR basado en archivo CSV.
    Implementa lógica de cálculo para identificar el Top 10% de publicaciones.
    
    Estrategia de búsqueda:
    1. Búsqueda primaria por ISSN (impreso/electrónico)
    2. Fallback por nombre normalizado de revista
    """

    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        # Caché primario: (issn_normalizado, año) -> (áreas, categorías)
        self._issn_cache: Dict[Tuple[str, int], Tuple[List[str], List[str]]] = {}
        # Caché secundario (fallback): (nombre_normalizado, año) -> (áreas, categorías)
        self._name_cache: Dict[Tuple[str, int], Tuple[List[str], List[str]]] = {}
        self._max_year_available: int = 0
        self._load_data()

    def get_max_available_year(self) -> int:
        return self._max_year_available

    def get_journal_data(
        self, 
        issns: List[str], 
        publication_year: int,
        source_title: str = ""
    ) -> Tuple[List[str], List[str], int]:
        """
        Busca datos de la revista usando ISSNs con fallback por nombre.
        
        Args:
            issns: Lista de ISSNs (impreso y/o electrónico) de la publicación
            publication_year: Año de la publicación
            source_title: Nombre de la revista (fallback si no hay match por ISSN)
        """
        if not self._issn_cache and not self._name_cache:
            return [], [], publication_year
        
        target_year = self._resolve_year(publication_year)
        
        # 1. Búsqueda primaria por ISSN
        for issn in issns:
            if not issn:
                continue
            clean_issn = self._normalize_issn_input(issn)
            data = self._issn_cache.get((clean_issn, target_year))
            if data:
                areas, categories = data
                logger.debug(f"SJR match por ISSN '{clean_issn}' año {target_year}")
                return areas, categories, target_year
        
        # 2. Fallback por nombre de revista
        if source_title:
            normalized_name = self.normalize_journal_name(source_title)
            data = self._name_cache.get((normalized_name, target_year))
            if data:
                areas, categories = data
                logger.debug(f"SJR match por nombre '{source_title}' año {target_year}")
                return areas, categories, target_year
        
        if issns or source_title:
            logger.debug(
                f"Sin match SJR: ISSNs={issns}, título='{source_title}', año={target_year}"
            )
        
        return [], [], target_year

    @staticmethod
    def _normalize_issn_input(issn: str) -> str:
        """Limpia un ISSN individual para búsqueda."""
        clean = issn.replace('-', '').strip()
        # Si por alguna razón quedó de 7 dígitos (ej: Excel se comió el cero antes de llegar aquí),
        # intentamos rellenar, aunque Scopus suele enviarlo bien.
        if len(clean) == 7 and clean.isdigit():
            clean = clean.zfill(8)
        return clean

    @lru_cache(maxsize=2048)
    def normalize_journal_name(self, name: str) -> str:
        if not isinstance(name, str):
            name = str(name) if name else ""
        
        name = name.lower().strip()
        name = unicodedata.normalize('NFKD', name)
        name = ''.join(c for c in name if not unicodedata.combining(c))
        name = name.replace('&', 'and')
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        name = ' '.join(name.split())
        return name

    def _resolve_year(self, requested_year: int) -> int:
        if self._max_year_available > 0 and requested_year > self._max_year_available:
            return self._max_year_available
        return requested_year

    def _load_data(self) -> None:
        """
        Carga el CSV, calcula percentiles y puebla el caché indexado por ISSN.
        """
        try:
            # 1. Cargar Dataframe forzando tipos string para evitar que pandas elimine ceros
            # 'dtype=str' es crucial para leer ISSNs como "01234567" y no 1234567
            df = pd.read_csv(self._csv_path, sep=';', decimal=',', dtype=str)
            
            # Limpiar nombres de columnas (strip espacios)
            df.columns = [c.strip() for c in df.columns]

            # CORRECCIÓN CRÍTICA 1: Detectar columna ISSN sin importar mayúsculas/minúsculas
            col_map = {c.lower(): c for c in df.columns}
            issn_col_name = col_map.get('issn') # Busca 'issn', 'Issn', 'ISSN'
            
            rank_col = 'Rank'
            if 'Rank' not in df.columns and 'SJR Rank' in df.columns:
                rank_col = 'SJR Rank'
            
            # Convertir Rank y Year a numéricos (ya que leímos todo como string)
            df[rank_col] = pd.to_numeric(df[rank_col], errors='coerce').fillna(float('inf'))
            df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)

            # Normalizar Título
            df['Title_norm'] = df['Title'].apply(self.normalize_journal_name)
            
            # Manejo de Issn
            if issn_col_name:
                df['Issn_Final'] = df[issn_col_name].fillna('')
            else:
                logger.warning("¡Columna ISSN no encontrada en el CSV de SJR!")
                df['Issn_Final'] = ''
            
            # Detectar año máximo
            self._max_year_available = int(df['year'].max()) if not df.empty else 0

            # --- FASE 1: Construir universos Q1 ---
            q1_universes: Dict[Tuple[int, str], List[float]] = defaultdict(list)
            processed_rows = []

            for _, row in df.iterrows():
                try:
                    year = int(row.get('year', 0))
                    rank = float(row.get(rank_col, float('inf')))
                    title_norm = row['Title_norm']
                    areas_str = str(row.get('Areas', ''))
                    categories_str = str(row.get('Categories', ''))
                    issn_str = str(row.get('Issn_Final', ''))

                    parsed_cats = self._parse_categories_structured(categories_str)
                    
                    processed_rows.append({
                        'key': (title_norm, year),
                        'rank': rank,
                        'areas': self._parse_areas(areas_str),
                        'categories': parsed_cats,
                        'issn_raw': issn_str
                    })

                    for cat in parsed_cats:
                        if cat['quartile'] == 'Q1':
                            q1_universes[(year, cat['name'])].append(rank)

                except (ValueError, TypeError):
                    continue

            # Ordenar universos
            for key in q1_universes:
                q1_universes[key].sort()

            # --- FASE 2: Calcular percentiles y guardar caché POR ISSN y NOMBRE ---
            count_issn_entries = 0
            count_name_entries = 0
            count_missed_issn = 0
            
            for item in processed_rows:
                title_norm = item['key'][0]
                year = item['key'][1]
                my_rank = item['rank']
                final_categories_str = []

                # Lógica de Top 10%
                for cat in item['categories']:
                    cat_name = cat['name']
                    quartile = cat['quartile']
                    cat_display = f"{cat_name} ({quartile})" if quartile else cat_name

                    if quartile == 'Q1':
                        universe = q1_universes.get((year, cat_name), [])
                        total_q1 = len(universe)
                        if total_q1 > 0:
                            try:
                                new_position = universe.index(my_rank) + 1
                                percent_top = (new_position / total_q1) * 25.0
                                if percent_top <= 10.0:
                                    cat_display += f"[Categoría dentro del 10% superior ({percent_top:.1f})]"
                            except ValueError:
                                pass 
                    final_categories_str.append(cat_display)

                result_tuple = (item['areas'], final_categories_str)

                # CACHÉ PRIMARIO: por ISSN
                issn_list = self._parse_issns(item['issn_raw'])
                
                if not issn_list:
                    count_missed_issn += 1
                
                for issn in issn_list:
                    self._issn_cache[(issn, year)] = result_tuple
                    count_issn_entries += 1
                
                # CACHÉ SECUNDARIO: por nombre normalizado de revista
                if title_norm:
                    self._name_cache[(title_norm, year)] = result_tuple
                    count_name_entries += 1
            
            logger.info(
                f"SJR cargado. "
                f"Caché ISSN: {count_issn_entries} entradas. "
                f"Caché Nombre: {count_name_entries} entradas. "
                f"Revistas sin ISSN útil: {count_missed_issn}. "
                f"Año máximo: {self._max_year_available}"
            )

        except FileNotFoundError:
            logger.error(f"No se encontró el archivo SJR en {self._csv_path}")
        except Exception as e:
            logger.error(f"Error procesando SJR: {e}", exc_info=True)

    @staticmethod
    def _parse_issns(issn_str: str) -> List[str]:
        """
        Parsea y normaliza ISSNs.
        CORRECCIÓN CRÍTICA 2: Recuperar ceros a la izquierda si se perdieron.
        """
        if not issn_str or issn_str.lower() == 'nan':
            return []
        
        # Reemplazar comas por espacios para separar
        clean_str = issn_str.replace(',', ' ')
        parts = clean_str.split()
        
        results = []
        for p in parts:
            # 1. Quitar guiones y espacios
            clean_issn = p.replace('-', '').strip()
            
            # 2. Validar si es numérico y tiene longitud 7 (error común de Excel/Pandas)
            # Un ISSN (E-ISSN) tiene 8 caracteres. El último puede ser 'X'.
            if len(clean_issn) == 7 and clean_issn.isdigit():
                clean_issn = clean_issn.zfill(8)
            
            if clean_issn:
                results.append(clean_issn)
        return results

    @staticmethod
    def _parse_categories_structured(categories_str: str) -> List[Dict[str, str]]:
        if not categories_str or categories_str == 'nan':
            return []
        results = []
        parts = categories_str.split(';')
        for part in parts:
            part = part.strip()
            if not part: continue
            quartile = ""
            name = part
            if part.endswith(')'):
                last_open = part.rfind('(')
                if last_open != -1:
                    q_candidate = part[last_open+1:-1].strip()
                    if q_candidate.startswith('Q') and len(q_candidate) <= 3:
                        quartile = q_candidate
                        name = part[:last_open].strip()
            results.append({'name': name, 'quartile': quartile})
        return results

    @staticmethod
    def _parse_areas(areas_str: str) -> List[str]:
        if not areas_str or areas_str == 'nan':
            return []
        parts = areas_str.split(';')
        return [part.strip() for part in parts if part.strip()]
