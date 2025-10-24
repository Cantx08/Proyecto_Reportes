"""
Modelo de base de datos para cargos académicos.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class PositionModel(Base):
    """Modelo de cargo académico."""
    __tablename__ = 'positions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    authors = relationship("AuthorModel", back_populates="position_rel")
    
    def __repr__(self):
        return f"<Position(id={self.id}, name={self.name})>"
