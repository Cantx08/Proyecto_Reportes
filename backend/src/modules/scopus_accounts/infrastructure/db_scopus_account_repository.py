from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from .scopus_account import ScopusAccountModel
from ..domain.scopus_account import ScopusAccount
from ..domain.scopus_account_repository import IScopusAccountRepository


class DBScopusAccountRepository(IScopusAccountRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_by_author(self, author_id: UUID) -> List[ScopusAccount]:
        models = self.db.query(ScopusAccountModel).filter(ScopusAccountModel.author_id == author_id).all()
        return [model.to_entity() for model in models]

    async def get_by_id(self, account_id: UUID) -> Optional[ScopusAccount]:
        model = self.db.query(ScopusAccountModel).filter(ScopusAccountModel.account_id == account_id).first()
        return model.to_entity() if model else None

    async def get_by_scopus_id(self, scopus_id: str) -> Optional[ScopusAccount]:
        model = self.db.query(ScopusAccountModel).filter(ScopusAccountModel.scopus_id == scopus_id).first()
        return model.to_entity() if model else None

    async def create(self, account: ScopusAccount) -> ScopusAccount:
        model = ScopusAccountModel(
            account_id=account.account_id,
            scopus_id=account.scopus_id,
            author_id=account.author_id
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    async def delete(self, account_id: UUID) -> bool:
        account = self.db.query(ScopusAccountModel).filter(ScopusAccountModel.account_id == account_id).first()
        if account:
            self.db.delete(account)
            self.db.commit()
            return True
        return False
