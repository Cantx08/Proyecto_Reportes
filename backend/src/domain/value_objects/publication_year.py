from dataclasses import dataclass
from datetime import datetime

from ..exceptions.publication_exceptions import InvalidPublicationYearError


@dataclass(frozen=True)
class PublicationYear:
    """
    Value Object para año de publicación.
    
    Valida que el año esté en un rango válido.
    """
    value: int
    
    # Rango válido de años (desde 1900 hasta el año actual + 2)
    MIN_YEAR = 1900
    MAX_YEAR = datetime.now().year + 2
    
    def __post_init__(self):
        """Valida el año al crear el objeto."""
        if not isinstance(self.value, int):
            raise InvalidPublicationYearError("Publication year must be an integer")
        
        if self.value < self.MIN_YEAR or self.value > self.MAX_YEAR:
            raise InvalidPublicationYearError(
                f"Publication year must be between {self.MIN_YEAR} and {self.MAX_YEAR}"
            )
    
    def __str__(self) -> str:
        """Representación string del año."""
        return str(self.value)
    
    def __int__(self) -> int:
        """Conversión a entero."""
        return self.value
    
    def __eq__(self, other) -> bool:
        """Compara años."""
        if isinstance(other, PublicationYear):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        return False
    
    def __hash__(self) -> int:
        """Hash del año."""
        return hash(self.value)
    
    def __lt__(self, other) -> bool:
        """Comparación menor que."""
        if isinstance(other, PublicationYear):
            return self.value < other.value
        if isinstance(other, int):
            return self.value < other
        return NotImplemented
    
    def __le__(self, other) -> bool:
        """Comparación menor o igual que."""
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other) -> bool:
        """Comparación mayor que."""
        if isinstance(other, PublicationYear):
            return self.value > other.value
        if isinstance(other, int):
            return self.value > other
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        """Comparación mayor o igual que."""
        return self.__gt__(other) or self.__eq__(other)
    
    @property
    def is_current_year(self) -> bool:
        """Verifica si es el año actual."""
        return self.value == datetime.now().year
    
    @property
    def is_future(self) -> bool:
        """Verifica si es un año futuro."""
        return self.value > datetime.now().year
    
    @property
    def is_recent(self, years_back: int = 5) -> bool:
        """Verifica si el año está dentro de los últimos N años."""
        current_year = datetime.now().year
        return current_year - years_back <= self.value <= current_year
    
    @classmethod
    def create(cls, value: int) -> 'PublicationYear':
        """Factory method para crear un PublicationYear."""
        return cls(value)
    
    @classmethod
    def current_year(cls) -> 'PublicationYear':
        """Retorna el año actual."""
        return cls(datetime.now().year)
    
    @classmethod
    def is_valid_year(cls, value: int) -> bool:
        """Verifica si un año es válido."""
        try:
            cls(value)
            return True
        except InvalidPublicationYearError:
            return False