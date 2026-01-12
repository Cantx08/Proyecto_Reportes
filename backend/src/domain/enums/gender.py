"""
Enumeración para el género de los docentes/autores.
"""
from enum import Enum


class Gender(str, Enum):
    """
    Enum para el género del docente.
    
    Usado para determinar el artículo gramatical correcto
    y otras variaciones de género en el texto del reporte.
    """
    MASCULINO = "M"
    FEMENINO = "F"
    
    @classmethod
    def from_string(cls, value: str) -> "Gender":
        """
        Crea un enum a partir de un string.
        
        Args:
            value: Valor del género ("M", "F", "MASCULINO", "FEMENINO")
            
        Returns:
            Gender enum correspondiente
            
        Raises:
            ValueError: Si el valor no es válido
        """
        if not isinstance(value, str):
            value = str(value)
        
        value_upper = value.upper().strip()
        
        # Mapeo de valores aceptados
        if value_upper in ["M", "MASCULINO", "HOMBRE", "MALE"]:
            return cls.MASCULINO
        elif value_upper in ["F", "FEMENINO", "MUJER", "FEMALE"]:
            return cls.FEMENINO
        else:
            raise ValueError(f"Valor de género no válido: {value}")
    
    def __str__(self) -> str:
        """Retorna el valor del género."""
        return self.value
