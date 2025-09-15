from dataclasses import dataclass
import re
from typing import Pattern

from ..exceptions.publication_exceptions import InvalidDOIError


@dataclass(frozen=True)
class DOI:
    """
    Value Object para Digital Object Identifier (DOI).
    
    Valida que el DOI tenga un formato correcto.
    """
    value: str
    
    # Patrón para validar DOIs
    DOI_PATTERN: Pattern = re.compile(
        r'^10\.\d{4,}\/[^\s]+$',
        re.IGNORECASE
    )
    
    def __post_init__(self):
        """Valida el DOI al crear el objeto."""
        if not self.value:
            raise InvalidDOIError("DOI cannot be empty")
        
        if not isinstance(self.value, str):
            raise InvalidDOIError("DOI must be a string")
        
        # Limpiar espacios y normalizar
        cleaned_value = self.value.strip()
        
        # Remover prefijo "doi:" si existe
        if cleaned_value.lower().startswith('doi:'):
            cleaned_value = cleaned_value[4:].strip()
        
        # Remover prefijo "https://doi.org/" si existe
        if cleaned_value.lower().startswith('https://doi.org/'):
            cleaned_value = cleaned_value[16:].strip()
        
        # Remover prefijo "http://dx.doi.org/" si existe
        if cleaned_value.lower().startswith('http://dx.doi.org/'):
            cleaned_value = cleaned_value[18:].strip()
        
        if not self.DOI_PATTERN.match(cleaned_value):
            raise InvalidDOIError(f"Invalid DOI format: {self.value}")
        
        # Usar object.__setattr__ porque la clase es frozen
        object.__setattr__(self, 'value', cleaned_value)
    
    def __str__(self) -> str:
        """Representación string del DOI."""
        return self.value
    
    def __eq__(self, other) -> bool:
        """Compara DOIs."""
        if isinstance(other, DOI):
            return self.value == other.value
        if isinstance(other, str):
            try:
                return self.value == DOI(other).value
            except InvalidDOIError:
                return False
        return False
    
    def __hash__(self) -> int:
        """Hash del DOI."""
        return hash(self.value)
    
    @property
    def url(self) -> str:
        """Retorna la URL completa del DOI."""
        return f"https://doi.org/{self.value}"
    
    @property
    def registrant(self) -> str:
        """Retorna el código del registrante (parte después de 10.)."""
        return self.value.split('/')[0].split('.')[1]
    
    @property
    def suffix(self) -> str:
        """Retorna el sufijo del DOI (parte después del /)."""
        return self.value.split('/', 1)[1]
    
    @classmethod
    def create(cls, value: str) -> 'DOI':
        """Factory method para crear un DOI."""
        return cls(value)
    
    @classmethod
    def is_valid_format(cls, value: str) -> bool:
        """Verifica si un string tiene formato válido de DOI."""
        try:
            cls(value)
            return True
        except InvalidDOIError:
            return False