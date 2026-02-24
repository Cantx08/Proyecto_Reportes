"""
Interfaz abstracta para el repositorio de metadatos de reportes.
Sigue DIP: el dominio define la abstracción, infrastructure implementa.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .report_metadata import ReportMetadata


class IReportMetadataRepository(ABC):
    """Interfaz del repositorio de metadatos de reportes."""

    @abstractmethod
    async def save(self, metadata: ReportMetadata) -> ReportMetadata:
        """Guarda un nuevo registro de metadatos."""
        ...

    @abstractmethod
    async def get_by_id(self, metadata_id: UUID) -> Optional[ReportMetadata]:
        """Obtiene metadatos por su ID."""
        ...

    @abstractmethod
    async def get_all(self) -> List[ReportMetadata]:
        """Obtiene todos los registros de metadatos, ordenados por actualización."""
        ...

    @abstractmethod
    async def update(self, metadata: ReportMetadata) -> ReportMetadata:
        """Actualiza un registro existente (solo campos editables)."""
        ...

    @abstractmethod
    async def delete(self, metadata_id: UUID) -> bool:
        """Elimina un registro por su ID. Retorna True si se eliminó."""
        ...
