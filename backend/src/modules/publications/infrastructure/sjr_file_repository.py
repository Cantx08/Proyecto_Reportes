import unicodedata
from typing import Dict, Tuple, List, Any

import pandas as pd

from ..domain.publication import SJRMetric
from ..domain.sjr_repository import ISJRRepository


class SJRFileRepository(ISJRRepository):
    """
    Repositorio de datos SJR basado en archivo CSV.
    
    Carga un histórico de SJR y proporciona métricas de revistas
    con mapeo dinámico de años futuros al último disponible.
    """

    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        # Cache: (nombre_normalizado, año) -> Lista de métricas
        self._metrics_cache: Dict[Tuple[str, int], List[SJRMetric]] = {}
        # Cache: (nombre_normalizado, año) -> Lista de áreas temáticas
        self._areas_cache: Dict[Tuple[str, int], List[str]] = {}
        self._max_year_available: int = 0
        self._load_data()

    def get_max_available_year(self) -> int:
        """Retorna el año máximo disponible en el CSV."""
        return self._max_year_available

    def get_journal_metrics(
        self, 
        journal_name: str, 
        publication_year: int
    ) -> List[SJRMetric]:
        """
        Obtiene las métricas SJR de una revista para un año específico.
        
        Si el año solicitado es mayor al disponible, utiliza el último año.
        """
        if not self._metrics_cache:
            return []
        
        normalized = self.normalize_journal_name(journal_name)
        target_year = self._resolve_year(publication_year)
        
        return self._metrics_cache.get((normalized, target_year), [])

    def get_subject_areas(
        self, 
        journal_name: str, 
        publication_year: int
    ) -> List[str]:
        """Obtiene las áreas temáticas de una revista."""
        if not self._areas_cache:
            return []
        
        normalized = self.normalize_journal_name(journal_name)
        target_year = self._resolve_year(publication_year)
        
        return self._areas_cache.get((normalized, target_year), [])

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
                
                # Parsear categorías
                categories_str = str(row.get('Categories', ''))
                parsed_categories = self._parse_categories(categories_str)
                
                # Parsear áreas
                areas_str = str(row.get('Areas', ''))
                parsed_areas = self._parse_areas(areas_str)
                
                # Construir métricas SJR
                metrics = [
                    SJRMetric(
                        category=cat['name'],
                        quartile=cat['quartile'],
                        percentile=0.0,  # Se calcula después si es necesario
                        sjr_year=year
                    )
                    for cat in parsed_categories
                ]
                
                self._metrics_cache[key] = metrics
                self._areas_cache[key] = parsed_areas
            
            print(f"SJR cargado: {len(self._metrics_cache)} registros. Año máximo: {self._max_year_available}")
            
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo SJR en {self._csv_path}")
        except Exception as e:
            print(f"Error procesando SJR: {e}")

    @staticmethod
    def _parse_categories(categories_str: str) -> List[Dict[str, str]]:
        """Parsea el string de categorías del CSV."""
        if not categories_str or categories_str == 'nan':
            return []
        
        results = []
        parts = categories_str.split(';')
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            quartile = "Q4"
            name = part
            
            if "(Q1)" in part:
                quartile, name = "Q1", part.replace("(Q1)", "").strip()
            elif "(Q2)" in part:
                quartile, name = "Q2", part.replace("(Q2)", "").strip()
            elif "(Q3)" in part:
                quartile, name = "Q3", part.replace("(Q3)", "").strip()
            elif "(Q4)" in part:
                quartile, name = "Q4", part.replace("(Q4)", "").strip()
            
            results.append({'name': name, 'quartile': quartile})
        
        return results

    @staticmethod
    def _parse_areas(areas_str: str) -> List[str]:
        """Parsea el string de áreas temáticas del CSV."""
        if not areas_str or areas_str == 'nan':
            return []
        
        parts = areas_str.split(';')
        return [part.strip() for part in parts if part.strip()]