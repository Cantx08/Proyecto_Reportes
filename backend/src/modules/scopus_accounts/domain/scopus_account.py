from dataclasses import dataclass
from uuid import UUID


@dataclass
class ScopusAccount:
    account_id: UUID
    scopus_id: str
    author_id: UUID
