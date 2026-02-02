"""
DTOs e inicialización de modelos Pydantic.

Este módulo maneja la resolución de referencias circulares
entre los DTOs usando model_rebuild().
"""

from .publication_dto import PublicationDTO, PublicationsResponseDTO, DocumentsByYearResponseDTO
from .report_dto import ReportRequestDTO
from .subject_area_dto import SubjectAreaResponseDTO

PublicationDTO.model_rebuild()
PublicationsResponseDTO.model_rebuild()

__all__ = [
    # Publication DTOs
    "PublicationDTO", "PublicationsResponseDTO", "DocumentsByYearResponseDTO",
    # Legacy DTOs
    "SubjectAreaResponseDTO", "ReportRequestDTO"
]