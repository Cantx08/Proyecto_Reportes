from typing import Optional, List

from pydantic import BaseModel, Field

from ...domain.entities.department import Department


class DepartmentCreateDTO(BaseModel):
    """ DTO para la creación de un departamento. """
    dep_code: str = Field(..., min_length=2, max_length=10, description="Siglas del departamento")
    dep_name: str = Field(..., min_length=2, description="Nombre del departamento")
    fac_name: str = Field(..., description="Facultad a la que pertenece el departamento")


class DepartmentUpdateDTO(BaseModel):
    """ DTO para la actualización de un departamento. """
    dep_code: Optional[str] = Field(None, min_length=2, max_length=10,
                                    description="Siglas actualizadas del departamento")
    dep_name: Optional[str] = Field(None, min_length=2, description="Nombre actualizado del departamento")
    fac_name: Optional[str] = Field(None, description="Actual facultad a la que pertenece")


class DepartmentResponseDTO(BaseModel):
    """ DTO para enviar la información de un departamento al cliente. """
    dep_id: int = Field(..., description="ID del departamento")
    dep_code: str = Field(..., description="Siglas del departamento")
    dep_name: str = Field(..., description="Nombre del departamento")
    fac_name: str = Field(..., description="Facultad a la que pertenece el departamento")

    class Config:
        from_attributes = True

    @classmethod
    def from_entity(cls, entity: Department) -> 'DepartmentResponseDTO':
        return cls(
            dep_id=entity.dep_id,
            dep_code=entity.dep_code,
            dep_name=entity.dep_name,
            fac_name=str(entity.fac_name)
        )


class DepartmentListResponseDTO(BaseModel):
    """ DTO para la lista de departamentos. """
    departments: List[DepartmentResponseDTO]
    total: int

    @classmethod
    def from_entities(cls, entities: List[Department]) -> 'DepartmentListResponseDTO':
        return cls(
            departments=[DepartmentResponseDTO.from_entity(e) for e in entities],
            total=len(entities)
        )
