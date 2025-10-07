"""
DTOs e inicialización de modelos Pydantic.

Este módulo maneja la resolución de referencias circulares
entre los DTOs usando model_rebuild().
"""

from .author_dto import (
    AuthorDTO, AuthorCreateDTO, AuthorUpdateDTO, 
    AuthorsResponseDTO, AuthorResponseDTO
)
from .publication_dto import PublicationDTO, PublicationsResponseDTO, DocumentsByYearResponseDTO
from .subject_area_dto import SubjectAreaResponseDTO
from .report_dto import ReportRequestDTO
from .department_dto import (
    DepartmentDTO, DepartmentCreateDTO, DepartmentUpdateDTO,
    DepartmentsResponseDTO, DepartmentResponseDTO
)
from .legacy_department_dto import LegacyDepartmentsResponseDTO
from .position_dto import (
    PositionDTO, PositionCreateDTO, PositionUpdateDTO,
    PositionsResponseDTO, PositionResponseDTO
)
from .scopus_account_dto import (
    ScopusAccountDTO, ScopusAccountCreateDTO, ScopusAccountUpdateDTO,
    ScopusAccountsResponseDTO, ScopusAccountResponseDTO, LinkAuthorScopusDTO
)
from .cargo_dto import CargoDTO, CargosResponseDTO

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
    # Department DTOs
    "DepartmentDTO", "DepartmentCreateDTO", "DepartmentUpdateDTO",
    "DepartmentsResponseDTO", "DepartmentResponseDTO", "LegacyDepartmentsResponseDTO",
    # Position DTOs
    "PositionDTO", "PositionCreateDTO", "PositionUpdateDTO",
    "PositionsResponseDTO", "PositionResponseDTO",
    # ScopusAccount DTOs
    "ScopusAccountDTO", "ScopusAccountCreateDTO", "ScopusAccountUpdateDTO",
    "ScopusAccountsResponseDTO", "ScopusAccountResponseDTO", "LinkAuthorScopusDTO",
    # Legacy DTOs
    "SubjectAreaResponseDTO", "ReportRequestDTO", "CargoDTO", "CargosResponseDTO"
]