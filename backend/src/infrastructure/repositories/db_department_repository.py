"""
Implementación del Repositorio de departamentos.
"""

from typing import List, Optional

from mako.testing.helpers import result_lines
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from ...domain.entities.department import Department
from ...domain.enums.faculty import Faculty
from ...domain.exceptions import DepartmentAlreadyExists, CannotDeleteDepartment
from ...domain.repositories.department_repository import IDepartmentRepository
from ..database.models import DepartmentModel
from ..database.connection import DatabaseConfig


class DBDepartmentRepository(IDepartmentRepository):
    """Implementación del repositorio de departamentos para la base de datos."""

    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            session: Una sesión de SQLAlchemy.
        """
        self._session = session

    @staticmethod
    def _to_entity(dep_model: DepartmentModel) -> Department:
        """
        Convierte el modelo a la entidad departamento.
        """

        return Department(
            dep_id=dep_model.id,
            dep_code=dep_model.dep_code,
            dep_name=dep_model.dep_name,
            fac_name=dep_model.fac_name
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
        dep_model.fac_name = dep_entity.fac_name

        return dep_model

    async def create(self, department: Department) -> Department:
        """Crea un nuevo departamento."""
        try:
            model = self._to_model(department)
            self._session.add(model)
            await self._session.flush()
            await self._session.refresh(model)

            return self._to_entity(model)

        except IntegrityError as e:
            await self._session.rollback()
            raise DepartmentAlreadyExists(dep_code=department.dep_code) from e
        except Exception:
            await self._session.rollback()
            raise

    async def get_all(self) -> List[Department]:
        """Obtiene todos los departamentos."""
        select_query = select(DepartmentModel).order_by(DepartmentModel.dep_name)
        result = await self._session.execute(select_query)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_by_id(self, dep_id: int) -> Optional[Department]:
        """Obtiene un departamento por su ID."""
        model = await self._session.get(DepartmentModel, dep_id)
        return self._to_entity(model) if model else None

    async def get_by_code(self, dep_code: str) -> Optional[Department]:
        """Obtiene un departamento por su sigla."""
        select_query = select(DepartmentModel).where(DepartmentModel.dep_code == dep_code.upper())
        result = await self._session.execute(select_query)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_name(self, dep_name: str) -> Optional[Department]:
        """Obtiene un departamento por su nombre."""
        select_query = select(DepartmentModel).where(DepartmentModel.dep_name == dep_name)
        result = await self._session.execute(select_query)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def filter_by_faculty(self, faculty: Faculty) -> List[Department]:
        """Filtra departamentos por facultad."""
        select_query = select(DepartmentModel).where(DepartmentModel.fac_name == faculty)
        result = await self._session.execute(select_query)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, department: Department) -> Department:
        """Actualiza un departamento existente."""
        try:
            model = await self._session.get(DepartmentModel, department.dep_id)
            if not model:
                raise NoResultFound
            model = self._to_model(department, model)

            await self._session.flush()
            await self._session.refresh(model)

            return self._to_entity(model)
        except IntegrityError as e:
            await self._session.rollback()
            raise DepartmentAlreadyExists(dep_code=department.dep_code) from e
        except Exception:
            await self._session.rollback()
            raise

    async def delete(self, dep_id: int) -> bool:
        """Elimina un departamento por su ID."""
        try:
            model = await self._session.get(DepartmentModel, dep_id)
            if model:
                await self._session.delete(model)
                await self._session.flush()
                return True
            return False
        except IntegrityError as e:
            await self._session.rollback()
            raise CannotDeleteDepartment(
                dep_id=dep_id,
                reason="El departamento tiene autores vinculados al departamento."
            ) from e
        except Exception:
            await self._session.rollback()
            raise

    async def search_by_name(self, search_term: str) -> List[Department]:
        """Busca departamentos por nombre."""
        with self.db_config.get_session() as session:
            models = session.query(DepartmentModel).filter(
                DepartmentModel.dep_name.ilike(f"%{search_term}%")
            ).all()

            return [self._to_entity(model) for model in models]
