from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

from ..domain.author import Author
from ..domain.gender import Gender


class AuthorCreateDTO(BaseModel):
    first_name: str
    last_name: str
    institutional_email: EmailStr
    title: Optional[str]
    gender: Optional[Gender]
    job_position_id: UUID
    department_id: UUID


class AuthorUpdateDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    job_position_id: Optional[UUID] = None
    department_id: Optional[UUID] = None


class AuthorResponseDTO(BaseModel):
    author_id: UUID
    full_name: str
    institutional_email: EmailStr
    title: Optional[str]
    gender: Optional[Gender]
    job_position_id: UUID
    department_id: UUID

    @staticmethod
    def from_entity(author: Author) -> 'AuthorResponseDTO':
        return AuthorResponseDTO(
            author_id=author.author_id,
            full_name=f"{author.first_name} {author.last_name}",
            institutional_email=author.institutional_email,
            title=author.title,
            gender=author.gender,
            job_position_id=author.job_position_id,
            department_id=author.department_id
        )
