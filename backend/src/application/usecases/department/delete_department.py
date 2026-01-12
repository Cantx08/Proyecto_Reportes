"""
Caso de uso para eliminar un departamento.
"""
from ....domain.exceptions import DepartmentNotFound, CannotDeleteDepartment
from ....domain.repositories.department_repository import IDepartmentRepository


class DeleteDepartmentUseCase:
    """Orquesta la eliminación de un departamento por su ID."""

    def __init__(self, repository: IDepartmentRepository):
        self._repository = repository

    async def execute(self, dept_id: int) -> bool:
        """
        Elimina un departamento.

        Args:
            dept_id: El ID del departamento a eliminar.

        Returns:
            True si la eliminación fue exitosa.

        Raises:
            DepartmentNotFound: Si el departamento no existe.
            CannotDeleteDepartment: En casos estrictos donde no pueda eliminarse el departamento.
        """

        department = await self._repository.get_by_id(dept_id)
        if department is None:
            raise DepartmentNotFound(dep_id=dept_id)

        try:
            success = await self._repository.delete(dept_id)
            return success
        except CannotDeleteDepartment as e:
            raise e