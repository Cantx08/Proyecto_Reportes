from typing import List
from ....application.services.subject_area_service import SubjectAreaService
from ....application.dtos import SubjectAreaResponseDTO


class SubjectAreasController:
    """Controlador para endpoints de áreas temáticas."""
    
    def __init__(self, subject_area_service: SubjectAreaService):
        self._subject_area_service = subject_area_service

    async def fetch_subject_areas(self, author_ids: List[str]) -> SubjectAreaResponseDTO:
        """Obtiene las áreas temáticas principales (generales) de autores."""
        areas = await self._subject_area_service.get_subject_areas(author_ids)
        
        return SubjectAreaResponseDTO(
            author_ids=author_ids,
            subject_areas=areas
        )
