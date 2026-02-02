"""
Modelos relacionados con journals, rankings SJR y categorías.

Este módulo contiene los modelos para gestionar journals,
rankings SJR, categorías y métricas de publicaciones.
"""

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


# ============================================================================
# MODELOS DE JOURNALS
# ============================================================================

class JournalModel(Base):
    """Modelo para journals/revistas científicas."""
    __tablename__ = 'journals'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    issn = Column(String(20))
    e_issn = Column(String(20))
    publisher = Column(String(255))
    source_type = Column(String(50), default="Journal")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    publications = relationship("PublicationModel", back_populates="journal")
    sjr_rankings = relationship("SJRRankingModel", back_populates="journal")


# ============================================================================
# MODELOS DE RANKINGS SJR
# ============================================================================

class SJRRankingModel(Base):
    """Modelo para rankings SJR anuales de journals."""
    __tablename__ = 'sjr_rankings'
    
    id = Column(Integer, primary_key=True)
    journal_id = Column(Integer, ForeignKey('journals.id'), nullable=False)
    year = Column(Integer, nullable=False)
    sjr_value = Column(DECIMAL(10, 4))
    h_index = Column(Integer)
    total_docs = Column(Integer)
    total_cites = Column(Integer)
    citable_docs = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    
    # Relaciones
    journal = relationship("JournalModel", back_populates="sjr_rankings")
    categories = relationship("SJRCategoryModel", back_populates="sjr_ranking")


class CategoryModel(Base):
    """Modelo para categorías académicas de SJR."""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relaciones
    sjr_categories = relationship("SJRCategoryModel", back_populates="category")


class SJRCategoryModel(Base):
    """Modelo para categorías SJR con métricas específicas."""
    __tablename__ = 'sjr_categories'
    
    id = Column(Integer, primary_key=True)
    sjr_ranking_id = Column(Integer, ForeignKey('sjr_rankings.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    quartile = Column(String(2))  # Q1, Q2, Q3, Q4
    rank_position = Column(Integer)
    percentile = Column(DECIMAL(5, 2))
    created_at = Column(DateTime, default=func.now())
    
    # Relaciones
    sjr_ranking = relationship("SJRRankingModel", back_populates="categories")
    category = relationship("CategoryModel", back_populates="sjr_categories")