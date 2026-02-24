"""
DTOs para operaciones CRUD de metadatos de reportes.
"""
from typing import Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime


class PublicationSnapshot(BaseModel):
    """Snapshot serializable de una publicación."""
    scopus_id: str
    eid: str = ""
    doi: Optional[str] = None
    title: str = ""
    year: int = 0
    publication_date: str = ""
    source_title: str = ""
    document_type: str = ""
    affiliation_name: str = ""
    affiliation_id: Optional[str] = None
    source_id: Optional[str] = None
    subject_areas: List[str] = Field(default_factory=list)
    categories_with_quartiles: List[str] = Field(default_factory=list)
    sjr_year_used: Optional[int] = None


class SaveReportMetadataDTO(BaseModel):
    """DTO para guardar metadatos de un reporte."""
    author_name: str
    author_gender: str
    department: str
    position: str
    author_ids: List[str]
    publications: List[PublicationSnapshot]
    subject_areas: List[str]
    documents_by_year: Dict[str, int]
    memorandum: Optional[str] = None
    signatory: Union[int, str] = 1
    signatory_name: Optional[str] = None
    report_date: Optional[str] = None
    elaborador: str = "M. Vásquez"
    label: str = ""


class UpdateReportMetadataDTO(BaseModel):
    """DTO para actualizar solo los campos editables."""
    memorandum: Optional[str] = None
    signatory: Union[int, str] = 1
    signatory_name: Optional[str] = None
    report_date: Optional[str] = None
    elaborador: str = "M. Vásquez"
    label: Optional[str] = None


class ReportMetadataResponseDTO(BaseModel):
    """DTO de respuesta con los metadatos del reporte."""
    id: UUID
    author_name: str
    author_gender: str
    department: str
    position: str
    author_ids: List[str]
    publications: List[Dict]
    subject_areas: List[str]
    documents_by_year: Dict[str, int]
    memorandum: Optional[str] = None
    signatory: Union[int, str] = 1
    signatory_name: Optional[str] = None
    report_date: Optional[str] = None
    elaborador: str = "M. Vásquez"
    label: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
