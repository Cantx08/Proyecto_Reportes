from typing import List

from ..external.scopus_api_client import ScopusApiClient
from ...domain.entities.subject_area import SubjectArea
from ...domain.repositories.subject_areas_repository import SubjectAreasRepository


class ScopusSubjectAreasRepository(SubjectAreasRepository):
    """Repositorio de áreas temáticas usando la API de Author Retrieval de Scopus."""

    def __init__(self, scopus_client: ScopusApiClient):
        self._client = scopus_client

    async def get_subject_areas_by_author(self, author_id: str) -> List[SubjectArea]:
        """
        Obtiene las áreas temáticas de un autor directamente desde su perfil.
        Esto es mucho más eficiente y completo que iterar sobre todas las publicaciones.
        """
        try:
            data = await self._client.get_author_details(author_id)

            # Navegar la respuesta JSON de Scopus Author Retrieval
            # Estructura típica: author-retrieval-response -> subject-areas -> subject-area
            retrieval_response = data.get("author-retrieval-response", [])

            # A veces viene como lista si se consultan varios, pero aquí es por ID único
            if isinstance(retrieval_response, list):
                if not retrieval_response: return []
                retrieval_response = retrieval_response[0]

            subject_areas_container = retrieval_response.get("subject-areas", {})
            subject_area_list = subject_areas_container.get("subject-area", [])

            areas = []

            # Normalizar a lista si es un solo objeto
            if isinstance(subject_area_list, dict):
                subject_area_list = [subject_area_list]

            for item in subject_area_list:
                # El nombre suele estar en '$' o a veces '@abbrev' dependiendo de lo que necesites
                # Usamos '$' que es el nombre completo (ej: "Computer Science")
                area_name = item.get("$", "")
                if area_name:
                    areas.append(SubjectArea(name=area_name))

            return areas

        except Exception as e:
            print(f"Error obteniendo áreas para el autor {author_id}: {e}")
            return []

    # Métodos no utilizados o auxiliares
    @staticmethod
    async def _extract_publication_subject_areas() -> List[SubjectArea]:
        return []  # Ya no se usa

    def get_all_subject_areas(self) -> List[SubjectArea]:
        return []

    def map_category_to_area(self, category: str) -> str:
        return category