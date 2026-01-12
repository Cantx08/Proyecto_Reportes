"""
Implementación del Repositorio de departamentos.
"""

from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...domain.entities.department import Department
from ...domain.enums.faculty import Faculty
from ...domain.exceptions import DepartmentAlreadyExists, CannotDeleteDepartment
from ...domain.repositories.department_repository import IDepartmentRepository
from ..database.models import DepartmentModel
from ..database.models.base import FacultyEnum
from ..database.connection import DatabaseConfig


class DBDepartmentRepository(IDepartmentRepository):
    """Implementación del repositorio de departamentos para la base de datos."""

    def __init__(self, db_config: DatabaseConfig):
        """
        Inicializa el repositorio con la configuración de base de datos.

        Args:
            db_config: Configuración de la base de datos.
        """
        self.db_config = db_config

    @staticmethod
    def _to_entity(dep_model: DepartmentModel) -> Department:
        """
        Convierte el modelo a la entidad departamento.
        """
        # Convertir FacultyEnum (BD) a Faculty (dominio)
        faculty = Faculty[dep_model.fac_name.name] if dep_model.fac_name else Faculty.DESCONOCIDA
        
        return Department(
            dep_id=dep_model.id,
            dep_code=dep_model.dep_code,
            dep_name=dep_model.dep_name,
            fac_name=faculty
        )

    @staticmethod
    def _to_model(dep_entity: Department,
                  dep_model: Optional[DepartmentModel] = None
                  ) -> DepartmentModel:
        """
        Convierte la entidad al modelo de la tabla departamentos.
        """
        if not dep_model:
            dep_model = DepartmentModel()

        if dep_entity.dep_id:
            dep_model.id = dep_entity.dep_id

        dep_model.dep_code = dep_entity.dep_code
        dep_model.dep_name = dep_entity.dep_name
        
        # Convertir Faculty (dominio) a FacultyEnum (BD)
        if isinstance(dep_entity.fac_name, Faculty):
            dep_model.fac_name = FacultyEnum[dep_entity.fac_name.name]
        elif isinstance(dep_entity.fac_name, str):
            dep_model.fac_name = FacultyEnum[dep_entity.fac_name]
        else:
            dep_model.fac_name = dep_entity.fac_name

        return dep_model

    async def create(self, department: Department) -> Department:
        """Crea un nuevo departamento."""
        with self.db_config.get_session() as session:
            try:
                model = self._to_model(department)
                session.add(model)
                session.flush()
                session.refresh(model)
                return self._to_entity(model)

            except IntegrityError as e:
                session.rollback()
                raise DepartmentAlreadyExists(dep_code=department.dep_code) from e

    async def get_all(self) -> List[Department]:
        """Obtiene todos los departamentos."""
        with self.db_config.get_session() as session:
            models = session.query(DepartmentModel).order_by(
                DepartmentModel.dep_name
            ).all()
            return [self._to_entity(model) for model in models]

    async def get_by_id(self, dep_id: int) -> Optional[Department]:
        """Obtiene un departamento por su ID."""
        with self.db_config.get_session() as session:
            model = session.query(DepartmentModel).filter(
                DepartmentModel.id == dep_id
            ).first()
            return self._to_entity(model) if model else None

    async def get_by_code(self, dep_code: str) -> Optional[Department]:
        """Obtiene un departamento por su sigla."""
        with self.db_config.get_session() as session:
            model = session.query(DepartmentModel).filter(
                DepartmentModel.dep_code == dep_code.upper()
            ).first()
            return self._to_entity(model) if model else None

    async def get_by_name(self, dep_name: str) -> Optional[Department]:
        """Obtiene un departamento por su nombre."""
        with self.db_config.get_session() as session:
            model = session.query(DepartmentModel).filter(
                DepartmentModel.dep_name == dep_name
            ).first()
            return self._to_entity(model) if model else None

    async def filter_by_faculty(self, faculty: Faculty) -> List[Department]:
        """Filtra departamentos por facultad."""
        with self.db_config.get_session() as session:
            models = session.query(DepartmentModel).filter(
                DepartmentModel.fac_name == faculty
            ).all()
            return [self._to_entity(model) for model in models]

    async def update(self, department: Department) -> Department:
        """Actualiza un departamento existente."""
        with self.db_config.get_session() as session:
            try:
                model = session.query(DepartmentModel).filter(
                    DepartmentModel.id == department.dep_id
                ).first()
                
                if not model:
                    raise ValueError(f"Departamento con ID {department.dep_id} no encontrado")
                
                model = self._to_model(department, model)
                session.flush()
                session.refresh(model)
                return self._to_entity(model)
                
            except IntegrityError as e:
                session.rollback()
                raise DepartmentAlreadyExists(dep_code=department.dep_code) from e

    async def delete(self, dep_id: int) -> bool:
        """Elimina un departamento por su ID."""
        with self.db_config.get_session() as session:
            try:
                model = session.query(DepartmentModel).filter(
                    DepartmentModel.id == dep_id
                ).first()
                
                if model:
                    session.delete(model)
                    session.flush()
                    return True
                return False
                
            except IntegrityError as e:
                session.rollback()
                raise CannotDeleteDepartment(
                    dep_id=dep_id,
                    reason="El departamento tiene autores vinculados al departamento."
                ) from e

    async def search_by_name(self, search_term: str) -> List[Department]:
        """Busca departamentos por nombre."""
        with self.db_config.get_session() as session:
            models = session.query(DepartmentModel).filter(
                DepartmentModel.dep_name.ilike(f"%{search_term}%")
            ).all()
            return [self._to_entity(model) for model in models]
