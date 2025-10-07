from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.scopus_account import ScopusAccount


class ScopusAccountRepository(ABC):
    """Interfaz del repositorio de cuentas Scopus."""
    
    @abstractmethod
    async def get_by_scopus_id(self, scopus_id: str) -> Optional["ScopusAccount"]:
        """Obtiene una cuenta Scopus por su ID de Scopus."""
        ...
    
    @abstractmethod
    async def get_by_author_id(self, author_id: str) -> List["ScopusAccount"]:
        """Obtiene todas las cuentas Scopus de un autor."""
        ...
    
    @abstractmethod
    async def get_all(self) -> List["ScopusAccount"]:
        """Obtiene todas las cuentas Scopus."""
        ...
    
    @abstractmethod
    async def create(self, scopus_account: "ScopusAccount") -> "ScopusAccount":
        """Crea una nueva cuenta Scopus."""
        ...
    
    @abstractmethod
    async def update(self, scopus_account: "ScopusAccount") -> "ScopusAccount":
        """Actualiza una cuenta Scopus existente."""
        ...
    
    @abstractmethod
    async def delete(self, scopus_id: str) -> bool:
        """Elimina una cuenta Scopus por su ID de Scopus."""
        ...
    
    @abstractmethod
    async def delete_by_author_id(self, author_id: str) -> bool:
        """Elimina todas las cuentas Scopus de un autor."""
        ...