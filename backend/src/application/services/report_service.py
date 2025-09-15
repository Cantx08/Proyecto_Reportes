from typing import List
from backend.src.domain.entities.publication import Publication
from ..interfaces.i_report import IReportGenerator
from ...domain.value_objects.report import (AuthorInfo, ReportConfiguration, PublicationCollections, PublicationsStatistics, Gender, Authority)
from ...infrastructure.style_manager import ReportLabStyleManager
from ...infrastructure.chart_generator import MatplotlibChartGenerator
from ...infrastructure.publication_formatter import ReportLabPublicationFormatter
from ...infrastructure.content_builder import ReportLabContentBuilder
from ...infrastructure.pdf_generator import ReportLabReportGenerator


class ReportService:
    """Servicio de aplicación para generar reportes de certificación."""
    
    def __init__(self):
        self._report_generator = self._initialize_dependencies()
    
    def _initialize_dependencies(self) -> IReportGenerator:
        """Configura las dependencias siguiendo el patrón de inyección de dependencias."""
        # Configurar componentes de infraestructura
        style_manager = ReportLabStyleManager()
        chart_generator = MatplotlibChartGenerator()
        publication_formatter = ReportLabPublicationFormatter(style_manager)
        content_builder = ReportLabContentBuilder(style_manager, chart_generator, publication_formatter)
        
        # Crear generador principal
        return ReportLabReportGenerator(content_builder)
    
    def generate_report(
        self,
        # Información del docente
        author_name: str,
        author_gender: str,
        department: str,
        role: str,
        
        # Configuración del reporte
        memorandum: str = "",
        signatory: int = 1,
        report_date: str = "",
        
        # Publicaciones
        scopus_publications: List[Publication] = None,
        wos_publications: List[Publication] = None,
        regional_publications: List[Publication] = None,
        event_memory: List[Publication] = None,
        book_chapters: List[Publication] = None,
        
        # Estadísticas
        subject_areas: List[str] = None,
        documents_by_year: dict = None
    ) -> bytes:
        """
        Genera un reporte de certificación de publicaciones en formato PDF.
        
        Args:
            docente_nombre: Nombre completo del docente
            docente_genero: Género del docente ("M" o "F")
            departamento: Departamento al que pertenece
            cargo: Cargo del docente
            memorando: Número de memorando (opcional)
            firmante: Tipo de firmante (1: Directora, 2: Vicerrector)
            fecha: Fecha del reporte (opcional, usa fecha actual si no se proporciona)
            publicaciones_scopus: Lista de publicaciones Scopus
            publicaciones_wos: Lista de publicaciones WOS
            publicaciones_regionales: Lista de publicaciones regionales
            memorias_eventos: Lista de memorias de eventos
            libros_capitulos: Lista de libros y capítulos
            areas_tematicas: Lista de áreas temáticas
            documentos_por_anio: Diccionario con documentos por año
            
        Returns:
            bytes: Contenido del PDF generado
            
        Raises:
            ValueError: Si faltan datos requeridos
        """
        # Validar datos de entrada
        self._check_input_data(author_name, author_gender, department, role)
        
        # Crear value objects
        author_info = self._create_author_profile(author_name, author_gender, department, role)
        config = self._create_report_configuration(memorandum, signatory, report_date)
        publications = self._create_publication_collections(
            scopus_publications, wos_publications, regional_publications,
            event_memory, book_chapters
        )
        statistics = self._create_publication_statistics(subject_areas, documents_by_year)

        # Generar reporte
        return self._report_generator.generate_report(author_info, config, publications, statistics)
    
    def _check_input_data(self, name: str, gender: str, department: str, role: str) -> None:
        """Valida que los datos de entrada sean correctos."""
        if not name or not name.strip():
            raise ValueError("El nombre del docente es requerido")
        
        if gender not in ["M", "F"]:
            raise ValueError("El género debe ser 'M' o 'F'")
        
        if not department or not department.strip():
            raise ValueError("El departamento es requerido")
        
        if not role or not role.strip():
            raise ValueError("El cargo es requerido")

    def _create_author_profile(self, name: str, gender: str, department: str, role: str) -> AuthorInfo:
        """Crea el value object DocenteInfo."""
        gender_enum = Gender.MASCULINO if gender == "M" else Gender.FEMENINO
        return AuthorInfo(
            name=name.strip(),
            gender=gender_enum,
            department=department.strip(),
            role=role.strip()
        )

    def _create_report_configuration(self, memorandum: str, signatory: int, date: str) -> ReportConfiguration:
        """Crea el value object ConfiguracionReporte."""
        signatory_type = Authority.DIRECTORA_INVESTIGACION if signatory == 1 else Authority.VICERRECTOR_INVESTIGACION

        if date and date.strip():
            return ReportConfiguration(memorandum.strip(), signatory_type, date.strip())
        else:
            return ReportConfiguration.generate_with_current_date(memorandum.strip(), signatory_type)

    def _create_publication_collections(
        self,
        scopus: List[Publication] = None,
        wos: List[Publication] = None,
        regionals: List[Publication] = None,
        memories: List[Publication] = None,
        books: List[Publication] = None
    ) -> PublicationCollections:
        """Crea el value object ColeccionesPublicaciones."""
        return PublicationCollections(
            scopus=scopus or [],
            wos=wos or [],
            regional_publications=regionals or [],
            memories=memories or [],
            books=books or []
        )
    
    def _generate_publication_statistics(
        self, 
        subject_areas: List[str] = None, 
        publications_by_year: dict = None
    ) -> PublicationsStatistics:
        """Crea el value object EstadisticasPublicaciones."""
        return PublicationsStatistics(
            subject_areas=subject_areas or [],
            publications_by_year=publications_by_year or {}
        )
