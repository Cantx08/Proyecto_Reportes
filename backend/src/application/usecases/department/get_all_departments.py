"""
Caso de uso para obtener todos los departamentos registrados.
"""
from typing import List

from ....domain.entities.department import Department
from ....domain.repositories.department_repository import IDepartmentRepository


class GetAllDepartmentsUseCase:
    def __init__(self, repository: IDepartmentRepository):
        """Inicializa el caso de uso con el repositorio de departamentos."""
        self.repository = repository

    async def execute(self) -> List[Department]:
        """
        Obtiene todos los departamentos.

        Returns:
            Una lista de Departamentos
        """

        return await self.repository.get_all()
