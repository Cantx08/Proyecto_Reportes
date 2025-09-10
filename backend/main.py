from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from typing import List
from src.dependencies import container
from src.presentation.dtos import (
    PublicacionesResponseDTO,
    DocumentosPorAnioResponseDTO, 
    AreasTematicasResponseDTO,
    ReportRequestDTO
)
from src.presentation.controllers import PublicacionesController, AreasTematicasController
from src.presentation.report_controller import ReportController

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


def get_publicaciones_controller() -> PublicacionesController:
    """Dependencia para obtener el controlador de publicaciones."""
    return container.publicaciones_controller


def get_areas_tematicas_controller() -> AreasTematicasController:
    """Dependencia para obtener el controlador de áreas temáticas."""
    return container.areas_tematicas_controller


def get_report_controller() -> ReportController:
    """Dependencia para obtener el controlador de reportes."""
    return container.report_controller


@app.get("/scopus/publications", response_model=PublicacionesResponseDTO)
async def get_publications(
    ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus"),
    controller: PublicacionesController = Depends(get_publicaciones_controller)
):
    """
    Obtiene publicaciones de uno o varios IDs de autor Scopus.
    Agrupa todas las publicaciones bajo un solo autor.
    """
    return await controller.obtener_publicaciones(ids)


@app.get("/scopus/docs_by_year", response_model=DocumentosPorAnioResponseDTO)
async def get_documents_by_year(
    ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus"),
    controller: PublicacionesController = Depends(get_publicaciones_controller)
):
    """
    Obtiene el número de publicaciones por año realizadas por un autor que tiene uno o varios IDs.
    """
    return await controller.obtener_documentos_por_anio(ids)


@app.get("/scopus/subject_areas", response_model=AreasTematicasResponseDTO)
async def get_subject_areas(
    ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus"),
    controller: AreasTematicasController = Depends(get_areas_tematicas_controller)
):
    """
    Obtiene las áreas temáticas generales de las publicaciones del autor.
    Mapea las subáreas específicas de Scopus a las áreas temáticas generales definidas.
    """
    return await controller.obtener_areas_tematicas(ids)


@app.get("/health")
async def health_check():
    """Endpoint de salud."""
    return {"status": "healthy", "message": "API funcionando correctamente"}


@app.post("/reports/certificacion", response_class=Response)
async def generar_reporte_certificacion(
    request: ReportRequestDTO,
    controller: ReportController = Depends(get_report_controller)
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
    return await controller.generar_reporte_certificacion(request)
