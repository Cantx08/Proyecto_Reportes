"""
Modelos SQLAlchemy para la base de datos.

Este módulo centraliza la importación de todos los modelos de base de datos
organizados por dominio para facilitar su mantenimiento y revisión.

Estructura modular:
- base.py: Configuración base y enums comunes
- associations.py: Tablas de asociación many-to-many
- author.py: Modelos de autores, departamentos y áreas temáticas
- journal.py: Modelos de journals, rankings SJR y categorías
- publication.py: Modelos de publicaciones académicas
- report.py: Modelos de reportes y documentos generados
"""

# ============================================================================
# IMPORTACIONES DE CONFIGURACIÓN BASE
# ============================================================================

from .base import (
    Base,
    GenderEnum,
    FacultyEnum,
    DocumentTypeEnum,
    SourceTypeEnum,
    ReportTypeEnum,
    ReportStatusEnum
)

# ============================================================================
# IMPORTACIONES DE TABLAS DE ASOCIACIÓN
# ============================================================================

from .associations import (
    publication_authors,
    publication_subject_areas,
    report_publications
)

# ============================================================================
# IMPORTACIONES DE MODELOS DE AUTORES Y DEPARTAMENTOS
# ============================================================================

from .author import (
    DepartmentModel,
    AuthorModel,
    ScopusAccountModel,
    SubjectAreaModel,
    SubjectCategoryModel
)

from .position import (
    PositionModel
)

# ============================================================================
# IMPORTACIONES DE MODELOS DE JOURNALS Y SJR
# ============================================================================

from .journal import (
    JournalModel,
    SJRRankingModel,
    CategoryModel,
    SJRCategoryModel
)

# ============================================================================
# IMPORTACIONES DE MODELOS DE PUBLICACIONES
# ============================================================================

from .publication import (
    PublicationModel
)

# ============================================================================
# IMPORTACIONES DE MODELOS DE REPORTES
# ============================================================================

from .report import (
    ReportModel
)

# ============================================================================
# EXPORTACIONES PÚBLICAS
# ============================================================================

__all__ = [
    # Base y enums
    "Base",
    "GenderEnum",
    "FacultyEnum",
    "DocumentTypeEnum",
    "SourceTypeEnum",
    "ReportTypeEnum",
    "ReportStatusEnum",
    
    # Tablas de asociación
    "publication_authors",
    "publication_subject_areas",
    "report_publications",
    
    # Modelos de autores y departamentos
    "DepartmentModel",
    "AuthorModel",
    "ScopusAccountModel",
    "SubjectAreaModel",
    "SubjectCategoryModel",
    "PositionModel",
    
    # Modelos de journals y SJR
    "JournalModel",
    "SJRRankingModel",
    "CategoryModel",
    "SJRCategoryModel",
    
    # Modelos de publicaciones
    "PublicationModel",
    
    # Modelos de reportes
    "ReportModel"
]