from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from backend.src.shared.database import get_db

from .db_department_repository import DBDepartmentRepository
from ..application.department_dto import DepartmentResponseDTO, DepartmentCreateDTO, DepartmentUpdateDTO
from ..application.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departamentos"])


def get_service(db: Session = Depends(get_db)) -> DepartmentService:
    """Inyector de dependencias local del módulo"""
    dept_repo = DBDepartmentRepository(db)
    return DepartmentService(dept_repo)


@router.get("", response_model=List[DepartmentResponseDTO])
async def get_departments(service: DepartmentService = Depends(get_service)):
    return await service.get_all_departments()


@router.get("/faculty/{faculty_code}", response_model=List[DepartmentResponseDTO])
async def get_departments_by_faculty(faculty_code: str, service: DepartmentService = Depends(get_service)):
    try:
        return await service.get_departments_by_faculty(faculty_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_model=DepartmentResponseDTO, status_code=201)
async def create_department(dto: DepartmentCreateDTO, service: DepartmentService = Depends(get_service)):
    return await service.create_department(dto)


@router.put("/{dep_id}", response_model=DepartmentResponseDTO)
async def update_department(
        dep_id: UUID,
        dto: DepartmentUpdateDTO,
        service: DepartmentService = Depends(get_service)
):
    try:
        return await service.update_department(dep_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{dep_id}")
async def delete_department(dep_id: UUID, service: DepartmentService = Depends(get_service)):
    deleted = await service.delete_department(dep_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return {"message": "Eliminado correctamente"}
