import unicodedata
import pandas as pd
from typing import Optional
from ...domain.repositories.sjr_repository import SJRRepository


class SJRFileRepository(SJRRepository):
    """Repositorio de datos SJR basado en archivo CSV."""
    
    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        self._df: Optional[pd.DataFrame] = None
        self._load_data()
    
    def _load_data(self) -> None:
        """Carga los datos del archivo CSV."""
        try:
            self._df = pd.read_csv(self._csv_path, sep=';')
            self._df['Title_norm'] = self._df['Title'].apply(self.normalize_journal_name)
        except FileNotFoundError:
            self._df = None
    
    def get_journal_categories(self, journal_name: str, year: str) -> str:
        """Obtiene las categorías de una revista en un año específico."""
        if self._df is None:
            return "No disponible"
        
        edition_year = str(year)
        normalized_journal = self.normalize_journal_name(journal_name)
        
        match = self._df[
            (self._df['Title_norm'] == normalized_journal) &
            (self._df['year'].astype(str) == edition_year)
        ]
        
        if not match.empty:
            return match.iloc[0]["Categories"]
        
        return "No indexada"
    
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
