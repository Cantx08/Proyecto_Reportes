"""
Repositorio de cargos académicos usando base de datos PostgreSQL.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...domain.entities.position import Position
from ...domain.repositories.position_repository import PositionRepository
from ..database.models.position import PositionModel
from ..database.connection import DatabaseConfig


class PositionDatabaseRepository(PositionRepository):
    """Implementación del repositorio de cargos usando PostgreSQL."""
    
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    def _to_entity(self, model: PositionModel) -> Position:
        """Convierte un modelo de base de datos a una entidad de dominio."""
        return Position(
            pos_id=str(model.id),
            pos_name=model.name
        )
    
    def _to_model(self, position: Position, model: Optional[PositionModel] = None) -> PositionModel:
        """Convierte una entidad de dominio a un modelo de base de datos."""
        if model is None:
            model = PositionModel()
        
        # Solo asignar el ID si ya existe en el modelo (para updates)
        # Para creates, el ID es autogenerado por la base de datos
        if model.id is None and position.pos_id and position.pos_id.isdigit():
            model.id = int(position.pos_id)
        
        model.name = position.pos_name
        
        return model
    
    async def get_by_id(self, pos_id: str) -> Optional[Position]:
        """Obtiene un cargo por su ID."""
        # Verificar que el pos_id sea numérico
        if not pos_id or not pos_id.isdigit():
            return None
            
        with self.db_config.get_session() as session:
            model = session.query(PositionModel).filter(
                PositionModel.id == int(pos_id)
            ).first()
            
            if model:
                return self._to_entity(model)
            return None
    
    async def get_all(self) -> List[Position]:
        """Obtiene todos los cargos."""
        with self.db_config.get_session() as session:
            models = session.query(PositionModel).all()
            return [self._to_entity(model) for model in models]
    
    async def create(self, position: Position) -> Position:
        """Crea un nuevo cargo."""
        with self.db_config.get_session() as session:
            try:
                # Verificar si ya existe
                existing = session.query(PositionModel).filter(
                    PositionModel.name == position.pos_name
                ).first()
                
                if existing:
                    raise ValueError(f"Position {position.pos_name} already exists")
                
                model = self._to_model(position)
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
    
    async def update(self, position: Position) -> Position:
        """Actualiza un cargo existente."""
        if not position.pos_id or not position.pos_id.isdigit():
            raise ValueError(f"Invalid position ID: {position.pos_id}")
            
        with self.db_config.get_session() as session:
            try:
                model = session.query(PositionModel).filter(
                    PositionModel.id == int(position.pos_id)
                ).first()
                
                if not model:
                    raise ValueError(f"Position with ID {position.pos_id} not found")
                
                self._to_model(position, model)
                session.commit()
                session.refresh(model)
                
                return self._to_entity(model)
                
            except Exception as e:
                session.rollback()
                raise
    
    async def delete(self, pos_id: str) -> bool:
        """Elimina un cargo por su ID."""
        if not pos_id or not pos_id.isdigit():
            raise ValueError(f"Invalid position ID: {pos_id}")
            
        with self.db_config.get_session() as session:
            try:
                model = session.query(PositionModel).filter(
                    PositionModel.id == int(pos_id)
                ).first()
                
                if not model:
                    return False
                
                # Verificar si tiene autores asociados
                if model.authors:
                    raise ValueError(f"Cannot delete position {model.name} because it has authors associated")
                
                session.delete(model)
                session.commit()
                
                return True
                
            except Exception as e:
                session.rollback()
                raise
    
    async def get_by_name(self, pos_name: str) -> List[Position]:
        """Busca cargos por nombre."""
        with self.db_config.get_session() as session:
            models = session.query(PositionModel).filter(
                PositionModel.name.ilike(f"%{pos_name}%")
            ).all()
            
            return [self._to_entity(model) for model in models]
