"""
Implementación del repositorio de metadatos de reportes usando SQLAlchemy.
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..domain.report_metadata import ReportMetadata
from ..domain.report_metadata_repository import IReportMetadataRepository
from .report_metadata_model import ReportMetadataModel


class DBReportMetadataRepository(IReportMetadataRepository):
    """Repositorio de metadatos de reportes con SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    async def save(self, metadata: ReportMetadata) -> ReportMetadata:
        model = ReportMetadataModel.from_entity(metadata)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    async def get_by_id(self, metadata_id: UUID) -> Optional[ReportMetadata]:
        model = (
            self.db.query(ReportMetadataModel)
            .filter(ReportMetadataModel.id == metadata_id)
            .first()
        )
        return model.to_entity() if model else None

    async def get_all(self) -> List[ReportMetadata]:
        models = (
            self.db.query(ReportMetadataModel)
            .order_by(ReportMetadataModel.updated_at.desc())
            .all()
        )
        return [m.to_entity() for m in models]

    async def update(self, metadata: ReportMetadata) -> ReportMetadata:
        model = (
            self.db.query(ReportMetadataModel)
            .filter(ReportMetadataModel.id == metadata.id)
            .first()
        )
        if not model:
            raise ValueError(f"Metadatos con id {metadata.id} no encontrados")

        # Solo actualizar campos editables
        model.memorandum = metadata.memorandum
        model.signatory = str(metadata.signatory)
        model.signatory_name = metadata.signatory_name
        model.report_date = metadata.report_date
        model.elaborador = metadata.elaborador
        model.label = metadata.label

        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    async def delete(self, metadata_id: UUID) -> bool:
        rows = (
            self.db.query(ReportMetadataModel)
            .filter(ReportMetadataModel.id == metadata_id)
            .delete()
        )
        self.db.commit()
        return rows > 0
