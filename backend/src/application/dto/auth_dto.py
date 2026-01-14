"""
DTOs para el módulo de autenticación.

Define las estructuras de datos para transferencia de información
relacionada con autenticación y usuarios.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from src.domain.enums.role import Role


# ============================================================================
# DTOs de SOLICITUD (Request)
# ============================================================================

class UserRegisterDTO(BaseModel):
    """DTO para registro de nuevo usuario."""
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: EmailStr = Field(..., description="Correo electrónico único")
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")
    full_name: Optional[str] = Field(None, max_length=255, description="Nombre completo")
    role: Role = Field(default=Role.USER, description="Rol del usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secretpassword123",
                "full_name": "John Doe",
                "role": "user"
            }
        }


class UserLoginDTO(BaseModel):
    """DTO para login de usuario."""
    username: str = Field(..., description="Nombre de usuario o correo electrónico")
    password: str = Field(..., description="Contraseña")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "secretpassword123"
            }
        }


class UserUpdateDTO(BaseModel):
    """DTO para actualización de usuario."""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Nuevo nombre de usuario")
    email: Optional[EmailStr] = Field(None, description="Nuevo correo electrónico")
    full_name: Optional[str] = Field(None, max_length=255, description="Nuevo nombre completo")
    is_active: Optional[bool] = Field(None, description="Estado activo del usuario")
    role: Optional[Role] = Field(None, description="Nuevo rol del usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johnupdated",
                "email": "newemail@example.com",
                "full_name": "John Updated Doe",
                "is_active": True,
                "role": "admin"
            }
        }


class PasswordChangeDTO(BaseModel):
    """DTO para cambio de contraseña."""
    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., min_length=8, description="Nueva contraseña")

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword456"
            }
        }


# ============================================================================
# DTOs de RESPUESTA (Response)
# ============================================================================

class TokenResponseDTO(BaseModel):
    """DTO para respuesta de token de autenticación."""
    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


class UserResponseDTO(BaseModel):
    """DTO para respuesta con información de usuario."""
    id: int = Field(..., description="ID único del usuario")
    username: str = Field(..., description="Nombre de usuario")
    email: str = Field(..., description="Correo electrónico")
    full_name: Optional[str] = Field(None, description="Nombre completo")
    role: str = Field(..., description="Rol del usuario")
    is_active: bool = Field(..., description="Estado activo del usuario")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "role": "user",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class UsersResponseDTO(BaseModel):
    """DTO para respuesta con lista de usuarios."""
    users: List[UserResponseDTO] = Field(..., description="Lista de usuarios")
    total: int = Field(..., description="Total de usuarios")

    class Config:
        json_schema_extra = {
            "example": {
                "users": [
                    {
                        "id": 1,
                        "username": "johndoe",
                        "email": "john@example.com",
                        "full_name": "John Doe",
                        "role": "user",
                        "is_active": True
                    }
                ],
                "total": 1
            }
        }


class AuthResponseDTO(BaseModel):
    """DTO para respuesta de autenticación completa."""
    user: UserResponseDTO = Field(..., description="Información del usuario")
    token: TokenResponseDTO = Field(..., description="Token de acceso")

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com",
                    "full_name": "John Doe",
                    "role": "user",
                    "is_active": True
                },
                "token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "expires_in": 3600
                }
            }
        }


class MessageResponseDTO(BaseModel):
    """DTO para respuestas de mensajes simples."""
    message: str = Field(..., description="Mensaje de respuesta")
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operación realizada exitosamente",
                "success": True
            }
        }
