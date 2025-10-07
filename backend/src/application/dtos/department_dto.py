from typing import List, Optional
from pydantic import BaseModel, Field


class DepartmentDTO(BaseModel):
    """DTO para información de un departamento."""
    dep_id: str = Field(..., description="ID único del departamento")
    dep_code: str = Field(..., description="Código/sigla del departamento")
    dep_name: str = Field(..., description="Nombre completo del departamento")
    fac_name: str = Field(..., description="Nombre de la facultad")

    class Config:
        from_attributes = True


class DepartmentCreateDTO(BaseModel):
    """DTO para crear un nuevo departamento."""
    dep_id: str = Field(..., description="ID único del departamento")
    dep_code: str = Field(..., description="Código/sigla del departamento")
    dep_name: str = Field(..., description="Nombre completo del departamento")
    fac_name: str = Field(..., description="Nombre de la facultad")


class DepartmentUpdateDTO(BaseModel):
    """DTO para actualizar un departamento."""
    dep_code: Optional[str] = Field(None, description="Código/sigla del departamento")
    dep_name: Optional[str] = Field(None, description="Nombre completo del departamento")
    fac_name: Optional[str] = Field(None, description="Nombre de la facultad")


class DepartmentsResponseDTO(BaseModel):
    """DTO para respuesta de lista de departamentos."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: List[DepartmentDTO] = Field(..., description="Lista de departamentos")
    message: str = Field(..., description="Mensaje descriptivo")
    total: int = Field(..., description="Total de departamentos")
    
    @classmethod
    def from_entities(cls, departments):
        """Crea un DepartmentsResponseDTO desde una lista de entidades Department."""
        department_dtos = [
            DepartmentDTO(
                dep_id=dept.dep_id,
                dep_code=dept.dep_code,
                dep_name=dept.dep_name,
                fac_name=dept.fac_name
            ) for dept in departments
        ]
        return cls(
            success=True,
            data=department_dtos,
            message=f"Se obtuvieron {len(departments)} departamentos exitosamente",
            total=len(departments)
        )


class DepartmentResponseDTO(BaseModel):
    """DTO para respuesta de un solo departamento."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: Optional[DepartmentDTO] = Field(None, description="Datos del departamento")
    message: str = Field(..., description="Mensaje descriptivo")
    
    @classmethod
    def from_entity(cls, department):
        """Crea un DepartmentResponseDTO desde una entidad Department."""
        return cls(
            success=True,
            data=DepartmentDTO(
                dep_id=department.dep_id,
                dep_code=department.dep_code,
                dep_name=department.dep_name,
                fac_name=department.fac_name
            ),
            message="Departamento obtenido exitosamente"
        )