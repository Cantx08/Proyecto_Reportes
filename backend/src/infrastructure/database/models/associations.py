"""
Tablas de asociación para relaciones many-to-many.

Este módulo contiene todas las tablas de asociación
que conectan las entidades principales del sistema.
"""

from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, JSON, Table
from sqlalchemy.sql import func
from .base import Base


# ============================================================================
# TABLAS DE ASOCIACIÓN MANY-TO-MANY
# ============================================================================

# Tabla de asociación para publicaciones y autores
publication_authors = Table(
    'publication_authors',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('publication_id', Integer, ForeignKey('publications.id')),
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('scopus_account_id', Integer, ForeignKey('scopus_accounts.id')),
    Column('author_order', Integer),
    Column('is_corresponding', Boolean, default=False),
    Column('created_at', DateTime, default=func.now())
)

# Tabla de asociación para publicaciones y áreas temáticas
publication_subject_areas = Table(
    'publication_subject_areas',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('publication_id', Integer, ForeignKey('publications.id')),
    Column('subject_area_id', Integer, ForeignKey('subject_areas.id')),
    Column('subject_subarea_id', Integer, ForeignKey('subject_subareas.id')),
    Column('created_at', DateTime, default=func.now())
)

# Tabla de asociación para reportes y publicaciones
report_publications = Table(
    'report_publications',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('report_id', Integer, ForeignKey('reports.id')),
    Column('publication_id', Integer, ForeignKey('publications.id')),
    Column('is_included', Boolean, default=True),
    Column('custom_data', JSON),
    Column('created_at', DateTime, default=func.now())
)