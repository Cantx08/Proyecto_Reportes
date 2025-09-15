"""
Value Objects para el dominio de reportes.
"""
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from enum import Enum

from ..entities.publication import Publication


class Gender(Enum):
    """Enum para el género del docente."""
    MASCULINO = "M"
    FEMENINO = "F"


class Authority(Enum):
    """Enum para el tipo de firmante."""
    DIRECTORA_INVESTIGACION = 1
    VICERRECTOR_INVESTIGACION = 2


@dataclass(frozen=True)
class AuthorInfo:
    """Value Object para la información básica del docente."""
    name: str
    gender: Gender
    department: str
    role: str
    
    def get_article(self) -> str:
        """Retorna el artículo apropiado según el género."""
        return "El" if self.gender == Gender.MASCULINO else "La"
    
    def get_author_coauthor(self) -> str:
        """Retorna la forma apropiada de autor/coautor según el género."""
        return "autor/co-autor" if self.gender == Gender.MASCULINO else "autora/co-autora"


@dataclass(frozen=True)
class ReportConfiguration:
    """Value Object para la configuración del reporte."""
    memorandum: str
    signatory: Authority
    report_date: str
    
    @classmethod
    def generate_with_current_date(cls, memorandum: str = "", signatory: Authority = Authority.DIRECTORA_INVESTIGACION):
        """Factory method para crear configuración con fecha actual."""
        report_date = datetime.now().strftime("%d de %B de %Y")
        return cls(memorandum, signatory, report_date)


@dataclass(frozen=True)
class PublicationsStatistics:
    """Value Object para las estadísticas de publicaciones."""
    subject_areas: List[str]
    documents_by_year: Dict[str, int]
    
    def has_sufficient_data_for_graph(self) -> bool:
        """Verifica si hay suficientes datos para mostrar un gráfico."""
        return len(self.documents_by_year) > 1


@dataclass(frozen=True)
class PublicationCollections:
    """Value Object que agrupa todas las colecciones de publicaciones."""
    scopus: List[Publication]
    wos: List[Publication]
    regional_publications: List[Publication]
    memories: List[Publication]
    books: List[Publication]
    
    def get_total_publications(self) -> int:
        """Calcula el total de publicaciones."""
        return (len(self.scopus) + len(self.wos) + len(self.regional_publications) + 
                len(self.memories) + len(self.books))
    
    def exists_scopus_publications(self) -> bool:
        """Verifica si hay publicaciones Scopus."""
        return len(self.scopus) > 0
