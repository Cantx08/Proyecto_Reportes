from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship

from ..models import Base
from ....domain.enums.faculty import Faculty


class DepartmentModel(Base):
    """Modelo de la tabla departamentos."""
    __tablename__ = 'departamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dep_code = Column(String(10), nullable=False)
    dep_name = Column(String(255), nullable=False)
    fac_name = Column(SQLEnum(Faculty), nullable=False)

    # Relaciones
    authors = relationship("AuthorModel", back_populates="department")

    def __repr__(self):
        return f"<DepartmentModel(id={self.id}, code='{self.dep_code}', name='{self.dep_name}')>"

