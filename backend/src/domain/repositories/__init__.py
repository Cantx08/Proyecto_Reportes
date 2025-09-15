"""
Interfaces de repositorios del dominio.

Este módulo contiene todas las interfaces de repositorios
que definen los contratos para el acceso a datos.
"""

from .author_repository import AuthorRepository
from .publication_repository import PublicationRepository
from .journal_repository import JournalRepository
from .report_repository import ReportRepository
from .sjr_repository import SJRRepository

__all__ = [
    'AuthorRepository',
    'PublicationRepository',
    'JournalRepository',
    'ReportRepository',
    'SJRRepository',
]