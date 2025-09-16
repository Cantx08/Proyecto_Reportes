"""
Configuración base para modelos SQLAlchemy.

Este módulo contiene la configuración base, enums comunes 
y configuraciones compartidas para todos los modelos.
"""

from sqlalchemy.ext.declarative import declarative_base
import enum

# Base declarativa para todos los modelos
Base = declarative_base()


# ============================================================================
# ENUMS COMUNES
# ============================================================================

class GenderEnum(enum.Enum):
    """Enumeración para géneros."""
    MALE = "M"
    FEMALE = "F"


class DocumentTypeEnum(enum.Enum):
    """Enumeración para tipos de documentos académicos."""
    ARTICLE = "Article"
    CONFERENCE_PAPER = "Conference Paper"
    REVIEW = "Review"
    BOOK_CHAPTER = "Book Chapter"
    BOOK = "Book"
    EDITORIAL = "Editorial"
    LETTER = "Letter"
    NOTE = "Note"
    SHORT_SURVEY = "Short Survey"
    ERRATUM = "Erratum"
    OTHER = "Other"


class SourceTypeEnum(enum.Enum):
    """Enumeración para tipos de fuentes de publicaciones."""
    SCOPUS = "Scopus"
    WOS = "WOS"
    REGIONAL = "Regional"
    MEMORY = "Memory"
    BOOK = "Book"
    OTHER = "Other"


class ReportTypeEnum(enum.Enum):
    """Enumeración para tipos de reportes."""
    DRAFT = "draft"
    FINAL = "final"


class ReportStatusEnum(enum.Enum):
    """Enumeración para estados de reportes."""
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"