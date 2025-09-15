"""
Excepciones relacionadas con publicaciones y sus value objects.
"""


class PublicationDomainError(Exception):
    """Excepción base para errores del dominio de Publication."""
    pass


class InvalidPublicationDataError(PublicationDomainError):
    """Se lanza cuando los datos de la publicación son inválidos."""
    pass


class InvalidDOIError(PublicationDomainError):
    """Se lanza cuando el DOI tiene formato inválido."""
    pass


class InvalidPublicationYearError(PublicationDomainError):
    """Se lanza cuando el año de publicación es inválido."""
    pass


class PublicationNotFoundError(PublicationDomainError):
    """Se lanza cuando no se encuentra una publicación."""
    pass


class DuplicatePublicationError(PublicationDomainError):
    """Se lanza cuando se intenta crear una publicación duplicada."""
    pass


class InvalidScopusDataError(PublicationDomainError):
    """Se lanza cuando los datos de Scopus son inválidos."""
    pass