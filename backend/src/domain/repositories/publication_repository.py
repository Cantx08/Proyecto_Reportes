from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from ..entities.publication import Publication, DocumentType, SourceType
from ..value_objects.scopus_id import ScopusId
from ..value_objects.publication_year import PublicationYear


class PublicationRepository(ABC):
    """
    Interface para el repositorio de publicaciones.
    
    Define los contratos para el acceso a datos de publicaciones.
    """

    @abstractmethod
    async def save(self, publication: Publication) -> Publication:
        """
        Guarda una publicación en el repositorio.
        
        Args:
            publication: Entidad Publication a guardar
            
        Returns:
            Publication: La publicación guardada con ID asignado
        """
        pass

    @abstractmethod
    async def find_by_id(self, publication_id: int) -> Optional[Publication]:
        """
        Busca una publicación por su ID.
        
        Args:
            publication_id: ID de la publicación
            
        Returns:
            Optional[Publication]: La publicación encontrada o None
        """
        pass

    @abstractmethod
    async def find_by_scopus_id(self, scopus_id: str) -> Optional[Publication]:
        """
        Busca una publicación por su ID de Scopus.
        
        Args:
            scopus_id: ID de Scopus de la publicación
            
        Returns:
            Optional[Publication]: La publicación encontrada o None
        """
        pass

    @abstractmethod
    async def find_by_doi(self, doi: str) -> Optional[Publication]:
        """
        Busca una publicación por su DOI.
        
        Args:
            doi: DOI de la publicación
            
        Returns:
            Optional[Publication]: La publicación encontrada o None
        """
        pass

    @abstractmethod
    async def find_by_author_scopus_ids(self, scopus_ids: List[ScopusId]) -> List[Publication]:
        """
        Busca publicaciones por IDs de Scopus de autores.
        
        Args:
            scopus_ids: Lista de IDs de Scopus de autores
            
        Returns:
            List[Publication]: Lista de publicaciones encontradas
        """
        pass

    @abstractmethod
    async def find_by_year_range(self, start_year: int, end_year: int) -> List[Publication]:
        """
        Busca publicaciones en un rango de años.
        
        Args:
            start_year: Año inicial
            end_year: Año final
            
        Returns:
            List[Publication]: Lista de publicaciones en el rango
        """
        pass

    @abstractmethod
    async def find_by_document_type(self, document_type: DocumentType) -> List[Publication]:
        """
        Busca publicaciones por tipo de documento.
        
        Args:
            document_type: Tipo de documento
            
        Returns:
            List[Publication]: Lista de publicaciones del tipo especificado
        """
        pass

    @abstractmethod
    async def find_by_source_type(self, source_type: SourceType) -> List[Publication]:
        """
        Busca publicaciones por tipo de fuente.
        
        Args:
            source_type: Tipo de fuente
            
        Returns:
            List[Publication]: Lista de publicaciones de la fuente especificada
        """
        pass

    @abstractmethod
    async def find_by_journal_id(self, journal_id: int) -> List[Publication]:
        """
        Busca publicaciones por ID de revista.
        
        Args:
            journal_id: ID de la revista
            
        Returns:
            List[Publication]: Lista de publicaciones de la revista
        """
        pass

    @abstractmethod
    async def search_by_title(self, title: str) -> List[Publication]:
        """
        Busca publicaciones por título (búsqueda parcial).
        
        Args:
            title: Título a buscar
            
        Returns:
            List[Publication]: Lista de publicaciones que coinciden
        """
        pass

    @abstractmethod
    async def find_recent_by_author(self, author_id: int, days: int = 30) -> List[Publication]:
        """
        Busca publicaciones recientes de un autor.
        
        Args:
            author_id: ID del autor
            days: Días hacia atrás para considerar "reciente"
            
        Returns:
            List[Publication]: Lista de publicaciones recientes
        """
        pass

    @abstractmethod
    async def update(self, publication: Publication) -> Publication:
        """
        Actualiza una publicación existente.
        
        Args:
            publication: Entidad Publication a actualizar
            
        Returns:
            Publication: La publicación actualizada
        """
        pass

    @abstractmethod
    async def delete(self, publication_id: int) -> bool:
        """
        Elimina una publicación.
        
        Args:
            publication_id: ID de la publicación a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass

    @abstractmethod
    async def exists_by_scopus_id(self, scopus_id: str) -> bool:
        """
        Verifica si existe una publicación con el Scopus ID dado.
        
        Args:
            scopus_id: ID de Scopus a verificar
            
        Returns:
            bool: True si existe
        """
        pass

    @abstractmethod
    async def exists_by_doi(self, doi: str) -> bool:
        """
        Verifica si existe una publicación con el DOI dado.
        
        Args:
            doi: DOI a verificar
            
        Returns:
            bool: True si existe
        """
        pass

    @abstractmethod
    async def count_by_year(self, year: int) -> int:
        """
        Cuenta publicaciones por año.
        
        Args:
            year: Año a consultar
            
        Returns:
            int: Número de publicaciones en el año
        """
        pass

    @abstractmethod
    async def get_years_with_publications(self) -> List[int]:
        """
        Obtiene todos los años que tienen publicaciones.
        
        Returns:
            List[int]: Lista de años con publicaciones
        """
        pass

    @abstractmethod
    async def get_statistics_by_author(self, author_id: int) -> Dict[str, int]:
        """
        Obtiene estadísticas de publicaciones por autor.
        
        Args:
            author_id: ID del autor
            
        Returns:
            Dict[str, int]: Estadísticas (total, por año, por tipo, etc.)
        """
        pass