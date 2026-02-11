from functools import lru_cache
import unicodedata
import logging
import pandas as pd
from typing import Dict, Tuple, List, Any
from collections import defaultdict

from ..domain.sjr_repository import ISJRRepository

logger = logging.getLogger(__name__)

class SJRFileRepository(ISJRRepository):
    """
    Repositorio de datos SJR basado en archivo CSV.
    Implementa lógica de cálculo para identificar el Top 10% de publicaciones
    usando ISSN como identificador principal.
    """

    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        # CAMBIO ESTRUCTURA CACHÉ:
        # Clave: (issn_normalizado, año) -> Valor: (áreas, categorías_formateadas)
        # Un ISSN apunta a una única configuración de revista en un año.
        self._data_cache: Dict[Tuple[str, int], Tuple[List[str], List[str]]] = {}
        self._max_year_available: int = 0
        self._load_data()

    def get_max_available_year(self) -> int:
        return self._max_year_available

    def get_journal_data(
        self, 
        issns: List[str], 
        publication_year: int
    ) -> Tuple[List[str], List[str], int]:
        """
        Busca datos de la revista usando la lista de ISSNs proporcionada.
        Retorna la primera coincidencia encontrada en el caché.
        """
        if not self._data_cache:
            return [], [], publication_year
        
        target_year = self._resolve_year(publication_year)
        
        # Iteramos sobre los ISSNs que trae la publicación (print, electronic, etc.)
        for issn in issns:
            if not issn:
                continue
            
            # Buscamos en el caché por (issn, año)
            # Scimago en CSV suele tener los ISSN sin guiones o separados por coma.
            # Aquí normalizamos quitando guiones para coincidir con cómo guardamos en _load_data
            clean_issn = issn.replace('-', '').strip()
            
            data = self._data_cache.get((clean_issn, target_year))
            if data:
                areas, categories = data
                return areas, categories, target_year
        
        # Si no hubo coincidencia por ningún ISSN
        return [], [], target_year

    @lru_cache(maxsize=2048)
    def normalize_journal_name(self, name: str) -> str:
        """
        Mantenemos este método porque la Interfaz ISJRRepository lo exige,
        aunque ya no lo usemos para la búsqueda principal.
        """
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
            # 1. Cargar Dataframe
            df = pd.read_csv(self._csv_path, sep=';', decimal=',')
            
            # Normalizar nombres de columnas (strip spaces, etc)
            df.columns = [c.strip() for c in df.columns]

            # Verificar columna Rank
            rank_col = 'Rank'
            if 'Rank' not in df.columns and 'SJR Rank' in df.columns:
                rank_col = 'SJR Rank'
            
            # Asegurar tipos de datos
            df['Title_norm'] = df['Title'].apply(self.normalize_journal_name)
            df[rank_col] = pd.to_numeric(df[rank_col], errors='coerce').fillna(float('inf'))
            
            # Asegurar que existe columna Issn y convertirla a string
            if 'Issn' in df.columns:
                df['Issn'] = df['Issn'].astype(str)
            else:
                # Si no existe la columna Issn, creamos una vacía para no romper el código
                df['Issn'] = ''
            
            # Detectar año máximo
            try:
                self._max_year_available = int(df['year'].max())
            except:
                self._max_year_available = 0

            # --- FASE 1: Construir universos de comparación (Q1) ---
            # Diccionario: {(Año, NombreCategoria): [Lista de Ranks de revistas Q1]}
            q1_universes: Dict[Tuple[int, str], List[float]] = defaultdict(list)

            # Lista temporal para procesar en Fase 2
            processed_rows = []

            for _, row in df.iterrows():
                try:
                    year = int(row.get('year', 0))
                    rank = float(row.get(rank_col, float('inf')))
                    title_norm = row['Title_norm']
                    areas_str = str(row.get('Areas', ''))
                    categories_str = str(row.get('Categories', ''))
                    # Capturamos el ISSN crudo (ej: "18790534, 00104655")
                    issn_str = str(row.get('Issn', ''))

                    # Parsear categorías estructuradas
                    parsed_cats = self._parse_categories_structured(categories_str)
                    
                    # Guardar datos para la Fase 2
                    processed_rows.append({
                        'key': (title_norm, year), # Mantenemos key temporal por compatibilidad lógica
                        'rank': rank,
                        'areas': self._parse_areas(areas_str),
                        'categories': parsed_cats,
                        'issn_raw': issn_str  # Guardamos el ISSN crudo
                    })

                    # Poblar universo: Si es Q1, agregamos su rank a la lista de esa categoría
                    for cat in parsed_cats:
                        if cat['quartile'] == 'Q1':
                            q1_universes[(year, cat['name'])].append(rank)

                except (ValueError, TypeError):
                    continue

            # Ordenar las listas de ranks (ascendente: Rank 1 es mejor que Rank 20)
            for key in q1_universes:
                q1_universes[key].sort()

            # --- FASE 2: Calcular percentiles y guardar caché POR ISSN ---
            count_entries = 0
            for item in processed_rows:
                year = item['key'][1]
                my_rank = item['rank']
                final_categories_str = []

                # Cálculo de Top 10%
                for cat in item['categories']:
                    cat_name = cat['name']
                    quartile = cat['quartile']
                    
                    cat_display = f"{cat_name} ({quartile})" if quartile else cat_name

                    if quartile == 'Q1':
                        universe = q1_universes.get((year, cat_name), [])
                        total_q1 = len(universe)
                        
                        if total_q1 > 0:
                            try:
                                # Nueva posición: índice en la lista ordenada + 1
                                new_position = universe.index(my_rank) + 1
                                # Porcentaje dentro del Q1 (que es el 25% total)
                                percent_top = (new_position / total_q1) * 25.0
                                
                                if percent_top <= 10.0:
                                    cat_display += f"[Categoría dentro del 10% superior ({percent_top:.1f})]"
                            except ValueError:
                                pass 

                    final_categories_str.append(cat_display)

                # PROCESAMIENTO DE ISSN
                # Obtenemos los ISSNs limpios de esta fila
                issn_list = self._parse_issns(item['issn_raw'])
                
                # Guardamos en caché una entrada por cada ISSN que tenga la revista
                # Todos apuntan a los mismos datos calculados (áreas y categorías)
                for issn in issn_list:
                    self._data_cache[(issn, year)] = (item['areas'], final_categories_str)
                    count_entries += 1
            
            logger.info(f"SJR cargado por ISSN. Total de claves en caché: {count_entries}. Año máximo: {self._max_year_available}")

        except FileNotFoundError:
            logger.error(f"No se encontró el archivo SJR en {self._csv_path}")
        except Exception as e:
            logger.error(f"Error procesando SJR: {e}")

    @staticmethod
    def _parse_issns(issn_str: str) -> List[str]:
        """
        Convierte cadena CSV "18790534, 00104655" en lista ['18790534', '00104655'].
        Elimina guiones y espacios.
        """
        if not issn_str or issn_str.lower() == 'nan':
            return []
        
        # Scimago suele usar ", " como separador. A veces " "
        # Normalizamos reemplazando comas por espacios para split más fácil si es mixto
        clean_str = issn_str.replace(',', ' ')
        parts = clean_str.split()
        
        results = []
        for p in parts:
            # Quitamos guiones y espacios
            clean_issn = p.replace('-', '').strip()
            if clean_issn:
                results.append(clean_issn)
        return results

    @staticmethod
    def _parse_categories_structured(categories_str: str) -> List[Dict[str, str]]:
        """
        Parsea string: "Immunology (Q1); Other (Q2)" -> [{'name': 'Immunology', 'quartile': 'Q1'}, ...]
        """
        if not categories_str or categories_str == 'nan':
            return []
        
        results = []
        parts = categories_str.split(';')
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            quartile = ""
            name = part
            
            # Extraer Q1, Q2, etc.
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