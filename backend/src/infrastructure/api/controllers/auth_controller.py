"""
Controlador de autenticación.

Este módulo maneja las peticiones HTTP relacionadas con la autenticación
y gestión de usuarios.
"""

from src.application.services.auth_service import AuthService
from src.application.dto.auth_dto import (
    UserRegisterDTO, UserLoginDTO, UserUpdateDTO, PasswordChangeDTO,
    TokenResponseDTO, UserResponseDTO, UsersResponseDTO, AuthResponseDTO,
    MessageResponseDTO
)
from src.domain.entities.user import User


class AuthController:
    """
    Controlador para operaciones de autenticación.
    
    Responsabilidades:
    - Manejar peticiones de registro y login
    - Gestionar operaciones CRUD de usuarios
    - Verificar tokens y sesiones
    """

    def __init__(self, auth_service: AuthService):
        """
        Inicializa el controlador.
        
        Args:
            auth_service: Servicio de autenticación
        """
        self._auth_service = auth_service

    # =========================================================================
    # ENDPOINTS PÚBLICOS
    # =========================================================================

    async def register(self, register_dto: UserRegisterDTO) -> AuthResponseDTO:
        """
        Registra un nuevo usuario.
        
        Args:
            register_dto: Datos del nuevo usuario
            
        Returns:
            AuthResponseDTO con el usuario creado y su token
        """
        # Verificar si es el primer usuario
        is_first = await self._auth_service.is_first_user()
        return await self._auth_service.register(register_dto, is_first_user=is_first)

    async def login(self, login_dto: UserLoginDTO) -> AuthResponseDTO:
        """
        Autentica un usuario.
        
        Args:
            login_dto: Credenciales de login
            
        Returns:
            AuthResponseDTO con el usuario y su token
        """
        return await self._auth_service.login(login_dto)

    async def verify_token(self, token: str) -> UserResponseDTO:
        """
        Verifica un token y retorna los datos del usuario.
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            UserResponseDTO con los datos del usuario
        """
        is_valid, user_response = await self._auth_service.verify_token(token)
        if not is_valid or not user_response:
            raise ValueError("Token inválido o expirado")
        return user_response

    # =========================================================================
    # ENDPOINTS DE USUARIO ACTUAL
    # =========================================================================

    async def get_me(self, current_user: User) -> UserResponseDTO:
        """
        Obtiene la información del usuario actual.
        
        Args:
            current_user: Usuario autenticado actual
            
        Returns:
            UserResponseDTO con la información del usuario
        """
        return UserResponseDTO(
            id=current_user.user_id,
            username=current_user.username,
            email=current_user.email,
            full_name=current_user.full_name,
            role=current_user.role.value,
            is_active=current_user.is_active,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at
        )

    async def update_me(
        self, 
        current_user: User, 
        update_dto: UserUpdateDTO
    ) -> UserResponseDTO:
        """
        Actualiza la información del usuario actual.
        
        Nota: Los usuarios normales no pueden cambiar su propio rol.
        
        Args:
            current_user: Usuario autenticado actual
            update_dto: Datos a actualizar
            
        Returns:
            UserResponseDTO con la información actualizada
        """
        # Los usuarios no-admin no pueden cambiar su propio rol
        if not current_user.is_admin() and update_dto.role is not None:
            update_dto.role = None
        
        # Los usuarios no pueden desactivarse a sí mismos
        if update_dto.is_active is False:
            update_dto.is_active = None
        
        return await self._auth_service.update_user(current_user.user_id, update_dto)

    async def change_my_password(
        self, 
        current_user: User, 
        password_dto: PasswordChangeDTO
    ) -> MessageResponseDTO:
        """
        Cambia la contraseña del usuario actual.
        
        Args:
            current_user: Usuario autenticado actual
            password_dto: Contraseñas actual y nueva
            
        Returns:
            MessageResponseDTO con confirmación
        """
        await self._auth_service.change_password(current_user.user_id, password_dto)
        return MessageResponseDTO(
            message="Contraseña actualizada exitosamente",
            success=True
        )

    # =========================================================================
    # ENDPOINTS DE ADMINISTRACIÓN (SOLO ADMIN)
    # =========================================================================

    async def get_all_users(self) -> UsersResponseDTO:
        """
        Obtiene todos los usuarios.
        
        Solo accesible por administradores.
        
        Returns:
            UsersResponseDTO con lista de usuarios
        """
        return await self._auth_service.get_all_users()

    async def get_user(self, user_id: int) -> UserResponseDTO:
        """
        Obtiene un usuario por su ID.
        
        Solo accesible por administradores.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            UserResponseDTO con la información del usuario
        """
        user = await self._auth_service.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")
        return user

    async def update_user(
        self, 
        user_id: int, 
        update_dto: UserUpdateDTO
    ) -> UserResponseDTO:
        """
        Actualiza un usuario por su ID.
        
        Solo accesible por administradores.
        
        Args:
            user_id: ID del usuario
            update_dto: Datos a actualizar
            
        Returns:
            UserResponseDTO con la información actualizada
        """
        return await self._auth_service.update_user(user_id, update_dto)

    async def delete_user(self, user_id: int, current_user: User) -> MessageResponseDTO:
        """
        Elimina un usuario por su ID.
        
        Solo accesible por administradores.
        Un usuario no puede eliminarse a sí mismo.
        
        Args:
            user_id: ID del usuario a eliminar
            current_user: Usuario que realiza la acción
            
        Returns:
            MessageResponseDTO con confirmación
        """
        if current_user.user_id == user_id:
            raise ValueError("No puedes eliminarte a ti mismo")
        
        deleted = await self._auth_service.delete_user(user_id)
        if not deleted:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")
        
        return MessageResponseDTO(
            message=f"Usuario con ID {user_id} eliminado exitosamente",
            success=True
        )

    async def create_user(
        self, 
        register_dto: UserRegisterDTO
    ) -> UserResponseDTO:
        """
        Crea un nuevo usuario (usado por administradores).
        
        A diferencia del registro público, el admin puede especificar
        cualquier rol para el nuevo usuario.
        
        Args:
            register_dto: Datos del nuevo usuario
            
        Returns:
            UserResponseDTO con el usuario creado
        """
        result = await self._auth_service.register(register_dto, is_first_user=False)
        return result.user
