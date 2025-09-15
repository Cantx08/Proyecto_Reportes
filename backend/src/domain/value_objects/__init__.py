"""
Value Objects del dominio.

Este módulo contiene todos los value objects utilizados
en el sistema de reportes de publicaciones académicas.
"""

from .scopus_id import ScopusId
from .email import Email
from .doi import DOI
from .publication_year import PublicationYear
from .quartile import SJRQuartile, Quartile

__all__ = [
    'ScopusId',
    'Email',
    'DOI',
    'PublicationYear',
    'SJRQuartile',
    'Quartile',
]