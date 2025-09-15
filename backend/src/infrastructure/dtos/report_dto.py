from typing import List, Optional
from pydantic import BaseModel, Field

class ReportRequestDTO(BaseModel):
    """DTO para solicitud de generación de reporte."""
    author_ids: List[str] = Field(..., description="IDs de autores para incluir en el reporte")
    docente_nombre: str = Field(..., description="Nombre completo del docente")
    docente_genero: str = Field(..., description="Género del docente (M/F)")
    departamento: str = Field(..., description="Departamento del docente")
    cargo: str = Field(..., description="Cargo del docente")
    memorando: Optional[str] = Field(None, description="Número de memorando de solicitud")
    firmante: int = Field(1, description="Tipo de firmante (1: Directora, 2: Vicerrector)")
    fecha: Optional[str] = Field(None, description="Fecha del reporte (opcional, usa fecha actual si no se especifica)")