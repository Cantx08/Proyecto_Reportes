from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from ..domain.job_position import JobPosition


class JobPositionCreateDTO(BaseModel):
    pos_name: str = Field(..., description="Ej: Profesor Principal A Tiempo Completo")


class JobPositionUpdateDTO(BaseModel):
    pos_name: Optional[str] = None


class JobPositionResponseDTO(BaseModel):
    pos_id: UUID
    pos_name: str

    @staticmethod
    def from_entity(job_pos: JobPosition):
        return JobPositionResponseDTO(
            pos_id=job_pos.pos_id,
            pos_name=job_pos.pos_name
        )
