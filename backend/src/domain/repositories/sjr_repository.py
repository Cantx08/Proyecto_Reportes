from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from ..entities.journal import Journal
from ..value_objects.quartile import SJRQuartile


class SJRRepository(ABC):
    """
    Interface para el repositorio de datos SJR.
    
    Define los contratos para acceder a datos de rankings SJR
    y categorías de revistas.
    """

    @abstractmethod
    async def find_journal_by_name_and_year(self, journal_name: str, year: int) -> Optional[Dict]:
        """
        Busca información SJR de una revista por nombre y año.
        
        Args:
            journal_name: Nombre de la revista
            year: Año del ranking
            
        Returns:
            Optional[Dict]: Información SJR de la revista o None
        """
        pass

    @abstractmethod
    async def get_categories_by_journal_and_year(self, journal_name: str, year: int) -> List[Dict]:
        """
        Obtiene las categorías SJR de una revista en un año específico.
        
        Args:
            journal_name: Nombre de la revista
            year: Año del ranking
            
        Returns:
            List[Dict]: Lista de categorías con cuartiles y rankings
        """
        pass

    @abstractmethod
    async def get_available_years(self) -> List[int]:
        """
        Obtiene todos los años disponibles en los datos SJR.
        
        Returns:
            List[int]: Lista de años disponibles
        """
        pass

    @abstractmethod
    async def search_journals_by_name(self, journal_name: str) -> List[str]:
        """
        Busca revistas por nombre en los datos SJR.
        
        Args:
            journal_name: Nombre de la revista a buscar
            
        Returns:
            List[str]: Lista de nombres de revistas que coinciden
        """
        pass

    @abstractmethod
    async def get_journal_history(self, journal_name: str) -> List[Dict]:
        """
        Obtiene el historial completo de una revista en SJR.
        
        Args:
            journal_name: Nombre de la revista
            
        Returns:
            List[Dict]: Historial de la revista por años
        """
        pass

    @abstractmethod
    async def get_quartile_distribution_by_year(self, year: int) -> Dict[str, int]:
        """
        Obtiene la distribución de cuartiles en un año específico.
        
        Args:
            year: Año a consultar
            
        Returns:
            Dict[str, int]: Distribución de revistas por cuartil
        """
        pass

    @abstractmethod
    async def find_top_journals_by_category_and_year(self, 
                                                    category: str, 
                                                    year: int, 
                                                    limit: int = 10) -> List[Dict]:
        """
        Encuentra las mejores revistas de una categoría en un año.
        
        Args:
            category: Categoría SJR
            year: Año del ranking
            limit: Límite de resultados
            
        Returns:
            List[Dict]: Lista de mejores revistas
        """
        pass

    @abstractmethod
    async def get_categories_list(self) -> List[str]:
        """
        Obtiene la lista de todas las categorías SJR disponibles.
        
        Returns:
            List[str]: Lista de categorías SJR
        """
        pass

    @abstractmethod
    async def map_journal_to_sjr_data(self, journal: Journal, year: int) -> Optional[Dict]:
        """
        Mapea una revista a sus datos SJR por año.
        
        Args:
            journal: Entidad Journal a mapear
            year: Año del ranking
            
        Returns:
            Optional[Dict]: Datos SJR mapeados o None
        """
        pass

    @abstractmethod
    async def bulk_map_journals(self, journals: List[Journal], year: int) -> Dict[int, Dict]:
        """
        Mapea múltiples revistas a sus datos SJR.
        
        Args:
            journals: Lista de revistas a mapear
            year: Año del ranking
            
        Returns:
            Dict[int, Dict]: Mapeo de journal_id -> datos SJR
        """
        pass