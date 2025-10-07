from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .publication import Publication


@dataclass
class Author:
    """Entidad que representa un autor académico."""
    author_id: str
    name: str
    surname: str
    title: str  # Dr., PhD., Ing., etc.
    birth_date: Optional[date]
    gender: str  # M, F, u otro valor personalizado
    position: str  # Nombre del cargo que ocupa
    department: str  # Nombre del departamento al que pertenece
    publications_list: Optional[List["Publication"]] = None
    error: Optional[str] = None

    def __post_init__(self):
        """Validaciones post-inicialización."""
        if self.publications_list is None:
            self.publications_list = []
        
        # Validaciones de campos requeridos
        if not self.author_id or not self.name or not self.surname:
            raise ValueError("author_id, name y surname son requeridos")

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
    
    def get_age(self) -> Optional[int]:
        """Calcula la edad del autor si se conoce la fecha de nacimiento."""
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None