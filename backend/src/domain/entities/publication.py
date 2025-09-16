from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .author import Author


@dataclass
class Publication:
    """Entidad que representa una publicación académica."""
    title: str
    year: str
    source: str
    document_type: str
    affiliation: str
    doi: str
    categories: str = ""

    def is_valid(self) -> bool:
        """Valida si la publicación tiene los datos mínimos requeridos."""
        return bool(self.title and self.year and self.source)

    def has_epn_affiliation(self) -> bool:
        """Verifica si la publicación tiene filiación con la EPN."""
        return "escuela politécnica nacional" in self.affiliation.lower()

@dataclass
class PublicationsCollection:
    """Colección de publicaciones con métodos de análisis."""
    authors: List["Author"]

    def get_all_publications(self) -> List[Publication]:
        """Obtiene todas las publicaciones de todos los autores."""
        publications = []
        for author in self.authors:
            publications.extend(author.publications_list)
        return publications

    def count_publications_by_year(self) -> dict[str, int]:
        """Cuenta las publicaciones agrupadas por año."""
        publications = self.get_all_publications()
        count = {}

        years_with_publications = [int(pub.year) for pub in publications if pub.year.strip()]

        if not years_with_publications:
            return {}

        first_year = min(years_with_publications)
        last_year = max(years_with_publications)

        # Inicializar todos los años con 0
        for year in range(first_year, last_year + 1):
            count[str(year)] = 0

        # Contar publicaciones reales
        for pub in publications:
            if pub.year.strip():
                count[pub.year] = count.get(pub.year, 0) + 1

        return count