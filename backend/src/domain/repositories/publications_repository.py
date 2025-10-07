from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.publication import Publication


class PublicationsRepository(ABC):
    """Interfaz para el repositorio de publicaciones."""
    
    @abstractmethod
    async def get_publications_by_author(self, author_id: str) -> List[Publication]:
        """Obtiene las publicaciones de un autor específico."""
        pass
    
    @abstractmethod
    async def get_publication_details(self, scopus_id: str) -> Optional[dict]:
        """Obtiene los detalles completos de una publicación."""
        pass