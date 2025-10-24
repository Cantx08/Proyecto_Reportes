from typing import List, Optional
from ...domain.entities.author import Author
from ...domain.repositories.author_repository import AuthorRepository


class AuthorService:
    """Servicio de aplicación para la gestión de autores."""

    def __init__(self, author_repository: AuthorRepository):
        self._author_repository = author_repository

    async def get_author_by_id(self, author_id: str) -> Optional[Author]:
        """Obtiene un autor por su ID."""
        if not author_id:
            raise ValueError("Author ID is required")
        return await self._author_repository.get_by_id(author_id)

    async def get_all_authors(self) -> List[Author]:
        """Obtiene todos los autores."""
        return await self._author_repository.get_all()

    async def create_author(self, author: Author) -> Author:
        """Crea un nuevo autor."""
        # El author_id es opcional en la creación, la BD lo generará automáticamente si no se proporciona
        # Solo verificar si se proporciona un ID y si ya existe
        if author.author_id and author.author_id.strip():
            existing_author = await self._author_repository.get_by_id(author.author_id)
            if existing_author:
                raise ValueError(f"Author with ID {author.author_id} already exists")

        return await self._author_repository.create(author)

    async def update_author(self, author: Author) -> Author:
        """Actualiza un autor existente."""
        if not author.author_id:
            raise ValueError("Author ID is required")

        # Verificar que existe
        existing_author = await self._author_repository.get_by_id(author.author_id)
        if not existing_author:
            raise ValueError(f"Author with ID {author.author_id} not found")

        return await self._author_repository.update(author)

    async def delete_author(self, author_id: str) -> bool:
        """Elimina un autor por su ID."""
        if not author_id:
            raise ValueError("Author ID is required")

        # Verificar que existe
        existing_author = await self._author_repository.get_by_id(author_id)
        if not existing_author:
            raise ValueError(f"Author with ID {author_id} not found")

        return await self._author_repository.delete(author_id)

    async def get_authors_by_department(self, department: str) -> List[Author]:
        """Obtiene autores por departamento."""
        if not department:
            raise ValueError("Department is required")
        return await self._author_repository.get_by_department(department)

    async def get_authors_by_position(self, position: str) -> List[Author]:
        """Obtiene autores por cargo."""
        if not position:
            raise ValueError("Position is required")
        return await self._author_repository.get_by_position(position)

    async def search_authors_by_name(self, search_term: str) -> List[Author]:
        """Busca autores por nombre o apellido."""
        if not search_term or len(search_term.strip()) < 2:
            raise ValueError("Search term must be at least 2 characters")
        return await self._author_repository.search_by_name(search_term.strip())

    async def get_author_statistics(self) -> dict:
        """Obtiene estadísticas de los autores."""
        authors = await self.get_all_authors()

        # Contar por departamento
        departments = {}
        positions = {}
        genders = {}

        for author in authors:
            # Departamentos
            if author.department:
                departments[author.department] = departments.get(author.department, 0) + 1

            # Cargos
            if author.position:
                positions[author.position] = positions.get(author.position, 0) + 1

            # Géneros
            if author.gender:
                genders[author.gender] = genders.get(author.gender, 0) + 1

        return {
            "total_authors": len(authors),
            "by_department": departments,
            "by_position": positions,
            "by_gender": genders
        }
