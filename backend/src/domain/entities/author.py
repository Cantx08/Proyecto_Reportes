from dataclasses import dataclass
from typing import List, Optional
from .publication import Publication


@dataclass
class Author:
    """Entidad que representa un autor académico."""
    author_id: str
    publications_list: Optional[List[Publication]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.publications_list is None:
            self.publications_list = []

    def add_publication(self, publication: Publication) -> None:
        """Agrega una publicación a la lista del autor."""
        if publication.is_valid():
            self.publications_list.append(publication)

    def get_publications_by_year(self, year: str) -> List[Publication]:
        """Obtiene las publicaciones de un año específico."""
        return [pub for pub in self.publications_list if pub.year == year]

    def count_publications(self) -> int:
        """Cuenta el total de publicaciones del autor."""
        return len(self.publications_list)