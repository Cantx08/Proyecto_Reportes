from typing import List, Optional, TYPE_CHECKING, Union
from pydantic import BaseModel, Field, field_validator
from datetime import date

if TYPE_CHECKING:
    from .publication_dto import PublicationDTO


class AuthorDTO(BaseModel):
    """DTO para autor."""
    author_id: str = Field(..., description="ID único del autor")
    name: str = Field(..., description="Nombre del autor")
    surname: str = Field(..., description="Apellido del autor")
    dni: str = Field(..., description="Documento Nacional de Identidad")
    title: str = Field("", description="Título académico (Dr., PhD., Ing., etc.)")
    birth_date: Optional[Union[date, str]] = Field(None, description="Fecha de nacimiento")
    gender: str = Field("M", description="Género del autor")
    position: str = Field("", description="Cargo que ocupa")
    department: str = Field("", description="Departamento al que pertenece")
    publications_list: Optional[List["PublicationDTO"]] = Field(None, description="Lista de publicaciones")
    error: Optional[str] = Field(None, description="Error si lo hay")

    class Config:
        from_attributes = True


class AuthorCreateDTO(BaseModel):
    """DTO para crear un nuevo autor."""
    author_id: Optional[str] = Field(None, description="ID único del autor (opcional, se genera automáticamente)")
    name: str = Field(..., description="Nombre del autor")
    surname: str = Field(..., description="Apellido del autor")
    dni: str = Field(..., description="Documento Nacional de Identidad")
    title: str = Field("", description="Título académico")
    birth_date: Optional[Union[date, str]] = Field(None, description="Fecha de nacimiento")
    gender: str = Field("M", description="Género del autor")
    position: str = Field("", description="Cargo que ocupa")
    department: str = Field("", description="Departamento al que pertenece")

    @field_validator('birth_date', mode='before')
    @classmethod
    def parse_birth_date(cls, v):
        """Convierte string a date si es necesario."""
        if isinstance(v, str) and v:
            from datetime import datetime
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return v


class AuthorUpdateDTO(BaseModel):
    """DTO para actualizar un autor."""
    name: Optional[str] = Field(None, description="Nombre del autor")
    surname: Optional[str] = Field(None, description="Apellido del autor")
    dni: Optional[str] = Field(None, description="Documento Nacional de Identidad")
    title: Optional[str] = Field(None, description="Título académico")
    birth_date: Optional[Union[date, str]] = Field(None, description="Fecha de nacimiento")
    gender: Optional[str] = Field(None, description="Género del autor")
    position: Optional[str] = Field(None, description="Cargo que ocupa")
    department: Optional[str] = Field(None, description="Departamento al que pertenece")

    @field_validator('birth_date', mode='before')
    @classmethod
    def parse_birth_date(cls, v):
        """Convierte string a date si es necesario."""
        if isinstance(v, str) and v:
            from datetime import datetime
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return v


class AuthorsResponseDTO(BaseModel):
    """DTO para respuesta de lista de autores."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: List[AuthorDTO] = Field(..., description="Lista de autores")
    message: str = Field(..., description="Mensaje de la operación")
    total: int = Field(..., description="Total de autores")


class AuthorResponseDTO(BaseModel):
    """DTO para respuesta de un solo autor."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: Optional[AuthorDTO] = Field(None, description="Datos del autor")
    message: str = Field(..., description="Mensaje de la operación")
