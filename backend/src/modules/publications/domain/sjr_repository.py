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
        journal_name: str, 
        publication_year: int
    ) -> Tuple[List[str], List[str], int]:
        """
        Obtiene los datos SJR de una revista para un año específico.
        
        Si el año solicitado es mayor al disponible, utiliza el último año
        disponible (mapeo dinámico).
        
        Args:
            journal_name: Nombre de la revista/fuente
            publication_year: Año de publicación del artículo
            
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
