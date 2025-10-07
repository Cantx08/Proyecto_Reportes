from typing import List
from pydantic import BaseModel, Field

class CargoDTO(BaseModel):
    """DTO para información de un cargo."""
    cargo: str = Field(..., description="Nombre del cargo")
    tiempo: str = Field(..., description="Tipo de tiempo (TC/TP)")

class CargosResponseDTO(BaseModel):
    """DTO para respuesta de lista de cargos."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: List[CargoDTO] = Field(..., description="Lista de cargos")
    message: str = Field(..., description="Mensaje descriptivo")