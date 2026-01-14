"""
Interfaz del repositorio de usuarios.

Define el contrato para cualquier implementación de persistencia de usuarios.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.user import User


class UserRepository(ABC):
    """Interfaz del repositorio de usuarios."""
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional["User"]:
        """Obtiene un usuario por su ID."""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional["User"]:
        """Obtiene un usuario por su nombre de usuario."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional["User"]:
        """Obtiene un usuario por su correo electrónico."""
        pass
    
    @abstractmethod
    async def get_all(self) -> List["User"]:
        """Obtiene todos los usuarios."""
        pass
    
    @abstractmethod
    async def create(self, user: "User") -> "User":
        """Crea un nuevo usuario."""
        pass
    
    @abstractmethod
    async def update(self, user: "User") -> "User":
        """Actualiza un usuario existente."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        pass
    
    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """Verifica si existe un usuario con el nombre de usuario dado."""
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Verifica si existe un usuario con el correo electrónico dado."""
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """Cuenta el total de usuarios."""
        pass
