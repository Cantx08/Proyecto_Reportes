from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from ..entities.journal import Journal


class JournalRepository(ABC):
    """
    Interface para el repositorio de revistas.
    
    Define los contratos para el acceso a datos de revistas académicas.
    """

    @abstractmethod
    async def save(self, journal: Journal) -> Journal:
        """
        Guarda una revista en el repositorio.
        
        Args:
            journal: Entidad Journal a guardar
            
        Returns:
            Journal: La revista guardada con ID asignado
        """
        pass

    @abstractmethod
    async def find_by_id(self, journal_id: int) -> Optional[Journal]:
        """
        Busca una revista por su ID.
        
        Args:
            journal_id: ID de la revista
            
        Returns:
            Optional[Journal]: La revista encontrada o None
        """
        pass

    @abstractmethod
    async def find_by_title(self, title: str) -> Optional[Journal]:
        """
        Busca una revista por su título exacto.
        
        Args:
            title: Título de la revista
            
        Returns:
            Optional[Journal]: La revista encontrada o None
        """
        pass

    @abstractmethod
    async def find_by_issn(self, issn: str) -> Optional[Journal]:
        """
        Busca una revista por ISSN o e-ISSN.
        
        Args:
            issn: ISSN o e-ISSN de la revista
            
        Returns:
            Optional[Journal]: La revista encontrada o None
        """
        pass

    @abstractmethod
    async def search_by_title(self, title: str) -> List[Journal]:
        """
        Busca revistas por título (búsqueda parcial).
        
        Args:
            title: Título a buscar
            
        Returns:
            List[Journal]: Lista de revistas que coinciden
        """
        pass

    @abstractmethod
    async def find_by_publisher(self, publisher: str) -> List[Journal]:
        """
        Busca revistas por editorial.
        
        Args:
            publisher: Editorial a buscar
            
        Returns:
            List[Journal]: Lista de revistas de la editorial
        """
        pass

    @abstractmethod
    async def find_all_active(self) -> List[Journal]:
        """
        Obtiene todas las revistas activas.
        
        Returns:
            List[Journal]: Lista de revistas activas
        """
        pass

    @abstractmethod
    async def update(self, journal: Journal) -> Journal:
        """
        Actualiza una revista existente.
        
        Args:
            journal: Entidad Journal a actualizar
            
        Returns:
            Journal: La revista actualizada
        """
        pass

    @abstractmethod
    async def delete(self, journal_id: int) -> bool:
        """
        Elimina una revista (soft delete).
        
        Args:
            journal_id: ID de la revista a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass

    @abstractmethod
    async def exists_by_title(self, title: str) -> bool:
        """
        Verifica si existe una revista con el título dado.
        
        Args:
            title: Título a verificar
            
        Returns:
            bool: True si existe
        """
        pass

    @abstractmethod
    async def exists_by_issn(self, issn: str) -> bool:
        """
        Verifica si existe una revista con el ISSN dado.
        
        Args:
            issn: ISSN a verificar
            
        Returns:
            bool: True si existe
        """
        pass