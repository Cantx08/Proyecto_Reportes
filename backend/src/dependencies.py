"""
Configuración de dependencias e inyección de dependencias.
"""
import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

from .application.services.subject_area_service import SubjectAreaService
from .application.services.publication_service import PublicationService
from .application.services.department_service import DepartmentService
from .application.services.cargo_service import CargoService
from .infrastructure.controllers.reports_controller import ReportsController
from .infrastructure.controllers.subject_areas_controller import SubjectAreasController
from .infrastructure.controllers.publications_controller import PublicationsController
from .infrastructure.controllers.departments_controller import DepartmentsController
from .infrastructure.controllers.cargos_controller import CargosController
from .infrastructure.csv.sjr_file_repository import SJRFileRepository
from .infrastructure.csv.subject_areas_file_repository import SubjectAreasFileRepository
from .infrastructure.csv.departments_file_repository import DepartmentsFileRepository
from .infrastructure.csv.cargos_file_repository import CargosFileRepository
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
        self._departments_repo = DepartmentsFileRepository()
        self._cargos_repo = CargosFileRepository()
        
        # Servicios de aplicación
        self._publication_service = PublicationService(
            self._scopus_publications_repository,
            self._sjr_file_repository
        )
        self._subject_area_service = SubjectAreaService(
            self._scopus_subject_areas_repository,  # Para obtener datos de Scopus
            self._subject_areas_repo  # Para mapear usando CSV
        )
        self._department_service = DepartmentService(self._departments_repo)
        self._cargo_service = CargoService(self._cargos_repo)
        
        # Controladores
        self._publication_controller = PublicationsController(self._publication_service)
        self._subject_area_controller = SubjectAreasController(self._subject_area_service)
        self._departments_controller = DepartmentsController(self._department_service)
        self._cargos_controller = CargosController(self._cargo_service)
        self._report_controller = ReportsController(
            self._publication_service,
            self._subject_area_service
        )
    
    @property
    def publications_controller(self) -> PublicationsController:
        """Obtiene el controlador de publicaciones."""
        return self._publication_controller
    
    @property
    def subject_areas_controller(self) -> SubjectAreasController:
        """Obtiene el controlador de áreas temáticas."""
        return self._subject_area_controller
    
    @property
    def reports_controller(self) -> ReportsController:
        """Obtiene el controlador de reportes."""
        return self._report_controller
    
    @property
    def departments_controller(self) -> DepartmentsController:
        """Obtiene el controlador de departamentos."""
        return self._departments_controller
    
    @property
    def cargos_controller(self) -> CargosController:
        """Obtiene el controlador de cargos."""
        return self._cargos_controller


# Instancia global del contenedor
container = DependencyContainer()