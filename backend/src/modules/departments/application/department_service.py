from typing import List
from uuid import uuid4, UUID

from .department_dto import DepartmentResponseDTO, DepartmentCreateDTO, DepartmentUpdateDTO
from ..domain.department import Department
from ..domain.department_repository import IDepartmentRepository
from ..domain.faculty import Faculty


class DepartmentService:
    """Servicio de aplicación para la gestión de departamentos."""

    def __init__(self, dept_repo: IDepartmentRepository):
        self.dept_repo = dept_repo

    async def get_all_departments(self) -> List[DepartmentResponseDTO]:
        deps = await self.dept_repo.get_all()
        return [DepartmentResponseDTO.from_entity(dep) for dep in deps]

    async def get_departments_by_faculty(self, faculty_str: str) -> List[DepartmentResponseDTO]:
        try:
            faculty_enum = Faculty(faculty_str)
        except ValueError:
            raise ValueError(f"Facultad '{faculty_str}' no válida.")

        deps = await self.dept_repo.get_by_faculty(faculty_enum)
        return [DepartmentResponseDTO.from_entity(dep) for dep in deps]

    async def get_department_by_id(self, dept_id: UUID) -> DepartmentResponseDTO:
        department = await self.dept_repo.get_by_id(dept_id)
        if not department:
            raise ValueError(f"El departamento con ID {dept_id} no existe.")
        return DepartmentResponseDTO.from_entity(department)

    async def create_department(self, dto: DepartmentCreateDTO) -> DepartmentResponseDTO:
        new_dept = Department(
            dep_id=uuid4(),
            dep_name=dto.dep_name,
            dep_code=dto.dep_code,
            faculty=dto.faculty
        )
        saved_dept = await self.dept_repo.create(new_dept)
        return DepartmentResponseDTO.from_entity(saved_dept)

    async def update_department(self, dept_id: UUID, dto: DepartmentUpdateDTO) -> DepartmentResponseDTO:
        existing = await self.dept_repo.get_by_id(dept_id)
        if not existing:
            raise ValueError(f"El departamento con ID {dept_id} no existe.")

        updated_entity = Department(
            dep_id=dept_id,
            dep_name=dto.dep_name if dto.dep_name else existing.dep_name,
            dep_code=dto.dep_code if dto.dep_code else existing.dep_code,
            faculty=dto.faculty if dto.faculty else existing.faculty
        )

        result = await self.dept_repo.update(dept_id, updated_entity)

        return DepartmentResponseDTO.from_entity(result)

    async def delete_department(self, dep_id: UUID) -> bool:
        return await self.dept_repo.delete(dep_id)

    def get_faculties(self) -> list[dict]:
        return [
            {"id": faculty.value, "name": faculty.fac_name, "acronym": faculty.value}
            for faculty in Faculty
        ]
