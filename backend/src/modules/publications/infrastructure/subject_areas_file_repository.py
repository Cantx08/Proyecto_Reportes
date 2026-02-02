import pandas as pd
from typing import List, Optional
from backend.src.modules.publications.domain.subject_area import SubjectArea
from backend.src.modules.publications.domain.subject_areas_repository import SubjectAreasRepository


class SubjectAreasFileRepository(SubjectAreasRepository):
    """Repositorio de áreas temáticas basado en archivo CSV."""

    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        self._areas: Optional[List[SubjectArea]] = None
        self._load_areas()

    def _load_areas(self) -> None:
        """Carga las áreas temáticas del archivo CSV."""
        try:
            df = pd.read_csv(self._csv_path, sep=';')
            self._areas = []

            for _, row in df.iterrows():
                area_key = str(row['CLAVE'])
                name = str(row['AREA TEMATICA'])
                subject_categories = row['CATEGORIAS']

                # Procesar subáreas
                categories = []
                if pd.notna(subject_categories) and subject_categories.strip():
                    # Dividir por ";" y limpiar espacios
                    categories = [sub.strip() for sub in subject_categories.split(';') if sub.strip()]

                area = SubjectArea(
                    name=name,
                    area_key=area_key,
                    categories=categories
                )
                self._areas.append(area)

        except Exception as e:
            print(f"Error cargando áreas temáticas: {str(e)}")
            self._areas = []

    @staticmethod
    def _normalize_text(texto: str) -> str:
        """Normaliza un texto para comparación."""
        return texto.lower().strip()

    def _belongs_to_subject_area(self, normalized_subject_category: str, area: SubjectArea) -> bool:
        """Verifica si una subárea normalizada pertenece a un área temática."""
        # Buscar coincidencias exactas o parciales en las subáreas
        for category in area.categories:
            normalized_category = self._normalize_text(category)

            # Coincidencia exacta
            if normalized_subject_category == normalized_category:
                return True

            # Coincidencia parcial (la subárea está contenida en la definición)
            if normalized_subject_category in normalized_category:
                return True

            # Coincidencia parcial inversa (la definición está contenida en la subárea)
            if normalized_category in normalized_subject_category:
                return True

        return False

    async def get_subject_areas_by_author(self, author_id: str) -> List[SubjectArea]:
        """
        Obtiene las áreas temáticas de un autor.
        Esta implementación del repositorio de archivos no puede obtener datos por autor,
        ya que es un repositorio de mapeo. Devuelve lista vacía.
        """
        return []

    def get_all_subject_areas(self) -> List[SubjectArea]:
        """Obtiene todas las áreas temáticas con sus subáreas."""
        return self._areas if self._areas else []

    def map_category_to_area(self, category: str) -> Optional[str]:
        """
        Mapea una subárea específica a su área temática principal.
        Args:
            category: El nombre de la subárea a mapear (ejemplo: "Computer Science Applications")
        Returns:
            El nombre del área temática principal (ejemplo: "Computer Science") o None si no se encuentra
        """
        if not self._areas or not category:
            return None

        normalized_category = self._normalize_text(category)

        # Area Multidisciplinary
        if "multidisciplinary" in normalized_category:
            return "Multidisciplinary"

        # Buscar en todas las áreas temáticas
        for area in self._areas:
            if self._belongs_to_subject_area(normalized_category, area):
                return area.name

        return None
