"""
Data Transfer Objects para la API.
"""
from pydantic import BaseModel
from typing import List
from .author_dto import AuthorDTO


class PublicationDTO(BaseModel):
    """DTO para publicación."""
    title: str
    anio: str
    fuente: str
    tipo_documento: str
    filiacion: str
    doi: str
    categorias: str = ""


class PublicationsResponseDTO(BaseModel):
    """DTO para respuesta de publicaciones."""
    publications: List[AuthorDTO]


class DocumentsByYearResponseDTO(BaseModel):
    """DTO para respuesta de documentos por año."""
    author_ids: List[str]
    documents_by_year: dict[str, int]