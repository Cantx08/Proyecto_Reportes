"""
Entidades del dominio.

Este módulo contiene todas las entidades principales del sistema
de reportes de publicaciones académicas.
"""

from .author import Author, Gender
from .publication import Publication, DocumentType, SourceType, PublicationCollection
from .journal import Journal
from .report import Report, ReportType, ReportStatus
from .department import Department, Category
from .subject_area import SubjectArea

__all__ = [
    # Author
    'Author',
    'Gender',
    
    # Publication
    'Publication',
    'DocumentType',
    'SourceType',
    'PublicationCollection',
    
    # Journal
    'Journal',
    
    # Report
    'Report',
    'ReportType',
    'ReportStatus',
    
    # Department and Category
    'Department',
    'Category',
    
    # Subject Area
    'SubjectArea',
]