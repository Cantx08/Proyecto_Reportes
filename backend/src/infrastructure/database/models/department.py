from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base, FacultyEnum


class DepartmentModel(Base):
    """Modelo de la tabla departments."""
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dep_id = Column(String(50), unique=True, nullable=True)  # Código externo opcional
    dep_code = Column(String(50), nullable=False)  # Siglas del departamento (DICC, DFB, etc.)
    dep_name = Column(String(255), nullable=False)  # Nombre completo
    fac_name = Column(SQLEnum(FacultyEnum), nullable=False)  # Facultad
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    authors = relationship("AuthorModel", back_populates="department")

    def __repr__(self):
        return f"<DepartmentModel(id={self.id}, code='{self.dep_code}', name='{self.dep_name}')>"

