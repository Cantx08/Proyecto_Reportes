"""
Modelos relacionados con autores y departamentos.

Este módulo contiene los modelos para gestionar autores,
departamentos, cuentas de Scopus y áreas temáticas.
"""

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base, GenderEnum
from .associations import publication_authors


# ============================================================================
# MODELOS DE AUTORES Y DEPARTAMENTOS
# ============================================================================


class AuthorModel(Base):
    """Modelo para autores/investigadores."""
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    dni = Column(String(20), unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    title = Column(String(255))  # Dr., PhD, etc.
    institutional_email = Column(String(255))  # Correo institucional
    position_id = Column(Integer, ForeignKey('positions.id'))  # Referencia a la tabla positions
    gender = Column(SQLEnum(GenderEnum))
    department_id = Column(Integer, ForeignKey('departments.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    department = relationship("DepartmentModel", back_populates="authors")
    position_rel = relationship("PositionModel", back_populates="authors")  # Relación con Position
    scopus_accounts = relationship("ScopusAccountModel", back_populates="author")
    publications = relationship("PublicationModel", secondary=publication_authors, back_populates="authors")
    
    # Relaciones con reportes: un autor puede tener reportes propios y reportes generados
    reports = relationship(
        "ReportModel", 
        foreign_keys="ReportModel.author_id",
        back_populates="author"
    )
    generated_reports = relationship(
        "ReportModel",
        foreign_keys="ReportModel.generated_by",
        back_populates="generator"
    )


class ScopusAccountModel(Base):
    """Modelo para cuentas/IDs de Scopus de autores."""
    __tablename__ = 'scopus_accounts'
    
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    scopus_id = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relaciones
    author = relationship("AuthorModel", back_populates="scopus_accounts")


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