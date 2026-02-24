"""
Modelo SQLAlchemy para la tabla report_metadata.
Almacena metadatos de reportes para regenerar certificados sin nueva búsqueda.
"""
import uuid
from sqlalchemy import Column, UUID, String, JSON, DateTime
from sqlalchemy.sql import func

from ....shared.database import Base
from ..domain.report_metadata import ReportMetadata


class ReportMetadataModel(Base):
    __tablename__ = "report_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Datos del autor
    author_name = Column(String(300), nullable=False)
    author_gender = Column(String(20), nullable=False)
    department = Column(String(300), nullable=False)
    position = Column(String(300), nullable=False)
    author_ids = Column(JSON, nullable=False, default=list)

    # Snapshot de datos oficiales
    publications = Column(JSON, nullable=False, default=list)
    subject_areas = Column(JSON, nullable=False, default=list)
    documents_by_year = Column(JSON, nullable=False, default=dict)

    # Metadatos editables
    memorandum = Column(String(200), nullable=True)
    signatory = Column(String(200), nullable=True, default="1")
    signatory_name = Column(String(300), nullable=True)
    report_date = Column(String(100), nullable=True)
    elaborador = Column(String(200), nullable=False, default="M. Vásquez")

    # Etiqueta descriptiva
    label = Column(String(500), nullable=True, default="")

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def to_entity(self) -> ReportMetadata:
        """Convierte el modelo de BD a entidad de dominio."""
        # Parsear signatory: intentar como int, si falla usar str
        signatory_value = self.signatory
        try:
            signatory_value = int(self.signatory)
        except (ValueError, TypeError):
            pass

        return ReportMetadata(
            id=self.id,
            author_name=self.author_name,
            author_gender=self.author_gender,
            department=self.department,
            position=self.position,
            author_ids=self.author_ids or [],
            publications=self.publications or [],
            subject_areas=self.subject_areas or [],
            documents_by_year=self.documents_by_year or {},
            memorandum=self.memorandum,
            signatory=signatory_value,
            signatory_name=self.signatory_name,
            report_date=self.report_date,
            elaborador=self.elaborador or "M. Vásquez",
            label=self.label or "",
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(entity: ReportMetadata) -> "ReportMetadataModel":
        """Crea un modelo de BD desde una entidad de dominio."""
        return ReportMetadataModel(
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
            signatory=str(entity.signatory),
            signatory_name=entity.signatory_name,
            report_date=entity.report_date,
            elaborador=entity.elaborador,
            label=entity.label,
        )
