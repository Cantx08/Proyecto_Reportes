"""
Repositorio de autores usando base de datos PostgreSQL.
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...domain.entities.author import Author
from ...domain.repositories.author_repository import AuthorRepository
from ..database.models.author import AuthorModel
from ..database.connection import DatabaseConfig


class AuthorDatabaseRepository(AuthorRepository):
    """Implementación del repositorio de autores usando PostgreSQL."""
    
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    def _to_entity(self, model: AuthorModel) -> Author:
        """Convierte un modelo de base de datos a una entidad de dominio."""
        return Author(
            author_id=str(model.id),
            name=model.first_name,
            surname=model.last_name,
            dni=model.dni or '',
            title=model.title or '',
            birth_date=model.birth_date,
            gender=model.gender.name if model.gender else 'M',  # Usar .name para obtener "M" o "F"
            position=model.position_rel.name if model.position_rel else '',
            department=model.department.dep_name if model.department else ''
        )
    
    def _to_model(self, author: Author, model: Optional[AuthorModel] = None) -> AuthorModel:
        """Convierte una entidad de dominio a un modelo de base de datos."""
        if model is None:
            model = AuthorModel()
        
        # Si el author_id es numérico, úsalo; de lo contrario, déjalo como None para que la BD lo genere
        if author.author_id and author.author_id.isdigit():
            model.id = int(author.author_id)
        
        model.dni = author.dni
        model.first_name = author.name
        model.last_name = author.surname
        model.title = author.title
        model.birth_date = author.birth_date
        model.gender = author.gender
        # position_id se manejará por separado en create/update
        # department se manejará por separado
        
        return model
    
    async def get_by_id(self, author_id: str) -> Optional[Author]:
        """Obtiene un autor por su ID."""
        with self.db_config.get_session() as session:
            model = session.query(AuthorModel).filter(
                AuthorModel.id == int(author_id)
            ).first()
            
            if model:
                return self._to_entity(model)
            return None
    
    async def get_all(self) -> List[Author]:
        """Obtiene todos los autores."""
        with self.db_config.get_session() as session:
            models = session.query(AuthorModel).filter(
                AuthorModel.is_active == True
            ).all()
            
            return [self._to_entity(model) for model in models]
    
    async def create(self, author: Author) -> Author:
        """Crea un nuevo autor."""
        with self.db_config.get_session() as session:
            try:
                # Verificar si ya existe un autor con ese DNI
                existing = session.query(AuthorModel).filter(
                    AuthorModel.dni == author.dni
                ).first()
                
                if existing:
                    raise ValueError(f"Author with DNI {author.dni} already exists")
                
                model = self._to_model(author)
                
                # Buscar o crear departamento
                if author.department:
                    from ..database.models import DepartmentModel
                    dept = session.query(DepartmentModel).filter(
                        DepartmentModel.dep_name == author.department
                    ).first()
                    
                    if not dept:
                        # Si no existe, crear uno nuevo con valores por defecto
                        dept = DepartmentModel(
                            dep_id=f"DEP-{author.department[:3].upper()}",
                            dep_code=author.department[:3].upper(),
                            dep_name=author.department,
                            fac_name="Facultad por Definir"
                        )
                        session.add(dept)
                        session.flush()
                    
                    model.department_id = dept.id
                
                # Buscar o crear cargo
                if author.position:
                    from ..database.models.position import PositionModel
                    pos = session.query(PositionModel).filter(
                        PositionModel.name == author.position
                    ).first()
                    
                    if not pos:
                        pos = PositionModel(name=author.position)
                        session.add(pos)
                        session.flush()
                    
                    model.position_id = pos.id
                
                session.add(model)
                session.commit()
                session.refresh(model)
                
                return self._to_entity(model)
                
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Database integrity error: {str(e)}")
            except Exception as e:
                session.rollback()
                raise
    
    async def update(self, author: Author) -> Author:
        """Actualiza un autor existente."""
        with self.db_config.get_session() as session:
            try:
                model = session.query(AuthorModel).filter(
                    AuthorModel.id == int(author.author_id)
                ).first()
                
                if not model:
                    raise ValueError(f"Author with ID {author.author_id} not found")
                
                # Actualizar campos
                self._to_model(author, model)
                
                # Actualizar departamento
                if author.department:
                    from ..database.models import DepartmentModel
                    dept = session.query(DepartmentModel).filter(
                        DepartmentModel.dep_name == author.department
                    ).first()
                    
                    if not dept:
                        # Si no existe, crear uno nuevo con valores por defecto
                        dept = DepartmentModel(
                            dep_id=f"DEP-{author.department[:3].upper()}",
                            dep_code=author.department[:3].upper(),
                            dep_name=author.department,
                            fac_name="Facultad por Definir"
                        )
                        session.add(dept)
                        session.flush()
                    
                    model.department_id = dept.id
                
                # Actualizar cargo
                if author.position:
                    from ..database.models.position import PositionModel
                    pos = session.query(PositionModel).filter(
                        PositionModel.name == author.position
                    ).first()
                    
                    if not pos:
                        pos = PositionModel(name=author.position)
                        session.add(pos)
                        session.flush()
                    
                    model.position_id = pos.id
                
                session.commit()
                session.refresh(model)
                
                return self._to_entity(model)
                
            except Exception as e:
                session.rollback()
                raise
    
    async def delete(self, author_id: str) -> bool:
        """Elimina un autor por su ID (soft delete)."""
        with self.db_config.get_session() as session:
            try:
                model = session.query(AuthorModel).filter(
                    AuthorModel.id == int(author_id)
                ).first()
                
                if not model:
                    return False
                
                # Soft delete
                model.is_active = False
                session.commit()
                
                return True
                
            except Exception as e:
                session.rollback()
                raise
    
    async def get_by_department(self, department: str) -> List[Author]:
        """Obtiene autores por departamento."""
        with self.db_config.get_session() as session:
            from ..database.models import DepartmentModel

            models = session.query(AuthorModel).join(
                DepartmentModel
            ).filter(
                DepartmentModel.dep_name.ilike(f"%{department}%"),
                AuthorModel.is_active == True
            ).all()
            
            return [self._to_entity(model) for model in models]
    
    async def get_by_position(self, position: str) -> List[Author]:
        """Obtiene autores por cargo."""
        with self.db_config.get_session() as session:
            models = session.query(AuthorModel).filter(
                AuthorModel.position.ilike(f"%{position}%"),
                AuthorModel.is_active == True
            ).all()
            
            return [self._to_entity(model) for model in models]
    
    async def search_by_name(self, search_term: str) -> List[Author]:
        """Busca autores por nombre o apellido."""
        with self.db_config.get_session() as session:
            models = session.query(AuthorModel).filter(
                (AuthorModel.first_name.ilike(f"%{search_term}%") |
                 AuthorModel.last_name.ilike(f"%{search_term}%")),
                AuthorModel.is_active == True
            ).all()
            
            return [self._to_entity(model) for model in models]
