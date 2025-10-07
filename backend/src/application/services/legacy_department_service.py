"""Servicio legacy para departamentos que funciona con el repositorio legacy."""

from ...infrastructure.repositories.departments_file_repository import DepartmentsFileRepository
from ..dtos.legacy_department_dto import LegacyDepartmentsResponseDTO


class LegacyDepartmentService:
    """Servicio legacy para manejar departamentos usando el repositorio legacy."""

    def __init__(self, departments_repository: DepartmentsFileRepository):
        """
        Inicializar el servicio con el repositorio legacy.
        
        Args:
            departments_repository: Repositorio legacy de departamentos
        """
        self.departments_repository = departments_repository

    async def get_all_departments(self) -> LegacyDepartmentsResponseDTO:
        """
        Obtener todos los departamentos usando el repositorio legacy.
        
        Returns:
            DTO de respuesta con la lista de departamentos
        """
        departments = self.departments_repository.get_all_departments()
        return LegacyDepartmentsResponseDTO(departments=departments)
