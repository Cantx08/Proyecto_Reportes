from typing import List
from pydantic import BaseModel


class SubjectAreaResponseDTO(BaseModel):
    """DTO para respuesta de áreas temáticas."""
    author_ids: List[str]
    subject_areas: List[str]