from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.department import Department


class DepartmentRepository(ABC):
    """Interfaz del repositorio de departamentos."""
    
    @abstractmethod
    async def get_by_id(self, dep_id: str) -> Optional["Department"]:
        """Obtiene un departamento por su ID."""
        ...
    
    @abstractmethod
    async def get_by_code(self, dep_code: str) -> Optional["Department"]:
        """Obtiene un departamento por su código/sigla."""
        ...
    
    @abstractmethod
    async def get_all(self) -> List["Department"]:
        """Obtiene todos los departamentos."""
        ...
    
    @abstractmethod
    async def create(self, department: "Department") -> "Department":
        """Crea un nuevo departamento."""
        ...
    
    @abstractmethod
    async def update(self, department: "Department") -> "Department":
        """Actualiza un departamento existente."""
        ...
    
    @abstractmethod
    async def delete(self, dep_id: str) -> bool:
        """Elimina un departamento por su ID."""
        ...
    
    @abstractmethod
    async def get_by_faculty(self, faculty_name: str) -> List["Department"]:
        """Obtiene departamentos por facultad."""
        ...