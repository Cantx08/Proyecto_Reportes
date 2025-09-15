from dataclasses import dataclass, field
from typing import List, Optional, Set
from datetime import datetime
from enum import Enum

from ..value_objects.doi import DOI
from ..value_objects.publication_year import PublicationYear
from ..exceptions.publication_exceptions import InvalidPublicationDataError


class DocumentType(Enum):
    """Tipos de documentos soportados."""
    ARTICLE = "Article"
    CONFERENCE_PAPER = "Conference Paper"
    REVIEW = "Review"
    BOOK_CHAPTER = "Book Chapter"
    BOOK = "Book"
    EDITORIAL = "Editorial"
    LETTER = "Letter"
    NOTE = "Note"
    SHORT_SURVEY = "Short Survey"
    ERRATUM = "Erratum"
    OTHER = "Other"


class SourceType(Enum):
    """Tipos de fuentes de publicaciones."""
    SCOPUS = "Scopus"
    WOS = "WOS"  # Web of Science
    REGIONAL = "Regional"
    MEMORY = "Memory"  # Memorias de eventos
    BOOK = "Book"
    OTHER = "Other"


@dataclass
class Publication:
    """
    Entidad que representa una publicación académica.
    
    Contiene toda la información de una publicación incluyendo
    metadatos, categorización SJR y estado de inclusión en reportes.
    """
    
    # Identificadores
    id: Optional[int] = None
    scopus_id: Optional[str] = None
    
    # Información básica
    title: str = ""
    abstract: Optional[str] = None
    publication_year: Optional[PublicationYear] = None
    doi: Optional[DOI] = None
    
    # Información de fuente
    journal_id: Optional[int] = None
    journal_name: Optional[str] = None  # Denormalizado para performance
    source_type: SourceType = SourceType.SCOPUS
    document_type: DocumentType = DocumentType.ARTICLE
    
    # Detalles de publicación
    affiliation: str = ""
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    
    # Métricas
    citation_count: int = 0
    is_open_access: bool = False
    
    # Control de inclusión en reportes
    is_editable: bool = True
    is_included_in_report: bool = True
    custom_data: dict = field(default_factory=dict)  # Datos editados para reportes
    
    # Áreas temáticas
    subject_areas: List[str] = field(default_factory=list)
    subject_subareas: List[str] = field(default_factory=list)
    
    # SJR Categories
    sjr_categories: List[dict] = field(default_factory=list)  # [{"name": "Computer Science", "quartile": "Q1", "rank": 15}]
    
    # Auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones posteriores a la inicialización."""
        self._validate()

    def _validate(self) -> None:
        """Valida los datos de la publicación."""
        if not self.title or len(self.title.strip()) < 3:
            raise InvalidPublicationDataError("Title must be at least 3 characters long")
        
        if self.publication_year and not isinstance(self.publication_year, PublicationYear):
            raise InvalidPublicationDataError("Publication year must be a PublicationYear value object")
        
        if self.doi and not isinstance(self.doi, DOI):
            raise InvalidPublicationDataError("DOI must be a DOI value object")

    @property
    def year(self) -> Optional[int]:
        """Retorna el año como entero para compatibilidad."""
        return self.publication_year.value if self.publication_year else None

    @property
    def display_title(self) -> str:
        """Retorna el título para mostrar (editado o original)."""
        return self.custom_data.get('title', self.title)

    @property
    def display_authors(self) -> str:
        """Retorna los autores para mostrar (editado o original)."""
        return self.custom_data.get('authors', '')

    @property
    def has_doi(self) -> bool:
        """Verifica si la publicación tiene DOI."""
        return self.doi is not None

    @property
    def doi_url(self) -> Optional[str]:
        """Retorna la URL del DOI si existe."""
        return self.doi.url if self.doi else None

    @property
    def has_sjr_categories(self) -> bool:
        """Verifica si tiene categorías SJR asignadas."""
        return len(self.sjr_categories) > 0

    @property
    def best_sjr_quartile(self) -> Optional[str]:
        """Retorna el mejor cuartil SJR de la publicación."""
        if not self.sjr_categories:
            return None
        
        quartiles = [cat.get('quartile') for cat in self.sjr_categories if cat.get('quartile')]
        if not quartiles:
            return None
        
        # Q1 es mejor que Q2, Q2 mejor que Q3, etc.
        quartile_order = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
        best = min(quartiles, key=lambda q: quartile_order.get(q, 5))
        return best

    def has_epn_affiliation(self) -> bool:
        """Verifica si la publicación tiene filiación con la EPN."""
        if not self.affiliation:
            return False
        
        epn_keywords = [
            "escuela politécnica nacional",
            "escuela politecnica nacional",
            "epn",
            "national polytechnic school"
        ]
        
        affiliation_lower = self.affiliation.lower()
        return any(keyword in affiliation_lower for keyword in epn_keywords)

    def set_custom_data(self, field: str, value: str) -> None:
        """
        Establece datos personalizados para el reporte.
        
        Args:
            field: Campo a personalizar (title, authors, etc.)
            value: Valor personalizado
        """
        if not self.is_editable:
            raise InvalidPublicationDataError("Publication is not editable")
        
        self.custom_data[field] = value
        self.updated_at = datetime.now()

    def get_custom_data(self, field: str, default: Optional[str] = None) -> Optional[str]:
        """Obtiene datos personalizados o el valor original."""
        return self.custom_data.get(field, default)

    def clear_custom_data(self) -> None:
        """Limpia todos los datos personalizados."""
        self.custom_data.clear()
        self.updated_at = datetime.now()

    def include_in_report(self) -> None:
        """Incluye la publicación en reportes."""
        self.is_included_in_report = True
        self.updated_at = datetime.now()

    def exclude_from_report(self) -> None:
        """Excluye la publicación de reportes."""
        self.is_included_in_report = False
        self.updated_at = datetime.now()

    def add_sjr_category(self, name: str, quartile: str, rank: Optional[int] = None) -> None:
        """
        Agrega una categoría SJR a la publicación.
        
        Args:
            name: Nombre de la categoría
            quartile: Cuartil (Q1, Q2, Q3, Q4)
            rank: Posición en el ranking
        """
        category = {
            "name": name,
            "quartile": quartile,
            "rank": rank
        }
        
        # Evitar duplicados
        if category not in self.sjr_categories:
            self.sjr_categories.append(category)
            self.updated_at = datetime.now()

    def clear_sjr_categories(self) -> None:
        """Limpia todas las categorías SJR."""
        self.sjr_categories.clear()
        self.updated_at = datetime.now()

    def add_subject_area(self, area: str) -> None:
        """Agrega un área temática."""
        if area not in self.subject_areas:
            self.subject_areas.append(area)
            self.updated_at = datetime.now()

    def add_subject_subarea(self, subarea: str) -> None:
        """Agrega una subárea temática."""
        if subarea not in self.subject_subareas:
            self.subject_subareas.append(subarea)
            self.updated_at = datetime.now()

    def is_recent(self, years_back: int = 5) -> bool:
        """Verifica si la publicación es reciente."""
        if not self.publication_year:
            return False
        return self.publication_year.is_recent(years_back)

    def __eq__(self, other) -> bool:
        """Compara publicaciones por ID o Scopus ID."""
        if not isinstance(other, Publication):
            return False
        
        if self.id and other.id:
            return self.id == other.id
        
        if self.scopus_id and other.scopus_id:
            return self.scopus_id == other.scopus_id
        
        # Comparación por DOI si ambos lo tienen
        if self.doi and other.doi:
            return self.doi == other.doi
        
        return False

    def __hash__(self) -> int:
        """Hash basado en ID, Scopus ID o DOI."""
        if self.id:
            return hash(self.id)
        if self.scopus_id:
            return hash(self.scopus_id)
        if self.doi:
            return hash(self.doi)
        return hash(self.title)


