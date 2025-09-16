"""
DTOs e inicialización de modelos Pydantic.

Este módulo maneja la resolución de referencias circulares
entre los DTOs usando model_rebuild().
"""

from .author_dto import AuthorDTO
from .publication_dto import PublicationDTO, PublicationsResponseDTO, DocumentsByYearResponseDTO
from .subject_area_dto import SubjectAreaResponseDTO
from .report_dto import ReportRequestDTO

# Resolver referencias circulares después de importar todos los modelos
AuthorDTO.model_rebuild()
PublicationDTO.model_rebuild()
PublicationsResponseDTO.model_rebuild()

__all__ = [
    "AuthorDTO",
    "PublicationDTO", 
    "PublicationsResponseDTO",
    "DocumentsByYearResponseDTO",
    "SubjectAreaResponseDTO",
    "ReportRequestDTO"
]