from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from .domain import JobPosition, IJobPositionRepository


# ============== DTOS para la gestión de cargos ==============
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


# ================= Servicio para la gestión de cargos =================
class JobPositionService:
    def __init__(self, pos_repo: IJobPositionRepository):
        self.pos_repo = pos_repo

    async def get_all_positions(self) -> List[JobPositionResponseDTO]:
        positions = await self.pos_repo.get_all()
        return [JobPositionResponseDTO(pos_id=job.pos_id, pos_name=job.pos_name) for job in positions]

    async def create_position(self, dto: JobPositionCreateDTO) -> JobPositionResponseDTO:
        new_pos = JobPosition(
            pos_id=uuid4(),
            pos_name=dto.pos_name
        )
        saved_pos = await self.pos_repo.create(new_pos)
        return JobPositionResponseDTO(pos_id=saved_pos.pos_id, pos_name=saved_pos.pos_name)

    async def update_position(self, job_pos_id: UUID, dto: JobPositionUpdateDTO) -> JobPositionResponseDTO:
        existing = await self.pos_repo.get_by_id(job_pos_id)
        if not existing:
            raise ValueError(f"El cargo con ID {job_pos_id} no existe.")

        new_name = dto.name if dto.name else existing.pos_name

        updated_entity = JobPosition(pos_id=job_pos_id, pos_name=new_name)
        result = await self.pos_repo.update(job_pos_id, updated_entity)

        return JobPositionResponseDTO.from_entity(result)

    async def delete_position(self, pos_id: UUID) -> bool:
        return await self.pos_repo.delete(pos_id)
