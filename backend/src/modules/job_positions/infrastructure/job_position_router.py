from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.src.shared.database import get_db

from .db_job_position_repository import DBJobPositionRepository
from ..application.job_position_dto import JobPositionResponseDTO, JobPositionCreateDTO, JobPositionUpdateDTO
from ..application.job_position_service import JobPositionService

router = APIRouter(prefix="/job-positions", tags=["Cargos"])


def get_service(db: Session = Depends(get_db)) -> JobPositionService:
    """Inyector de dependencias local del módulo"""
    pos_repo = DBJobPositionRepository(db)
    return JobPositionService(pos_repo)


@router.get("", response_model=List[JobPositionResponseDTO])
async def get_positions(service: JobPositionService = Depends(get_service)):
    return await service.get_all_positions()


@router.post("", response_model=JobPositionResponseDTO, status_code=201)
async def create_position(dto: JobPositionCreateDTO, service: JobPositionService = Depends(get_service)):
    return await service.create_position(dto)


@router.put("/{pos_id}", response_model=JobPositionResponseDTO)
async def update_position(
        pos_id: UUID,
        dto: JobPositionUpdateDTO,
        service: JobPositionService = Depends(get_service)
):
    try:
        return await service.update_position(pos_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        if "unique" in str(e).lower():
            raise HTTPException(status_code=409, detail="Ya existe un cargo con ese nombre.")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{pos_id}")
async def delete_position(pos_id: UUID, service: JobPositionService = Depends(get_service)):
    deleted = await service.delete_position(pos_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return {"message": "Eliminado correctamente"}
