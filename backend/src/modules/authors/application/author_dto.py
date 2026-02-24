""" Módulo de DTOs para autores. Define las estructuras de datos para la gestión de autores. """

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

from ..domain.author import Author
from ..domain.gender import Gender


class AuthorCreateDTO(BaseModel):
    """ DTO para la creación de un autor. """
    first_name: str
    last_name: str
    institutional_email: EmailStr
    title: Optional[str]
    gender: Optional[Gender]
    job_position_id: UUID
    department_id: UUID


class AuthorUpdateDTO(BaseModel):
    """ DTO para la actualización de un autor. """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    job_position_id: Optional[UUID] = None
    department_id: Optional[UUID] = None


class AuthorResponseDTO(BaseModel):
    """ DTO para la respuesta de un autor. """
    author_id: UUID
    first_name: str
    last_name: str
    institutional_email: EmailStr
    title: Optional[str]
    gender: Optional[Gender]
    job_position_id: UUID
    department_id: UUID

    @staticmethod
    def from_entity(author: Author) -> 'AuthorResponseDTO':
        """ Crea un AuthorResponseDTO a partir de una entidad Author. """
        return AuthorResponseDTO(
            author_id=author.author_id,
            first_name=author.first_name,
            last_name=author.last_name,
            institutional_email=author.institutional_email,
            title=author.title,
            gender=author.gender,
            job_position_id=author.job_position_id,
            department_id=author.department_id
        )
