from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.author import Author


class AuthorRepository(ABC):
    """Interfaz del repositorio de autores."""
    
    @abstractmethod
    async def get_by_id(self, author_id: str) -> Optional["Author"]:
        """Obtiene un autor por su ID."""
        ...
    
    @abstractmethod
    async def get_all(self) -> List["Author"]:
        """Obtiene todos los autores."""
        ...
    
    @abstractmethod
    async def create(self, author: "Author") -> "Author":
        """Crea un nuevo autor."""
        ...
    
    @abstractmethod
    async def update(self, author: "Author") -> "Author":
        """Actualiza un autor existente."""
        ...
    
    @abstractmethod
    async def delete(self, author_id: str) -> bool:
        """Elimina un autor por su ID."""
        ...
    
    @abstractmethod
    async def get_by_department(self, department: str) -> List["Author"]:
        """Obtiene autores por departamento."""
        ...
    
    @abstractmethod
    async def get_by_position(self, position: str) -> List["Author"]:
        """Obtiene autores por cargo."""
        ...
    
    @abstractmethod
    async def search_by_name(self, search_term: str) -> List["Author"]:
        """Busca autores por nombre o apellido."""
        ...