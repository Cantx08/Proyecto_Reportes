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
    Implementa lógica de cálculo para identificar el Top 10% de publicaciones.
    """

    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        # Cache: (nombre_normalizado, año) -> (áreas, categorías_formateadas)
        self._data_cache: Dict[Tuple[str, int], Tuple[List[str], List[str]]] = {}
        self._max_year_available: int = 0
        self._load_data()

    def get_max_available_year(self) -> int:
        return self._max_year_available

    def get_journal_data(
        self, 
        journal_name: str, 
        publication_year: int
    ) -> Tuple[List[str], List[str], int]:
        if not self._data_cache:
            return [], [], publication_year
        
        normalized = self.normalize_journal_name(journal_name)
        target_year = self._resolve_year(publication_year)
        
        data = self._data_cache.get((normalized, target_year))
        if data:
            areas, categories = data
            return areas, categories, target_year
        
        return [], [], target_year

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
        Carga el CSV y calcula si las categorías Q1 están en el Top 10%.
        """
        try:
            # 1. Cargar Dataframe
            # IMPORTANTE: Asegúrate que el separador (sep) y decimal sean correctos para tu CSV
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
            
            # Detectar año máximo
            try:
                self._max_year_available = int(df['year'].max())
            except:
                self._max_year_available = 0

            # --- FASE 1: Construir universos de comparación (Q1) ---
            # Diccionario: {(Año, NombreCategoria): [Lista de Ranks de revistas Q1]}
            q1_universes: Dict[Tuple[int, str], List[float]] = defaultdict(list)

            # Lista temporal para no iterar el DF dos veces completamente
            processed_rows = []

            for _, row in df.iterrows():
                try:
                    year = int(row.get('year', 0))
                    rank = float(row.get(rank_col, float('inf')))
                    title_norm = row['Title_norm']
                    areas_str = str(row.get('Areas', ''))
                    categories_str = str(row.get('Categories', ''))

                    # Parsear categorías estructuradas: [{'name': 'Inmunology', 'quartile': 'Q1'}, ...]
                    parsed_cats = self._parse_categories_structured(categories_str)
                    
                    # Guardar datos básicos para la Fase 2
                    processed_rows.append({
                        'key': (title_norm, year),
                        'rank': rank,
                        'areas': self._parse_areas(areas_str),
                        'categories': parsed_cats
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

            # --- FASE 2: Calcular percentiles y guardar caché ---
            for item in processed_rows:
                year = item['key'][1]
                my_rank = item['rank']
                final_categories_str = []

                for cat in item['categories']:
                    cat_name = cat['name']
                    quartile = cat['quartile']
                    
                    # Texto base: "Immunology (Q1)"
                    cat_display = f"{cat_name} ({quartile})" if quartile else cat_name

                    # Lógica Top 10%
                    if quartile == 'Q1':
                        universe = q1_universes.get((year, cat_name), [])
                        total_q1 = len(universe)
                        
                        if total_q1 > 0:
                            try:
                                # Nueva posición: índice en la lista ordenada + 1
                                # .index() devuelve la primera ocurrencia, lo cual es correcto para empates en Rank
                                new_position = universe.index(my_rank) + 1
                                
                                # Regla de 3: Si Total_Q1 es el 25%, ¿qué % es mi posición?
                                # Porcentaje = (Posición / Total) * 25
                                percent_top = (new_position / total_q1) * 25.0
                                
                                if percent_top <= 10.0:
                                    cat_display += f"[Categoría dentro del 10% superior ({percent_top:.1f})]"
                            except ValueError:
                                pass # Rank no encontrado en universo (no debería ocurrir)

                    final_categories_str.append(cat_display)

                self._data_cache[item['key']] = (item['areas'], final_categories_str)
            
            logger.info(f"SJR cargado: {len(self._data_cache)} registros. Año máximo: {self._max_year_available}")

        except FileNotFoundError:
            logger.error(f"No se encontró el archivo SJR en {self._csv_path}")
        except Exception as e:
            logger.error(f"Error procesando SJR: {e}")

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