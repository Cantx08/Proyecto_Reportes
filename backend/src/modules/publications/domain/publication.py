from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Publication:
    """
    Entidad de dominio que representa una publicación científica.
    
    Contiene los datos esenciales de una publicación obtenida de Scopus,
    enriquecida con datos SJR para las categorías temáticas.
    """
    # Identificadores
    scopus_id: str              # ID único de la publicación en Scopus
    eid: str                    # Electronic ID de Scopus (para enlaces)
    doi: Optional[str]          # Digital Object Identifier
    
    # Datos básicos de la publicación
    title: str                  # Título de la publicación
    year: int                   # Año de publicación
    publication_date: str       # Fecha completa de publicación (YYYY-MM-DD)
    source_title: str           # Nombre de la revista/conferencia
    document_type: str          # Tipo de documento (Article, Conference Paper, etc.)
    
    # Filiación institucional del autor consultado
    affiliation_name: str       # Nombre de la filiación del autor dueño del Scopus ID
    affiliation_id: Optional[str] = None  # ID de la filiación en Scopus
    
    # Clasificación temática (del SJR histórico)
    # Áreas temáticas generales (ej: ["Computer Science", "Engineering"])
    subject_areas: List[str] = field(default_factory=list)
    # Categorías con cuartiles tal como vienen del SJR (ej: ["Software (Q1)", "Artificial Intelligence (Q2)"])
    categories_with_quartiles: List[str] = field(default_factory=list)
    # Año del SJR utilizado (para años futuros se mapea al último disponible)
    sjr_year_used: Optional[int] = None

    def has_institutional_affiliation(self, institution_keywords: List[str]) -> bool:
        """
        Verifica si la publicación tiene filiación con alguna institución específica.
        
        Args:
            institution_keywords: Lista de palabras clave para identificar la institución
            
        Returns:
            True si la filiación contiene alguna de las palabras clave
        """
        affiliation_lower = self.affiliation_name.lower()
        return any(
            keyword.lower() in affiliation_lower 
            for keyword in institution_keywords
        )