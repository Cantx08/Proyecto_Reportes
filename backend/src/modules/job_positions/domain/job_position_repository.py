from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .job_position import JobPosition


class IJobPositionRepository(ABC):
    """Interfaz del repositorio de cargos/posiciones."""

    @abstractmethod
    async def get_all(self) -> List[JobPosition]:
        """Obtiene todos los cargos."""

    @abstractmethod
    async def get_by_id(self, pos_id: UUID) -> Optional[JobPosition]:
        """Obtiene un cargo por su ID."""

    @abstractmethod
    async def create(self, position: JobPosition) -> JobPosition:
        """Crea un nuevo cargo."""

    @abstractmethod
    async def update(self, pos_id: UUID, position: JobPosition) -> JobPosition:
        """Actualiza un cargo existente."""

    @abstractmethod
    async def delete(self, pos_id: UUID) -> bool:
        """Elimina un cargo por su ID."""
