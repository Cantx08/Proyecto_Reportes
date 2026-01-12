"""Controlador para la gestión de departamentos."""

from typing import List
from fastapi import HTTPException, status

from ....application.services.department_service import DepartmentService
from ....domain.entities.department import Department
from ....application.dto.department_dto import (
    DepartmentCreateDTO,
    DepartmentUpdateDTO,
    DepartmentResponseDTO,
    DepartmentsResponseDTO
)


class DepartmentsController:
    """Controlador para operaciones CRUD de departamentos."""

    def __init__(self, department_service: DepartmentService):
        self.department_service = department_service

    async def create_department(self, department_data: DepartmentCreateDTO) -> DepartmentResponseDTO:
        """Crea un nuevo departamento."""
        try:
            department = Department(
                dep_id=department_data.dep_id,
                dep_code=department_data.dep_code,
                dep_name=department_data.dep_name,
                faculty=department_data.fac_name
            )

            created_department = await self.department_service.create_department(department)
            return DepartmentResponseDTO.from_entity(created_department)

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Datos inválidos: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear departamento: {str(e)}"
            )

    async def get_department(self, dep_id: str) -> DepartmentResponseDTO:
        """Obtiene un departamento por ID."""
        try:
            department = await self.department_service.get_department_by_id(dep_id)
            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Departamento con ID {dep_id} no encontrado"
                )
            return DepartmentResponseDTO.from_entity(department)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener departamento: {str(e)}"
            )

    async def get_all_departments(self) -> DepartmentsResponseDTO:
        """Obtiene todos los departamentos."""
        try:
            departments = await self.department_service.get_all_departments()
            return DepartmentsResponseDTO.from_entities(departments)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener departamentos: {str(e)}"
            )

    async def get_departments_by_faculty(self, fac_name: str) -> List[DepartmentResponseDTO]:
        """Obtiene departamentos por facultad."""
        try:
            departments = await self.department_service.filter_departments_by_faculty(fac_name)
            return [DepartmentResponseDTO.from_entity(dept) for dept in departments]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener departamentos por facultad: {str(e)}"
            )

    async def update_department(self, dep_id: str, department_data: DepartmentUpdateDTO) -> DepartmentResponseDTO:
        """Actualiza un departamento existente."""
        try:
            # Verificar que el departamento existe
            existing_department = await self.department_service.get_department_by_id(dep_id)
            if not existing_department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Departamento con ID {dep_id} no encontrado"
                )

            # Actualizar solo los campos proporcionados
            updated_department = Department(
                dep_id=dep_id,
                dep_code=department_data.dep_code or existing_department.dep_code,
                dep_name=department_data.dep_name or existing_department.dep_name,
                faculty=department_data.fac_name or existing_department.faculty
            )

            result = await self.department_service.update_department(updated_department)
            return DepartmentResponseDTO.from_entity(result)

        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Datos inválidos: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar departamento: {str(e)}"
            )

    async def delete_department(self, dep_id: str) -> dict:
        """Elimina un departamento."""
        try:
            # Verificar que el departamento existe
            existing_department = await self.department_service.get_department_by_id(dep_id)
            if not existing_department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Departamento con ID {dep_id} no encontrado"
                )

            success = await self.department_service.delete_department(dep_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al eliminar departamento"
                )

            return {"message": f"Departamento {dep_id} eliminado correctamente"}

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar departamento: {str(e)}"
            )
