from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from typing import List
from src.dependencies import container
from src.application.dtos import (
    ReportRequestDTO, SubjectAreaResponseDTO, PublicationsResponseDTO,
    DocumentsByYearResponseDTO, CargosResponseDTO,
    AuthorDTO, AuthorCreateDTO, AuthorUpdateDTO, AuthorsResponseDTO, AuthorResponseDTO,
    DepartmentDTO, DepartmentCreateDTO, DepartmentUpdateDTO, DepartmentResponseDTO, DepartmentsResponseDTO,
    PositionDTO, PositionCreateDTO, PositionUpdateDTO, PositionsResponseDTO, PositionResponseDTO,
    ScopusAccountDTO, ScopusAccountCreateDTO, ScopusAccountUpdateDTO,
    ScopusAccountsResponseDTO, ScopusAccountResponseDTO, LinkAuthorScopusDTO, LegacyDepartmentsResponseDTO
)
from src.infrastructure.api.controllers.subject_areas_controller import SubjectAreasController
from src.infrastructure.api.controllers.publications_controller import PublicationsController
from src.infrastructure.api.controllers.reports_controller import ReportsController
from src.infrastructure.api.controllers.departments_controller import DepartmentsController
from src.infrastructure.api.controllers.new_departments_controller import NewDepartmentsController
from src.infrastructure.api.controllers.cargos_controller import CargosController
from src.infrastructure.api.controllers.authors_controller import AuthorsController
from src.infrastructure.api.controllers.positions_controller import PositionsController
from src.infrastructure.api.controllers.scopus_accounts_controller import ScopusAccountsController

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


def get_departments_controller_old() -> DepartmentsController:
    """Dependencia para obtener el controlador de departamentos legacy."""
    return container.departments_controller_old


def get_cargos_controller() -> CargosController:
    """Dependencia para obtener el controlador de cargos legacy."""
    return container.cargos_controller


def get_authors_controller() -> AuthorsController:
    """Dependencia para obtener el controlador de autores."""
    return container.authors_controller


def get_new_departments_controller() -> NewDepartmentsController:
    """Dependencia para obtener el controlador de nuevos departamentos."""
    return container.departments_controller


def get_positions_controller() -> PositionsController:
    """Dependencia para obtener el controlador de posiciones."""
    return container.positions_controller


def get_scopus_accounts_controller() -> ScopusAccountsController:
    """Dependencia para obtener el controlador de cuentas Scopus."""
    return container.scopus_accounts_controller


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


@app.get("/departments", response_model=LegacyDepartmentsResponseDTO)
async def get_departments_legacy(
        controller: DepartmentsController = Depends(get_departments_controller_old)
):
    """
    Obtiene la lista de todos los departamentos disponibles (legacy).
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


# ===========================
# NUEVOS ENDPOINTS - AUTORES
# ===========================

@app.get("/authors", response_model=AuthorsResponseDTO)
async def get_all_authors(
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Obtiene todos los autores."""
    return await controller.get_all_authors()


