from dataclasses import dataclass
from typing import Pattern
import re

from ..exceptions.author_exceptions import InvalidScopusIdError


@dataclass(frozen=True)
class ScopusId:
    """
    Value Object para ID de Scopus.
    
    Valida que el ID de Scopus tenga el formato correcto.
    """
    value: str
    
    # Patrón para validar IDs de Scopus (números de 10-11 dígitos)
    SCOPUS_ID_PATTERN: Pattern = re.compile(r'^\d{10,11}$')
    
    def __post_init__(self):
        """Valida el ID de Scopus al crear el objeto."""
        if not self.value:
            raise InvalidScopusIdError("Scopus ID cannot be empty")
        
        if not isinstance(self.value, str):
            raise InvalidScopusIdError("Scopus ID must be a string")
        
        # Limpiar espacios y caracteres especiales
        cleaned_value = self.value.strip().replace('-', '').replace(' ', '')
        
        if not self.SCOPUS_ID_PATTERN.match(cleaned_value):
            raise InvalidScopusIdError(
                f"Invalid Scopus ID format: {self.value}. "
                "Expected 10-11 digit number"
            )
        
        # Usar object.__setattr__ porque la clase es frozen
        object.__setattr__(self, 'value', cleaned_value)
    
    def __str__(self) -> str:
        """Representación string del ID."""
        return self.value
    
    def __eq__(self, other) -> bool:
        """Compara IDs de Scopus."""
        if isinstance(other, ScopusId):
            return self.value == other.value
        if isinstance(other, str):
            try:
                return self.value == ScopusId(other).value
            except InvalidScopusIdError:
                return False
        return False
    
    def __hash__(self) -> int:
        """Hash del ID de Scopus."""
        return hash(self.value)
    
    @classmethod
    def create(cls, value: str) -> 'ScopusId':
        """Factory method para crear un ScopusId."""
        return cls(value)
    
    @classmethod
    def is_valid_format(cls, value: str) -> bool:
        """Verifica si un string tiene formato válido de Scopus ID."""
        try:
            cls(value)
            return True
        except InvalidScopusIdError:
            return False