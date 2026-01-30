from typing import List, Optional

from sqlalchemy import UUID
from sqlalchemy.orm import Session

from ..domain.department import Department
from ..domain.department_repository import IDepartmentRepository
from .department import DepartmentModel
from ..domain.faculty import Faculty


class DBDepartmentRepository(IDepartmentRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self) -> List[Department]:
        models = self.db.query(DepartmentModel).all()
        return [model.to_entity() for model in models]

    async def get_by_faculty(self, faculty: Faculty) -> List[Department]:
        models = self.db.query(DepartmentModel).filter(DepartmentModel.faculty == faculty).all()
        return [model.to_entity() for model in models]

    async def get_by_id(self, dep_id: UUID) -> Optional[Department]:
        dept = self.db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
        return dept.to_entity() if dept else None

    async def create(self, department: Department) -> Department:
        model = DepartmentModel(
            dep_id=department.dep_id,
            dep_name=department.dep_name,
            dep_code=department.dep_code,
            faculty=department.faculty
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    async def update(self, dep_id: UUID, department: Department) -> Department:
        model = self.db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
        if not model:
            raise ValueError(f"El departamento no fue encontrado.")
        model.dep_name = department.dep_name
        model.dep_code = department.dep_code
        model.faculty = department.faculty

        try:
            self.db.commit()
            self.db.refresh(model)
            return model.to_entity()
        except Exception:
            self.db.rollback()
            raise

    async def delete(self, dep_id: UUID) -> bool:
        dept = self.db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
        if dept:
            self.db.delete(dept)
            self.db.commit()
            return True
        return False
