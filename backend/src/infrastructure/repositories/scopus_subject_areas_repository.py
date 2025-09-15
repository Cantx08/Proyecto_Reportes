from typing import List
from ...domain.entities.subject_area import SubjectArea
from ..external_services.scopus_api_client import ScopusApiClient
from ...application.repositories.subject_areas_repository import SubjectAreasRepository


class ScopusSubjectAreasRepository(SubjectAreasRepository):
    """Repositorio de áreas temáticas usando la API de Scopus."""
    
    def __init__(self, scopus_client: ScopusApiClient):
        self._client = scopus_client
    
    def _extract_publication_subject_areas(self, entry: dict) -> List[SubjectArea]:
        """Extrae las áreas temáticas de una publicación."""
        scopus_id = entry.get("dc:identifier", "").replace("SCOPUS_ID:", "")
        if not scopus_id:
            return []
        
        try:
            detail_data = self._client.get_publication_details(scopus_id)
            abstracts_retrieval = detail_data.get("abstracts-retrieval-response", {})
            subject_areas_data = abstracts_retrieval.get("subject-areas", {})
            
            areas = []
            if subject_areas_data and "subject-area" in subject_areas_data:
                subject_area_list = subject_areas_data["subject-area"]
                
                if isinstance(subject_area_list, list):
                    for sa in subject_area_list:
                        area_name = sa.get("$", "")
                        if area_name:
                            areas.append(SubjectArea(name=area_name))
                elif isinstance(subject_area_list, dict):
                    area_name = subject_area_list.get("$", "")
                    if area_name:
                        areas.append(SubjectArea(name=area_name))

            return areas
        except Exception:
            return []
        
    async def get_subject_areas_by_author(self, author_id: str) -> List[SubjectArea]:
        """Obtiene las áreas temáticas de un autor."""
        data = self._client.get_publications_by_author(author_id)
        entries = data.get("search-results", {}).get("entry", [])
        
        subject_areas = set()
        
        for entry in entries:
            areas = self._extract_publication_subject_areas(entry)
            subject_areas.update(areas)
        
        return list(subject_areas)

    def get_all_subject_areas(self) -> List[SubjectArea]:
        """
        Obtiene todas las áreas temáticas disponibles.
        Implementación básica - devuelve lista vacía ya que Scopus no provee un endpoint directo.
        """
        return []
    
    def map_subarea_to_area(self, subarea: str) -> str:
        """
        Mapeo básico de subáreas - debe ser sobrescrito por el repositorio de archivos.
        Esta implementación devuelve la misma subárea.
        """
        return subarea