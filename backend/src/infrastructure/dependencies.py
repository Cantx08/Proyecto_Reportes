"""
Configuración de dependencias e inyección de dependencias.

Este módulo implementa el patrón de Composición Root (Composition Root)
de Clean Architecture, donde se ensamblan todas las dependencias de la aplicación.

Principios seguidos:
- Inversión de Dependencias (DIP): Los servicios de aplicación dependen de abstracciones
- Single Responsibility: Cada método configura un tipo específico de dependencia
- Open/Closed: Fácil de extender sin modificar el código existente
"""
import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

# ============================================================================
# SERVICIOS DE APLICACIÓN (Application Layer)
# Dependen de abstracciones definidas en Domain
# ============================================================================
from src.application.services.subject_area_service import SubjectAreaService
from src.application.services.publication_service import PublicationService
from src.application.services.author_service import AuthorService
from src.application.services.scopus_account_service import ScopusAccountService
from src.application.services.draft_processor_service import DraftProcessorService
from src.application.services.report_service import ReportService

# ============================================================================
# CONTROLADORES (Infrastructure Layer - API/Presentation)
# Orquestan la comunicación entre HTTP y los servicios de aplicación
# ============================================================================
from src.infrastructure.api.controllers.reports_controller import ReportsController
from src.infrastructure.api.controllers.subject_areas_controller import SubjectAreasController
from src.infrastructure.api.controllers.publications_controller import PublicationsController
from src.infrastructure.api.controllers.authors_controller import AuthorsController
from src.infrastructure.api.controllers.scopus_accounts_controller import ScopusAccountsController
from src.infrastructure.api.controllers.draft_processor_controller import DraftProcessorController

# ============================================================================
# REPOSITORIOS - IMPLEMENTACIONES (Infrastructure Layer)
# Implementan las interfaces definidas en Domain
# ============================================================================
# Base de datos
from src.infrastructure.repositories.author_db_repository import AuthorDatabaseRepository
from src.infrastructure.repositories.scopus_account_db_repository import ScopusAccountDBRepository

# Archivos (datos estáticos/externos)
from src.infrastructure.repositories.sjr_file_repository import SJRFileRepository
from src.infrastructure.repositories.subject_areas_file_repository import SubjectAreasFileRepository

# APIs externas
from src.infrastructure.external.scopus_api_client import ScopusApiClient
from src.infrastructure.repositories.scopus_publication_repository import ScopusPublicationsRepository
from src.infrastructure.repositories.scopus_subject_areas_repository import ScopusSubjectAreasRepository

