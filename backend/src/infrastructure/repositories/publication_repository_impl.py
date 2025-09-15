"""
Implementación del repositorio de publicaciones usando SQLAlchemy.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, asc

from ...domain.entities.publication import Publication
from ...domain.repositories.publication_repository import PublicationRepository
from ...domain.value_objects.doi import DOI
from ...domain.value_objects.scopus_id import ScopusId
from ...domain.value_objects.publication_year import PublicationYear
from ...domain.enums import PublicationType, SJRQuartile
from ..database.models import (
    PublicationModel, AuthorModel, JournalModel, 
    SJRRankingModel, PublicationAuthorModel
)
from ..database.connection import db_config


class SQLAlchemyPublicationRepository(PublicationRepository):
    """Implementación del repositorio de publicaciones usando SQLAlchemy."""
    
    def __init__(self, session: Optional[Session] = None):
        self._session = session
    
    @property
    def session(self) -> Session:
        """Obtiene la sesión de base de datos."""
        if self._session is None:
            self._session = db_config.get_session_sync()
        return self._session
    
    def save(self, publication: Publication) -> Publication:
        """Guarda una publicación en la base de datos."""
        # Verificar si existe
        existing = None
        if publication.doi:
            existing = self.session.query(PublicationModel).filter(
                PublicationModel.doi == str(publication.doi)
            ).first()
        elif publication.scopus_id:
            existing = self.session.query(PublicationModel).filter(
                PublicationModel.scopus_id == str(publication.scopus_id)
            ).first()
        
        if existing:
            # Actualizar existente
            self._update_publication_model(existing, publication)
            publication_model = existing
        else:
            # Crear nuevo
            publication_model = self._create_publication_model(publication)
            self.session.add(publication_model)
        
        self.session.commit()
        self.session.refresh(publication_model)
        
        return self._map_to_domain(publication_model)
    
    def find_by_doi(self, doi: DOI) -> Optional[Publication]:
        """Busca una publicación por DOI."""
        publication_model = self.session.query(PublicationModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        ).filter(PublicationModel.doi == str(doi)).first()
        
        if not publication_model:
            return None
        
        return self._map_to_domain(publication_model)
    
    def find_by_scopus_id(self, scopus_id: ScopusId) -> Optional[Publication]:
        """Busca una publicación por Scopus ID."""
        publication_model = self.session.query(PublicationModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        ).filter(PublicationModel.scopus_id == str(scopus_id)).first()
        
        if not publication_model:
            return None
        
        return self._map_to_domain(publication_model)
    
    def find_by_author(self, author_dni: str) -> List[Publication]:
        """Busca publicaciones por autor."""
        publication_models = self.session.query(PublicationModel).join(
            PublicationAuthorModel
        ).join(AuthorModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        ).filter(AuthorModel.dni == author_dni).all()
        
        return [self._map_to_domain(model) for model in publication_models]
    
    def find_by_year_range(self, start_year: int, end_year: int) -> List[Publication]:
        """Busca publicaciones por rango de años."""
        publication_models = self.session.query(PublicationModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        ).filter(
            and_(
                PublicationModel.year >= start_year,
                PublicationModel.year <= end_year
            )
        ).all()
        
        return [self._map_to_domain(model) for model in publication_models]
    
    def find_by_journal(self, journal_id: int) -> List[Publication]:
        """Busca publicaciones por journal."""
        publication_models = self.session.query(PublicationModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        ).filter(PublicationModel.journal_id == journal_id).all()
        
        return [self._map_to_domain(model) for model in publication_models]
    
    def find_by_type(self, publication_type: PublicationType) -> List[Publication]:
        """Busca publicaciones por tipo."""
        publication_models = self.session.query(PublicationModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        ).filter(PublicationModel.type == publication_type.value).all()
        
        return [self._map_to_domain(model) for model in publication_models]
    
    def search_by_title(self, title_query: str) -> List[Publication]:
        """Busca publicaciones por título (búsqueda parcial)."""
        search_term = f"%{title_query.lower()}%"
        
        publication_models = self.session.query(PublicationModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        ).filter(PublicationModel.title.ilike(search_term)).all()
        
        return [self._map_to_domain(model) for model in publication_models]
    
    def find_with_filters(self, filters: Dict[str, Any]) -> List[Publication]:
        """Busca publicaciones con filtros múltiples."""
        query = self.session.query(PublicationModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        )
        
        # Aplicar filtros
        if 'year_start' in filters:
            query = query.filter(PublicationModel.year >= filters['year_start'])
        
        if 'year_end' in filters:
            query = query.filter(PublicationModel.year <= filters['year_end'])
        
        if 'type' in filters:
            query = query.filter(PublicationModel.type == filters['type'])
        
        if 'journal_id' in filters:
            query = query.filter(PublicationModel.journal_id == filters['journal_id'])
        
        if 'author_dni' in filters:
            query = query.join(PublicationAuthorModel).join(AuthorModel).filter(
                AuthorModel.dni == filters['author_dni']
            )
        
        if 'quartile' in filters:
            query = query.join(JournalModel).join(SJRRankingModel).filter(
                SJRRankingModel.quartile == filters['quartile']
            )
        
        if 'title' in filters:
            search_term = f"%{filters['title'].lower()}%"
            query = query.filter(PublicationModel.title.ilike(search_term))
        
        # Ordenar
        order_by = filters.get('order_by', 'year')
        order_dir = filters.get('order_dir', 'desc')
        
        if order_by == 'year':
            order_field = PublicationModel.year
        elif order_by == 'title':
            order_field = PublicationModel.title
        elif order_by == 'citations':
            order_field = PublicationModel.citation_count
        else:
            order_field = PublicationModel.year
        
        if order_dir == 'desc':
            query = query.order_by(desc(order_field))
        else:
            query = query.order_by(asc(order_field))
        
        # Aplicar límite si se especifica
        if 'limit' in filters:
            query = query.limit(filters['limit'])
        
        if 'offset' in filters:
            query = query.offset(filters['offset'])
        
        publication_models = query.all()
        return [self._map_to_domain(model) for model in publication_models]
    
    def find_all(self) -> List[Publication]:
        """Obtiene todas las publicaciones."""
        publication_models = self.session.query(PublicationModel).options(
            joinedload(PublicationModel.journal),
            joinedload(PublicationModel.authors)
        ).all()
        
        return [self._map_to_domain(model) for model in publication_models]
    
    def delete(self, publication_id: int) -> bool:
        """Elimina una publicación por ID."""
        publication_model = self.session.query(PublicationModel).filter(
            PublicationModel.id == publication_id
        ).first()
        
        if not publication_model:
            return False
        
        self.session.delete(publication_model)
        self.session.commit()
        return True
    
    def count_by_author(self, author_dni: str) -> int:
        """Cuenta las publicaciones de un autor."""
        return self.session.query(PublicationModel).join(
            PublicationAuthorModel
        ).join(AuthorModel).filter(AuthorModel.dni == author_dni).count()
    
    def count_by_year(self, year: int) -> int:
        """Cuenta las publicaciones de un año."""
        return self.session.query(PublicationModel).filter(
            PublicationModel.year == year
        ).count()
    
    def _create_publication_model(self, publication: Publication) -> PublicationModel:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""
        publication_model = PublicationModel(
            title=publication.title,
            abstract=publication.abstract,
            year=publication.year.value,
            type=publication.type.value,
            doi=str(publication.doi) if publication.doi else None,
            scopus_id=str(publication.scopus_id) if publication.scopus_id else None,
            journal_id=publication.journal_id,
            pages=publication.pages,
            volume=publication.volume,
            issue=publication.issue,
            citation_count=publication.citation_count,
            keywords=','.join(publication.keywords) if publication.keywords else None,
            is_open_access=publication.is_open_access,
            url=publication.url,
            source=publication.source,
            is_editable=publication.is_editable,
            notes=publication.notes,
            created_at=publication.created_at,
            updated_at=publication.updated_at
        )
        
        return publication_model
    
    def _update_publication_model(self, publication_model: PublicationModel, publication: Publication):
        """Actualiza un modelo existente con datos de la entidad de dominio."""
        publication_model.title = publication.title
        publication_model.abstract = publication.abstract
        publication_model.year = publication.year.value
        publication_model.type = publication.type.value
        publication_model.doi = str(publication.doi) if publication.doi else None
        publication_model.scopus_id = str(publication.scopus_id) if publication.scopus_id else None
        publication_model.journal_id = publication.journal_id
        publication_model.pages = publication.pages
        publication_model.volume = publication.volume
        publication_model.issue = publication.issue
        publication_model.citation_count = publication.citation_count
        publication_model.keywords = ','.join(publication.keywords) if publication.keywords else None
        publication_model.is_open_access = publication.is_open_access
        publication_model.url = publication.url
        publication_model.source = publication.source
        publication_model.is_editable = publication.is_editable
        publication_model.notes = publication.notes
        publication_model.updated_at = publication.updated_at
    
    def _map_to_domain(self, publication_model: PublicationModel) -> Publication:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""
        return Publication(
            id=publication_model.id,
            title=publication_model.title,
            abstract=publication_model.abstract,
            year=PublicationYear(publication_model.year),
            type=PublicationType(publication_model.type),
            doi=DOI(publication_model.doi) if publication_model.doi else None,
            scopus_id=ScopusId(publication_model.scopus_id) if publication_model.scopus_id else None,
            journal_id=publication_model.journal_id,
            pages=publication_model.pages,
            volume=publication_model.volume,
            issue=publication_model.issue,
            citation_count=publication_model.citation_count or 0,
            keywords=publication_model.keywords.split(',') if publication_model.keywords else [],
            is_open_access=publication_model.is_open_access,
            url=publication_model.url,
            source=publication_model.source,
            is_editable=publication_model.is_editable,
            notes=publication_model.notes,
            created_at=publication_model.created_at,
            updated_at=publication_model.updated_at
        )