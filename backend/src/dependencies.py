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
from .application.services.author_service import AuthorService
from .application.services.position_service import PositionService
from .application.services.scopus_account_service import ScopusAccountService
from .application.services.department_service import DepartmentService
from .application.services.draft_processor_service import DraftProcessorService

# Controladores
from .infrastructure.api.controllers.reports_controller import ReportsController
from .infrastructure.api.controllers.subject_areas_controller import SubjectAreasController
from .infrastructure.api.controllers.publications_controller import PublicationsController
from .infrastructure.api.controllers.authors_controller import AuthorsController
from .infrastructure.api.controllers.positions_controller import PositionsController
from .infrastructure.api.controllers.scopus_accounts_controller import ScopusAccountsController
from .infrastructure.api.controllers.departments_controller import DepartmentsController
from .infrastructure.api.controllers.draft_processor_controller import DraftProcessorController

# Repositorios de base de datos
from .infrastructure.repositories.author_db_repository import AuthorDatabaseRepository
from .infrastructure.repositories.department_db_repository import DepartmentDatabaseRepository
from .infrastructure.repositories.position_db_repository import PositionDatabaseRepository
from .infrastructure.repositories.scopus_account_db_repository import ScopusAccountDBRepository

# Repositorios CSV (para datos que aún no están en BD)
from .infrastructure.repositories.sjr_file_repository import SJRFileRepository
from .infrastructure.repositories.subject_areas_file_repository import SubjectAreasFileRepository
from .infrastructure.repositories.scopus_account_file_repository import ScopusAccountFileRepository

# Clientes y conexiones
from .infrastructure.external.scopus_api_client import ScopusApiClient
from .infrastructure.repositories.scopus_publication_repository import ScopusPublicationsRepository
from .infrastructure.repositories.scopus_subject_areas_repository import ScopusSubjectAreasRepository
from .infrastructure.database.connection import DatabaseConfig
from .infrastructure.repositories.report.template_overlay_service import TemplateOverlayService

load_dotenv()

# Obtener el directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    """Configuración de la aplicación."""
    scopus_api_key: str = os.getenv("SCOPUS_API_KEY", "")
    sjr_csv_path: str = os.getenv("SJR_CSV_PATH", str(BASE_DIR / "data" / "df_sjr_24_04_2025.csv"))
    areas_csv_path: str = os.getenv("AREAS_CSV_PATH", str(BASE_DIR / "data" / "areas_categories.csv"))
    scopus_accounts_csv_path: str = os.getenv("SCOPUS_ACCOUNTS_CSV_PATH",
                                              str(BASE_DIR / "data" / "scopus_accounts.csv"))


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
        # Configuración de base de datos (usa variables de entorno del .env)
        self._db_config = DatabaseConfig()
        
        # No crear tablas aquí para evitar problemas de orden
        # Las tablas se crearán con un script separado o manualmente
        # self._db_config.create_tables()
        
        # Clientes externos
        self._scopus_client = ScopusApiClient(self._settings.scopus_api_key)

        # Repositorios Scopus/externos
        self._scopus_publications_repository = ScopusPublicationsRepository(self._scopus_client)
        self._scopus_subject_areas_repository = ScopusSubjectAreasRepository(self._scopus_client)
        self._sjr_file_repository = SJRFileRepository(self._settings.sjr_csv_path)
        self._subject_areas_repo = SubjectAreasFileRepository(self._settings.areas_csv_path)

        # Repositorios de base de datos (reemplazan CSV para autores, departamentos y cargos)
        self._author_repo = AuthorDatabaseRepository(self._db_config)
        self._department_repo = DepartmentDatabaseRepository(self._db_config)
        self._position_repo = PositionDatabaseRepository(self._db_config)
        self._scopus_account_repo = ScopusAccountDBRepository(self._db_config)

        # Servicios de aplicación
        self._publication_service = PublicationService(
            self._scopus_publications_repository,
            self._sjr_file_repository,
            self._scopus_account_repo
        )
        self._subject_area_service = SubjectAreaService(
            self._scopus_subject_areas_repository,  # Para obtener datos de Scopus
            self._subject_areas_repo,  # Para mapear usando CSV
            self._scopus_account_repo  # Para resolver Author IDs a Scopus IDs
        )
        self._author_service = AuthorService(self._author_repo)
        self._department_service = DepartmentService(self._department_repo)
        self._position_service = PositionService(self._position_repo)
        self._scopus_account_service = ScopusAccountService(self._scopus_account_repo)

        # Servicio de procesamiento de borradores
        self._template_overlay_service = TemplateOverlayService()
        self._draft_processor_service = DraftProcessorService(self._template_overlay_service)

        # Controladores legacy
        self._publication_controller = PublicationsController(self._publication_service)
        self._subject_area_controller = SubjectAreasController(self._subject_area_service)
        self._report_controller = ReportsController(
            self._publication_service,
            self._subject_area_service
        )
        self._authors_controller = AuthorsController(self._author_service)
        self._departments_controller = DepartmentsController(self._department_service)
        self._positions_controller = PositionsController(self._position_service)
        self._scopus_accounts_controller = ScopusAccountsController(self._scopus_account_service)
        self._draft_processor_controller = DraftProcessorController(self._draft_processor_service)

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
    def authors_controller(self) -> AuthorsController:
        """Obtiene el controlador de autores."""
        return self._authors_controller

    @property
    def departments_controller(self) -> DepartmentsController:
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

    @property
    def draft_processor_controller(self) -> DraftProcessorController:
        """Obtiene el controlador de procesamiento de borradores."""
        return self._draft_processor_controller


# Instancia global del contenedor
container = DependencyContainer()
