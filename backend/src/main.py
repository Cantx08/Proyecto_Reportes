from typing import List, Dict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Importación del Contenedor Global (Configuración)
from .container import get_container
# 2. Importación de los Routers
from .modules.departments.domain.faculty import Faculty
from .modules.departments.infrastructure.department_router import router as department_router
from .modules.job_positions.infrastructure.job_position_router import router as job_position_router
from .modules.authors.infrastructure.author_router import router as author_router
from .modules.scopus_accounts.infrastructure.scopus_account_router import router as account_router
from .modules.publications.infrastructure.publication_router import router as publication_router

# Obtener configuración
container = get_container()
settings = container.settings

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para gestión de reportes científicos EPN"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verifica que la API y la BD estén vivas."""
    try:
        with container.db_handler.get_session_sync() as session:
            session.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "active",
        "version": settings.VERSION,
        "database": db_status,
        "modules_loaded": ["organization"]
    }


@app.get("/faculties", response_model=List[Dict[str, str]], tags=["Facultades"])
async def get_faculties():
    return [
        {"key": f.fac_code, "value": f.fac_name}
        for f in Faculty
    ]


# ==============================================================================
# ROUTERS
# ==============================================================================
app.include_router(department_router)
app.include_router(job_position_router)
app.include_router(author_router)
app.include_router(account_router)
app.include_router(publication_router)
# app.include_router(reports_router)


# ==============================================================================
# ENDPOINTS GLOBALES / UTILITARIOS
# ==============================================================================

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
