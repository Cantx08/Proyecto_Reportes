import unicodedata
import pandas as pd
from typing import Optional
from ...domain import SJRRepository


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
            self._df['Title_norm'] = self._df['Title'].apply(self.normalizar_nombre_revista)
        except Exception:
            self._df = None
    
    def obtener_categorias_revista(self, nombre_revista: str, anio: str) -> str:
        """Obtiene las categorías de una revista en un año específico."""
        if self._df is None:
            return "No disponible"
        
        anio_str = str(anio)
        revista_normalizada = self.normalizar_nombre_revista(nombre_revista)
        
        match = self._df[
            (self._df['Title_norm'] == revista_normalizada) & 
            (self._df['year'].astype(str) == anio_str)
        ]
        
        if not match.empty:
            return match.iloc[0]["Categories"]
        
        return "No indexada"
    
    def normalizar_nombre_revista(self, nombre: str) -> str:
        """
        Normaliza el nombre de una revista para mejorar las coincidencias.
        Elimina tildes, convierte a minúsculas, elimina símbolos y espacios extra.
        """
        if not isinstance(nombre, str):
            nombre = str(nombre)
        
        # Convertir a minúsculas y quitar espacios
        nombre = nombre.lower().strip()
        
        # Normalizar unicode (eliminar tildes)
        nombre = unicodedata.normalize('NFKD', nombre)
        nombre = ''.join(c for c in nombre if not unicodedata.combining(c))
        
        # Reemplazar símbolos comunes
        nombre = nombre.replace('&', 'and')
        
        # Mantener solo alfanuméricos y espacios
        nombre = ''.join(c for c in nombre if c.isalnum() or c.isspace())
        
        # Normalizar espacios múltiples
        nombre = ' '.join(nombre.split())
        
        return nombre
