from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .department import Department
from .faculty import Faculty


class IDepartmentRepository(ABC):
    """Interfaz del repositorio de departamentos."""

    @abstractmethod
    async def get_all(self) -> List[Department]:
        """Obtiene todos los departamentos."""

    @abstractmethod
    async def get_by_faculty(self, faculty: Faculty) -> List[Department]:
        """Obtiene departamentos por facultad."""

    @abstractmethod
    async def get_by_id(self, dep_id: UUID) -> Optional[Department]:
        """Obtiene un departamento por su ID."""

    @abstractmethod
    async def create(self, department: Department) -> Department:
        """Crea un nuevo departamento."""

    @abstractmethod
    async def update(self, dep_id: UUID, department: Department) -> Department:
        """Actualiza un departamento existente."""

    @abstractmethod
    async def delete(self, dep_id: UUID) -> bool:
        """Elimina un departamento por su ID."""
