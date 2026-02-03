from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SJRMetric:
    """Métrica SJR para una categoría específica."""
    category: str           # Nombre de la categoría (ej: "Software", "Computer Science")
    quartile: str           # Cuartil (Q1, Q2, Q3, Q4)
    percentile: float       # Percentil calculado
    sjr_year: int           # Año del SJR utilizado (mapeo dinámico 2025->2024)


@dataclass
class Publication:
    """
    Entidad de dominio que representa una publicación científica.
    
    Contiene los datos esenciales de una publicación obtenida de Scopus,
    enriquecida con métricas SJR para las categorías temáticas.
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
    
    # Filiación institucional
    affiliation_name: str       # Nombre de la filiación principal del autor
    affiliation_id: Optional[str] = None  # ID de la filiación en Scopus
    
    # Clasificación temática
    subject_areas: List[str] = field(default_factory=list)  # Áreas temáticas generales
    sjr_metrics: List[SJRMetric] = field(default_factory=list)  # Categorías con cuartiles

    def best_quartile(self) -> Optional[str]:
        """
        Retorna el mejor cuartil de todas las categorías.
        
        Returns:
            El mejor cuartil (Q1 > Q2 > Q3 > Q4) o None si no hay métricas.
        """
        if not self.sjr_metrics:
            return None
        
        quartile_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
        best = min(
            self.sjr_metrics, 
            key=lambda m: quartile_order.get(m.quartile, 5)
        )
        return best.quartile

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