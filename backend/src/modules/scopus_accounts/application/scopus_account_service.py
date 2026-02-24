from typing import List, Optional
from uuid import uuid4, UUID

from .scopus_account_dto import ScopusAccountCreateDTO, ScopusAccountResponseDTO
from ..domain.scopus_account import ScopusAccount
from ..domain.scopus_account_repository import IScopusAccountRepository


class ScopusAccountService:
    def __init__(self, scopus_account_repo: IScopusAccountRepository):
        self.scopus_account_repo = scopus_account_repo

    async def get_accounts_by_author(self, author_id: UUID) -> List[ScopusAccountResponseDTO]:
        accounts = await self.scopus_account_repo.get_by_author(author_id)
        return [ScopusAccountResponseDTO.from_entity(account) for account in accounts]

    async def get_account_by_scopus_id(self, scopus_id: str) -> Optional[ScopusAccountResponseDTO]:
        account = await self.scopus_account_repo.get_by_scopus_id(scopus_id)
        if not account:
            raise ValueError(f"La cuenta Scopus no fue encontrada.")
        return ScopusAccountResponseDTO.from_entity(account)

    async def create_account(self, account: ScopusAccountCreateDTO) -> ScopusAccountResponseDTO:
        existing = await self.scopus_account_repo.get_by_scopus_id(account.scopus_id)
        if existing:
            raise ValueError(f"El Scopus ID corresponde a otro autor.")
        new_account = ScopusAccount(
            account_id=uuid4(),
            scopus_id=account.scopus_id,
            author_id=account.author_id
        )
        saved_account = await self.scopus_account_repo.create(new_account)
        return ScopusAccountResponseDTO.from_entity(saved_account)

    async def delete_account(self, account_id: UUID) -> bool:
        existing = await self.scopus_account_repo.get_by_id(account_id)
        if not existing:
            raise ValueError(f"La cuenta Scopus no fue encontrada.")
        return await self.scopus_account_repo.delete(account_id)
