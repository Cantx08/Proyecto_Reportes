"""
Configuración de dependencias e inyección de dependencias.
"""
import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from .application.services.subject_area_service import SubjectAreaService
from .application.services.publication_service import PublicationService
from .infrastructure.controllers.report_controller import ReportController
from .infrastructure.controllers.subject_area_controller import SubjectAreaController
from .infrastructure.controllers.publication_controller import PublicationController
from .infrastructure.csv.sjr_file_repository import SJRFileRepository
from .infrastructure.csv.subject_areas_file_repository import SubjectAreasFileRepository
from .infrastructure.external_services.scopus_api_client import ScopusApiClient
from .infrastructure.repositories.scopus_publication_repository import ScopusPublicationsRepository
from .infrastructure.repositories.scopus_subject_areas_repository import ScopusSubjectAreasRepository

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
        self._scopus_publications_repository = ScopusPublicationsRepository(self._scopus_client)
        self._scopus_subject_areas_repository = ScopusSubjectAreasRepository(self._scopus_client)
        self._sjr_file_repository = SJRFileRepository(self._settings.sjr_csv_path)
        self._subject_areas_repo = SubjectAreasFileRepository(self._settings.areas_csv_path)
        
        # Servicios de aplicación
        self._publication_service = PublicationService(
            self._scopus_publications_repository,
            self._sjr_file_repository
        )
        self._subject_area_service = SubjectAreaService(
            self._scopus_subject_areas_repository,  # Para obtener datos de Scopus
            self._subject_areas_repo  # Para mapear usando CSV
        )
        
        # Controladores
        self._publication_controller = PublicationController(self._publication_service)
        self._subject_area_controller = SubjectAreaController(self._subject_area_service)
        self._report_controller = ReportController(
            self._publication_service,
            self._subject_area_service
        )
    
    @property
    def publication_controller(self) -> PublicationController:
        """Obtiene el controlador de publicaciones."""
        return self._publication_controller
    
    @property
    def subject_area_controller(self) -> SubjectAreaController:
        """Obtiene el controlador de áreas temáticas."""
        return self._areas_tematicas_controller
    
    @property
    def report_controller(self) -> ReportController:
        """Obtiene el controlador de reportes."""
        return self._report_controller


# Instancia global del contenedor
container = DependencyContainer()
