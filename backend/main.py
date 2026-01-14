from fastapi import FastAPI, Query, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from src.infrastructure.dependencies import container
from src.application.dto import (
    ReportRequestDTO, SubjectAreaResponseDTO, PublicationsResponseDTO,
    DocumentsByYearResponseDTO,
    AuthorCreateDTO, AuthorUpdateDTO, AuthorsResponseDTO, AuthorResponseDTO,
    DepartmentCreateDTO, DepartmentUpdateDTO, DepartmentResponseDTO, DepartmentsResponseDTO,
    PositionCreateDTO, PositionUpdateDTO, PositionsResponseDTO, PositionResponseDTO,
    ScopusAccountCreateDTO, ScopusAccountUpdateDTO,
    ScopusAccountsResponseDTO, ScopusAccountResponseDTO, LinkAuthorScopusDTO
)
from src.application.dto.auth_dto import (
    UserRegisterDTO, UserLoginDTO, UserUpdateDTO, PasswordChangeDTO,
    TokenResponseDTO, UserResponseDTO, UsersResponseDTO, AuthResponseDTO, MessageResponseDTO
)
from src.infrastructure.api.controllers.subject_areas_controller import SubjectAreasController
from src.infrastructure.api.controllers.publications_controller import PublicationsController
from src.infrastructure.api.controllers.reports_controller import ReportsController
from src.infrastructure.api.controllers.departments_controller import DepartmentsController
from src.infrastructure.api.controllers.authors_controller import AuthorsController
from src.infrastructure.api.controllers.positions_controller import PositionsController
from src.infrastructure.api.controllers.scopus_accounts_controller import ScopusAccountsController
from src.infrastructure.api.controllers.draft_processor_controller import DraftProcessorController
from src.infrastructure.api.controllers.auth_controller import AuthController
from src.domain.entities.user import User
from src.domain.enums.role import Role

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


def get_authors_controller() -> AuthorsController:
    """Dependencia para obtener el controlador de autores."""
    return container.authors_controller


def get_departments_controller() -> DepartmentsController:
    """Dependencia para obtener el controlador de nuevos departamentos."""
    return container.departments_controller


def get_positions_controller() -> PositionsController:
    """Dependencia para obtener el controlador de posiciones."""
    return container.positions_controller


def get_scopus_accounts_controller() -> ScopusAccountsController:
    """Dependencia para obtener el controlador de cuentas Scopus."""
    return container.scopus_accounts_controller


def get_draft_processor_controller() -> DraftProcessorController:
    """Dependencia para obtener el controlador de procesamiento de borradores."""
    return container.draft_processor_controller


def get_auth_controller() -> AuthController:
    """Dependencia para obtener el controlador de autenticación."""
    return container.auth_controller


# Esquema de seguridad
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Dependencia para obtener el usuario actual autenticado."""
    token = credentials.credentials
    user = await container.auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependencia para obtener el usuario activo actual."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )
    return current_user


async def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependencia que requiere rol de administrador."""
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere rol de administrador"
        )
    return current_user


@app.get("/health")
async def health_check():
    """Endpoint de salud."""
    return {"status": "healthy", "message": "API funcionando correctamente"}


# ===========================
# ENDPOINTS - AUTENTICACIÓN
# ===========================

