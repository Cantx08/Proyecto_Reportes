from typing import List
from uuid import UUID, uuid4

from .author_dto import AuthorResponseDTO, AuthorCreateDTO, AuthorUpdateDTO
from ..domain.author import Author
from ..domain.author_repository import IAuthorRepository


class AuthorService:
    """Servicio de aplicación para la gestión de autores."""

    def __init__(self, author_repo: IAuthorRepository):
        self.author_repo = author_repo

    async def get_all_authors(self) -> List[AuthorResponseDTO]:
        authors = await self.author_repo.get_all()
        return [AuthorResponseDTO.from_entity(author) for author in authors]

    async def get_authors_by_department(self, dep_code: str) -> List[AuthorResponseDTO]:
        if dep_code is None:
            raise ValueError("Se requiere las siglas del departamento.")

        authors = await self.author_repo.get_by_department(dep_code)
        return [AuthorResponseDTO.from_entity(author) for author in authors]

    async def get_author_by_id(self, author_id: UUID) -> AuthorResponseDTO:
        author = await self.author_repo.get_by_id(author_id)
        if not author:
            raise ValueError(f"El autor no fue encontrado.")
        return AuthorResponseDTO.from_entity(author)

    async def create_author(self, author: AuthorCreateDTO) -> AuthorResponseDTO:
        existing_author = await self.author_repo.get_by_email(author.institutional_email)
        if existing_author:
            raise ValueError(f"El correo ya fue asociado a otro autor.")
        new_author = Author(
            author_id=uuid4(),
            first_name=author.first_name,
            last_name=author.last_name,
            institutional_email=author.institutional_email,
            title=author.title,
            gender=author.gender,
            job_position_id=author.job_position_id,
            department_id=author.department_id
        )
        saved_author = await self.author_repo.create(new_author)
        return AuthorResponseDTO.from_entity(saved_author)

    async def update_author(self, researcher_id: UUID, author: AuthorUpdateDTO) -> AuthorResponseDTO:
        existing = await self.author_repo.get_by_id(researcher_id)
        if not existing:
            raise ValueError(f"El autor con ID {researcher_id} no existe.")

        updated_author = Author(
            author_id=researcher_id,
            first_name=author.first_name if author.first_name else existing.first_name,
            last_name=author.last_name if author.last_name else existing.last_name,
            institutional_email=existing.institutional_email,
            title=author.title if author.title else existing.title,
            gender=existing.gender,
            job_position_id=author.job_position_id if author.job_position_id else existing.job_position_id,
            department_id=author.department_id if author.department_id else existing.department_id
        )

        result = await self.author_repo.update(researcher_id, updated_author)

        return AuthorResponseDTO.from_entity(result)

    async def delete_author(self, author_id: UUID) -> bool:
        existing = await self.author_repo.get_by_id(author_id)
        if not existing:
            raise ValueError(f"El autor con ID {author_id} no existe.")

        return await self.author_repo.delete(author_id)
