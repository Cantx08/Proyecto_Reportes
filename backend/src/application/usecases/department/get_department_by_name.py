"""
Caso de uso para obtener un departamento por su nombre.
"""

from ....domain.entities.department import Department
from ....domain.exceptions import DepartmentNotFound
from ....domain.repositories.department_repository import IDepartmentRepository


class GetDepartmentByNameUseCase:
    """Permite obtener la información de un departamento específico mediante su nombre."""

    def __init__(self, repository: IDepartmentRepository):
        """Inicializa el caso de uso con el repositorio de departamentos."""
        self._repository = repository

    async def execute(self, dept_name: str) -> Department:
        """
        Obtiene un departamento por su nombre.

        Args:
            dept_name: Departamento a buscar.

        Returns:
            El departamento encontrado.

        Raises:
            DepartmentNotFound: Si no se encuentra ningún departamento con ese nombre.
        """

        department = await self._repository.get_by_name(dept_name)

        if department is None:
            raise DepartmentNotFound(dep_name=dept_name)

        return department
