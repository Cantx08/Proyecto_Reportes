from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from ..domain.department import Department
from ..domain.faculty import Faculty


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
