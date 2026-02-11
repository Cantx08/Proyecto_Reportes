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
            # Leer CSV forzando string para no perder ceros en ISSN
            df = pd.read_csv(self._csv_path, sep=';', decimal=',', dtype=str)
            
            # Limpiar nombres de columnas
            df.columns = [c.strip() for c in df.columns]

            # Detectar columna ISSN
            col_map = {c.lower(): c for c in df.columns}
            issn_col_name = col_map.get('issn')
            
            rank_col = 'Rank'
            if 'Rank' not in df.columns and 'SJR Rank' in df.columns:
                rank_col = 'SJR Rank'
            
            # Convertir a numéricos
            df[rank_col] = pd.to_numeric(df[rank_col], errors='coerce').fillna(float('inf'))
            df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)

            df['Title_norm'] = df['Title'].apply(self.normalize_journal_name)
            
            if issn_col_name:
                df['Issn_Final'] = df[issn_col_name].fillna('')
            else:
                logger.warning("¡Columna ISSN no encontrada en el CSV de SJR!")
                df['Issn_Final'] = ''
            
            self._max_year_available = int(df['year'].max()) if not df.empty else 0

            # --- FASE 1: Construir universos COMPLETOS (Corregido) ---
            # Ahora guardamos TODOS los ranks de cada categoría, no solo los Q1.
            # Esto nos permite saber el total real de revistas (el denominador).
            category_universes: Dict[Tuple[int, str], List[float]] = defaultdict(list)
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

                    # CORRECCIÓN: Agregamos el rank a la lista de la categoría SIEMPRE.
                    # Así 'len(category_universes[key])' será el total real (ej: 71, no 72 estimado).
                    for cat in parsed_cats:
                        category_universes[(year, cat['name'])].append(rank)

                except (ValueError, TypeError):
                    continue

            # Ordenamos las listas para poder calcular la posición (ranking relativo)
            for key in category_universes:
                category_universes[key].sort()

            # --- FASE 2: Calcular percentiles y guardar caché ---
            count_issn_entries = 0
            count_name_entries = 0
            
            for item in processed_rows:
                title_norm = item['key'][0]
                year = item['key'][1]
                my_rank = item['rank']
                final_categories_str = []

                # Lógica de cálculo de Top 10%
                for cat in item['categories']:
                    cat_name = cat['name']
                    quartile = cat['quartile']
                    cat_display = f"{cat_name} ({quartile})" if quartile else cat_name

                    # Solo nos interesa marcar Top 10% si la revista ya es Q1
                    if quartile == 'Q1':
                        universe = category_universes.get((year, cat_name), [])
                        total_journals = len(universe)
                        
                        if total_journals > 0:
                            try:
                                # Encontramos la posición de mi rank en el universo completo ordenado
                                # index es 0-based, así que sumamos 1 para obtener el ranking (1st, 2nd...)
                                # Usamos .index() que retorna la primera coincidencia (mejor ranking en caso de empate)
                                real_position = universe.index(my_rank) + 1
                                
                                # CÁLCULO PRECISO: (Posición / Total Real) * 100
                                percent_top = (real_position / total_journals) * 100.0
                                
                                if percent_top <= 10.0:
                                    cat_display += f"[Categoría dentro del 10% superior ({percent_top:.1f})]"
                            except ValueError:
                                pass 
                    final_categories_str.append(cat_display)

                result_tuple = (item['areas'], final_categories_str)

                # Guardar en Caché Primario (ISSN)
                issn_list = self._parse_issns(item['issn_raw'])
                for issn in issn_list:
                    self._issn_cache[(issn, year)] = result_tuple
                    count_issn_entries += 1
                
                # Guardar en Caché Secundario (Nombre)
                if title_norm:
                    self._name_cache[(title_norm, year)] = result_tuple
                    count_name_entries += 1
            
            logger.info(
                f"SJR cargado. ISSNs: {count_issn_entries}. Nombres: {count_name_entries}. "
                f"Año máximo: {self._max_year_available}"
            )

        except FileNotFoundError:
            logger.error(f"No se encontró el archivo SJR en {self._csv_path}")
        except Exception as e:
            logger.error(f"Error procesando SJR: {e}", exc_info=True)

    @staticmethod
    def _parse_issns(issn_str: str) -> List[str]:
        if not issn_str or issn_str.lower() == 'nan':
            return []
        
        clean_str = issn_str.replace(',', ' ')
        parts = clean_str.split()
        
        results = []
        for p in parts:
            clean_issn = p.replace('-', '').strip()
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