"""
Interfaces y contratos para el sistema de reportes.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..domain.entities import Publicacion
from ..domain.value_objects import DocenteInfo, ConfiguracionReporte, EstadisticasPublicaciones, ColeccionesPublicaciones


class IChartGenerator(ABC):
    """Interface para generadores de gráficos."""
    
    @abstractmethod
    def generar_grafico_tendencias(self, documentos_por_anio: Dict[str, int], docente_nombre: str) -> bytes:
        """Genera un gráfico de tendencias por año."""
        pass


class IStyleManager(ABC):
    """Interface para manejo de estilos de documento."""
    
    @abstractmethod
    def obtener_estilo(self, nombre: str) -> Any:
        """Obtiene un estilo por nombre."""
        pass
    
    @abstractmethod
    def configurar_estilos_personalizados(self) -> None:
        """Configura estilos personalizados."""
        pass


class IContentBuilder(ABC):
    """Interface para construcción de contenido del reporte."""
    
    @abstractmethod
    def construir_encabezado(self, docente: DocenteInfo, config: ConfiguracionReporte) -> List[Any]:
        """Construye el encabezado del documento."""
        pass
    
    @abstractmethod
    def construir_resumen(self, docente: DocenteInfo, config: ConfiguracionReporte, 
                         publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la sección de resumen."""
        pass
    
    @abstractmethod
    def construir_informe_tecnico(self, docente: DocenteInfo, 
                                 publicaciones: ColeccionesPublicaciones,
                                 estadisticas: EstadisticasPublicaciones) -> List[Any]:
        """Construye la sección de informe técnico."""
        pass
    
    @abstractmethod
    def construir_conclusion(self, docente: DocenteInfo, config: ConfiguracionReporte,
                           publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la sección de conclusión."""
        pass
    
    @abstractmethod
    def construir_firmas(self, config: ConfiguracionReporte) -> List[Any]:
        """Construye la sección de firmas."""
        pass


class IReportGenerator(ABC):
    """Interface principal para generación de reportes."""
    
    @abstractmethod
    def generar_reporte(self, docente: DocenteInfo, config: ConfiguracionReporte,
                       publicaciones: ColeccionesPublicaciones, 
                       estadisticas: EstadisticasPublicaciones) -> bytes:
        """Genera el reporte completo en formato PDF."""
        pass


class IPublicationFormatter(ABC):
    """Interface para formateo de publicaciones."""
    
    @abstractmethod
    def formatear_lista_publicaciones(self, publicaciones: List[Publicacion], tipo: str) -> List[Any]:
        """Formatea una lista de publicaciones."""
        pass
    
    @abstractmethod
    def obtener_distribucion_tipos(self, publicaciones: List[Publicacion]) -> str:
        """Obtiene la distribución de tipos de documentos."""
        pass
