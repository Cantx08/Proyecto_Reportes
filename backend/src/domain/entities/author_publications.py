from dataclasses import dataclass
from typing import List, Optional
from .publication import Publication


@dataclass
class AuthorPublications:
    """Representa un autor con sus publicaciones (vista simplificada para consultas de Scopus)."""
    author_id: str
    publications_list: List[Publication]
    error: Optional[str] = None

    def __post_init__(self):
        """Validaciones post-inicialización."""
        if self.publications_list is None:
            self.publications_list = []

    def get_publications_by_year(self, year: str) -> List[Publication]:
        """Obtiene las publicaciones de un año específico."""
        return [pub for pub in self.publications_list if pub.year == year]

    def count_publications(self) -> int:
        """Cuenta el total de publicaciones del autor."""
        return len(self.publications_list)
