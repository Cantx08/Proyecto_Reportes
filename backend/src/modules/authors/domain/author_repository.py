from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr

from .author import Author


class IAuthorRepository(ABC):
    """Interfaz del repositorio de autores."""

    @abstractmethod
    async def get_all(self) -> List[Author]:
        """Obtiene todos los autores."""
        pass

    @abstractmethod
    async def get_by_department(self, dep_id: UUID) -> List[Author]:
        """Obtiene autores por departamento."""
        pass

    @abstractmethod
    async def get_by_id(self, author_id: UUID) -> Optional[Author]:
        """Obtiene un autor por su ID."""
        pass

    @abstractmethod
    async def get_by_email(self, author_email: EmailStr) -> Optional[Author]:
        """Obtiene un autor por su ID."""
        pass

    @abstractmethod
    async def create(self, author: Author) -> Author:
        """Crea un nuevo autor."""
        pass

    @abstractmethod
    async def update(self, author_id: UUID, author: Author) -> Author:
        """Actualiza un autor existente."""
        pass

    @abstractmethod
    async def delete(self, author_id: UUID) -> bool:
        """Elimina un autor por su ID."""
        pass
