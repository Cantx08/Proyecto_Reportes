"""
Entidad de dominio para metadatos de reportes de certificación.
Permite almacenar toda la información necesaria para regenerar un certificado
sin necesidad de volver a buscar publicaciones.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import UUID


@dataclass
class ReportMetadata:
    """
    Entidad de dominio que almacena los metadatos de un reporte de certificación.
    
    Contiene tanto datos oficiales (no editables: publicaciones, áreas temáticas)
    como datos editables (memorando, fecha, firmante, elaborador).
    """
    id: UUID

    # Datos del autor (provenientes de la búsqueda original)
    author_name: str
    author_gender: str
    department: str
    position: str
    author_ids: List[str]

    # Snapshot de datos oficiales (no editables por el usuario)
    publications: List[Dict]          # Publicaciones serializadas como dicts
    subject_areas: List[str]          # Áreas temáticas del autor
    documents_by_year: Dict[str, int] # Conteo de documentos por año

    # Metadatos editables del certificado
    memorandum: Optional[str] = None
    signatory: Union[int, str] = 1
    signatory_name: Optional[str] = None
    report_date: Optional[str] = None
    elaborador: str = "M. Vásquez"

    # Nombre descriptivo para identificar el reporte en la lista
    label: str = ""

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
