"""
Configuración de dependencias e inyección de dependencias.
"""
import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

from .infrastructure.scopus_repository import ScopusApiClient, ScopusPublicacionesRepository, ScopusAreasTematicasRepository
from .infrastructure.sjr_repository import SJRFileRepository
from .infrastructure.areas_repository import AreasTematicasFileRepository
from .application.services import PublicacionesService, AreasTematicasService
from .presentation.controllers import PublicacionesController, AreasTematicasController
from .presentation.report_controller import ReportController

load_dotenv()

# Obtener el directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    """Configuración de la aplicación."""
    scopus_api_key: str = os.getenv("SCOPUS_API_KEY", "")
    sjr_csv_path: str = os.getenv("SJR_CSV_PATH", str(BASE_DIR / "data" / "df_sjr_24_04_2025.csv"))
    areas_csv_path: str = os.getenv("AREAS_CSV_PATH", str(BASE_DIR / "data" / "areas_subareas.csv"))


@lru_cache()
def get_settings() -> Settings:
    """Obtiene la configuración de la aplicación."""
    return Settings()


class DependencyContainer:
    """Contenedor de dependencias."""
    
    def __init__(self):
        self._settings = get_settings()
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        """Configura todas las dependencias."""
        # Clientes externos
        self._scopus_client = ScopusApiClient(self._settings.scopus_api_key)
        
        # Repositorios
        self._publicaciones_repo = ScopusPublicacionesRepository(self._scopus_client)
        self._areas_tematicas_repo_scopus = ScopusAreasTematicasRepository(self._scopus_client)
        self._sjr_repo = SJRFileRepository(self._settings.sjr_csv_path)
        self._areas_tematicas_repo = AreasTematicasFileRepository(self._settings.areas_csv_path)
        
        # Servicios de aplicación
        self._publicaciones_service = PublicacionesService(
            self._publicaciones_repo,
            self._sjr_repo
        )
        self._areas_tematicas_service = AreasTematicasService(
            self._areas_tematicas_repo_scopus,  # Para obtener datos de Scopus
            self._areas_tematicas_repo  # Para mapear usando CSV
        )
        
        # Controladores
        self._publicaciones_controller = PublicacionesController(self._publicaciones_service)
        self._areas_tematicas_controller = AreasTematicasController(self._areas_tematicas_service)
        self._report_controller = ReportController(
            self._publicaciones_service,
            self._areas_tematicas_service
        )
    
    @property
    def publicaciones_controller(self) -> PublicacionesController:
        """Obtiene el controlador de publicaciones."""
        return self._publicaciones_controller
    
    @property
    def areas_tematicas_controller(self) -> AreasTematicasController:
        """Obtiene el controlador de áreas temáticas."""
        return self._areas_tematicas_controller
    
    @property
    def report_controller(self) -> ReportController:
        """Obtiene el controlador de reportes."""
        return self._report_controller


# Instancia global del contenedor
container = DependencyContainer()
