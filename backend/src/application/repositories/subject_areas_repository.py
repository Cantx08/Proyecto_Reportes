from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.entities.subject_area import SubjectArea

class SubjectAreasRepository(ABC):
    """Interfaz para el repositorio de áreas temáticas."""
    
    @abstractmethod
    async def get_subject_areas_by_author(self, author_id: str) -> List[SubjectArea]:
        """Obtiene las áreas temáticas de un autor."""
        pass
    
    @abstractmethod
    def get_all_subject_areas(self) -> List[SubjectArea]:
        """Obtiene todas las áreas temáticas con sus subáreas."""
        pass
    
    @abstractmethod
    def map_subarea_to_area(self, subarea: str) -> Optional[str]:
        """Mapea una subárea específica a su área temática principal."""
        pass