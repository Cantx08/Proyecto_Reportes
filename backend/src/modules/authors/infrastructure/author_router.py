from typing import List
from uuid import UUID
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from .db_author_repository import DBAuthorRepository
from ..application.author_dto import AuthorUpdateDTO, AuthorCreateDTO, AuthorResponseDTO
from ..application.author_service import AuthorService
from ....shared.database import get_db

router = APIRouter(prefix="/authors", tags=["Autores"])


def get_service(db: Session = Depends(get_db)) -> AuthorService:
    author_repo = DBAuthorRepository(db)
    return AuthorService(author_repo)


@router.get("", response_model=List[AuthorResponseDTO])
async def get_authors(service: AuthorService = Depends(get_service)):
    return await service.get_all_authors()


@router.get("/{author_id}", response_model=AuthorResponseDTO)
async def get_author_by_id(author_id: UUID, service: AuthorService = Depends(get_service)):
    try:
        return await service.get_author_by_id(author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/departments/{dep_code}", response_model=List[AuthorResponseDTO])
async def get_authors_by_department(dep_code: str, service: AuthorService = Depends(get_service)):
    try:
        return await service.get_authors_by_department(dep_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_model=AuthorResponseDTO, status_code=201)
async def create_author(dto: AuthorCreateDTO, service: AuthorService = Depends(get_service)):
    try:
        return await service.create_author(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{author_id}", response_model=AuthorResponseDTO)
async def update_author(
        author_id: UUID,
        dto: AuthorUpdateDTO,
        service: AuthorService = Depends(get_service)
):
    try:
        return await service.update_author(author_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{author_id}")
async def delete_author(author_id: UUID, service: AuthorService = Depends(get_service)):
    deleted = await service.delete_author(author_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return {"message": "Autor y cuentas Scopus eliminadas."}
