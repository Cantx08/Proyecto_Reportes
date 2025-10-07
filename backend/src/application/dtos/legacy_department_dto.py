"""DTOs legacy para departamentos que funcionan con el sistema anterior."""

from typing import List
from pydantic import BaseModel, Field


class LegacyDepartmentDTO(BaseModel):
    """DTO legacy para información de un departamento."""
    sigla: str = Field(..., description="Sigla del departamento")
    nombre: str = Field(..., description="Nombre completo del departamento")
    facultad: str = Field(..., description="Nombre de la facultad")

    class Config:
        from_attributes = True


class LegacyDepartmentsResponseDTO(BaseModel):
    """DTO de respuesta legacy para la lista de departamentos."""
    departments: List[LegacyDepartmentDTO] = Field(..., description="Lista de departamentos")

    class Config:
        from_attributes = True