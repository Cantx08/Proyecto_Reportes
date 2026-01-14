"""
Módulo que define la entidad Usuario.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..enums.role import Role


@dataclass
class User:
    """
    Entidad que representa un usuario del sistema.
    
    Attributes:
        username: Nombre de usuario único
        email: Correo electrónico único
        hashed_password: Contraseña hasheada
        role: Rol del usuario (ADMIN o USER)
        user_id: ID único del usuario (opcional en creación)
        full_name: Nombre completo del usuario
        is_active: Si el usuario está activo
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """
    username: str
    email: str
    hashed_password: str
    role: Role
    user_id: Optional[int] = None
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones post-inicialización."""
        if not self.username:
            raise ValueError("El nombre de usuario es requerido")
        if not self.email:
            raise ValueError("El correo electrónico es requerido")
        if not self.hashed_password:
            raise ValueError("La contraseña es requerida")
        if not isinstance(self.role, Role):
            if isinstance(self.role, str):
                self.role = Role.from_string(self.role)
            else:
                raise ValueError("El rol debe ser una instancia de Role")

    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador."""
        return self.role == Role.ADMIN

    def can_manage_users(self) -> bool:
        """Verifica si el usuario puede gestionar otros usuarios."""
        return self.is_admin()

    def can_manage_system(self) -> bool:
        """Verifica si el usuario puede gestionar la configuración del sistema."""
        return self.is_admin()

    def can_generate_reports(self) -> bool:
        """Verifica si el usuario puede generar reportes/certificaciones."""
        # Tanto Admin como User pueden generar reportes
        return self.is_active

    def get_display_name(self) -> str:
        """Retorna el nombre para mostrar del usuario."""
        return self.full_name if self.full_name else self.username