@app.get("/authors/{author_id}", response_model=AuthorResponseDTO)
async def get_author(
        author_id: str,
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Obtiene un autor por ID."""
    return await controller.get_author(author_id)


@app.post("/authors", response_model=AuthorResponseDTO)
async def create_author(
        author_data: AuthorCreateDTO,
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Crea un nuevo autor."""
    return await controller.create_author(author_data)


@app.put("/authors/{author_id}", response_model=AuthorResponseDTO)
async def update_author(
        author_id: str,
        author_data: AuthorUpdateDTO,
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Actualiza un autor existente."""
    return await controller.update_author(author_id, author_data)


@app.delete("/authors/{author_id}")
async def delete_author(
        author_id: str,
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Elimina un autor."""
    return await controller.delete_author(author_id)


# ===========================
# NUEVOS ENDPOINTS - DEPARTAMENTOS
# ===========================

@app.get("/new-departments", response_model=DepartmentsResponseDTO)
async def get_all_new_departments(
        controller: NewDepartmentsController = Depends(get_new_departments_controller)
):
    """Obtiene todos los departamentos nuevos."""
    return await controller.get_all_departments()


@app.get("/new-departments/{dep_id}", response_model=DepartmentResponseDTO)
async def get_new_department(
        dep_id: str,
        controller: NewDepartmentsController = Depends(get_new_departments_controller)
):
    """Obtiene un departamento por ID."""
    return await controller.get_department(dep_id)


@app.get("/new-departments/faculty/{fac_name}", response_model=List[DepartmentResponseDTO])
async def get_departments_by_faculty(
        fac_name: str,
        controller: NewDepartmentsController = Depends(get_new_departments_controller)
):
    """Obtiene departamentos por facultad."""
    return await controller.get_departments_by_faculty(fac_name)


@app.post("/new-departments", response_model=DepartmentResponseDTO)
async def create_new_department(
        department_data: DepartmentCreateDTO,
        controller: NewDepartmentsController = Depends(get_new_departments_controller)
):
    """Crea un nuevo departamento."""
    return await controller.create_department(department_data)


@app.put("/new-departments/{dep_id}", response_model=DepartmentResponseDTO)
async def update_new_department(
        dep_id: str,
        department_data: DepartmentUpdateDTO,
        controller: NewDepartmentsController = Depends(get_new_departments_controller)
):
    """Actualiza un departamento existente."""
    return await controller.update_department(dep_id, department_data)


@app.delete("/new-departments/{dep_id}")
async def delete_new_department(
        dep_id: str,
        controller: NewDepartmentsController = Depends(get_new_departments_controller)
):
    """Elimina un departamento."""
    return await controller.delete_department(dep_id)


# ===========================
# NUEVOS ENDPOINTS - POSICIONES/CARGOS
# ===========================

@app.get("/positions", response_model=PositionsResponseDTO)
async def get_all_positions(
        controller: PositionsController = Depends(get_positions_controller)
):
    """Obtiene todas las posiciones."""
    return await controller.get_all_positions()


@app.get("/positions/{pos_id}", response_model=PositionResponseDTO)
async def get_position(
        pos_id: str,
        controller: PositionsController = Depends(get_positions_controller)
):
    """Obtiene una posición por ID."""
    return await controller.get_position(pos_id)


@app.post("/positions", response_model=PositionResponseDTO)
async def create_position(
        position_data: PositionCreateDTO,
        controller: PositionsController = Depends(get_positions_controller)
):
    """Crea una nueva posición."""
    return await controller.create_position(position_data)


@app.put("/positions/{pos_id}", response_model=PositionResponseDTO)
async def update_position(
        pos_id: str,
        position_data: PositionUpdateDTO,
        controller: PositionsController = Depends(get_positions_controller)
):
    """Actualiza una posición existente."""
    return await controller.update_position(pos_id, position_data)


@app.delete("/positions/{pos_id}")
async def delete_position(
        pos_id: str,
        controller: PositionsController = Depends(get_positions_controller)
):
    """Elimina una posición."""
    return await controller.delete_position(pos_id)


# ===========================
# NUEVOS ENDPOINTS - CUENTAS SCOPUS
# ===========================

@app.get("/scopus-accounts", response_model=ScopusAccountsResponseDTO)
async def get_all_scopus_accounts(
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Obtiene todas las cuentas Scopus."""
    return await controller.get_all_scopus_accounts()


@app.get("/scopus-accounts/{scopus_id}", response_model=ScopusAccountResponseDTO)
async def get_scopus_account(
        scopus_id: str,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Obtiene una cuenta Scopus por ID."""
    return await controller.get_scopus_account(scopus_id)


@app.get("/scopus-accounts/by-author/{author_id}", response_model=List[ScopusAccountResponseDTO])
async def get_scopus_accounts_by_author(
        author_id: str,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Obtiene cuentas Scopus de un autor específico."""
    return await controller.get_scopus_accounts_by_author(author_id)


@app.post("/scopus-accounts", response_model=ScopusAccountResponseDTO)
async def create_scopus_account(
        account_data: ScopusAccountCreateDTO,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Crea una nueva cuenta Scopus."""
    return await controller.create_scopus_account(account_data)


@app.put("/scopus-accounts/{scopus_id}", response_model=ScopusAccountResponseDTO)
async def update_scopus_account(
        scopus_id: str,
        account_data: ScopusAccountUpdateDTO,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Actualiza una cuenta Scopus existente."""
    return await controller.update_scopus_account(scopus_id, account_data)


@app.delete("/scopus-accounts/{scopus_id}")
async def delete_scopus_account(
        scopus_id: str,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Elimina una cuenta Scopus."""
    return await controller.delete_scopus_account(scopus_id)


@app.post("/scopus-accounts/link", response_model=ScopusAccountResponseDTO)
async def link_author_scopus(
        link_data: LinkAuthorScopusDTO,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Vincula un autor con una cuenta Scopus."""
    return await controller.link_author_scopus(link_data)


@app.get("/scopus-accounts/author-ids")
async def get_all_scopus_ids(
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Obtiene todos los ID de Scopus para usar en otras consultas."""
    return await controller.get_all_scopus_ids()