# ============================================================================
# COMPONENTES DE INFRAESTRUCTURA
# Implementaciones concretas de interfaces de dominio
# ============================================================================
from src.infrastructure.database.connection import DatabaseConfig
from src.infrastructure.repositories.report.template_overlay_service import TemplateOverlayService
from src.infrastructure.repositories.report.style_manager import ReportLabStyleManager
from src.infrastructure.repositories.report.chart_generator import MatplotlibChartGenerator
from src.infrastructure.repositories.report.publication_formatter import ReportLabPublicationFormatter
from src.infrastructure.repositories.report.content_builder import ReportLabContentBuilder
from src.infrastructure.repositories.report.pdf_generator import ReportLabReportGenerator

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
    """
    Contenedor de dependencias siguiendo el patrón Composition Root.

    Responsabilidades:
    - Crear y configurar todas las dependencias de la aplicación
    - Ensamblar las capas siguiendo Clean Architecture
    - Proveer acceso a los controladores para los endpoints

    Flujo de dependencias (de adentro hacia afuera):
    Domain ← Application ← Infrastructure
    """

    def __init__(self):
        self._settings = get_settings()
        self._setup_dependencies()

    def _setup_dependencies(self):
        """
        Orquesta la configuración de todas las dependencias.
        El orden es importante: primero infraestructura, luego aplicación.
        """
        self._setup_infrastructure()
        self._setup_repositories()
        self._setup_application_services()
        self._setup_controllers()

    # =========================================================================
    # SETUP INFRASTRUCTURE (Capa más externa)
    # =========================================================================
    def _setup_infrastructure(self):
        """Configura componentes de infraestructura base."""
        # Base de datos
        self._db_config = DatabaseConfig()

        # Cliente API externa (Scopus)
        self._scopus_client = ScopusApiClient(self._settings.scopus_api_key)

    # =========================================================================
    # SETUP REPOSITORIES (Implementaciones de interfaces de Domain)
    # =========================================================================
    def _setup_repositories(self):
        """
        Configura los repositorios que implementan las interfaces de Domain.
        Estos proveen acceso a datos desde diferentes fuentes.
        """
        # Repositorios de Base de Datos (Implementan interfaces de Domain)
        self._author_repo = AuthorDatabaseRepository(self._db_config)
        self._scopus_account_repo = ScopusAccountDBRepository(self._db_config)

        # Repositorios de Archivos (datos estáticos/externos)
        self._sjr_file_repository = SJRFileRepository(self._settings.sjr_csv_path)
        self._subject_areas_repo = SubjectAreasFileRepository(self._settings.areas_csv_path)

        # Repositorios de API Externa (Scopus)
        self._scopus_publications_repository = ScopusPublicationsRepository(self._scopus_client)
        self._scopus_subject_areas_repository = ScopusSubjectAreasRepository(self._scopus_client)

        # Componentes de generación de reportes (implementan IReportGenerator y relacionados)
        self._setup_report_components()

    def _setup_report_components(self):
        """
        Configura los componentes de generación de reportes.
        Sigue el patrón de composición para construir el generador de reportes.
        """
        # Componentes base
        self._style_manager = ReportLabStyleManager()
        self._chart_generator = MatplotlibChartGenerator()

        # Componentes compuestos
        self._publication_formatter = ReportLabPublicationFormatter(self._style_manager)
        self._content_builder = ReportLabContentBuilder(
            self._style_manager,
            self._chart_generator,
            self._publication_formatter
        )

        # Generador principal (implementa IReportGenerator)
        self._report_generator = ReportLabReportGenerator(self._content_builder)

        # Servicio de plantillas (implementa ITemplateOverlayService)
        self._template_overlay_service = TemplateOverlayService()

    # =========================================================================
    # SETUP APPLICATION SERVICES (Capa de aplicación)
    # =========================================================================
    def _setup_application_services(self):
        """
        Configura los servicios de aplicación.
        Estos servicios orquestan la lógica de negocio usando repositorios.
        Dependen de abstracciones (interfaces), no de implementaciones.
        """
        # Servicios CRUD básicos
        self._author_service = AuthorService(self._author_repo)
        self._scopus_account_service = ScopusAccountService(self._scopus_account_repo)

        # Servicios de integración con Scopus
        self._publication_service = PublicationService(
            self._scopus_publications_repository,
            self._sjr_file_repository,
            self._scopus_account_repo
        )
        self._subject_area_service = SubjectAreaService(
            self._scopus_subject_areas_repository,
            self._subject_areas_repo,
            self._scopus_account_repo
        )

        # Servicios de generación de documentos
        self._report_service = ReportService(self._report_generator)
        self._draft_processor_service = DraftProcessorService(self._template_overlay_service)

    # =========================================================================
    # SETUP CONTROLLERS (Capa de presentación/API)
    # =========================================================================
    def _setup_controllers(self):
        """
        Configura los controladores que manejan las peticiones HTTP.
        Los controladores delegan a los servicios de aplicación.
        """
        # Controladores CRUD
        self._authors_controller = AuthorsController(self._author_service)
        self._scopus_accounts_controller = ScopusAccountsController(self._scopus_account_service)

        # Controladores de consulta Scopus
        self._publication_controller = PublicationsController(self._publication_service)
        self._subject_area_controller = SubjectAreasController(self._subject_area_service)

        # Controladores de generación de documentos
        self._report_controller = ReportsController(
            self._publication_service,
            self._subject_area_service,
            self._report_service
        )
        self._draft_processor_controller = DraftProcessorController(self._draft_processor_service)

    # =========================================================================
    # PROPIEDADES PÚBLICAS - Acceso a Controladores
    # =========================================================================
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
    def scopus_accounts_controller(self) -> ScopusAccountsController:
        """Obtiene el controlador de cuentas Scopus."""
        return self._scopus_accounts_controller

    @property
    def draft_processor_controller(self) -> DraftProcessorController:
        """Obtiene el controlador de procesamiento de borradores."""
        return self._draft_processor_controller

# Instancia global del contenedor
container = DependencyContainer()
