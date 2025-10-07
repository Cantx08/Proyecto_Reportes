from typing import List
from ...domain.repositories.subject_areas_repository import SubjectAreasRepository


class SubjectAreaService:
    """Servicio para manejo de áreas temáticas."""

    def __init__(self, scopus_repository: SubjectAreasRepository, mapping_repository: SubjectAreasRepository):
        self._scopus_repository = scopus_repository  # Para obtener datos de Scopus
        self._mapping_repository = mapping_repository  # Para mapear usando CSV

    async def get_subject_areas(self, author_ids: List[str]) -> List[str]:
        """
        Obtiene las áreas temáticas principales (generales) de múltiples autores.
        Mapea las subáreas específicas a áreas temáticas generales usando el CSV.
        """
        categories = set()

        # Obtener todas las subáreas específicas de Scopus
        for author_id in author_ids:
            try:
                areas = await self._scopus_repository.get_subject_areas_by_author(author_id)
                for area in areas:
                    categories.add(area.name)
            except Exception as e:
                # Log error silently and continue
                print(f"Error obteniendo áreas para autor {author_id}: {e}")
                continue

        # Mapear subáreas a áreas temáticas principales
        subject_areas = set()
        for category in categories:
            subject_area = self._mapping_repository.map_category_to_area(category)
            if subject_area:
                subject_areas.add(subject_area)

        return sorted(list(subject_areas))
