from typing import List, Optional, Union
from pydantic import BaseModel, Field

class ReportRequestDTO(BaseModel):
    """DTO para solicitud de generación de reporte."""
    author_ids: List[str] = Field(..., description="IDs de autores para incluir en el reporte")
    docente_nombre: str = Field(..., description="Nombre completo del docente")
    docente_genero: str = Field(..., description="Género del docente (M/F o texto personalizado)")
    departamento: str = Field(..., description="Departamento del docente")
    cargo: str = Field(..., description="Cargo del docente")
    memorando: Optional[str] = Field(None, description="Número de memorando de solicitud")
    firmante: Union[int, str] = Field(1, description="Tipo de firmante (1: Directora, 2: Vicerrector, o cargo personalizado)")
    firmante_nombre: Optional[str] = Field(None, description="Nombre del firmante (requerido para firmantes personalizados)")
    fecha: Optional[str] = Field(None, description="Fecha del reporte (opcional, usa fecha actual si no se especifica)")
    es_borrador: bool = Field(False, description="True para generar borrador, False para certificado final con plantilla")


class ProcessDraftRequestDTO(BaseModel):
    """DTO para procesar un borrador existente y convertirlo en certificado final."""
    # Los metadatos se envían como Form data junto con el archivo
    memorando: Optional[str] = Field(None, description="Número de memorando (opcional)")
    firmante: Optional[int] = Field(None, description="Tipo de firmante (1=Directora, 2=Vicerrectora)")
    firmante_nombre: Optional[str] = Field(None, description="Nombre personalizado del firmante")
    fecha: Optional[str] = Field(None, description="Fecha del certificado (opcional)")