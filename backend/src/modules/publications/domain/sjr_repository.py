from abc import ABC, abstractmethod
from typing import List, Tuple


class ISJRRepository(ABC):
    """
    Interfaz del repositorio de datos SJR (Scimago Journal Rank).
    
    Define el contrato para obtener datos SJR de revistas científicas,
    incluyendo áreas temáticas y categorías con cuartiles.
    """

    @abstractmethod
    def get_max_available_year(self) -> int:
        """
        Obtiene el año más reciente disponible en los datos SJR.
        
        Returns:
            El año máximo disponible en el histórico SJR
        """
        pass

    @abstractmethod
    def get_journal_data(
        self, 
        issns: List[str], 
        publication_year: int,
        source_title: str = ""
    ) -> Tuple[List[str], List[str], int]:
        """
        Obtiene los datos SJR de una revista para un año específico.
        
        Estrategia de búsqueda:
        1. Búsqueda primaria por ISSNs (impreso/electrónico)
        2. Fallback por nombre normalizado de revista
        
        Si el año solicitado es mayor al disponible, utiliza el último año
        disponible (mapeo dinámico).
        
        Args:
            issns: Lista de ISSNs asociados a la revista/fuente
            publication_year: Año de publicación del artículo
            source_title: Nombre de la revista (usado como fallback)
            
        Returns:
            Tupla con:
            - Lista de áreas temáticas (ej: ["Computer Science", "Engineering"])
            - Lista de categorías con cuartiles (ej: ["Software (Q1)", "AI (Q2)"])
            - Año del SJR utilizado (para mostrar el mapeo dinámico)
        """
        pass

    @abstractmethod
    def normalize_journal_name(self, name: str) -> str:
        """
        Normaliza el nombre de una revista para búsqueda consistente.
        
        Args:
            name: Nombre original de la revista
            
        Returns:
            Nombre normalizado (minúsculas, sin acentos, etc.)
        """
        pass
