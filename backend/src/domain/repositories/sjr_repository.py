from abc import ABC, abstractmethod


class SJRRepository(ABC):
    """Interfaz para el repositorio de datos SJR."""
    
    @abstractmethod
    def get_journal_categories(self, journal_name: str, year: str) -> str:
        """Obtiene las categorías de una revista en un año específico."""
        pass
    
    @abstractmethod
    def normalize_journal_name(self, name: str) -> str:
        """Normaliza el nombre de una revista para búsqueda."""
        pass
