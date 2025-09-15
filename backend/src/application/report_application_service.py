"""
Servicio de aplicación para generación de reportes de certificación.
Implementa Clean Architecture y principios SOLID.
"""
from typing import List
from ..domain.entities import Publicacion
from ..domain.interfaces import IReportGenerator
from ..domain.value_objects import (
    DocenteInfo, ConfiguracionReporte, ColeccionesPublicaciones, 
    EstadisticasPublicaciones, Genero, TipoFirmante
)
from ..infrastructure.style_manager import ReportLabStyleManager
from ..infrastructure.chart_generator import MatplotlibChartGenerator
from ..infrastructure.publication_formatter import ReportLabPublicationFormatter
from ..infrastructure.content_builder import ReportLabContentBuilder
from ..infrastructure.pdf_generator import ReportLabReportGenerator


class ReportApplicationService:
    """Servicio de aplicación para generar reportes de certificación."""
    
    def __init__(self):
        self._report_generator = self._configurar_dependencias()
    
    def _configurar_dependencias(self) -> IReportGenerator:
        """Configura las dependencias siguiendo el patrón de inyección de dependencias."""
        # Configurar componentes de infraestructura
        style_manager = ReportLabStyleManager()
        chart_generator = MatplotlibChartGenerator()
        publication_formatter = ReportLabPublicationFormatter(style_manager)
        content_builder = ReportLabContentBuilder(style_manager, chart_generator, publication_formatter)
        
        # Crear generador principal
        return ReportLabReportGenerator(content_builder)
    
    def generar_reporte_certificacion(
        self,
        # Información del docente
        docente_nombre: str,
        docente_genero: str,
        departamento: str,
        cargo: str,
        
        # Configuración del reporte
        memorando: str = "",
        firmante: int = 1,
        fecha: str = "",
        
        # Publicaciones
        publicaciones_scopus: List[Publicacion] = None,
        publicaciones_wos: List[Publicacion] = None,
        publicaciones_regionales: List[Publicacion] = None,
        memorias_eventos: List[Publicacion] = None,
        libros_capitulos: List[Publicacion] = None,
        
        # Estadísticas
        areas_tematicas: List[str] = None,
        documentos_por_anio: dict = None
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
        self._validar_datos_entrada(docente_nombre, docente_genero, departamento, cargo)
        
        # Crear value objects
        docente = self._crear_docente_info(docente_nombre, docente_genero, departamento, cargo)
        config = self._crear_configuracion_reporte(memorando, firmante, fecha)
        publicaciones = self._crear_colecciones_publicaciones(
            publicaciones_scopus, publicaciones_wos, publicaciones_regionales,
            memorias_eventos, libros_capitulos
        )
        estadisticas = self._crear_estadisticas_publicaciones(areas_tematicas, documentos_por_anio)
        
        # Generar reporte
        return self._report_generator.generar_reporte(docente, config, publicaciones, estadisticas)
    
    def _validar_datos_entrada(self, nombre: str, genero: str, departamento: str, cargo: str) -> None:
        """Valida que los datos de entrada sean correctos."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del docente es requerido")
        
        if genero not in ["M", "F"]:
            raise ValueError("El género debe ser 'M' o 'F'")
        
        if not departamento or not departamento.strip():
            raise ValueError("El departamento es requerido")
        
        if not cargo or not cargo.strip():
            raise ValueError("El cargo es requerido")
    
    def _crear_docente_info(self, nombre: str, genero: str, departamento: str, cargo: str) -> DocenteInfo:
        """Crea el value object DocenteInfo."""
        genero_enum = Genero.MASCULINO if genero == "M" else Genero.FEMENINO
        return DocenteInfo(
            nombre=nombre.strip(),
            genero=genero_enum,
            departamento=departamento.strip(),
            cargo=cargo.strip()
        )
    
    def _crear_configuracion_reporte(self, memorando: str, firmante: int, fecha: str) -> ConfiguracionReporte:
        """Crea el value object ConfiguracionReporte."""
        tipo_firmante = TipoFirmante.DIRECTORA_INVESTIGACION if firmante == 1 else TipoFirmante.VICERRECTOR_INVESTIGACION
        
        if fecha and fecha.strip():
            return ConfiguracionReporte(memorando.strip(), tipo_firmante, fecha.strip())
        else:
            return ConfiguracionReporte.crear_con_fecha_actual(memorando.strip(), tipo_firmante)
    
    def _crear_colecciones_publicaciones(
        self, 
        scopus: List[Publicacion] = None,
        wos: List[Publicacion] = None,
        regionales: List[Publicacion] = None,
        memorias: List[Publicacion] = None,
        libros: List[Publicacion] = None
    ) -> ColeccionesPublicaciones:
        """Crea el value object ColeccionesPublicaciones."""
        return ColeccionesPublicaciones(
            scopus=scopus or [],
            wos=wos or [],
            regionales=regionales or [],
            memorias=memorias or [],
            libros=libros or []
        )
    
    def _crear_estadisticas_publicaciones(
        self, 
        areas_tematicas: List[str] = None, 
        documentos_por_anio: dict = None
    ) -> EstadisticasPublicaciones:
        """Crea el value object EstadisticasPublicaciones."""
        return EstadisticasPublicaciones(
            areas_tematicas=areas_tematicas or [],
            documentos_por_anio=documentos_por_anio or {}
        )
