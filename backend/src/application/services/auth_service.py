"""
Servicio de autenticación.

Este módulo implementa la lógica de negocio relacionada con la autenticación
de usuarios, incluyendo registro, login, verificación de tokens y gestión
de contraseñas.
"""

import base64
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Tuple

import bcrypt
from jose import JWTError, jwt

from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.domain.repositories.user_repository import UserRepository
from src.application.dto.auth_dto import (
    UserRegisterDTO, UserLoginDTO, UserUpdateDTO, PasswordChangeDTO,
    TokenResponseDTO, UserResponseDTO, UsersResponseDTO, AuthResponseDTO
)


class AuthService:
    """
    Servicio de autenticación que maneja toda la lógica de usuarios.
    
    Responsabilidades:
    - Registro de nuevos usuarios
    - Autenticación (login)
    - Generación y verificación de tokens JWT
    - Gestión de contraseñas
    - Operaciones CRUD sobre usuarios (para administradores)
    """

    def __init__(
        self,
        user_repository: UserRepository,
        secret_key: str = None,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 60
    ):
        """
        Inicializa el servicio de autenticación.
        
        Args:
            user_repository: Repositorio de usuarios
            secret_key: Clave secreta para firmar tokens JWT
            algorithm: Algoritmo de encriptación para JWT
            access_token_expire_minutes: Tiempo de expiración del token en minutos
        """
        self._user_repository = user_repository
        self._secret_key = secret_key or os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
        self._algorithm = algorithm
        self._access_token_expire_minutes = access_token_expire_minutes

    # =========================================================================
    # MÉTODOS DE HASHING DE CONTRASEÑAS
    # =========================================================================

    def _prepare_password(self, password: str) -> bytes:
        """
        Prepara la contraseña para bcrypt.
        
        Siempre usamos SHA256 + base64 para normalizar la contraseña.
        Esto evita el límite de 72 bytes de bcrypt y permite
        cualquier longitud de contraseña de forma segura.
        """
        # Hashear con SHA256 y codificar en base64
        # Esto produce siempre 44 caracteres, seguro para bcrypt
        sha256_hash = hashlib.sha256(password.encode('utf-8')).digest()
        return base64.b64encode(sha256_hash)

    def _hash_password(self, password: str) -> str:
        """Hashea una contraseña usando bcrypt."""
        prepared = self._prepare_password(password)
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(prepared, salt)
        return hashed.decode('utf-8')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash."""
        try:
            prepared = self._prepare_password(plain_password)
            return bcrypt.checkpw(prepared, hashed_password.encode('utf-8'))
        except Exception:
            return False

    # =========================================================================
    # MÉTODOS DE TOKEN JWT
    # =========================================================================

    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Crea un token JWT.
        
        Args:
            data: Datos a incluir en el token
            expires_delta: Tiempo de expiración personalizado
            
        Returns:
            Token JWT como string
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self._access_token_expire_minutes))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[dict]:
        """
        Decodifica y valida un token JWT.
        
        Args:
            token: Token JWT a decodificar
            
        Returns:
            Diccionario con los datos del token o None si es inválido
        """
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except JWTError:
            return None

    # =========================================================================
    # MÉTODOS DE CONVERSIÓN
    # =========================================================================

    def _user_to_response(self, user: User) -> UserResponseDTO:
        """Convierte una entidad User a DTO de respuesta."""
        return UserResponseDTO(
            id=user.user_id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    def _create_token_response(self, user: User) -> TokenResponseDTO:
        """Crea un TokenResponseDTO para un usuario."""
        token_data = {
            "sub": str(user.user_id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value
        }
        access_token = self._create_access_token(token_data)
        return TokenResponseDTO(
            access_token=access_token,
            token_type="bearer",
            expires_in=self._access_token_expire_minutes * 60
        )

    # =========================================================================
    # REGISTRO DE USUARIOS
    # =========================================================================

    async def register(self, register_dto: UserRegisterDTO, is_first_user: bool = False) -> AuthResponseDTO:
        """
        Registra un nuevo usuario.
        
        Args:
            register_dto: Datos del nuevo usuario
            is_first_user: Si es True, el primer usuario se crea como ADMIN
            
        Returns:
            AuthResponseDTO con el usuario y su token
            
        Raises:
            ValueError: Si el username o email ya existen
        """
        # Verificar que el username no exista
        if await self._user_repository.exists_by_username(register_dto.username):
            raise ValueError(f"El nombre de usuario '{register_dto.username}' ya está en uso")
        
        # Verificar que el email no exista
        if await self._user_repository.exists_by_email(register_dto.email):
            raise ValueError(f"El correo electrónico '{register_dto.email}' ya está registrado")
        
        # Determinar el rol
        role = register_dto.role
        if is_first_user:
            # El primer usuario siempre es administrador
            role = Role.ADMIN
        
        # Crear la entidad de usuario
        user = User(
            username=register_dto.username,
            email=register_dto.email,
            hashed_password=self._hash_password(register_dto.password),
            full_name=register_dto.full_name,
            role=role,
            is_active=True
        )
        
        # Persistir el usuario
        created_user = await self._user_repository.create(user)
        
        # Generar respuesta
        user_response = self._user_to_response(created_user)
        token_response = self._create_token_response(created_user)
        
        return AuthResponseDTO(user=user_response, token=token_response)

    # =========================================================================
    # LOGIN
    # =========================================================================

    async def login(self, login_dto: UserLoginDTO) -> AuthResponseDTO:
        """
        Autentica un usuario.
        
        Args:
            login_dto: Credenciales de login
            
        Returns:
            AuthResponseDTO con el usuario y su token
            
        Raises:
            ValueError: Si las credenciales son inválidas
        """
        # Buscar por username o email
        user = await self._user_repository.get_by_username(login_dto.username)
        if not user:
            user = await self._user_repository.get_by_email(login_dto.username)
        
        if not user:
            raise ValueError("Credenciales inválidas")
        
        # Verificar contraseña
        if not self._verify_password(login_dto.password, user.hashed_password):
            raise ValueError("Credenciales inválidas")
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            raise ValueError("El usuario está desactivado")
        
        # Generar respuesta
        user_response = self._user_to_response(user)
        token_response = self._create_token_response(user)
        
        return AuthResponseDTO(user=user_response, token=token_response)

    # =========================================================================
    # VERIFICACIÓN DE TOKEN
    # =========================================================================

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Obtiene el usuario actual basado en el token.
        
        Args:
            token: Token JWT
            
        Returns:
            User si el token es válido, None en caso contrario
        """
        payload = self.decode_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        try:
            user = await self._user_repository.get_by_id(int(user_id))
            if user and user.is_active:
                return user
            return None
        except (ValueError, TypeError):
            return None

    async def verify_token(self, token: str) -> Tuple[bool, Optional[UserResponseDTO]]:
        """
        Verifica si un token es válido.
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Tupla (es_válido, usuario_response)
        """
        user = await self.get_current_user(token)
        if user:
            return True, self._user_to_response(user)
        return False, None

    # =========================================================================
    # GESTIÓN DE USUARIOS (ADMIN)
    # =========================================================================

    async def get_all_users(self) -> UsersResponseDTO:
        """Obtiene todos los usuarios (solo para administradores)."""
        users = await self._user_repository.get_all()
        user_responses = [self._user_to_response(user) for user in users]
        return UsersResponseDTO(users=user_responses, total=len(user_responses))

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponseDTO]:
        """Obtiene un usuario por su ID."""
        user = await self._user_repository.get_by_id(user_id)
        if user:
            return self._user_to_response(user)
        return None

    async def update_user(self, user_id: int, update_dto: UserUpdateDTO) -> UserResponseDTO:
        """
        Actualiza un usuario.
        
        Args:
            user_id: ID del usuario a actualizar
            update_dto: Datos a actualizar
            
        Returns:
            UserResponseDTO con el usuario actualizado
            
        Raises:
            ValueError: Si el usuario no existe o el email ya está en uso
        """
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")
        
        # Actualizar campos proporcionados
        if update_dto.email is not None and update_dto.email != user.email:
            if await self._user_repository.exists_by_email(update_dto.email):
                raise ValueError(f"El correo electrónico '{update_dto.email}' ya está en uso")
            user.email = update_dto.email
        
        if update_dto.full_name is not None:
            user.full_name = update_dto.full_name
        
        if update_dto.is_active is not None:
            user.is_active = update_dto.is_active
        
        if update_dto.role is not None:
            user.role = update_dto.role
        
        updated_user = await self._user_repository.update(user)
        return self._user_to_response(updated_user)

    async def delete_user(self, user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        return await self._user_repository.delete(user_id)

    async def change_password(
        self, 
        user_id: int, 
        password_dto: PasswordChangeDTO
    ) -> bool:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            user_id: ID del usuario
            password_dto: DTO con la contraseña actual y nueva
            
        Returns:
            True si el cambio fue exitoso
            
        Raises:
            ValueError: Si la contraseña actual es incorrecta o el usuario no existe
        """
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")
        
        if not self._verify_password(password_dto.current_password, user.hashed_password):
            raise ValueError("La contraseña actual es incorrecta")
        
        user.hashed_password = self._hash_password(password_dto.new_password)
        await self._user_repository.update(user)
        return True

    async def is_first_user(self) -> bool:
        """Verifica si no hay usuarios en el sistema (para crear el primer admin)."""
        count = await self._user_repository.count()
        return count == 0
