import unicodedata
import pandas as pd
from typing import Optional, Dict, Tuple
from ...domain.repositories.sjr_repository import SJRRepository


class SJRFileRepository(SJRRepository):
    """Repositorio de datos SJR basado en archivo CSV."""
    
    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        self._data_cache: Dict[Tuple[str, str], str] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Carga los datos del archivo CSV."""
        try:
            df = pd.read_csv(self._csv_path, sep=';')
            # Pre-calcular la columna normalizada una sola vez
            df['Title_norm'] = df['Title'].apply(self.normalize_journal_name)
            
            # Construir el diccionario de caché
            # Iteramos una vez y guardamos en memoria para acceso rápido
            for _, row in df.iterrows():
                key = (str(row['Title_norm']), str(row['year']))
                self._data_cache[key] = row['Categories']
                
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo SJR en {self._csv_path}")
            self._data_cache = {}
    
    def get_journal_categories(self, journal_name: str, year: str) -> str:
        """Obtiene las categorías de una revista en un año específico."""
        if not self._data_cache:
            return "No disponible"
        
        edition_year = str(year)
        normalized_journal = self.normalize_journal_name(journal_name)
        
        # Búsqueda directa en diccionario (Milisegundos vs Segundos)
        return self._data_cache.get((normalized_journal, edition_year), "No indexada")
    
    def normalize_journal_name(self, name: str) -> str:
        """
        Normaliza el nombre de una revista para mejorar las coincidencias.
        Elimina tildes, convierte a minúsculas, elimina símbolos y espacios extra.
        """
        if not isinstance(name, str):
            name = str(name)
        
        # Convertir a minúsculas y quitar espacios
        name = name.lower().strip()
        
        # Normalizar unicode (eliminar tildes)
        name = unicodedata.normalize('NFKD', name)
        name = ''.join(c for c in name if not unicodedata.combining(c))
        
        # Reemplazar símbolos comunes
        name = name.replace('&', 'and')
        
        # Mantener solo alfanuméricos y espacios
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        
        # Normalizar espacios múltiples
        name = ' '.join(name.split())
        
        return name
