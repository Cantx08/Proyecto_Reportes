from uuid import UUID
from pydantic import BaseModel

from ..domain.scopus_account import ScopusAccount


class ScopusAccountCreateDTO(BaseModel):
    scopus_id: str
    author_id: UUID


class ScopusAccountResponseDTO(BaseModel):
    account_id: UUID
    scopus_id: str
    author_id: UUID

    @staticmethod
    def from_entity(scopus_account: ScopusAccount) -> 'ScopusAccountResponseDTO':
        return ScopusAccountResponseDTO(
            account_id=scopus_account.account_id,
            scopus_id=scopus_account.scopus_id,
            author_id=scopus_account.author_id
        )
