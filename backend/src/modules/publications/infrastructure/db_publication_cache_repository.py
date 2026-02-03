from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from .publication_cache_model import PublicationCacheModel
from ..domain.publication import Publication, SJRMetric
from ..domain.publication_cache_repository import IPublicationCacheRepository


class DBPublicationCacheRepository(IPublicationCacheRepository):
    """
    Implementación del repositorio de caché de publicaciones usando PostgreSQL.
    
    Almacena las publicaciones consultadas desde Scopus para reducir
    llamadas a la API y permitir consultas más rápidas.
    """

    def __init__(self, db: Session):
        self._db = db

    async def get_by_scopus_account(self, scopus_account_id: UUID) -> List[Publication]:
        """Obtiene todas las publicaciones cacheadas de una cuenta Scopus."""
        models = self._db.query(PublicationCacheModel).filter(
            PublicationCacheModel.scopus_account_id == scopus_account_id
        ).all()
        
        return [self._model_to_entity(m) for m in models]

    async def get_by_scopus_id(self, scopus_id: str) -> Optional[Publication]:
        """Obtiene una publicación específica de la caché."""
        model = self._db.query(PublicationCacheModel).filter(
            PublicationCacheModel.scopus_id == scopus_id
        ).first()
        
        if model:
            # Actualizar last_accessed
            model.last_accessed = datetime.utcnow()
            self._db.commit()
            return self._model_to_entity(model)
        
        return None

    async def save_publications(
        self, 
        publications: List[Publication], 
        scopus_account_id: UUID
    ) -> int:
        """Guarda o actualiza publicaciones en la caché."""
        saved_count = 0
        
        for pub in publications:
            # Buscar si ya existe
            existing = self._db.query(PublicationCacheModel).filter(
                PublicationCacheModel.scopus_id == pub.scopus_id
            ).first()
            
            if existing:
                # Actualizar registro existente
                self._update_model(existing, pub)
            else:
                # Crear nuevo registro
                model = self._entity_to_model(pub, scopus_account_id)
                self._db.add(model)
            
            saved_count += 1
        
        try:
            self._db.commit()
        except Exception:
            self._db.rollback()
            raise
        
        return saved_count

    async def is_cache_valid(self, scopus_account_id: UUID, max_age_hours: int = 24) -> bool:
        """Verifica si la caché está vigente (no más antigua que max_age_hours)."""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        # Buscar la publicación más reciente cacheada
        newest = self._db.query(PublicationCacheModel).filter(
            PublicationCacheModel.scopus_account_id == scopus_account_id,
            PublicationCacheModel.cached_at >= cutoff_time
        ).first()
        
        return newest is not None

    async def invalidate_cache(self, scopus_account_id: UUID) -> int:
        """Elimina todas las publicaciones cacheadas de una cuenta."""
        deleted = self._db.query(PublicationCacheModel).filter(
            PublicationCacheModel.scopus_account_id == scopus_account_id
        ).delete()
        
        self._db.commit()
        return deleted

    def _model_to_entity(self, model: PublicationCacheModel) -> Publication:
        """Convierte un modelo de BD a entidad de dominio."""
        # Reconstruir métricas SJR desde JSON
        sjr_metrics = []
        if model.sjr_metrics:
            for m in model.sjr_metrics:
                sjr_metrics.append(SJRMetric(
                    category=m.get("category", ""),
                    quartile=m.get("quartile", ""),
                    percentile=m.get("percentile", 0.0),
                    sjr_year=m.get("sjr_year", 0)
                ))
        
        return Publication(
            scopus_id=model.scopus_id,
            eid=model.eid or "",
            doi=model.doi,
            title=model.title,
            year=model.year,
            publication_date=model.publication_date or "",
            source_title=model.source_title or "",
            document_type=model.document_type or "",
            affiliation_name=model.affiliation_name or "",
            affiliation_id=model.affiliation_id,
            subject_areas=model.subject_areas or [],
            sjr_metrics=sjr_metrics
        )

    def _entity_to_model(
        self, 
        pub: Publication, 
        scopus_account_id: UUID
    ) -> PublicationCacheModel:
        """Convierte una entidad de dominio a modelo de BD."""
        # Serializar métricas SJR a JSON
        sjr_metrics_json = [
            {
                "category": m.category,
                "quartile": m.quartile,
                "percentile": m.percentile,
                "sjr_year": m.sjr_year
            }
            for m in pub.sjr_metrics
        ]
        
        return PublicationCacheModel(
            scopus_id=pub.scopus_id,
            eid=pub.eid,
            doi=pub.doi,
            title=pub.title,
            year=pub.year,
            publication_date=pub.publication_date,
            source_title=pub.source_title,
            document_type=pub.document_type,
            affiliation_name=pub.affiliation_name,
            affiliation_id=pub.affiliation_id,
            subject_areas=pub.subject_areas,
            sjr_metrics=sjr_metrics_json,
            scopus_account_id=scopus_account_id,
            cached_at=datetime.utcnow()
        )

    def _update_model(self, model: PublicationCacheModel, pub: Publication) -> None:
        """Actualiza un modelo existente con datos nuevos."""
        model.eid = pub.eid
        model.doi = pub.doi
        model.title = pub.title
        model.year = pub.year
        model.publication_date = pub.publication_date
        model.source_title = pub.source_title
        model.document_type = pub.document_type
        model.affiliation_name = pub.affiliation_name
        model.affiliation_id = pub.affiliation_id
        model.subject_areas = pub.subject_areas
        model.sjr_metrics = [
            {
                "category": m.category,
                "quartile": m.quartile,
                "percentile": m.percentile,
                "sjr_year": m.sjr_year
            }
            for m in pub.sjr_metrics
        ]
        model.cached_at = datetime.utcnow()
