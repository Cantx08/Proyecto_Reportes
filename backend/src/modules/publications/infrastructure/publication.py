"""
Modelos relacionados con publicaciones académicas.

Este módulo contiene los modelos para gestionar publicaciones,
documentos académicos y sus metadatos.
"""

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base, DocumentTypeEnum, SourceTypeEnum
from .associations import publication_authors, publication_subject_areas, report_publications


# ============================================================================
# MODELOS DE PUBLICACIONES
# ============================================================================

class PublicationModel(Base):
    """Modelo para publicaciones académicas."""
    __tablename__ = 'publications'
    
    id = Column(Integer, primary_key=True)
    scopus_id = Column(String(50), unique=True)
    title = Column(Text, nullable=False)
    abstract = Column(Text)
    publication_year = Column(Integer, nullable=False)
    journal_id = Column(Integer, ForeignKey('journals.id'))
    doi = Column(String(255))
    document_type = Column(SQLEnum(DocumentTypeEnum), default=DocumentTypeEnum.ARTICLE)
    source_type = Column(SQLEnum(SourceTypeEnum), default=SourceTypeEnum.SCOPUS)
    affiliation = Column(Text)
    volume = Column(String(50))
    issue = Column(String(50))
    pages = Column(String(100))
    citation_count = Column(Integer, default=0)
    is_open_access = Column(Boolean, default=False)
    is_editable = Column(Boolean, default=True)
    is_included_in_report = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    journal = relationship("JournalModel", back_populates="publications")
    authors = relationship("AuthorModel", secondary=publication_authors, back_populates="publications")
    subject_areas = relationship("SubjectAreaModel", secondary=publication_subject_areas)
    reports = relationship("ReportModel", secondary=report_publications, back_populates="publications")

    # ============================================================================
    # MODELOS DE ÁREAS TEMÁTICAS
    # ============================================================================

    class SubjectAreaModel(Base):
        """Modelo para áreas temáticas principales."""
        __tablename__ = 'subject_areas'

        id = Column(Integer, primary_key=True)
        code = Column(String(10), unique=True, nullable=False)
        name = Column(String(255), nullable=False)
        description = Column(Text)
        created_at = Column(DateTime, default=func.now())

        # Relaciones
        categories = relationship("SubjectCategoryModel", back_populates="area")

    class SubjectCategoryModel(Base):
        """Modelo para subáreas temáticas."""
        __tablename__ = 'subject_category'

        id = Column(Integer, primary_key=True)
        area_id = Column(Integer, ForeignKey('subject_areas.id'), nullable=False)
        code = Column(String(10), unique=True, nullable=False)
        name = Column(String(255), nullable=False)
        description = Column(Text)
        created_at = Column(DateTime, default=func.now())

        # Relaciones
        area = relationship("SubjectAreaModel", back_populates="categories")