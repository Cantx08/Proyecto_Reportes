import uuid
from sqlalchemy import Column, UUID, String

from backend.src.shared.database import Base

from ..domain.job_position import JobPosition


class JobPositionModel(Base):
    __tablename__ = "positions"

    pos_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    pos_name = Column(String, unique=True, nullable=False)

    def to_entity(self) -> JobPosition:
        return JobPosition(
            pos_id=self.pos_id,
            pos_name=self.pos_name
        )
