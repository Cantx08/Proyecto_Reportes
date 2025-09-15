"""
Implementación del repositorio de autores usando SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_

from ...domain.entities.author import Author
from ...domain.repositories.author_repository import AuthorRepository
from ...domain.value_objects.scopus_id import ScopusId
from ...domain.value_objects.email import Email
from ..database.models import AuthorModel, ScopusAccountModel, DepartmentModel
from ..database.connection import db_config


class SQLAlchemyAuthorRepository(AuthorRepository):
    """Implementación del repositorio de autores usando SQLAlchemy."""
    
    def __init__(self, session: Optional[Session] = None):
        self._session = session
    
    @property
    def session(self) -> Session:
        """Obtiene la sesión de base de datos."""
        if self._session is None:
            self._session = db_config.get_session_sync()
        return self._session
    
    def save(self, author: Author) -> Author:
        """Guarda un autor en la base de datos."""
        # Verificar si existe
        existing = self.session.query(AuthorModel).filter(
            AuthorModel.dni == author.dni
        ).first()
        
        if existing:
            # Actualizar existente
            self._update_author_model(existing, author)
            author_model = existing
        else:
            # Crear nuevo
            author_model = self._create_author_model(author)
            self.session.add(author_model)
        
        self.session.commit()
        self.session.refresh(author_model)
        
        return self._map_to_domain(author_model)
    
    def find_by_dni(self, dni: str) -> Optional[Author]:
        """Busca un autor por DNI."""
        author_model = self.session.query(AuthorModel).options(
            joinedload(AuthorModel.scopus_accounts),
            joinedload(AuthorModel.department)
        ).filter(AuthorModel.dni == dni).first()
        
        if not author_model:
            return None
        
        return self._map_to_domain(author_model)
    
    def find_by_scopus_id(self, scopus_id: ScopusId) -> Optional[Author]:
        """Busca un autor por Scopus ID."""
        author_model = self.session.query(AuthorModel).join(
            ScopusAccountModel
        ).options(
            joinedload(AuthorModel.scopus_accounts),
            joinedload(AuthorModel.department)
        ).filter(
            ScopusAccountModel.scopus_id == str(scopus_id)
        ).first()
        
        if not author_model:
            return None
        
        return self._map_to_domain(author_model)
    
    def find_by_email(self, email: Email) -> Optional[Author]:
        """Busca un autor por email."""
        author_model = self.session.query(AuthorModel).options(
            joinedload(AuthorModel.scopus_accounts),
            joinedload(AuthorModel.department)
        ).filter(AuthorModel.email == str(email)).first()
        
        if not author_model:
            return None
        
        return self._map_to_domain(author_model)
    
    def find_by_department(self, department_id: int) -> List[Author]:
        """Busca autores por departamento."""
        author_models = self.session.query(AuthorModel).options(
            joinedload(AuthorModel.scopus_accounts),
            joinedload(AuthorModel.department)
        ).filter(AuthorModel.department_id == department_id).all()
        
        return [self._map_to_domain(model) for model in author_models]
    
    def search_by_name(self, name_query: str) -> List[Author]:
        """Busca autores por nombre (búsqueda parcial)."""
        search_term = f"%{name_query.lower()}%"
        
        author_models = self.session.query(AuthorModel).options(
            joinedload(AuthorModel.scopus_accounts),
            joinedload(AuthorModel.department)
        ).filter(
            or_(
                AuthorModel.first_name.ilike(search_term),
                AuthorModel.last_name.ilike(search_term),
                (AuthorModel.first_name + ' ' + AuthorModel.last_name).ilike(search_term)
            )
        ).all()
        
        return [self._map_to_domain(model) for model in author_models]
    
    def find_all(self) -> List[Author]:
        """Obtiene todos los autores."""
        author_models = self.session.query(AuthorModel).options(
            joinedload(AuthorModel.scopus_accounts),
            joinedload(AuthorModel.department)
        ).all()
        
        return [self._map_to_domain(model) for model in author_models]
    
    def delete(self, dni: str) -> bool:
        """Elimina un autor por DNI."""
        author_model = self.session.query(AuthorModel).filter(
            AuthorModel.dni == dni
        ).first()
        
        if not author_model:
            return False
        
        self.session.delete(author_model)
        self.session.commit()
        return True
    
    def _create_author_model(self, author: Author) -> AuthorModel:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""
        author_model = AuthorModel(
            dni=author.dni,
            first_name=author.first_name,
            last_name=author.last_name,
            email=str(author.email),
            department_id=author.department_id,
            is_active=author.is_active,
            created_at=author.created_at,
            updated_at=author.updated_at
        )
        
        # Crear cuentas de Scopus
        for scopus_account in author.scopus_accounts:
            scopus_model = ScopusAccountModel(
                scopus_id=str(scopus_account.scopus_id),
                is_primary=scopus_account.is_primary,
                is_active=scopus_account.is_active,
                verified_at=scopus_account.verified_at,
                created_at=scopus_account.created_at
            )
            author_model.scopus_accounts.append(scopus_model)
        
        return author_model
    
    def _update_author_model(self, author_model: AuthorModel, author: Author):
        """Actualiza un modelo existente con datos de la entidad de dominio."""
        author_model.first_name = author.first_name
        author_model.last_name = author.last_name
        author_model.email = str(author.email)
        author_model.department_id = author.department_id
        author_model.is_active = author.is_active
        author_model.updated_at = author.updated_at
        
        # Actualizar cuentas de Scopus
        existing_scopus_ids = {account.scopus_id for account in author_model.scopus_accounts}
        new_scopus_ids = {str(account.scopus_id) for account in author.scopus_accounts}
        
        # Eliminar cuentas que ya no existen
        for scopus_model in list(author_model.scopus_accounts):
            if scopus_model.scopus_id not in new_scopus_ids:
                author_model.scopus_accounts.remove(scopus_model)
        
        # Agregar o actualizar cuentas
        for scopus_account in author.scopus_accounts:
            scopus_id_str = str(scopus_account.scopus_id)
            existing_model = None
            
            for scopus_model in author_model.scopus_accounts:
                if scopus_model.scopus_id == scopus_id_str:
                    existing_model = scopus_model
                    break
            
            if existing_model:
                # Actualizar existente
                existing_model.is_primary = scopus_account.is_primary
                existing_model.is_active = scopus_account.is_active
                existing_model.verified_at = scopus_account.verified_at
            else:
                # Crear nuevo
                new_scopus_model = ScopusAccountModel(
                    scopus_id=scopus_id_str,
                    is_primary=scopus_account.is_primary,
                    is_active=scopus_account.is_active,
                    verified_at=scopus_account.verified_at,
                    created_at=scopus_account.created_at
                )
                author_model.scopus_accounts.append(new_scopus_model)
    
    def _map_to_domain(self, author_model: AuthorModel) -> Author:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""
        from ...domain.entities.scopus_account import ScopusAccount
        
        # Crear cuentas de Scopus
        scopus_accounts = []
        for scopus_model in author_model.scopus_accounts:
            scopus_account = ScopusAccount(
                scopus_id=ScopusId(scopus_model.scopus_id),
                is_primary=scopus_model.is_primary,
                is_active=scopus_model.is_active,
                verified_at=scopus_model.verified_at,
                created_at=scopus_model.created_at
            )
            scopus_accounts.append(scopus_account)
        
        return Author(
            dni=author_model.dni,
            first_name=author_model.first_name,
            last_name=author_model.last_name,
            email=Email(author_model.email),
            department_id=author_model.department_id,
            scopus_accounts=scopus_accounts,
            is_active=author_model.is_active,
            created_at=author_model.created_at,
            updated_at=author_model.updated_at
        )