@app.post("/auth/register", response_model=AuthResponseDTO, tags=["Autenticación"])
async def register(
        register_data: UserRegisterDTO,
        controller: AuthController = Depends(get_auth_controller)
):
    """
    Registra un nuevo usuario.
    
    El primer usuario registrado será automáticamente administrador.
    """
    try:
        return await controller.register(register_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/auth/login", response_model=AuthResponseDTO, tags=["Autenticación"])
async def login(
        login_data: UserLoginDTO,
        controller: AuthController = Depends(get_auth_controller)
):
    """Autentica un usuario y retorna un token JWT."""
    try:
        return await controller.login(login_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.get("/auth/me", response_model=UserResponseDTO, tags=["Autenticación"])
async def get_me(
        current_user: User = Depends(get_current_active_user),
        controller: AuthController = Depends(get_auth_controller)
):
    """Obtiene la información del usuario actual autenticado."""
    return await controller.get_me(current_user)


@app.put("/auth/me", response_model=UserResponseDTO, tags=["Autenticación"])
async def update_me(
        update_data: UserUpdateDTO,
        current_user: User = Depends(get_current_active_user),
        controller: AuthController = Depends(get_auth_controller)
):
    """Actualiza la información del usuario actual."""
    try:
        return await controller.update_me(current_user, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/auth/me/change-password", response_model=MessageResponseDTO, tags=["Autenticación"])
async def change_my_password(
        password_data: PasswordChangeDTO,
        current_user: User = Depends(get_current_active_user),
        controller: AuthController = Depends(get_auth_controller)
):
    """Cambia la contraseña del usuario actual."""
    try:
        return await controller.change_my_password(current_user, password_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ===========================
# ENDPOINTS - GESTIÓN DE USUARIOS (SOLO ADMIN)
# ===========================

@app.get("/users", response_model=UsersResponseDTO, tags=["Usuarios (Admin)"])
async def get_all_users(
        admin_user: User = Depends(require_admin),
        controller: AuthController = Depends(get_auth_controller)
):
    """Obtiene todos los usuarios. Solo accesible por administradores."""
    return await controller.get_all_users()


@app.get("/users/{user_id}", response_model=UserResponseDTO, tags=["Usuarios (Admin)"])
async def get_user(
        user_id: int,
        admin_user: User = Depends(require_admin),
        controller: AuthController = Depends(get_auth_controller)
):
    """Obtiene un usuario por ID. Solo accesible por administradores."""
    try:
        return await controller.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.post("/users", response_model=UserResponseDTO, tags=["Usuarios (Admin)"])
async def create_user(
        user_data: UserRegisterDTO,
        admin_user: User = Depends(require_admin),
        controller: AuthController = Depends(get_auth_controller)
):
    """Crea un nuevo usuario. Solo accesible por administradores."""
    try:
        return await controller.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put("/users/{user_id}", response_model=UserResponseDTO, tags=["Usuarios (Admin)"])
async def update_user(
        user_id: int,
        update_data: UserUpdateDTO,
        admin_user: User = Depends(require_admin),
        controller: AuthController = Depends(get_auth_controller)
):
    """Actualiza un usuario. Solo accesible por administradores."""
    try:
        return await controller.update_user(user_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/users/{user_id}", response_model=MessageResponseDTO, tags=["Usuarios (Admin)"])
async def delete_user(
        user_id: int,
        admin_user: User = Depends(require_admin),
        controller: AuthController = Depends(get_auth_controller)
):
    """Elimina un usuario. Solo accesible por administradores."""
    try:
        return await controller.delete_user(user_id, admin_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/authors", response_model=AuthorsResponseDTO, tags=["Autores"])
async def get_all_authors(
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Obtiene todos los autores."""
    return await controller.get_all_authors()


# ===========================
# ENDPOINTS - AUTORES
# ===========================

@app.get("/authors/{author_id}", response_model=AuthorResponseDTO, tags=["Autores"])
async def get_author(
        author_id: str,
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Obtiene un autor por ID."""
    return await controller.get_author_by_id(author_id)


@app.post("/authors", response_model=AuthorResponseDTO, tags=["Autores"])
async def create_author(
        author_data: AuthorCreateDTO,
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Crea un nuevo autor."""
    return await controller.create_author(author_data)


@app.put("/authors/{author_id}", response_model=AuthorResponseDTO, tags=["Autores"])
async def update_author(
        author_id: str,
        author_data: AuthorUpdateDTO,
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Actualiza un autor existente."""
    return await controller.update_author(author_id, author_data)


@app.delete("/authors/{author_id}", tags=["Autores"])
async def delete_author(
        author_id: str,
        controller: AuthorsController = Depends(get_authors_controller)
):
    """Elimina un autor."""
    return await controller.delete_author(author_id)


# ===========================
# ENDPOINTS - DEPARTAMENTOS
# ===========================

@app.get("/faculties", tags=["Departamentos"])
async def get_faculties():
    """Obtiene todas las facultades disponibles."""
    from src.domain.enums.faculty import Faculty
    return {
        "success": True,
        "data": [{"key": f.name, "value": f.value} for f in Faculty if f != Faculty.DESCONOCIDA],
        "message": "Faculties retrieved successfully"
    }


@app.get("/departments", response_model=DepartmentsResponseDTO, tags=["Departamentos"])
async def get_all_departments(
        controller: DepartmentsController = Depends(get_departments_controller)
):
    """Obtiene todos los departamentos nuevos."""
    return await controller.get_all_departments()


@app.get("/departments/{dep_id}", response_model=DepartmentResponseDTO, tags=["Departamentos"])
async def get_department(
        dep_id: str,
        controller: DepartmentsController = Depends(get_departments_controller)
):
    """Obtiene un departamento por ID."""
    return await controller.get_department(dep_id)


@app.get("/departments/faculty/{fac_name}", response_model=List[DepartmentResponseDTO], tags=["Departamentos"])
async def get_departments_by_faculty(
        fac_name: str,
        controller: DepartmentsController = Depends(get_departments_controller)
):
    """Obtiene departamentos por facultad."""
    return await controller.get_departments_by_faculty(fac_name)


@app.post("/departments", response_model=DepartmentResponseDTO, tags=["Departamentos"])
async def create_department(
        department_data: DepartmentCreateDTO,
        controller: DepartmentsController = Depends(get_departments_controller)
):
    """Crea un nuevo departamento."""
    return await controller.create_department(department_data)


@app.put("/departments/{dep_id}", response_model=DepartmentResponseDTO, tags=["Departamentos"])
async def update_department(
        dep_id: str,
        department_data: DepartmentUpdateDTO,
        controller: DepartmentsController = Depends(get_departments_controller)
):
    """Actualiza un departamento existente."""
    return await controller.update_department(dep_id, department_data)


@app.delete("/departments/{dep_id}", tags=["Departamentos"])
async def delete_department(
        dep_id: str,
        controller: DepartmentsController = Depends(get_departments_controller)
):
    """Elimina un departamento."""
    return await controller.delete_department(dep_id)


# ===========================
# ENDPOINTS - CARGOS
# ===========================

@app.get("/positions", response_model=PositionsResponseDTO, tags=["Cargos"])
async def get_all_positions(
        controller: PositionsController = Depends(get_positions_controller)
):
    """Obtiene todas las posiciones."""
    return await controller.get_all_positions()


@app.get("/positions/{pos_id}", response_model=PositionResponseDTO, tags=["Cargos"])
async def get_position(
        pos_id: str,
        controller: PositionsController = Depends(get_positions_controller)
):
    """Obtiene una posición por ID."""
    return await controller.get_position_by_id(pos_id)


@app.post("/positions", response_model=PositionResponseDTO, tags=["Cargos"])
async def create_position(
        position_data: PositionCreateDTO,
        controller: PositionsController = Depends(get_positions_controller)
):
    """Crea una nueva posición."""
    return await controller.create_position(position_data)


@app.put("/positions/{pos_id}", response_model=PositionResponseDTO, tags=["Cargos"])
async def update_position(
        pos_id: str,
        position_data: PositionUpdateDTO,
        controller: PositionsController = Depends(get_positions_controller)
):
    """Actualiza una posición existente."""
    return await controller.update_position(pos_id, position_data)


@app.delete("/positions/{pos_id}", tags=["Cargos"])
async def delete_position(
        pos_id: str,
        controller: PositionsController = Depends(get_positions_controller)
):
    """Elimina una posición."""
    return await controller.delete_position(pos_id)


# ===========================
# NUEVOS ENDPOINTS - CUENTAS SCOPUS
# ===========================

@app.get("/scopus-accounts", response_model=ScopusAccountsResponseDTO, tags=["Cuentas Scopus"])
async def get_all_scopus_accounts(
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Obtiene todas las cuentas Scopus."""
    return await controller.get_all_accounts()


@app.get("/scopus-accounts/{scopus_id}", response_model=ScopusAccountResponseDTO, tags=["Cuentas Scopus"])
async def get_scopus_account(
        scopus_id: str,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Obtiene una cuenta Scopus por ID."""
    return await controller.get_account_by_scopus_id(scopus_id)


@app.get("/scopus-accounts/by-author/{author_id}", response_model=ScopusAccountsResponseDTO,
         tags=["Cuentas Scopus"])
async def get_scopus_accounts_by_author(
        author_id: str,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Obtiene cuentas Scopus de un autor específico."""
    return await controller.get_accounts_by_author_id(author_id)


@app.post("/scopus-accounts", response_model=ScopusAccountResponseDTO, tags=["Cuentas Scopus"])
async def create_scopus_account(
        account_data: ScopusAccountCreateDTO,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Crea una nueva cuenta Scopus."""
    return await controller.create_account(account_data)


@app.put("/scopus-accounts/{scopus_id}", response_model=ScopusAccountResponseDTO, tags=["Cuentas Scopus"])
async def update_scopus_account(
        scopus_id: str,
        account_data: ScopusAccountUpdateDTO,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Actualiza una cuenta Scopus existente."""
    return await controller.update_account(scopus_id, account_data)


@app.delete("/scopus-accounts/{scopus_id}", tags=["Cuentas Scopus"])
async def delete_scopus_account(
        scopus_id: str,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Elimina una cuenta Scopus."""
    return await controller.delete_account(scopus_id)


@app.post("/scopus-accounts/link", response_model=ScopusAccountsResponseDTO, tags=["Autores", "Cuentas Scopus"])
async def link_author_scopus(
        link_data: LinkAuthorScopusDTO,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Vincula un autor con múltiples cuentas Scopus."""
    return await controller.link_author_to_scopus(link_data)


@app.get("/scopus-accounts/author-ids/{author_id}", tags=["Cuentas Scopus"])
async def get_all_scopus_ids(
        author_id: str,
        controller: ScopusAccountsController = Depends(get_scopus_accounts_controller)
):
    """Obtiene todos los ID de Scopus de un autor."""
    return await controller.get_scopus_ids_by_author(author_id)


# ===========================
# ENDPOINTS - PUBLICACIONES, ÁREAS TEMÁTICAS Y REPORTES
# ===========================

@app.get("/scopus/publications", response_model=PublicationsResponseDTO, tags=["Publicaciones"])
async def get_publications(
        ids: List[str] = Query(..., description="Lista de IDs de Scopus o IDs de autor de la base de datos"),
        controller: PublicationsController = Depends(get_publications_controller)
):
    """
    Obtiene publicaciones de uno o varios autores.
    
    Puedes usar:
    - IDs de Scopus (numéricos de 11 dígitos, ej: 57832340700)
    - IDs de autor de la base de datos (cualquier formato, ej: A001)
    
    El sistema automáticamente resolverá los IDs de autor a sus Scopus IDs asociados.
    """
    return await controller.get_publications(ids)


@app.get("/scopus/docs_by_year", response_model=DocumentsByYearResponseDTO, tags=["Publicaciones"])
async def get_documents_by_year(
        ids: List[str] = Query(..., description="Lista de IDs de Scopus o IDs de autor de la base de datos"),
        controller: PublicationsController = Depends(get_publications_controller)
):
    """
    Obtiene el número de publicaciones por año de uno o varios autores.
    
    Puedes usar:
    - IDs de Scopus (numéricos de 11 dígitos, ej: 57832340700)
    - IDs de autor de la base de datos (cualquier formato, ej: A001)
    
    El sistema automáticamente resolverá los IDs de autor a sus Scopus IDs asociados.
    """
    return await controller.get_documents_by_year(ids)


@app.get("/scopus/subject_areas", response_model=SubjectAreaResponseDTO, tags=["Publicaciones"])
async def get_subject_areas(
        ids: List[str] = Query(..., description="Lista de IDs de Scopus o IDs de autor de la base de datos"),
        controller: SubjectAreasController = Depends(get_subject_areas_controller)
):
    """
    Obtiene las áreas temáticas generales de las publicaciones de uno o varios autores.
    
    Puedes usar:
    - IDs de Scopus (numéricos de 11 dígitos, ej: 57832340700)
    - IDs de autor de la base de datos (cualquier formato, ej: A001)
    
    El sistema automáticamente resolverá los IDs de autor a sus Scopus IDs asociados.
    Mapea las subáreas específicas de Scopus a las áreas temáticas generales definidas.
    """
    return await controller.fetch_subject_areas(ids)


@app.post("/reports/inform", response_class=Response, tags=["Reportes"])
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


@app.post("/reports/process-draft", response_class=Response, tags=["Reportes"])
async def procesar_borrador(
        file: UploadFile = File(..., description="Archivo PDF borrador a procesar"),
        memorando: Optional[str] = Form(None, description="Número de memorando"),
        firmante: Optional[int] = Form(None, description="Tipo de firmante (1=Directora, 2=Vicerrectora)"),
        firmante_nombre: Optional[str] = Form(None, description="Nombre del firmante"),
        fecha: Optional[str] = Form(None, description="Fecha del certificado"),
        controller: DraftProcessorController = Depends(get_draft_processor_controller)
):
    """
    Procesa un borrador PDF existente y lo convierte en certificado final.
    
    Este endpoint toma un PDF borrador (sin plantilla institucional) y le aplica
    la plantilla oficial de la EPN (form.pdf) con encabezados, logos y formato oficial.
    
    Args:
        file: Archivo PDF borrador (máximo 10MB)
        memorando: Número de memorando (opcional, para extensión futura)
        firmante: Tipo de firmante (opcional, para extensión futura)
        firmante_nombre: Nombre del firmante (opcional, para extensión futura)
        fecha: Fecha del certificado (opcional, para extensión futura)
    
    Returns:
        Response: PDF final con plantilla institucional aplicada
        
    Raises:
        HTTPException 400: Si el archivo no es un PDF válido o excede el tamaño máximo
        HTTPException 500: Si hay un error al procesar el PDF
    """
    return await controller.process_draft(
        file=file,
        memorando=memorando,
        firmante=firmante,
        firmante_nombre=firmante_nombre,
        fecha=fecha
    )
