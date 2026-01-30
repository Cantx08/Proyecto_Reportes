import uuid

from pydantic import EmailStr
from sqlalchemy import Column, String, ForeignKey, UUID, Enum

from ..domain.author import Author
from ..domain.gender import Gender
from ....shared.database import Base


class AuthorModel(Base):
    __tablename__ = 'authors'

    author_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    institutional_email = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=True)
    gender = Column(Enum(Gender), nullable=False)

    job_position_id = Column(UUID(as_uuid=True), ForeignKey('positions.pos_id'), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.dep_id'), nullable=False)

    # scopus_accounts = relationship("ScopusAccountModel", back_populates="author", cascade="all, delete-orphan")

    def to_entity(self) -> Author:
        return Author(
            author_id=self.author_id,
            first_name=self.first_name,
            last_name=self.last_name,
            institutional_email=EmailStr(self.institutional_email),
            title=self.title,
            gender=self.gender,
            job_position_id=self.job_position_id,
            department_id=self.department_id
        )
