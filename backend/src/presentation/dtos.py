"""
Data Transfer Objects para la API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class PublicacionDTO(BaseModel):
    """DTO para publicación."""
    titulo: str
    anio: str
    fuente: str
    tipo_documento: str
    filiacion: str
    doi: str
    categorias: str = ""


class AutorDTO(BaseModel):
    """DTO para autor."""
    id_autor: str
    lista_publicaciones: Optional[List[PublicacionDTO]] = None
    error: Optional[str] = None


class PublicacionesResponseDTO(BaseModel):
    """DTO para respuesta de publicaciones."""
    publicaciones: List[AutorDTO]


class DocumentosPorAnioResponseDTO(BaseModel):
    """DTO para respuesta de documentos por año."""
    author_ids: List[str]
    documentos_por_anio: dict[str, int]


class AreasTematicasResponseDTO(BaseModel):
    """DTO para respuesta de áreas temáticas."""
    author_ids: List[str]
    areas_tematicas: List[str]
