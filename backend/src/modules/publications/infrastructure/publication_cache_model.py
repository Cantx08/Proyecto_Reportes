"""
Modelo SQLAlchemy para caché de publicaciones.

Esta tabla almacena las publicaciones consultadas desde Scopus
para evitar llamadas repetidas a la API.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, UUID, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ....shared.database import Base


class PublicationCacheModel(Base):
    """
    Modelo de caché para publicaciones de Scopus.
    
    Almacena las publicaciones consultadas para reducir llamadas a la API
    y permitir consultas offline.
    """
    __tablename__ = 'publication_cache'
    
    # Identificador interno
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Identificadores de Scopus
    scopus_id = Column(String(50), unique=True, nullable=False, index=True)
    eid = Column(String(100), nullable=True)
    doi = Column(String(255), nullable=True, index=True)
    
    # Datos básicos de la publicación
    title = Column(Text, nullable=False)
    year = Column(Integer, nullable=False, index=True)
    publication_date = Column(String(20), nullable=True)
    source_title = Column(String(500), nullable=True)
    document_type = Column(String(100), nullable=True)
    
    # Filiación
    affiliation_name = Column(String(500), nullable=True)
    affiliation_id = Column(String(50), nullable=True)
    
    # Áreas temáticas y categorías con cuartiles (almacenadas como JSON)
    subject_areas = Column(JSON, nullable=True, default=list)
    categories_with_quartiles = Column(JSON, nullable=True, default=list)
    sjr_year_used = Column(Integer, nullable=True)
    
    # Relación con la cuenta Scopus que originó la consulta
    scopus_account_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("scopus_accounts.account_id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Metadatos de caché
    cached_at = Column(DateTime, default=func.now(), nullable=False)
    last_accessed = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relación
    scopus_account = relationship("ScopusAccountModel", backref="cached_publications")

    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario para transformación a entidad."""
        return {
            "scopus_id": self.scopus_id,
            "eid": self.eid or "",
            "doi": self.doi,
            "title": self.title,
            "year": self.year,
            "publication_date": self.publication_date or "",
            "source_title": self.source_title or "",
            "document_type": self.document_type or "",
            "affiliation_name": self.affiliation_name or "",
            "affiliation_id": self.affiliation_id,
            "subject_areas": self.subject_areas or [],
            "categories_with_quartiles": self.categories_with_quartiles or [],
            "sjr_year_used": self.sjr_year_used
        }
