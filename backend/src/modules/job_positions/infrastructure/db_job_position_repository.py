from typing import List
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from .job_position import JobPositionModel
from ..domain.job_position import JobPosition
from ..domain.job_position_repository import IJobPositionRepository


class DBJobPositionRepository(IJobPositionRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self) -> List[JobPosition]:
        models = self.db.query(JobPositionModel).all()
        return [m.to_entity() for m in models]

    async def get_by_id(self, pos_id: UUID) -> JobPosition:
        job_pos = self.db.query(JobPositionModel).filter(JobPositionModel.pos_id == pos_id).first()
        return job_pos.to_entity() if job_pos else None

    async def create(self, position: JobPosition) -> JobPosition:
        model = JobPositionModel(
            pos_id=position.pos_id,
            pos_name=position.pos_name
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    async def update(self, pos_id: UUID, position: JobPosition) -> JobPosition:
        model = self.db.query(JobPositionModel).filter(JobPositionModel.pos_id == pos_id).first()
        if not model:
            raise ValueError(f"El cargo no fue encontrado.")
        model.pos_name = position.pos_name

        try:
            self.db.commit()
            self.db.refresh(model)
            return model.to_entity()
        except Exception:
            self.db.rollback()
            raise

    async def delete(self, pos_id: UUID) -> bool:
        job_pos = self.db.query(JobPositionModel).filter(JobPositionModel.pos_id == pos_id).first()
        if job_pos:
            self.db.delete(job_pos)
            self.db.commit()
            return True
        return False
