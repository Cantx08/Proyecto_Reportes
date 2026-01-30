"""
DTOs e inicialización de modelos Pydantic.

Este módulo maneja la resolución de referencias circulares
entre los DTOs usando model_rebuild().
"""

from backend.src.modules.authors.application.author_dto import (
    AuthorDTO, AuthorCreateDTO, AuthorUpdateDTO, 
    AuthorsResponseDTO, AuthorResponseDTO
)
from .publication_dto import PublicationDTO, PublicationsResponseDTO, DocumentsByYearResponseDTO
from .subject_area_dto import SubjectAreaResponseDTO
from .report_dto import ReportRequestDTO
from .scopus_account_dto import (
    ScopusAccountDTO, ScopusAccountCreateDTO, ScopusAccountUpdateDTO,
    ScopusAccountsResponseDTO, ScopusAccountResponseDTO, LinkAuthorScopusDTO
)

# Resolver referencias circulares después de importar todos los modelos
AuthorDTO.model_rebuild()
PublicationDTO.model_rebuild()
PublicationsResponseDTO.model_rebuild()

__all__ = [
    # Author DTOs
    "AuthorDTO", "AuthorCreateDTO", "AuthorUpdateDTO", 
    "AuthorsResponseDTO", "AuthorResponseDTO",
    # Publication DTOs
    "PublicationDTO", "PublicationsResponseDTO", "DocumentsByYearResponseDTO",
    # ScopusAccount DTOs
    "ScopusAccountDTO", "ScopusAccountCreateDTO", "ScopusAccountUpdateDTO",
    "ScopusAccountsResponseDTO", "ScopusAccountResponseDTO", "LinkAuthorScopusDTO",
    # Legacy DTOs
    "SubjectAreaResponseDTO", "ReportRequestDTO"
]