from typing import List, Optional
from uuid import UUID
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..domain.author import Author
from .author import AuthorModel
from ..domain.author_repository import IAuthorRepository


class DBAuthorRepository(IAuthorRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self) -> List[Author]:
        models = self.db.query(AuthorModel).all()
        return [model.to_entity() for model in models]

    async def get_by_department(self, dep_id: UUID) -> List[Author]:
        models = self.db.query(AuthorModel).filter(AuthorModel.department_id == dep_id).all()
        return [model.to_entity() for model in models]

    async def get_by_id(self, author_id: UUID) -> Optional[Author]:
        author = self.db.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
        return author.to_entity() if author else None

    async def get_by_email(self, author_email: EmailStr) -> Optional[Author]:
        author = self.db.query(AuthorModel).filter(AuthorModel.institutional_email == author_email).first()
        return author.to_entity() if author else None

    async def create(self, author: Author) -> Author:
        model = AuthorModel(
            author_id=author.author_id,
            first_name=author.first_name,
            last_name=author.last_name,
            institutional_email=str(author.institutional_email),
            title=author.title,
            gender=author.gender,
            job_position_id=author.job_position_id,
            department_id=author.department_id
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    async def update(self, author_id: UUID, author: Author) -> Author:
        model = self.db.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
        if not model:
            raise ValueError(f"El autor no fue encontrado.")
        model.first_name = author.first_name
        model.last_name = author.last_name
        model.title = author.title
        model.job_position_id = author.job_position_id
        model.department_id = author.department_id

        try:
            self.db.commit()
            self.db.refresh(model)
            return model.to_entity()
        except Exception:
            self.db.rollback()
            raise

    async def delete(self, author_id: UUID) -> bool:
        author = self.db.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
        if author:
            self.db.delete(author)
            self.db.commit()
            return True
        return False
