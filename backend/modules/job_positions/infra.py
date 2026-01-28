import uuid
from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import Session

from backend.shared.database import Base, get_db

from .application import JobPositionService, JobPositionResponseDTO, JobPositionCreateDTO, JobPositionUpdateDTO
from .domain import JobPosition, IJobPositionRepository


# ========== Modelos de SQLAlchemy para Cargos ========== #
class JobPositionModel(Base):
    __tablename__ = "positions"

    pos_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    pos_name = Column(String, unique=True, nullable=False)

    def to_entity(self) -> JobPosition:
        return JobPosition(
            pos_id=self.pos_id,
            pos_name=self.pos_name
        )


# ========== Implementación de Repositorio de Cargos ========== #
class DBJobPositionRepository(IJobPositionRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self) -> List[JobPosition]:
        models = self.db.query(JobPositionModel).all()
        return [m.to_entity() for m in models]

    async def get_by_id(self, pos_id: UUID) -> JobPosition:
        job_pos = self.db.query(JobPositionModel).filter(JobPositionModel.pos_id == pos_id).first()
        return job_pos.to_entity() if job_pos else None

    async def create(self, position: JobPosition) -> JobPosition:
        model = JobPositionModel(
            pos_id=position.pos_id,
            pos_name=position.pos_name
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    async def update(self, pos_id: UUID, position: JobPosition) -> JobPosition:
        model = self.db.query(JobPositionModel).filter(JobPositionModel.pos_id == pos_id).first()
        if not model:
            raise ValueError(f"El cargo no fue encontrado.")
        model.pos_name = position.pos_name

        try:
            self.db.commit()
            self.db.refresh(model)
            return model.to_entity()
        except Exception:
            self.db.rollback()
            raise

    async def delete(self, pos_id: UUID) -> bool:
        job_pos = self.db.query(JobPositionModel).filter(JobPositionModel.pos_id == pos_id).first()
        if job_pos:
            self.db.delete(job_pos)
            self.db.commit()
            return True
        return False


# ========== Router de FastAPI para Cargos ========== #
router = APIRouter(prefix="/job-positions", tags=["Cargos"])


def get_service(db: Session = Depends(get_db)) -> JobPositionService:
    """Inyector de dependencias local del módulo"""
    pos_repo = DBJobPositionRepository(db)
    return JobPositionService(pos_repo)


@router.get("", response_model=List[JobPositionResponseDTO])
async def get_positions(service: JobPositionService = Depends(get_service)):
    return await service.get_all_positions()


@router.post("", response_model=JobPositionResponseDTO, status_code=201)
async def create_position(dto: JobPositionCreateDTO, service: JobPositionService = Depends(get_service)):
    return await service.create_position(dto)


@router.put("/{pos_id}", response_model=JobPositionResponseDTO)
async def update_position(
        pos_id: UUID,
        dto: JobPositionUpdateDTO,
        service: JobPositionService = Depends(get_service)
):
    try:
        return await service.update_position(pos_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        if "unique" in str(e).lower():
            raise HTTPException(status_code=409, detail="Ya existe un cargo con ese nombre.")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{pos_id}")
async def delete_position(pos_id: UUID, service: JobPositionService = Depends(get_service)):
    deleted = await service.delete_position(pos_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return {"message": "Eliminado correctamente"}
