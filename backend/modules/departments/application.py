from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel

from .domain import Faculty, Department, IDepartmentRepository


# ============== DTOS para la gestión de departamentos ==============
class DepartmentCreateDTO(BaseModel):
    dep_name: str
    dep_code: str
    faculty: Faculty


class DepartmentUpdateDTO(BaseModel):
    dep_name: Optional[str] = None
    dep_code: Optional[str] = None
    faculty: Optional[Faculty] = None


class DepartmentResponseDTO(BaseModel):
    dep_id: UUID
    dep_name: str
    dep_code: str
    faculty_code: str
    faculty_name: str

    @staticmethod
    def from_entity(dept: Department) -> 'DepartmentResponseDTO':
        return DepartmentResponseDTO(
            dep_id=dept.dep_id,
            dep_name=dept.dep_name,
            dep_code=dept.dep_code,
            faculty_code=dept.faculty.fac_code,
            faculty_name=dept.faculty.fac_name
        )


# ============== Servicios para la gestión de departamentos ==============
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
