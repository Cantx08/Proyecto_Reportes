"""
Caso de uso para obtener un departamento por su sigla.
"""

from ....domain.entities.department import Department
from ....domain.exceptions import DepartmentNotFound
from ....domain.repositories.department_repository import IDepartmentRepository


class GetDepartmentByCodeUseCase:
    """Permite obtener la información de un departamento específico mediante su sigla."""

    def __init__(self, repository: IDepartmentRepository):
        """Inicializa el caso de uso con el repositorio de departamentos."""
        self._repository = repository

    async def execute(self, dept_code: str) -> Department:
        """
        Obtiene un departamento por su sigla.

        Args:
            dept_code: Sigla del departamento a buscar.

        Returns:
            El departamento encontrado.

        Raises:
            DepartmentNotFound: Si no se encuentra ningún departamento con esa sigla.
        """

        department = await self._repository.get_by_code(dept_code)

        if department is None:
            raise DepartmentNotFound(dep_code=dept_code)

        return department
