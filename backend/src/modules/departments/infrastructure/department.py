import uuid
from sqlalchemy import Column, UUID, String, Enum

from backend.src.shared.database import Base

from ..domain.department import Department
from ..domain.faculty import Faculty


class DepartmentModel(Base):
    __tablename__ = "departments"

    dep_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dep_name = Column(String, nullable=False)
    dep_code = Column(String, nullable=False)
    faculty = Column(Enum(Faculty), nullable=False)

    def to_entity(self) -> Department:
        return Department(
            dep_id=self.dep_id,
            dep_name=self.dep_name,
            dep_code=self.dep_code,
            faculty=self.faculty
        )
