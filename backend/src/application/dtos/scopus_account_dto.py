from typing import List, Optional
from pydantic import BaseModel, Field


class ScopusAccountDTO(BaseModel):
    """DTO para información de una cuenta Scopus."""
    scopus_id: str = Field(..., description="ID de Scopus")
    scopus_user: str = Field(..., description="Usuario de Scopus")
    author_id: str = Field(..., description="ID del autor asociado")

    class Config:
        from_attributes = True


class ScopusAccountCreateDTO(BaseModel):
    """DTO para crear una nueva cuenta Scopus."""
    scopus_id: str = Field(..., description="ID de Scopus")
    scopus_user: str = Field("", description="Usuario de Scopus")
    author_id: str = Field(..., description="ID del autor asociado")


class ScopusAccountUpdateDTO(BaseModel):
    """DTO para actualizar una cuenta Scopus."""
    scopus_user: Optional[str] = Field(None, description="Usuario de Scopus")
    author_id: Optional[str] = Field(None, description="ID del autor asociado")


class ScopusAccountsResponseDTO(BaseModel):
    """DTO para respuesta de lista de cuentas Scopus."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: List[ScopusAccountDTO] = Field(..., description="Lista de cuentas Scopus")
    message: str = Field(..., description="Mensaje descriptivo")
    total: int = Field(..., description="Total de cuentas")


class ScopusAccountResponseDTO(BaseModel):
    """DTO para respuesta de una sola cuenta Scopus."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: Optional[ScopusAccountDTO] = Field(None, description="Datos de la cuenta Scopus")
    message: str = Field(..., description="Mensaje descriptivo")


class LinkAuthorScopusDTO(BaseModel):
    """DTO para vincular un autor con cuentas Scopus."""
    author_id: str = Field(..., description="ID del autor")
    scopus_ids: List[str] = Field(..., description="Lista de IDs de Scopus a vincular")