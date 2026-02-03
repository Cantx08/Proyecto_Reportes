import unicodedata
from typing import Dict, Tuple, List

import pandas as pd

from ..domain.sjr_repository import ISJRRepository


class SJRFileRepository(ISJRRepository):
    """
    Repositorio de datos SJR basado en archivo CSV.
    
    Carga un histórico de SJR y proporciona datos de revistas
    con mapeo dinámico de años futuros al último disponible.
    """

    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        # Cache: (nombre_normalizado, año) -> (áreas, categorías_con_cuartiles)
        self._data_cache: Dict[Tuple[str, int], Tuple[List[str], List[str]]] = {}
        self._max_year_available: int = 0
        self._load_data()

    def get_max_available_year(self) -> int:
        """Retorna el año máximo disponible en el CSV."""
        return self._max_year_available

    def get_journal_data(
        self, 
        journal_name: str, 
        publication_year: int
    ) -> Tuple[List[str], List[str], int]:
        """
        Obtiene los datos SJR de una revista para un año específico.
        
        Returns:
            Tupla con (áreas, categorías_con_cuartiles, año_sjr_usado)
        """
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
        """Normaliza el nombre de una revista para búsqueda consistente."""
        if not isinstance(name, str):
            name = str(name) if name else ""
        
        name = name.lower().strip()
        # Remover acentos
        name = unicodedata.normalize('NFKD', name)
        name = ''.join(c for c in name if not unicodedata.combining(c))
        # Normalizar ampersand
        name = name.replace('&', 'and')
        # Solo alfanuméricos y espacios
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        # Normalizar espacios
        name = ' '.join(name.split())
        
        return name

    def _resolve_year(self, requested_year: int) -> int:
        """
        Resuelve el año a utilizar para la búsqueda.
        
        Si el año solicitado es mayor al disponible, retorna el último disponible.
        """
        if self._max_year_available > 0 and requested_year > self._max_year_available:
            return self._max_year_available
        return requested_year

    def _load_data(self) -> None:
        """Carga y procesa el archivo CSV de SJR."""
        try:
            df = pd.read_csv(self._csv_path, sep=';', decimal=',')
            
            # Normalizar títulos
            df['Title_norm'] = df['Title'].apply(self.normalize_journal_name)
            
            # Detectar año máximo
            max_year = 0
            for _, row in df.iterrows():
                try:
                    year = int(row.get('year', 0))
                    if year > max_year:
                        max_year = year
                except (ValueError, TypeError):
                    continue
            
            self._max_year_available = max_year
            
            # Procesar cada fila
            for _, row in df.iterrows():
                title_norm = row['Title_norm']
                
                try:
                    year = int(row.get('year', 0))
                except (ValueError, TypeError):
                    continue
                
                key = (title_norm, year)
                
                # Obtener categorías con cuartiles (tal como vienen del CSV)
                categories_str = str(row.get('Categories', ''))
                categories_with_quartiles = self._parse_categories_raw(categories_str)
                
                # Obtener áreas temáticas
                areas_str = str(row.get('Areas', ''))
                areas = self._parse_areas(areas_str)
                
                self._data_cache[key] = (areas, categories_with_quartiles)
            
            print(f"SJR cargado: {len(self._data_cache)} registros. Año máximo: {self._max_year_available}")
            
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo SJR en {self._csv_path}")
        except Exception as e:
            print(f"Error procesando SJR: {e}")

    @staticmethod
    def _parse_categories_raw(categories_str: str) -> List[str]:
        """
        Parsea las categorías del CSV manteniéndolas tal como vienen.
        
        Ejemplo entrada: "Software (Q1); Artificial Intelligence (Q2)"
        Ejemplo salida: ["Software (Q1)", "Artificial Intelligence (Q2)"]
        """
        if not categories_str or categories_str == 'nan':
            return []
        
        parts = categories_str.split(';')
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def _parse_areas(areas_str: str) -> List[str]:
        """Parsea el string de áreas temáticas del CSV."""
        if not areas_str or areas_str == 'nan':
            return []
        
        parts = areas_str.split(';')
        return [part.strip() for part in parts if part.strip()]