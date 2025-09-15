from dataclasses import dataclass
from enum import Enum


class Quartile(Enum):
    """Enumeración para cuartiles SJR."""
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"


@dataclass(frozen=True)
class SJRQuartile:
    """
    Value Object para cuartil SJR.
    
    Representa el cuartil de una revista en una categoría específica.
    """
    value: Quartile
    
    def __post_init__(self):
        """Valida el cuartil al crear el objeto."""
        if not isinstance(self.value, Quartile):
            raise ValueError("Quartile must be a Quartile enum value")
    
    def __str__(self) -> str:
        """Representación string del cuartil."""
        return self.value.value
    
    def __eq__(self, other) -> bool:
        """Compara cuartiles."""
        if isinstance(other, SJRQuartile):
            return self.value == other.value
        if isinstance(other, Quartile):
            return self.value == other
        if isinstance(other, str):
            try:
                return self.value == Quartile(other)
            except ValueError:
                return False
        return False
    
    def __hash__(self) -> int:
        """Hash del cuartil."""
        return hash(self.value)
    
    def __lt__(self, other) -> bool:
        """Comparación menor que (Q1 < Q2 < Q3 < Q4)."""
        if isinstance(other, SJRQuartile):
            quartile_order = {Quartile.Q1: 1, Quartile.Q2: 2, Quartile.Q3: 3, Quartile.Q4: 4}
            return quartile_order[self.value] < quartile_order[other.value]
        return NotImplemented
    
    def __le__(self, other) -> bool:
        """Comparación menor o igual que."""
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other) -> bool:
        """Comparación mayor que."""
        if isinstance(other, SJRQuartile):
            quartile_order = {Quartile.Q1: 1, Quartile.Q2: 2, Quartile.Q3: 3, Quartile.Q4: 4}
            return quartile_order[self.value] > quartile_order[other.value]
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        """Comparación mayor o igual que."""
        return self.__gt__(other) or self.__eq__(other)
    
    @property
    def is_top_quartile(self) -> bool:
        """Verifica si es Q1 (mejor cuartil)."""
        return self.value == Quartile.Q1
    
    @property
    def is_high_impact(self) -> bool:
        """Verifica si es Q1 o Q2 (alto impacto)."""
        return self.value in [Quartile.Q1, Quartile.Q2]
    
    @property
    def numeric_value(self) -> int:
        """Retorna el valor numérico del cuartil (1-4)."""
        quartile_map = {Quartile.Q1: 1, Quartile.Q2: 2, Quartile.Q3: 3, Quartile.Q4: 4}
        return quartile_map[self.value]
    
    @classmethod
    def create(cls, value: str) -> 'SJRQuartile':
        """Factory method para crear un SJRQuartile."""
        try:
            quartile = Quartile(value.upper())
            return cls(quartile)
        except ValueError:
            raise ValueError(f"Invalid quartile value: {value}. Must be Q1, Q2, Q3, or Q4")
    
    @classmethod
    def q1(cls) -> 'SJRQuartile':
        """Retorna Q1."""
        return cls(Quartile.Q1)
    
    @classmethod
    def q2(cls) -> 'SJRQuartile':
        """Retorna Q2."""
        return cls(Quartile.Q2)
    
    @classmethod
    def q3(cls) -> 'SJRQuartile':
        """Retorna Q3."""
        return cls(Quartile.Q3)
    
    @classmethod
    def q4(cls) -> 'SJRQuartile':
        """Retorna Q4."""
        return cls(Quartile.Q4)
    
    @classmethod
    def is_valid_quartile(cls, value: str) -> bool:
        """Verifica si un string es un cuartil válido."""
        try:
            Quartile(value.upper())
            return True
        except ValueError:
            return False