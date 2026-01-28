import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column, UUID, String, Enum
from sqlalchemy.orm import Session

from backend.shared.database import Base, get_db

from .application import DepartmentService, DepartmentResponseDTO, DepartmentCreateDTO, DepartmentUpdateDTO
from .domain import Faculty, Department, IDepartmentRepository


# ============= Modelos de SQLAlchemy para Departamentos ============= #
class DepartmentModel(Base):
    __tablename__ = "departments"

    dep_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dep_name = Column(String, nullable=False)
    dep_code = Column(String, nullable=False)
    faculty = Column(Enum(Faculty), nullable=False)

    def to_entity(self) -> Department:
        return Department(
            dep_id=self.dep_id,
            dep_name=self.dep_name,
            dep_code=self.dep_code,
            faculty=self.faculty
        )


# ============= Implementación de repositorio de Departamentos ============= #
class DBDepartmentRepository(IDepartmentRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self) -> List[Department]:
        models = self.db.query(DepartmentModel).all()
        return [model.to_entity() for model in models]

    async def get_by_faculty(self, faculty: Faculty) -> List[Department]:
        models = self.db.query(DepartmentModel).filter(DepartmentModel.faculty == faculty).all()
        return [model.to_entity() for model in models]

    async def get_by_id(self, dep_id: UUID) -> Department:
        dept = self.db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
        return dept.to_entity() if dept else None

    async def create(self, department: Department) -> Department:
        model = DepartmentModel(
            dep_id=department.dep_id,
            dep_name=department.dep_name,
            dep_code=department.dep_code,
            faculty=department.faculty
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    async def update(self, dep_id: UUID, department: Department) -> Department:
        model = self.db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
        if not model:
            raise ValueError(f"El departamento no fue encontrado.")
        model.dep_name = department.dep_name
        model.dep_code = department.dep_code
        model.faculty = department.faculty

        try:
            self.db.commit()
            self.db.refresh(model)
            return model.to_entity()
        except Exception:
            self.db.rollback()
            raise

    async def delete(self, dep_id: UUID) -> bool:
        dept = self.db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
        if dept:
            self.db.delete(dept)
            self.db.commit()
            return True
        return False


# ================= Enrutadores para Departamentos ================= #
router = APIRouter(prefix="/departments", tags=["Departamentos"])


def get_service(db: Session = Depends(get_db)) -> DepartmentService:
    """Inyector de dependencias local del módulo"""
    dept_repo = DBDepartmentRepository(db)
    return DepartmentService(dept_repo)


@router.get("", response_model=List[DepartmentResponseDTO])
async def get_departments(service: DepartmentService = Depends(get_service)):
    return await service.get_all_departments()


@router.get("/faculty/{faculty_code}", response_model=List[DepartmentResponseDTO])
async def get_departments_by_faculty(faculty_code: str, service: DepartmentService = Depends(get_service)):
    try:
        return await service.get_departments_by_faculty(faculty_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_model=DepartmentResponseDTO, status_code=201)
async def create_department(dto: DepartmentCreateDTO, service: DepartmentService = Depends(get_service)):
    return await service.create_department(dto)


@router.put("/{dep_id}", response_model=DepartmentResponseDTO)
async def update_department(
        dep_id: UUID,
        dto: DepartmentUpdateDTO,
        service: DepartmentService = Depends(get_service)
):
    try:
        return await service.update_department(dep_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{dep_id}")
async def delete_department(dep_id: UUID, service: DepartmentService = Depends(get_service)):
    deleted = await service.delete_department(dep_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return {"message": "Eliminado correctamente"}
