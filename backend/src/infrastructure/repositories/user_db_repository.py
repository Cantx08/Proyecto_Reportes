"""
Implementación del repositorio de usuarios con SQLAlchemy.

Este módulo proporciona la implementación concreta del repositorio de usuarios
utilizando SQLAlchemy como ORM.
"""

from typing import List, Optional

from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.connection import DatabaseConfig
from src.infrastructure.database.models.user import UserModel, RoleEnum


class UserDatabaseRepository(UserRepository):
    """
    Implementación del repositorio de usuarios con PostgreSQL.
    
    Utiliza SQLAlchemy para la persistencia de usuarios en la base de datos.
    """

    def __init__(self, db_config: DatabaseConfig):
        """
        Inicializa el repositorio.
        
        Args:
            db_config: Configuración de la base de datos
        """
        self._db_config = db_config

    def _model_to_entity(self, model: UserModel) -> User:
        """
        Convierte un modelo SQLAlchemy a entidad de dominio.
        
        Args:
            model: Modelo de SQLAlchemy
            
        Returns:
            Entidad User de dominio
        """
        return User(
            user_id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            role=Role(model.role.value),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _entity_to_model(self, entity: User) -> UserModel:
        """
        Convierte una entidad de dominio a modelo SQLAlchemy.
        
        Args:
            entity: Entidad User de dominio
            
        Returns:
            Modelo SQLAlchemy UserModel
        """
        model = UserModel(
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            full_name=entity.full_name,
            role=RoleEnum(entity.role.value),
            is_active=entity.is_active
        )
        if entity.user_id:
            model.id = entity.user_id
        return model

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        with self._db_config.get_session() as session:
            model = session.query(UserModel).filter(UserModel.id == user_id).first()
            if model:
                return self._model_to_entity(model)
            return None

    async def get_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por su nombre de usuario."""
        with self._db_config.get_session() as session:
            model = session.query(UserModel).filter(UserModel.username == username).first()
            if model:
                return self._model_to_entity(model)
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su correo electrónico."""
        with self._db_config.get_session() as session:
            model = session.query(UserModel).filter(UserModel.email == email).first()
            if model:
                return self._model_to_entity(model)
            return None

    async def get_all(self) -> List[User]:
        """Obtiene todos los usuarios."""
        with self._db_config.get_session() as session:
            models = session.query(UserModel).order_by(UserModel.id).all()
            return [self._model_to_entity(model) for model in models]

    async def create(self, user: User) -> User:
        """Crea un nuevo usuario."""
        with self._db_config.get_session() as session:
            model = UserModel(
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                full_name=user.full_name,
                role=RoleEnum(user.role.value),
                is_active=user.is_active
            )
            session.add(model)
            session.flush()
            session.refresh(model)
            return self._model_to_entity(model)

    async def update(self, user: User) -> User:
        """Actualiza un usuario existente."""
        with self._db_config.get_session() as session:
            model = session.query(UserModel).filter(UserModel.id == user.user_id).first()
            if not model:
                raise ValueError(f"Usuario con ID {user.user_id} no encontrado")
            
            model.username = user.username
            model.email = user.email
            model.hashed_password = user.hashed_password
            model.full_name = user.full_name
            model.role = RoleEnum(user.role.value)
            model.is_active = user.is_active
            
            session.flush()
            session.refresh(model)
            return self._model_to_entity(model)

    async def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        with self._db_config.get_session() as session:
            model = session.query(UserModel).filter(UserModel.id == user_id).first()
            if model:
                session.delete(model)
                return True
            return False

    async def exists_by_username(self, username: str) -> bool:
        """Verifica si existe un usuario con el nombre de usuario dado."""
        with self._db_config.get_session() as session:
            count = session.query(UserModel).filter(UserModel.username == username).count()
            return count > 0

    async def exists_by_email(self, email: str) -> bool:
        """Verifica si existe un usuario con el correo electrónico dado."""
        with self._db_config.get_session() as session:
            count = session.query(UserModel).filter(UserModel.email == email).count()
            return count > 0

    async def count(self) -> int:
        """Cuenta el total de usuarios."""
        with self._db_config.get_session() as session:
            return session.query(UserModel).count()
