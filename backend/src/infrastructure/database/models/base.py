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
    M = "Masculino"
    F = "Femenino"


class FacultyEnum(enum.Enum):
    """Enumeración para facultades de la EPN."""
    FIEE = "Facultad de Ingeniería Eléctrica y Electrónica"
    FC = "Facultad de Ciencias"
    FCA = "Facultad de Ciencias Administrativas"
    FIQA = "Facultad de Ingeniería Química y Agroindustria"
    CS = "Ciencias Sociales"
    DFB = "Formación Básica"
    FIGP = "Facultad de Geología y Petróleos"
    FIS = "Facultad de Ingeniería de Sistemas"
    FICA = "Facultad de Ingeniería Civil y Ambiental"
    FIM = "Facultad de Ingeniería Mecánica"
    ESFOT = "Escuela de Formación de Tecnólogos"
    IG = "Instituto Geofísico"
    DESCONOCIDA = "No encontrada"


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