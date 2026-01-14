from fastapi import HTTPException
from typing import List

from ....application.dto import (
    AuthorDTO, AuthorCreateDTO, AuthorUpdateDTO,
    AuthorsResponseDTO, AuthorResponseDTO
)
from ....application.services.author_service import AuthorService
from ....domain.entities.author import Author


class AuthorsController:
    """Controlador para manejar endpoints relacionados con autores."""
    
    def __init__(self, author_service: AuthorService):
        self.author_service = author_service

    async def export_authors(self) -> List[dict]:
        """Exporta todos los autores con datos completos para CSV."""
        try:
            return await self.author_service.get_authors_for_export()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def import_authors(self, authors_data: List[dict]) -> dict:
        """Importa autores desde datos de CSV."""
        try:
            return await self.author_service.import_authors(authors_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_author_by_id(self, author_id: str) -> AuthorResponseDTO:
        """Obtiene un autor por su ID."""
        try:
            author = await self.author_service.get_author_by_id(author_id)
            if not author:
                return AuthorResponseDTO(
                    success=False,
                    data=None,
                    message=f"Author with ID {author_id} not found"
                )
            
            author_dto = AuthorDTO(
                author_id=author.author_id,
                name=author.name,
                surname=author.surname,
                dni=author.dni,
                title=author.title,
                institutional_email=author.institutional_email,
                gender=author.gender,
                position=author.position,
                department=author.department,
                publications_list=None,  # Se puede cargar por separado
                error=author.error
            )
            
            return AuthorResponseDTO(
                success=True,
                data=author_dto,
                message="Author retrieved successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_all_authors(self) -> AuthorsResponseDTO:
        """Obtiene todos los autores."""
        try:
            authors = await self.author_service.get_all_authors()
            
            authors_dto = [
                AuthorDTO(
                    author_id=author.author_id,
                    name=author.name,
                    surname=author.surname,
                    dni=author.dni,
                    title=author.title,
                    institutional_email=author.institutional_email,
                    gender=author.gender,
                    position=author.position,
                    department=author.department,
                    publications_list=None,
                    error=author.error
                )
                for author in authors
            ]
            
            return AuthorsResponseDTO(
                success=True,
                data=authors_dto,
                message=f"Retrieved {len(authors)} authors successfully",
                total=len(authors)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def create_author(self, author_create: AuthorCreateDTO) -> AuthorResponseDTO:
        """Crea un nuevo autor."""
        try:
            author = Author(
                author_id=author_create.author_id,
                name=author_create.name,
                surname=author_create.surname,
                dni=author_create.dni,
                title=author_create.title,
                institutional_email=author_create.institutional_email,
                gender=author_create.gender,
                position=author_create.position,
                department=author_create.department
            )
            
            created_author = await self.author_service.create_author(author)
            
            author_dto = AuthorDTO(
                author_id=created_author.author_id,
                name=created_author.name,
                surname=created_author.surname,
                dni=created_author.dni,
                title=created_author.title,
                institutional_email=created_author.institutional_email,
                gender=created_author.gender,
                position=created_author.position,
                department=created_author.department,
                publications_list=None,
                error=None
            )
            
            return AuthorResponseDTO(
                success=True,
                data=author_dto,
                message="Author created successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_author(self, author_id: str, author_update: AuthorUpdateDTO) -> AuthorResponseDTO:
        """Actualiza un autor existente."""
        try:
            # Obtener el autor actual
            existing_author = await self.author_service.get_author_by_id(author_id)
            if not existing_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
            
            # Actualizar solo los campos proporcionados
            updated_author = Author(
                author_id=existing_author.author_id,
                name=author_update.name if author_update.name is not None else existing_author.name,
                surname=author_update.surname if author_update.surname is not None else existing_author.surname,
                dni=author_update.dni if author_update.dni is not None else existing_author.dni,
                title=author_update.title if author_update.title is not None else existing_author.title,
                institutional_email=author_update.institutional_email if author_update.institutional_email is not None else existing_author.institutional_email,
                gender=author_update.gender if author_update.gender is not None else existing_author.gender,
                position=author_update.position if author_update.position is not None else existing_author.position,
                department=author_update.department if author_update.department is not None else existing_author.department,
                publications_list=existing_author.publications_list
            )
            
            result_author = await self.author_service.update_author(updated_author)
            
            author_dto = AuthorDTO(
                author_id=result_author.author_id,
                name=result_author.name,
                surname=result_author.surname,
                dni=result_author.dni,
                title=result_author.title,
                institutional_email=result_author.institutional_email,
                gender=result_author.gender,
                position=result_author.position,
                department=result_author.department,
                publications_list=None,
                error=None
            )
            
            return AuthorResponseDTO(
                success=True,
                data=author_dto,
                message="Author updated successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def delete_author(self, author_id: str) -> AuthorResponseDTO:
        """Elimina un autor por su ID."""
        try:
            deleted = await self.author_service.delete_author(author_id)
            if not deleted:
                raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
            
            return AuthorResponseDTO(
                success=True,
                data=None,
                message="Author deleted successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def search_authors(self, search_term: str) -> AuthorsResponseDTO:
        """Busca autores por nombre o apellido."""
        try:
            authors = await self.author_service.search_authors_by_name(search_term)
            
            authors_dto = [
                AuthorDTO(
                    author_id=author.author_id,
                    name=author.name,
                    surname=author.surname,
                    dni=author.dni,
                    title=author.title,
                    institutional_email=author.institutional_email,
                    gender=author.gender,
                    position=author.position,
                    department=author.department,
                    publications_list=None,
                    error=author.error
                )
                for author in authors
            ]
            
            return AuthorsResponseDTO(
                success=True,
                data=authors_dto,
                message=f"Found {len(authors)} authors matching '{search_term}'",
                total=len(authors)
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_authors_by_department(self, department: str) -> AuthorsResponseDTO:
        """Obtiene autores por departamento."""
        try:
            authors = await self.author_service.get_authors_by_department(department)
            
            authors_dto = [
                AuthorDTO(
                    author_id=author.author_id,
                    name=author.name,
                    surname=author.surname,
                    dni=author.dni,
                    title=author.title,
                    institutional_email=author.institutional_email,
                    gender=author.gender,
                    position=author.position,
                    department=author.department,
                    publications_list=None,
                    error=author.error
                )
                for author in authors
            ]
            
            return AuthorsResponseDTO(
                success=True,
                data=authors_dto,
                message=f"Found {len(authors)} authors in department '{department}'",
                total=len(authors)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_authors_by_position(self, position: str) -> AuthorsResponseDTO:
        """Obtiene autores por cargo."""
        try:
            authors = await self.author_service.get_authors_by_position(position)
            
            authors_dto = [
                AuthorDTO(
                    author_id=author.author_id,
                    name=author.name,
                    surname=author.surname,
                    dni=author.dni,
                    title=author.title,
                    institutional_email=author.institutional_email,
                    gender=author.gender,
                    position=author.position,
                    department=author.department,
                    publications_list=None,
                    error=author.error
                )
                for author in authors
            ]
            
            return AuthorsResponseDTO(
                success=True,
                data=authors_dto,
                message=f"Found {len(authors)} authors with position '{position}'",
                total=len(authors)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))