from typing import List, Optional
from sqlalchemy.orm import Session

from ...domain.entities.scopus_account import ScopusAccount
from ...domain.repositories.scopus_account_repository import ScopusAccountRepository
from ..database.models.author import ScopusAccountModel
from ..database.connection import DatabaseConfig


class ScopusAccountDBRepository(ScopusAccountRepository):
    """Repositorio de base de datos para cuentas Scopus."""
    
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    def _get_session(self) -> Session:
        """Obtiene una nueva sesión de base de datos."""
        return self.db_config.SessionLocal()
    
    def _to_entity(self, model: ScopusAccountModel) -> ScopusAccount:
        """Convierte un modelo de base de datos a entidad de dominio."""
        return ScopusAccount(
            scopus_id=model.scopus_id,
            author_id=str(model.author_id),
            is_active=model.is_active
        )
    
    def _to_model(self, entity: ScopusAccount, model: Optional[ScopusAccountModel] = None) -> ScopusAccountModel:
        """Convierte una entidad de dominio a modelo de base de datos."""
        if model is None:
            model = ScopusAccountModel()
        
        model.scopus_id = entity.scopus_id
        model.author_id = int(entity.author_id)
        model.is_active = entity.is_active
        
        return model
    
    async def get_by_scopus_id(self, scopus_id: str) -> Optional[ScopusAccount]:
        """Obtiene una cuenta Scopus por su ID de Scopus."""
        session = self._get_session()
        try:
            model = session.query(ScopusAccountModel).filter(
                ScopusAccountModel.scopus_id == scopus_id
            ).first()
            
            return self._to_entity(model) if model else None
        finally:
            session.close()
    
    async def get_by_author_id(self, author_id: str) -> List[ScopusAccount]:
        """Obtiene todas las cuentas Scopus de un autor."""
        session = self._get_session()
        try:
            models = session.query(ScopusAccountModel).filter(
                ScopusAccountModel.author_id == int(author_id)
            ).order_by(ScopusAccountModel.created_at).all()
            
            return [self._to_entity(model) for model in models]
        finally:
            session.close()
    
    async def get_all(self) -> List[ScopusAccount]:
        """Obtiene todas las cuentas Scopus."""
        session = self._get_session()
        try:
            models = session.query(ScopusAccountModel).order_by(
                ScopusAccountModel.author_id, 
                ScopusAccountModel.created_at
            ).all()
            
            return [self._to_entity(model) for model in models]
        finally:
            session.close()
    
    async def create(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """Crea una nueva cuenta Scopus."""
        session = self._get_session()
        try:
            # Verificar si ya existe
            existing = session.query(ScopusAccountModel).filter(
                ScopusAccountModel.scopus_id == scopus_account.scopus_id
            ).first()
            
            if existing:
                raise ValueError(f"Scopus account with ID {scopus_account.scopus_id} already exists")
            
            model = self._to_model(scopus_account)
            session.add(model)
            session.commit()
            session.refresh(model)
            
            return self._to_entity(model)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    async def update(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """Actualiza una cuenta Scopus existente."""
        session = self._get_session()
        try:
            model = session.query(ScopusAccountModel).filter(
                ScopusAccountModel.scopus_id == scopus_account.scopus_id
            ).first()
            
            if not model:
                raise ValueError(f"Scopus account with ID {scopus_account.scopus_id} not found")
            
            model = self._to_model(scopus_account, model)
            session.commit()
            session.refresh(model)
            
            return self._to_entity(model)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    async def delete(self, scopus_id: str) -> bool:
        """Elimina una cuenta Scopus por su ID de Scopus."""
        session = self._get_session()
        try:
            result = session.query(ScopusAccountModel).filter(
                ScopusAccountModel.scopus_id == scopus_id
            ).delete()
            session.commit()
            
            return result > 0
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    async def delete_by_author_id(self, author_id: str) -> bool:
        """Elimina todas las cuentas Scopus de un autor."""
        session = self._get_session()
        try:
            result = session.query(ScopusAccountModel).filter(
                ScopusAccountModel.author_id == int(author_id)
            ).delete()
            session.commit()
            
            return result > 0
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
