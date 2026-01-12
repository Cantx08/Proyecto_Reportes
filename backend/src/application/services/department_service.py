from typing import List, Optional
from ...domain.entities.department import Department
from ...domain.repositories.department_repository import IDepartmentRepository


class DepartmentService:
    """Servicio de aplicación para la gestión de departamentos."""
    
    def __init__(self, department_repository: IDepartmentRepository):
        self._department_repository = department_repository
    
    async def get_department_by_id(self, dep_id: int) -> Optional[Department]:
        """Obtiene un departamento por su ID."""
        if not dep_id:
            raise ValueError("Department ID is required")
        return await self._department_repository.get_by_id(dep_id)
    
    async def get_department_by_code(self, dep_code: str) -> Optional[Department]:
        """Obtiene un departamento por su código/sigla."""
        if not dep_code:
            raise ValueError("Department code is required")
        return await self._department_repository.get_by_name(dep_code)
    
    async def get_all_departments(self) -> List[Department]:
        """Obtiene todos los departamentos."""
        return await self._department_repository.get_all()
    
    async def create_department(self, department: Department) -> Department:
        """Crea un nuevo departamento."""
        # Verificar que no exista el código
        existing_code = await self._department_repository.get_by_code(department.dep_code)
        if existing_code:
            raise ValueError(f"Department with code {department.dep_code} already exists")
        
        return await self._department_repository.create(department)
    
    async def update_department(self, department: Department) -> Department:
        """Actualiza un departamento existente."""
        if not department.dep_id:
            raise ValueError("Department ID is required")
        
        # Verificar que existe
        existing_dept = await self._department_repository.get_by_id(department.dep_id)
        if not existing_dept:
            raise ValueError(f"Department with ID {department.dep_id} not found")
        
        return await self._department_repository.update(department)
    
    async def delete_department(self, dep_id: str) -> bool:
        """Elimina un departamento por su ID."""
        if not dep_id:
            raise ValueError("Department ID is required")
        
        # Verificar que existe
        existing_dept = await self._department_repository.get_by_id(dep_id)
        if not existing_dept:
            raise ValueError(f"Department with ID {dep_id} not found")
        
        return await self._department_repository.delete(dep_id)
    
    async def filter_departments_by_faculty(self, faculty_name: str) -> List[Department]:
        """Obtiene departamentos por facultad."""
        if not faculty_name:
            raise ValueError("Faculty name is required")
        return await self._department_repository.filter_by_faculty(faculty_name)