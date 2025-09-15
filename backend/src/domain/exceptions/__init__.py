"""
Excepciones del dominio.
"""

# Importar todas las excepciones para facilitar el acceso
from .author_exceptions import (
    AuthorDomainError,
    InvalidAuthorDataError,
    InvalidScopusIdError,
    InvalidEmailError,
    AuthorNotFoundError,
    DuplicateAuthorError,
    ScopusAccountError
)

__all__ = [
    'AuthorDomainError',
    'InvalidAuthorDataError',
    'InvalidScopusIdError',
    'InvalidEmailError',
    'AuthorNotFoundError',
    'DuplicateAuthorError',
    'ScopusAccountError'
]