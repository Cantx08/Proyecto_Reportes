"""
Repositorio de departamentos usando base de datos PostgreSQL.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...domain.entities.department import Department
from ...domain.value_objects.faculty import Faculty
from ...domain.repositories.department_repository import DepartmentRepository
from ..database.models.author import DepartmentModel
from ..database.models.base import FacultyEnum
from ..database.connection import DatabaseConfig


class DepartmentDatabaseRepository(DepartmentRepository):
    """Implementación del repositorio de departamentos usando PostgreSQL."""
    
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    def _to_entity(self, model: DepartmentModel) -> Department:
        """Convierte un modelo de base de datos a una entidad de dominio."""
        # Convertir FacultyEnum a Faculty (domain value object)
        faculty = Faculty[model.fac_name.name] if isinstance(model.fac_name, FacultyEnum) else Faculty.from_string(model.fac_name)
        
        return Department(
            dep_id=model.dep_id,
            dep_code=model.dep_code,
            dep_name=model.dep_name,
            fac_name=faculty
        )
    
    def _to_model(self, department: Department, model: Optional[DepartmentModel] = None) -> DepartmentModel:
        """Convierte una entidad de dominio a un modelo de base de datos."""
        if model is None:
            model = DepartmentModel()
        
        model.dep_id = department.dep_id
        model.dep_code = department.dep_code
        model.dep_name = department.dep_name
        
        # Convertir Faculty (domain) a FacultyEnum (database)
        if isinstance(department.fac_name, Faculty):
            model.fac_name = FacultyEnum[department.fac_name.name]
        else:
            model.fac_name = FacultyEnum[Faculty.from_string(department.fac_name).name]
        
        return model
    
    async def get_by_id(self, dep_id: str) -> Optional[Department]:
        """Obtiene un departamento por su ID."""
        with self.db_config.get_session() as session:
            model = session.query(DepartmentModel).filter(
                DepartmentModel.dep_id == dep_id
            ).first()
            
            if model:
                return self._to_entity(model)
            return None
    
    async def get_by_code(self, dep_code: str) -> Optional[Department]:
        """Obtiene un departamento por su código/sigla."""
        with self.db_config.get_session() as session:
            model = session.query(DepartmentModel).filter(
                DepartmentModel.dep_code == dep_code
            ).first()
            
            if model:
                return self._to_entity(model)
            return None
    
    async def get_all(self) -> List[Department]:
        """Obtiene todos los departamentos."""
        with self.db_config.get_session() as session:
            models = session.query(DepartmentModel).all()
            return [self._to_entity(model) for model in models]
    
    async def create(self, department: Department) -> Department:
        """Crea un nuevo departamento."""
        with self.db_config.get_session() as session:
            try:
                # Verificar si ya existe por dep_id
                existing = session.query(DepartmentModel).filter(
                    DepartmentModel.dep_id == department.dep_id
                ).first()
                
                if existing:
                    raise ValueError(f"Department with ID {department.dep_id} already exists")
                
                model = self._to_model(department)
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
    
    async def update(self, department: Department) -> Department:
        """Actualiza un departamento existente."""
        with self.db_config.get_session() as session:
            try:
                model = session.query(DepartmentModel).filter(
                    DepartmentModel.dep_id == department.dep_id
                ).first()
                
                if not model:
                    raise ValueError(f"Department with ID {department.dep_id} not found")
                
                self._to_model(department, model)
                session.commit()
                session.refresh(model)
                
                return self._to_entity(model)
                
            except Exception as e:
                session.rollback()
                raise
    
    async def delete(self, dep_id: str) -> bool:
        """Elimina un departamento por su ID."""
        with self.db_config.get_session() as session:
            try:
                model = session.query(DepartmentModel).filter(
                    DepartmentModel.dep_id == dep_id
                ).first()
                
                if not model:
                    return False
                
                # Verificar si tiene autores asociados
                if model.authors:
                    raise ValueError(f"Cannot delete department {model.dep_name} because it has authors associated")
                
                session.delete(model)
                session.commit()
                
                return True
                
            except Exception as e:
                session.rollback()
                raise
    
    async def get_by_faculty(self, faculty_name: str) -> List[Department]:
        """Obtiene departamentos por facultad."""
        with self.db_config.get_session() as session:
            # Convertir el string a Faculty y luego a FacultyEnum
            faculty = Faculty.from_string(faculty_name)
            faculty_enum = FacultyEnum[faculty.name]
            
            models = session.query(DepartmentModel).filter(
                DepartmentModel.fac_name == faculty_enum
            ).all()
            
            return [self._to_entity(model) for model in models]
    
    async def search_by_name(self, search_term: str) -> List[Department]:
        """Busca departamentos por nombre."""
        with self.db_config.get_session() as session:
            models = session.query(DepartmentModel).filter(
                DepartmentModel.dep_name.ilike(f"%{search_term}%")
            ).all()
            
            return [self._to_entity(model) for model in models]
