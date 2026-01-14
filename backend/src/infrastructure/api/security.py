"""
Dependencias de seguridad para FastAPI.

Este módulo proporciona las dependencias para verificar autenticación
y autorización en los endpoints de la API.
"""

from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.application.services.auth_service import AuthService


# Esquema de seguridad HTTP Bearer
security = HTTPBearer()


class SecurityDependencies:
    """
    Dependencias de seguridad para inyección en endpoints.
    
    Proporciona métodos para verificar autenticación y roles de usuarios.
    """

    def __init__(self, auth_service: AuthService):
        """
        Inicializa las dependencias de seguridad.
        
        Args:
            auth_service: Servicio de autenticación
        """
        self._auth_service = auth_service

    async def get_current_user(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        """
        Obtiene el usuario actual autenticado.
        
        Esta dependencia verifica el token JWT y retorna el usuario.
        
        Args:
            credentials: Credenciales HTTP Bearer
            
        Returns:
            User: Usuario autenticado
            
        Raises:
            HTTPException: Si el token es inválido o el usuario no existe
        """
        token = credentials.credentials
        user = await self._auth_service.get_current_user(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return user

    async def get_current_active_user(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        """
        Obtiene el usuario actual activo.
        
        Args:
            credentials: Credenciales HTTP Bearer
            
        Returns:
            User: Usuario activo autenticado
            
        Raises:
            HTTPException: Si el usuario no está activo
        """
        user = await self.get_current_user(credentials)
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario desactivado"
            )
        
        return user

    def require_roles(self, allowed_roles: List[Role]):
        """
        Factory para crear una dependencia que requiere roles específicos.
        
        Args:
            allowed_roles: Lista de roles permitidos
            
        Returns:
            Dependencia que verifica el rol del usuario
        """
        async def role_checker(
            credentials: HTTPAuthorizationCredentials = Depends(security)
        ) -> User:
            user = await self.get_current_active_user(credentials)
            
            if user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Acceso denegado. Se requiere uno de los siguientes roles: {[r.value for r in allowed_roles]}"
                )
            
            return user
        
        return role_checker

    def require_admin(self):
        """
        Crea una dependencia que requiere rol de administrador.
        
        Returns:
            Dependencia que verifica rol ADMIN
        """
        return self.require_roles([Role.ADMIN])

    def require_user_or_admin(self):
        """
        Crea una dependencia que permite tanto USER como ADMIN.
        
        Returns:
            Dependencia que permite ambos roles
        """
        return self.require_roles([Role.ADMIN, Role.USER])


def create_security_dependencies(auth_service: AuthService) -> SecurityDependencies:
    """
    Factory function para crear las dependencias de seguridad.
    
    Args:
        auth_service: Servicio de autenticación
        
    Returns:
        Instancia de SecurityDependencies
    """
    return SecurityDependencies(auth_service)
