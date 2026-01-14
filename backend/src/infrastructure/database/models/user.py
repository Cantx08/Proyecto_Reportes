"""
Modelo SQLAlchemy para usuarios.

Este módulo contiene el modelo de base de datos para la gestión de usuarios
y autenticación del sistema.
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
)
from sqlalchemy.sql import func
import enum

from .base import Base


class RoleEnum(enum.Enum):
    """Enumeración para roles de usuario en la base de datos."""
    ADMIN = "admin"
    USER = "user"


class UserModel(Base):
    """
    Modelo para usuarios del sistema.
    
    Atributos:
        id: Identificador único del usuario
        username: Nombre de usuario único
        email: Correo electrónico único
        hashed_password: Contraseña hasheada con bcrypt
        full_name: Nombre completo del usuario
        role: Rol del usuario (ADMIN o USER)
        is_active: Indica si el usuario está activo
        created_at: Fecha de creación del registro
        updated_at: Fecha de última actualización
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.USER)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<UserModel(id={self.id}, username='{self.username}', role='{self.role.value}')>"
