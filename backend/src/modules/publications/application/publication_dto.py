from typing import List, Optional
from pydantic import BaseModel

from ..domain.publication import Publication, SJRMetric


class SJRMetricDTO(BaseModel):
    """DTO para métricas SJR de una categoría."""
    category: str
    quartile: str
    percentile: float
    sjr_year: int

    @staticmethod
    def from_entity(metric: SJRMetric) -> 'SJRMetricDTO':
        return SJRMetricDTO(
            category=metric.category,
            quartile=metric.quartile,
            percentile=metric.percentile,
            sjr_year=metric.sjr_year
        )


class PublicationResponseDTO(BaseModel):
    """DTO de respuesta para una publicación."""
    scopus_id: str
    eid: str
    doi: Optional[str]
    title: str
    year: int
    publication_date: str
    source_title: str
    document_type: str
    affiliation_name: str
    affiliation_id: Optional[str]
    subject_areas: List[str]
    sjr_metrics: List[SJRMetricDTO]
    best_quartile: Optional[str]

    @staticmethod
    def from_entity(publication: Publication) -> 'PublicationResponseDTO':
        return PublicationResponseDTO(
            scopus_id=publication.scopus_id,
            eid=publication.eid,
            doi=publication.doi,
            title=publication.title,
            year=publication.year,
            publication_date=publication.publication_date,
            source_title=publication.source_title,
            document_type=publication.document_type,
            affiliation_name=publication.affiliation_name,
            affiliation_id=publication.affiliation_id,
            subject_areas=publication.subject_areas,
            sjr_metrics=[SJRMetricDTO.from_entity(m) for m in publication.sjr_metrics],
            best_quartile=publication.best_quartile()
        )


class AuthorPublicationsResponseDTO(BaseModel):
    """DTO de respuesta para las publicaciones de un autor."""
    author_id: str
    scopus_ids: List[str]
    total_publications: int
    publications: List[PublicationResponseDTO]


class DocumentsByYearDTO(BaseModel):
    """DTO para estadísticas de documentos por año."""
    year: int
    count: int


class PublicationsStatsResponseDTO(BaseModel):
    """DTO de respuesta para estadísticas de publicaciones."""
    author_id: str
    total_publications: int
    documents_by_year: List[DocumentsByYearDTO]
    documents_by_type: dict
