"""
Caso de Uso para obtener los departamentos de una facultad.
"""

from typing import List
from ....domain.entities.department import Department
from ....domain.enums.faculty import Faculty
from ....domain.repositories.department_repository import IDepartmentRepository


class FilterDepartmentsByFacultyUseCase:
    """
    Obtiene una lista de todos los departamentos que pertenecen a una facultad específica.
    """

    def __init__(self, repository: IDepartmentRepository):
        """Inicializa el caso de uso con el repositorio de departamentos."""
        self._repository = repository

    async def execute(self, faculty_name: str) -> List[Department]:
        """
        Filtra departamentos por facultad.

        Args:
            faculty_name: El nombre de la facultad.

        Returns:
            Una lista de Departamentos pertenecientes a dicha facultad.
        """

        faculty = Faculty.from_string(faculty_name)

        return await self._repository.filter_by_faculty(faculty)
