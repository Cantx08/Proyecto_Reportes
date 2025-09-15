"""
Excepciones relacionadas con la entidad Author y sus value objects.
"""


class AuthorDomainError(Exception):
    """Excepción base para errores del dominio de Author."""
    pass


class InvalidAuthorDataError(AuthorDomainError):
    """Se lanza cuando los datos del autor son inválidos."""
    pass


class InvalidScopusIdError(AuthorDomainError):
    """Se lanza cuando el ID de Scopus tiene formato inválido."""
    pass


class InvalidEmailError(AuthorDomainError):
    """Se lanza cuando el email tiene formato inválido."""
    pass


class AuthorNotFoundError(AuthorDomainError):
    """Se lanza cuando no se encuentra un autor."""
    pass


class DuplicateAuthorError(AuthorDomainError):
    """Se lanza cuando se intenta crear un autor duplicado."""
    pass


class ScopusAccountError(AuthorDomainError):
    """Se lanza cuando hay errores con las cuentas de Scopus."""
    pass