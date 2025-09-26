from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from typing import List
from src.dependencies import container
from src.infrastructure.dtos import ReportRequestDTO, SubjectAreaResponseDTO, PublicationsResponseDTO, DocumentsByYearResponseDTO, DepartmentsResponseDTO, CargosResponseDTO
from src.infrastructure.controllers.subject_areas_controller import SubjectAreasController
from src.infrastructure.controllers.publications_controller import PublicationsController
from src.infrastructure.controllers.reports_controller import ReportsController
from src.infrastructure.controllers.departments_controller import DepartmentsController
from src.infrastructure.controllers.cargos_controller import CargosController

app = FastAPI(
    title="Sistema de Publicaciones Académicas",
    description="API para consultar publicaciones académicas de Scopus",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_publications_controller() -> PublicationsController:
    """Dependencia para obtener el controlador de publicaciones."""
    return container.publications_controller


def get_subject_areas_controller() -> SubjectAreasController:
    """Dependencia para obtener el controlador de áreas temáticas."""
    return container.subject_areas_controller


def get_reports_controller() -> ReportsController:
    """Dependencia para obtener el controlador de reportes."""
    return container.reports_controller


def get_departments_controller() -> DepartmentsController:
    """Dependencia para obtener el controlador de departamentos."""
    return container.departments_controller


def get_cargos_controller() -> CargosController:
    """Dependencia para obtener el controlador de cargos."""
    return container.cargos_controller


@app.get("/scopus/publications", response_model=PublicationsResponseDTO)
async def get_publications(
    ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus"),
    controller: PublicationsController = Depends(get_publications_controller)
):
    """
    Obtiene publicaciones de uno o varios ID de autor Scopus.
    Agrupa todas las publicaciones bajo un solo autor.
    """
    return await controller.get_publications(ids)


@app.get("/scopus/docs_by_year", response_model=DocumentsByYearResponseDTO)
async def get_documents_by_year(
    ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus"),
    controller: PublicationsController = Depends(get_publications_controller)
):
    """
    Obtiene el número de publicaciones por año realizadas por un autor que tiene uno o varios ID.
    """
    return await controller.get_documents_by_year(ids)


@app.get("/scopus/subject_areas", response_model=SubjectAreaResponseDTO)
async def get_subject_areas(
    ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus"),
    controller: SubjectAreasController = Depends(get_subject_areas_controller)
):
    """
    Obtiene las áreas temáticas generales de las publicaciones del autor.
    Mapea las subáreas específicas de Scopus a las áreas temáticas generales definidas.
    """
    return await controller.fetch_subject_areas(ids)


@app.get("/departments", response_model=DepartmentsResponseDTO)
async def get_departments(
    controller: DepartmentsController = Depends(get_departments_controller)
):
    """
    Obtiene la lista de todos los departamentos disponibles.
    """
    return await controller.get_departments()


@app.get("/cargos", response_model=CargosResponseDTO)
async def get_cargos(
    controller: CargosController = Depends(get_cargos_controller)
):
    """
    Obtiene la lista de todos los cargos disponibles.
    """
    return await controller.get_cargos()


@app.get("/health")
async def health_check():
    """Endpoint de salud."""
    return {"status": "healthy", "message": "API funcionando correctamente"}


@app.post("/reports/inform", response_class=Response)
async def generar_informe(
    request: ReportRequestDTO,
    controller: ReportsController = Depends(get_reports_controller)
):
    """
    Genera un reporte de certificación de publicaciones en formato PDF.
    
    Incluye:
    - Información del docente
    - Publicaciones Scopus, Web of Science, regionales, etc.
    - Áreas temáticas
    - Estadísticas por año
    - Firmas oficiales
    """
    return await controller.generate_report(request)
