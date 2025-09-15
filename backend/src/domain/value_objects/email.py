from dataclasses import dataclass
import re
from typing import Pattern

from ..exceptions.author_exceptions import InvalidEmailError


@dataclass(frozen=True)
class Email:
    """
    Value Object para direcciones de email.
    
    Valida que el email tenga un formato correcto.
    """
    value: str
    
    # Patrón básico para validar emails
    EMAIL_PATTERN: Pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    def __post_init__(self):
        """Valida el email al crear el objeto."""
        if not self.value:
            raise InvalidEmailError("Email cannot be empty")
        
        if not isinstance(self.value, str):
            raise InvalidEmailError("Email must be a string")
        
        # Limpiar y normalizar
        cleaned_value = self.value.strip().lower()
        
        if not self.EMAIL_PATTERN.match(cleaned_value):
            raise InvalidEmailError(f"Invalid email format: {self.value}")
        
        # Usar object.__setattr__ porque la clase es frozen
        object.__setattr__(self, 'value', cleaned_value)
    
    def __str__(self) -> str:
        """Representación string del email."""
        return self.value
    
    def __eq__(self, other) -> bool:
        """Compara emails."""
        if isinstance(other, Email):
            return self.value == other.value
        if isinstance(other, str):
            try:
                return self.value == Email(other).value
            except InvalidEmailError:
                return False
        return False
    
    def __hash__(self) -> int:
        """Hash del email."""
        return hash(self.value)
    
    @property
    def domain(self) -> str:
        """Retorna el dominio del email."""
        return self.value.split('@')[1]
    
    @property
    def local_part(self) -> str:
        """Retorna la parte local del email (antes del @)."""
        return self.value.split('@')[0]
    
    @classmethod
    def create(cls, value: str) -> 'Email':
        """Factory method para crear un Email."""
        return cls(value)
    
    @classmethod
    def is_valid_format(cls, value: str) -> bool:
        """Verifica si un string tiene formato válido de email."""
        try:
            cls(value)
            return True
        except InvalidEmailError:
            return False