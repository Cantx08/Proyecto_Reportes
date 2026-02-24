"""
Modelos relacionados con reportes y generación de documentos.

Este módulo contiene los modelos para gestionar reportes,
memorandos y documentos generados por el sistema.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, JSON, Date, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .associations import report_publications
from .base import Base, ReportTypeEnum, ReportStatusEnum


# ============================================================================
# MODELOS DE REPORTES
# ============================================================================

class ReportModel(Base):
    """Modelo para reportes generados por el sistema."""
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    title = Column(String(500), nullable=False)
    report_type = Column(SQLEnum(ReportTypeEnum), default=ReportTypeEnum.DRAFT)
    memo_number = Column(String(100))
    memo_date = Column(Date)
    signatory = Column(String(255))
    generated_by = Column(Integer, ForeignKey('authors.id'))
    file_path = Column(String(500))
    report_metadata = Column(JSON)  # Renombrado de 'metadata' a 'report_metadata' (metadata es reservado)
    status = Column(SQLEnum(ReportStatusEnum), default=ReportStatusEnum.GENERATING)
    error_message = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    generated_at = Column(DateTime)
    
    # Relaciones
    # Especificamos foreign_keys para ambas relaciones ya que hay 2 FKs a authors
    author = relationship(
        "AuthorModel", 
        foreign_keys=[author_id], 
        back_populates="reports"
    )
    generator = relationship(
        "AuthorModel",
        foreign_keys=[generated_by],
        back_populates="generated_reports"
    )
    publications = relationship("PublicationModel", secondary=report_publications, back_populates="reports")