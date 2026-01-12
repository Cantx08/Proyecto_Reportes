"""
Caso de uso para actualizar un departamento.
"""
from ....domain.entities.department import Department
from ....domain.enums.faculty import Faculty
from ....domain.exceptions import DepartmentNotFound, DepartmentAlreadyExists, InvalidEntityData
from ....domain.repositories.department_repository import IDepartmentRepository


class UpdateDepartmentUseCase:
    """Orquesta la actualización de un departamento existente."""

    def __init__(self, repository: IDepartmentRepository):
        """Inicializa el caso de uso con el repositorio de departamentos."""
        self._repository = repository

    async def execute(self, dept_id: int, dept_code: str, dept_name: str, fac_name: str) -> Department:
        """
        Actualiza la información de un departamento existente.

        Args:
            dept_id: El ID del departamento a actualizar.
            dept_code: La sigla modificada del departamento.
            dept_name: El nombre modificado del departamento.
            fac_name: La facultad actualizada a la cual pertenece.

        Returns:
            El departamento con su información actualizada.

        Raises:
            DepartmentNotFound: Si el departamento a actualizar no existe.
            DepartmentAlreadyExists: Si la sigla o el nombre modificado corresponden a *otro* departamento.
            InvalidEntityData: Si los nuevos datos no cumplen las reglas de negocio.
        """

        department = await self._repository.get_by_id(dept_id)
        if department is None:
            raise DepartmentNotFound(dep_id=dept_id)

        if dept_code.upper() != department.dep_code:
            existing_by_code = await self._repository.get_by_code(dept_code)
            if existing_by_code and existing_by_code.dep_id != dept_id:
                raise DepartmentAlreadyExists(dep_code=dept_code)

        if dept_name.strip() != department.dep_name:
            existing_by_name = await self._repository.get_by_name(dept_name)
            if existing_by_name and existing_by_name.dep_id != dept_id:
                raise DepartmentAlreadyExists(dep_name=dept_name)

        new_faculty = Faculty.from_string(fac_name)

        try:
            department.update_details(
                dep_name=dept_name,
                dep_code=dept_code,
                faculty=new_faculty
            )
        except InvalidEntityData as e:
            raise e

        updated_department = await self._repository.update(department)

        return updated_department
