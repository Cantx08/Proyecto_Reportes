"""
Caso de uso para crear un departamento.
"""

from ....domain.entities.department import Department
from ....domain.enums.faculty import Faculty
from ....domain.exceptions import DepartmentAlreadyExists, InvalidEntityData
from ....domain.repositories.department_repository import IDepartmentRepository


class CreateDepartmentUseCase:
    """Asegura la creación eficiente de un nuevo departamento."""

    def __init__(self, repository: IDepartmentRepository):
        """Inicializa el caso de uso con el repositorio de departamentos."""
        self._repository = repository

    async def execute(self, dept_code: str, dept_name: str, fac_name: str) -> Department:
        """
        Crea un nuevo departamento.

        Args:
            dept_code: Siglas del departamento.
            dept_name: Nombre del departamento.
            fac_name: Nombre de la facultad a la que pertenece el departamento.

        Returns:
            El departamento creado.

        Raises:
            InvalidEntityData: Si los datos de entrada no cumplen las reglas de negocio.
            DepartmentAlreadyExists: Si ya existe un departamento con ese código o nombre.
        """

        existing_by_code = await self._repository.get_by_code(dept_code)
        if existing_by_code:
            raise DepartmentAlreadyExists(dep_code=dept_code)

        existing_by_name = await self._repository.get_by_name(dept_name)
        if existing_by_name:
            raise DepartmentAlreadyExists(dep_name=dept_name)

        faculty_enum = Faculty.from_string(fac_name)

        try:
            department = Department(
                dep_code=dept_code,
                dep_name=dept_name,
                fac_name=faculty_enum
            )
        except InvalidEntityData as e:
            raise e

        created_department = await self._repository.create(department)

        return created_department
