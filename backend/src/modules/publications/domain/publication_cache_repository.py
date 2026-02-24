from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .publication import Publication


class IPublicationCacheRepository(ABC):
    """
    Interfaz del repositorio de caché de publicaciones.
    
    Define el contrato para almacenar y recuperar publicaciones
    cacheadas en la base de datos local.
    """

    @abstractmethod
    async def get_by_scopus_account(self, scopus_account_id: UUID) -> List[Publication]:
        """
        Obtiene las publicaciones cacheadas de una cuenta Scopus.
        
        Args:
            scopus_account_id: ID de la cuenta Scopus en el sistema
            
        Returns:
            Lista de publicaciones cacheadas
        """
        pass

    @abstractmethod
    async def get_by_scopus_id(self, scopus_id: str) -> Optional[Publication]:
        """
        Obtiene una publicación cacheada por su Scopus ID.
        
        Args:
            scopus_id: ID de la publicación en Scopus
            
        Returns:
            Publicación si existe en caché, None si no
        """
        pass

    @abstractmethod
    async def save_publications(
        self, 
        publications: List[Publication], 
        scopus_account_id: UUID
    ) -> int:
        """
        Guarda una lista de publicaciones en la caché.
        
        Args:
            publications: Lista de publicaciones a cachear
            scopus_account_id: ID de la cuenta Scopus origen
            
        Returns:
            Número de publicaciones guardadas/actualizadas
        """
        pass

    @abstractmethod
    async def is_cache_valid(self, scopus_account_id: UUID, max_age_hours: int = 24) -> bool:
        """
        Verifica si la caché de una cuenta está vigente.
        
        Args:
            scopus_account_id: ID de la cuenta Scopus
            max_age_hours: Antigüedad máxima en horas (default 24h)
            
        Returns:
            True si la caché es válida, False si necesita actualización
        """
        pass

    @abstractmethod
    async def invalidate_cache(self, scopus_account_id: UUID) -> int:
        """
        Invalida (elimina) la caché de una cuenta Scopus.
        
        Args:
            scopus_account_id: ID de la cuenta Scopus
            
        Returns:
            Número de registros eliminados
        """
        pass
