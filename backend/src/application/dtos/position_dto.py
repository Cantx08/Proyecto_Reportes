from typing import List, Optional
from pydantic import BaseModel, Field


class PositionDTO(BaseModel):
    """DTO para información de un cargo/posición."""
    pos_id: str = Field(..., description="ID único del cargo")
    pos_name: str = Field(..., description="Nombre del cargo")

    class Config:
        from_attributes = True


class PositionCreateDTO(BaseModel):
    """DTO para crear un nuevo cargo."""
    pos_id: str = Field(..., description="ID único del cargo")
    pos_name: str = Field(..., description="Nombre del cargo")


class PositionUpdateDTO(BaseModel):
    """DTO para actualizar un cargo."""
    pos_name: str = Field(..., description="Nombre del cargo")


class PositionsResponseDTO(BaseModel):
    """DTO para respuesta de lista de cargos."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: List[PositionDTO] = Field(..., description="Lista de cargos")
    message: str = Field(..., description="Mensaje descriptivo")
    total: int = Field(..., description="Total de cargos")


class PositionResponseDTO(BaseModel):
    """DTO para respuesta de un solo cargo."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: Optional[PositionDTO] = Field(None, description="Datos del cargo")
    message: str = Field(..., description="Mensaje descriptivo")