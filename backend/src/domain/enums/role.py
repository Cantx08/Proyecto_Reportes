"""
Enumeración de roles de usuario.

Define los roles disponibles en el sistema de autenticación.
"""

from enum import Enum


class Role(str, Enum):
    """
    Roles disponibles en el sistema.
    
    - ADMIN: Acceso completo a todas las funcionalidades, incluyendo
             gestión de usuarios, información del sistema y configuración.
    - USER: Acceso enfocado en la generación de certificaciones y PDFs.
    """
    ADMIN = "admin"
    USER = "user"
    
    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def from_string(cls, value: str) -> "Role":
        """Convierte un string a Role."""
        value_lower = value.lower()
        for role in cls:
            if role.value == value_lower:
                return role
        raise ValueError(f"Rol no válido: {value}")
