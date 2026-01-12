"""
Caso de uso para obtener un departamento por su ID.
"""

from ....domain.entities.department import Department
from ....domain.exceptions import DepartmentNotFound
from ....domain.repositories.department_repository import IDepartmentRepository


class GetDepartmentByIDUseCase:
    """Permite obtener la información de un departamento específico mediante su ID."""

    def __init__(self, repository: IDepartmentRepository):
        """Inicializa el caso de uso con el repositorio de departamentos."""
        self._repository = repository

    async def execute(self, dept_id: int) -> Department:
        """
        Obtiene un departamento por su ID.

        Args:
            dept_id: ID del departamento a buscar.

        Returns:
            El departamento encontrado.

        Raises:
            DepartmentNotFound: Si no se encuentra ningún departamento con ese ID.
        """

        department = await self._repository.get_by_id(dept_id)

        if department is None:
            raise DepartmentNotFound(dep_id=dept_id)

        return department
