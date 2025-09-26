from typing import List
from pydantic import BaseModel, Field

class DepartmentDTO(BaseModel):
    """DTO para información de un departamento."""
    sigla: str = Field(..., description="Sigla del departamento")
    nombre: str = Field(..., description="Nombre completo del departamento")
    facultad: str = Field(..., description="Facultad a la que pertenece")

class DepartmentsResponseDTO(BaseModel):
    """DTO para respuesta de lista de departamentos."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: List[DepartmentDTO] = Field(..., description="Lista de departamentos")
    message: str = Field(..., description="Mensaje descriptivo")