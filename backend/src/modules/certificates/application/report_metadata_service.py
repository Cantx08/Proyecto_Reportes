"""
Servicio de aplicación para gestionar metadatos de reportes.
Permite guardar, listar, actualizar y eliminar metadatos sin repetir la búsqueda de publicaciones.
"""
import uuid
from typing import List, Optional
from uuid import UUID

from ..domain.report_metadata import ReportMetadata
from ..domain.report_metadata_repository import IReportMetadataRepository
from .report_metadata_dto import (
    SaveReportMetadataDTO,
    UpdateReportMetadataDTO,
    ReportMetadataResponseDTO,
)


class ReportMetadataService:
    """Servicio de aplicación para CRUD de metadatos de reportes."""

    def __init__(self, repository: IReportMetadataRepository):
        self._repo = repository

    async def save(self, dto: SaveReportMetadataDTO) -> ReportMetadataResponseDTO:
        """Guarda un nuevo conjunto de metadatos."""
        entity = ReportMetadata(
            id=uuid.uuid4(),
            author_name=dto.author_name,
            author_gender=dto.author_gender,
            department=dto.department,
            position=dto.position,
            author_ids=dto.author_ids,
            publications=[pub.model_dump() for pub in dto.publications],
            subject_areas=dto.subject_areas,
            documents_by_year=dto.documents_by_year,
            memorandum=dto.memorandum,
            signatory=dto.signatory,
            signatory_name=dto.signatory_name,
            report_date=dto.report_date,
            elaborador=dto.elaborador,
            label=dto.label or f"Reporte - {dto.author_name}",
        )
        saved = await self._repo.save(entity)
        return self._to_response(saved)

    async def get_by_id(self, metadata_id: UUID) -> Optional[ReportMetadataResponseDTO]:
        """Obtiene metadatos por ID."""
        entity = await self._repo.get_by_id(metadata_id)
        return self._to_response(entity) if entity else None

    async def get_all(self) -> List[ReportMetadataResponseDTO]:
        """Lista todos los metadatos guardados."""
        entities = await self._repo.get_all()
        return [self._to_response(e) for e in entities]

    async def update(self, metadata_id: UUID, dto: UpdateReportMetadataDTO) -> ReportMetadataResponseDTO:
        """Actualiza solo los campos editables de un registro."""
        entity = await self._repo.get_by_id(metadata_id)
        if not entity:
            raise ValueError(f"Metadatos con id {metadata_id} no encontrados")

        # Actualizar solo campos editables
        entity.memorandum = dto.memorandum
        entity.signatory = dto.signatory
        entity.signatory_name = dto.signatory_name
        entity.report_date = dto.report_date
        entity.elaborador = dto.elaborador
        if dto.label is not None:
            entity.label = dto.label

        updated = await self._repo.update(entity)
        return self._to_response(updated)

    async def delete(self, metadata_id: UUID) -> bool:
        """Elimina un registro."""
        return await self._repo.delete(metadata_id)

    @staticmethod
    def _to_response(entity: ReportMetadata) -> ReportMetadataResponseDTO:
        return ReportMetadataResponseDTO(
            id=entity.id,
            author_name=entity.author_name,
            author_gender=entity.author_gender,
            department=entity.department,
            position=entity.position,
            author_ids=entity.author_ids,
            publications=entity.publications,
            subject_areas=entity.subject_areas,
            documents_by_year=entity.documents_by_year,
            memorandum=entity.memorandum,
            signatory=entity.signatory,
            signatory_name=entity.signatory_name,
            report_date=entity.report_date,
            elaborador=entity.elaborador,
            label=entity.label,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
