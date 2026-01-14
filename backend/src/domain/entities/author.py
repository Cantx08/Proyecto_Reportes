"""
Módulo que define la entidad Autor.
"""

from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .publication import Publication


@dataclass
class Author:
    """Entidad que representa un autor académico."""
    name: str
    surname: str
    dni: str
    title: str  # Dr., PhD., Msc., etc.
    gender: str
    position: str  # Cargo que ocupa
    department: str  # Departamento al que pertenece
    author_id: Optional[str] = None
    institutional_email: Optional[str] = None  # Correo institucional
    publications_list: Optional[List["Publication"]] = None
    error: Optional[str] = None
    _skip_validation: bool = False  # Flag interno para saltar validación

    def __post_init__(self):
        """Validaciones post-inicialización."""
        if self.publications_list is None:
            self.publications_list = []

        # Validaciones de campos requeridos (solo si no se salta la validación)
        # La validación se salta cuando se carga desde la BD
        if not self._skip_validation:
            if not self.name or not self.surname or not self.dni:
                raise ValueError("name, surname y dni son requeridos")

    def get_full_name(self) -> str:
        """Retorna el nombre completo del autor."""
        return f"{self.name} {self.surname}"

    def get_formal_name(self) -> str:
        """Retorna el nombre formal con título."""
        if self.title:
            return f"{self.title} {self.name} {self.surname}"
        return self.get_full_name()

    def add_publication(self, publication: "Publication") -> None:
        """Agrega una publicación a la lista del autor."""
        if publication.is_valid():
            self.publications_list.append(publication)

    def get_publications_by_year(self, year: str) -> List["Publication"]:
        """Obtiene las publicaciones de un año específico."""
        return [pub for pub in self.publications_list if pub.year == year]

    def count_publications(self) -> int:
        """Cuenta el total de publicaciones del autor."""
        return len(self.publications_list)