@dataclass
class PublicationCollection:
    """
    Colección de publicaciones con métodos de análisis y agrupación.
    """
    publications: List[Publication] = field(default_factory=list)

    def add_publication(self, publication: Publication) -> None:
        """Agrega una publicación a la colección."""
        if publication not in self.publications:
            self.publications.append(publication)

    def remove_publication(self, publication: Publication) -> None:
        """Elimina una publicación de la colección."""
        if publication in self.publications:
            self.publications.remove(publication)

    def get_included_publications(self) -> List[Publication]:
        """Retorna solo las publicaciones incluidas en reportes."""
        return [pub for pub in self.publications if pub.is_included_in_report]

    def get_publications_by_year(self, year: int) -> List[Publication]:
        """Obtiene publicaciones de un año específico."""
        return [pub for pub in self.publications if pub.year == year]

    def get_publications_by_type(self, document_type: DocumentType) -> List[Publication]:
        """Obtiene publicaciones por tipo de documento."""
        return [pub for pub in self.publications if pub.document_type == document_type]

    def get_publications_by_quartile(self, quartile: str) -> List[Publication]:
        """Obtiene publicaciones por cuartil SJR."""
        return [pub for pub in self.publications if pub.best_sjr_quartile == quartile]

    def count_by_year(self) -> dict[int, int]:
        """Cuenta publicaciones agrupadas por año."""
        included_pubs = self.get_included_publications()
        count = {}
        
        for pub in included_pubs:
            if pub.year:
                count[pub.year] = count.get(pub.year, 0) + 1
        
        return count

    def count_by_quartile(self) -> dict[str, int]:
        """Cuenta publicaciones por cuartil SJR."""
        included_pubs = self.get_included_publications()
        count = {}
        
        for pub in included_pubs:
            quartile = pub.best_sjr_quartile
            if quartile:
                count[quartile] = count.get(quartile, 0) + 1
        
        return count

    def get_subject_areas_summary(self) -> dict[str, int]:
        """Obtiene resumen de áreas temáticas."""
        included_pubs = self.get_included_publications()
        count = {}
        
        for pub in included_pubs:
            for area in pub.subject_areas:
                count[area] = count.get(area, 0) + 1
        
        return count

    def get_year_range(self) -> tuple[Optional[int], Optional[int]]:
        """Obtiene el rango de años de las publicaciones."""
        included_pubs = self.get_included_publications()
        years = [pub.year for pub in included_pubs if pub.year]
        
        if not years:
            return None, None
        
        return min(years), max(years)

    def total_citations(self) -> int:
        """Calcula el total de citas de todas las publicaciones."""
        return sum(pub.citation_count for pub in self.get_included_publications())

    def __len__(self) -> int:
        """Retorna el número de publicaciones."""
        return len(self.publications)

    def __iter__(self):
        """Permite iterar sobre las publicaciones."""
        return iter(self.publications)