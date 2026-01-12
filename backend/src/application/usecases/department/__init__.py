"""Paquete de casos de uso para la entidad Departamento."""

from .create_department import CreateDepartmentUseCase
from .get_all_departments import GetAllDepartmentsUseCase
from .get_department_by_id import GetDepartmentByIDUseCase
from .get_department_by_code import GetDepartmentByCodeUseCase
from .get_department_by_name import GetDepartmentByNameUseCase
from .filter_departments_by_faculty import FilterDepartmentsByFacultyUseCase
from .update_department import UpdateDepartmentUseCase
from .delete_department import DeleteDepartmentUseCase

__all__ = [
    "CreateDepartmentUseCase",
    "GetAllDepartmentsUseCase",
    "GetDepartmentByIDUseCase",
    "GetDepartmentByCodeUseCase",
    "GetDepartmentByNameUseCase",
    "FilterDepartmentsByFacultyUseCase",
    "UpdateDepartmentUseCase",
    "DeleteDepartmentUseCase"
]