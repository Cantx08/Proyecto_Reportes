from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.author import Author
from ..value_objects.scopus_id import ScopusId


class AuthorRepository(ABC):
    """
    Interface para el repositorio de autores.
    
    Define los contratos para el acceso a datos de autores.
    """

    @abstractmethod
    async def save(self, author: Author) -> Author:
        """
        Guarda un autor en el repositorio.
        
        Args:
            author: Entidad Author a guardar
            
        Returns:
            Author: El autor guardado con ID asignado
            
        Raises:
            DuplicateAuthorError: Si el autor ya existe
        """
        pass

    @abstractmethod
    async def find_by_id(self, author_id: int) -> Optional[Author]:
        """
        Busca un autor por su ID.
        
        Args:
            author_id: ID del autor
            
        Returns:
            Optional[Author]: El autor encontrado o None
        """
        pass

    @abstractmethod
    async def find_by_dni(self, dni: str) -> Optional[Author]:
        """
        Busca un autor por su DNI.
        
        Args:
            dni: DNI del autor
            
        Returns:
            Optional[Author]: El autor encontrado o None
        """
        pass

    @abstractmethod
    async def find_by_scopus_id(self, scopus_id: ScopusId) -> Optional[Author]:
        """
        Busca un autor por su ID de Scopus.
        
        Args:
            scopus_id: ID de Scopus
            
        Returns:
            Optional[Author]: El autor encontrado o None
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Author]:
        """
        Busca un autor por su email.
        
        Args:
            email: Email del autor
            
        Returns:
            Optional[Author]: El autor encontrado o None
        """
        pass

    @abstractmethod
    async def find_by_department(self, department_id: int) -> List[Author]:
        """
        Busca autores por departamento.
        
        Args:
            department_id: ID del departamento
            
        Returns:
            List[Author]: Lista de autores del departamento
        """
        pass

    @abstractmethod
    async def find_all_active(self) -> List[Author]:
        """
        Obtiene todos los autores activos.
        
        Returns:
            List[Author]: Lista de autores activos
        """
        pass

    @abstractmethod
    async def search_by_name(self, name: str) -> List[Author]:
        """
        Busca autores por nombre (búsqueda parcial).
        
        Args:
            name: Nombre a buscar
            
        Returns:
            List[Author]: Lista de autores que coinciden
        """
        pass

    @abstractmethod
    async def update(self, author: Author) -> Author:
        """
        Actualiza un autor existente.
        
        Args:
            author: Entidad Author a actualizar
            
        Returns:
            Author: El autor actualizado
            
        Raises:
            AuthorNotFoundError: Si el autor no existe
        """
        pass

    @abstractmethod
    async def delete(self, author_id: int) -> bool:
        """
        Elimina un autor (soft delete).
        
        Args:
            author_id: ID del autor a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            AuthorNotFoundError: Si el autor no existe
        """
        pass

    @abstractmethod
    async def exists_by_dni(self, dni: str) -> bool:
        """
        Verifica si existe un autor con el DNI dado.
        
        Args:
            dni: DNI a verificar
            
        Returns:
            bool: True si existe
        """
        pass

    @abstractmethod
    async def exists_by_scopus_id(self, scopus_id: ScopusId) -> bool:
        """
        Verifica si existe un autor con el Scopus ID dado.
        
        Args:
            scopus_id: ID de Scopus a verificar
            
        Returns:
            bool: True si existe
        """
        pass