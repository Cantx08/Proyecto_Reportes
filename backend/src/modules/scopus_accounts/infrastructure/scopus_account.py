from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, UUID

from ..domain.scopus_account import ScopusAccount
from ....shared.database import Base


class ScopusAccountModel(Base):
    __tablename__ = "scopus_accounts"

    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    scopus_id = Column(String, unique=True, nullable=False, index=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.author_id", ondelete="CASCADE"), nullable=False)

    def to_entity(self) -> ScopusAccount:
        return ScopusAccount(
            account_id=self.account_id,
            scopus_id=self.scopus_id,
            author_id=self.author_id
        )