from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from .scopus_account import ScopusAccount


class IScopusAccountRepository(ABC):
    @abstractmethod
    async def get_by_author(self, author_id: UUID) -> List[ScopusAccount]:
        """Obtiene las cuentas de Scopus asociadas a un autor."""
        pass

    @abstractmethod
    async def get_by_id(self, account_id: UUID) -> Optional[ScopusAccount]:
        """Obtiene una cuenta de Scopus por su ID."""
        pass

    @abstractmethod
    async def get_by_scopus_id(self, scopus_id: str) -> Optional[ScopusAccount]:
        """Obtiene una cuenta de Scopus por su Scopus ID."""
        pass

    @abstractmethod
    async def create(self, account: ScopusAccount) -> ScopusAccount:
        """Crea una nueva cuenta de Scopus."""
        pass

    @abstractmethod
    async def delete(self, account_id: UUID) -> bool:
        """Elimina una cuenta de Scopus por su ID."""
        pass
