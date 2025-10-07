"""
Configuración de dependencias e inyección de dependencias.
"""
import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

# Servicios de aplicación
from .application.services.subject_area_service import SubjectAreaService
from .application.services.publication_service import PublicationService
from .application.services.cargo_service import CargoService
from .application.services.legacy_department_service import LegacyDepartmentService
from .application.services.author_service import AuthorService
from .application.services.position_service import PositionService  
from .application.services.scopus_account_service import ScopusAccountService
from .application.services.department_service_new import DepartmentService as NewDepartmentService

# Controladores
from .infrastructure.api.controllers.reports_controller import ReportsController
from .infrastructure.api.controllers.subject_areas_controller import SubjectAreasController
from .infrastructure.api.controllers.publications_controller import PublicationsController
from .infrastructure.api.controllers.departments_controller import DepartmentsController as LegacyDepartmentsController
from .infrastructure.api.controllers.cargos_controller import CargosController
from .infrastructure.api.controllers.authors_controller import AuthorsController
from .infrastructure.api.controllers.positions_controller import PositionsController
from .infrastructure.api.controllers.scopus_accounts_controller import ScopusAccountsController
from .infrastructure.api.controllers.new_departments_controller import NewDepartmentsController

# Repositorios CSV
from .infrastructure.repositories.sjr_file_repository import SJRFileRepository
from .infrastructure.repositories.subject_areas_file_repository import SubjectAreasFileRepository
from .infrastructure.repositories.departments_file_repository import DepartmentsFileRepository
from .infrastructure.repositories.cargos_file_repository import CargosFileRepository
from .infrastructure.repositories.author_file_repository import AuthorFileRepository
from .infrastructure.repositories.department_file_repository import DepartmentFileRepository
from .infrastructure.repositories.position_file_repository import PositionFileRepository
from .infrastructure.repositories.scopus_account_file_repository import ScopusAccountFileRepository
from .infrastructure.external.scopus_api_client import ScopusApiClient
from .infrastructure.repositories.scopus_publication_repository import ScopusPublicationsRepository
from .infrastructure.repositories.scopus_subject_areas_repository import ScopusSubjectAreasRepository

load_dotenv()

# Obtener el directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    """Configuración de la aplicación."""
    scopus_api_key: str = os.getenv("SCOPUS_API_KEY", "")
    sjr_csv_path: str = os.getenv("SJR_CSV_PATH", str(BASE_DIR / "data" / "df_sjr_24_04_2025.csv"))
    areas_csv_path: str = os.getenv("AREAS_CSV_PATH", str(BASE_DIR / "data" / "areas_categories.csv"))
    departments_csv_path: str = os.getenv("DEPARTMENTS_CSV_PATH", str(BASE_DIR / "data" / "deps.csv"))
    authors_csv_path: str = os.getenv("AUTHORS_CSV_PATH", str(BASE_DIR / "data" / "docentes.csv"))
    positions_csv_path: str = os.getenv("POSITIONS_CSV_PATH", str(BASE_DIR / "data" / "cargos.csv"))
    scopus_accounts_csv_path: str = os.getenv("SCOPUS_ACCOUNTS_CSV_PATH", str(BASE_DIR / "data" / "scopus_accounts.csv"))


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
        
        # Repositorios Scopus/externos
        self._scopus_publications_repository = ScopusPublicationsRepository(self._scopus_client)
        self._scopus_subject_areas_repository = ScopusSubjectAreasRepository(self._scopus_client)
        self._sjr_file_repository = SJRFileRepository(self._settings.sjr_csv_path)
        self._subject_areas_repo = SubjectAreasFileRepository(self._settings.areas_csv_path)
        
        # Repositorios CSV legacy (para compatibilidad)
        self._departments_repo_old = DepartmentsFileRepository()
        self._cargos_repo = CargosFileRepository()
        
        # Nuevos repositorios CSV
        self._author_repo = AuthorFileRepository(self._settings.authors_csv_path)
        self._department_repo = DepartmentFileRepository(self._settings.departments_csv_path)
        self._position_repo = PositionFileRepository(self._settings.positions_csv_path)
        self._scopus_account_repo = ScopusAccountFileRepository(self._settings.scopus_accounts_csv_path)
        
        # Servicios de aplicación legacy
        self._publication_service = PublicationService(
            self._scopus_publications_repository,
            self._sjr_file_repository
        )
        self._subject_area_service = SubjectAreaService(
            self._scopus_subject_areas_repository,  # Para obtener datos de Scopus
            self._subject_areas_repo  # Para mapear usando CSV
        )
        self._department_service_old = LegacyDepartmentService(self._departments_repo_old)
        self._cargo_service = CargoService(self._cargos_repo)
        
        # Nuevos servicios de aplicación
        self._author_service = AuthorService(self._author_repo)
        self._department_service = NewDepartmentService(self._department_repo)  
        self._position_service = PositionService(self._position_repo)
        self._scopus_account_service = ScopusAccountService(self._scopus_account_repo)
        
        # Controladores legacy
        self._publication_controller = PublicationsController(self._publication_service)
        self._subject_area_controller = SubjectAreasController(self._subject_area_service)
        self._departments_controller_old = LegacyDepartmentsController(self._department_service_old)
        self._cargos_controller = CargosController(self._cargo_service)
        self._report_controller = ReportsController(
            self._publication_service,
            self._subject_area_service
        )
        
        # Nuevos controladores
        self._authors_controller = AuthorsController(self._author_service)
        self._departments_controller = NewDepartmentsController(self._department_service)
        self._positions_controller = PositionsController(self._position_service)
        self._scopus_accounts_controller = ScopusAccountsController(self._scopus_account_service)
    
    # Controladores legacy
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
    def departments_controller_old(self) -> LegacyDepartmentsController:
        """Obtiene el controlador de departamentos legacy."""
        return self._departments_controller_old
    
    @property
    def cargos_controller(self) -> CargosController:
        """Obtiene el controlador de cargos legacy."""
        return self._cargos_controller
    
    # Nuevos controladores
    @property
    def authors_controller(self) -> AuthorsController:
        """Obtiene el controlador de autores."""
        return self._authors_controller
    
    @property
    def departments_controller(self) -> NewDepartmentsController:
        """Obtiene el controlador de departamentos."""
        return self._departments_controller
    
    @property
    def positions_controller(self) -> PositionsController:
        """Obtiene el controlador de posiciones."""
        return self._positions_controller
    
    @property
    def scopus_accounts_controller(self) -> ScopusAccountsController:
        """Obtiene el controlador de cuentas Scopus."""
        return self._scopus_accounts_controller


# Instancia global del contenedor
container = DependencyContainer()