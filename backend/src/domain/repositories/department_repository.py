"""
Repositorio de departamentos académicos.
Contiene la lógica de negocio referente a la gestión de departamentos.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.department import Department
from ..enums.faculty import Faculty


class IDepartmentRepository(ABC):
    """Interfaz del repositorio de departamentos."""

    @abstractmethod
    async def create(self, department: Department) -> Department:
        """Crea un nuevo departamento."""

    @abstractmethod
    async def get_all(self) -> List[Department]:
        """Obtiene todos los departamentos."""

    @abstractmethod
    async def get_by_id(self, dep_id: int) -> Optional[Department]:
        """Obtiene un departamento por su ID."""

    @abstractmethod
    async def get_by_code(self, dep_code: str) -> Optional[Department]:
        """Obtiene un departamento por su código/sigla."""

    @abstractmethod
    async def get_by_name(self, dep_name: str) -> Optional[Department]:
        """Obtiene un departamento por su nombre."""

    @abstractmethod
    async def filter_by_faculty(self, faculty: Faculty) -> List[Department]:
        """Obtiene departamentos por facultad."""

    @abstractmethod
    async def update(self, department: Department) -> Department:
        """Actualiza un departamento existente."""

    @abstractmethod
    async def delete(self, dep_id: int) -> bool:
        """Elimina un departamento por su ID."""
