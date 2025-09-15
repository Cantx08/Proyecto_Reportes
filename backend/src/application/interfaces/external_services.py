from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from ..entities.publication import Publication
from ..value_objects.scopus_id import ScopusId


class ScopusService(ABC):
    """
    Interface para el servicio de Scopus API.
    
    Define los contratos para obtener datos de Scopus.
    """

    @abstractmethod
    async def get_author_publications(self, scopus_id: ScopusId) -> List[Publication]:
        """
        Obtiene las publicaciones de un autor desde Scopus.
        
        Args:
            scopus_id: ID de Scopus del autor
            
        Returns:
            List[Publication]: Lista de publicaciones del autor
        """
        pass

    @abstractmethod
    async def get_publication_details(self, scopus_id: str) -> Optional[Publication]:
        """
        Obtiene los detalles de una publicación específica.
        
        Args:
            scopus_id: ID de Scopus de la publicación
            
        Returns:
            Optional[Publication]: Detalles de la publicación o None
        """
        pass

    @abstractmethod
    async def search_publications(self, query: str, limit: int = 100) -> List[Publication]:
        """
        Busca publicaciones por criterios específicos.
        
        Args:
            query: Consulta de búsqueda
            limit: Límite de resultados
            
        Returns:
            List[Publication]: Lista de publicaciones encontradas
        """
        pass

    @abstractmethod
    async def get_author_profile(self, scopus_id: ScopusId) -> Dict:
        """
        Obtiene el perfil completo de un autor.
        
        Args:
            scopus_id: ID de Scopus del autor
            
        Returns:
            Dict: Información del perfil del autor
        """
        pass

    @abstractmethod
    async def verify_scopus_id(self, scopus_id: ScopusId) -> bool:
        """
        Verifica si un ID de Scopus es válido.
        
        Args:
            scopus_id: ID de Scopus a verificar
            
        Returns:
            bool: True si el ID es válido
        """
        pass


class PDFService(ABC):
    """
    Interface para el servicio de generación de PDFs.
    
    Define los contratos para generar reportes en PDF.
    """

    @abstractmethod
    async def generate_draft_report(self, data: Dict) -> bytes:
        """
        Genera un reporte borrador sin encabezados institucionales.
        
        Args:
            data: Datos del reporte
            
        Returns:
            bytes: Contenido del PDF generado
        """
        pass

    @abstractmethod
    async def generate_final_report(self, data: Dict) -> bytes:
        """
        Genera un reporte final con encabezados institucionales.
        
        Args:
            data: Datos del reporte
            
        Returns:
            bytes: Contenido del PDF generado
        """
        pass

    @abstractmethod
    async def validate_template(self, template_path: str) -> bool:
        """
        Valida si una plantilla de PDF es válida.
        
        Args:
            template_path: Ruta de la plantilla
            
        Returns:
            bool: True si la plantilla es válida
        """
        pass


class ChartService(ABC):
    """
    Interface para el servicio de generación de gráficos.
    
    Define los contratos para generar gráficos y visualizaciones.
    """

    @abstractmethod
    async def generate_publications_by_year_chart(self, data: Dict[int, int]) -> bytes:
        """
        Genera gráfico de publicaciones por año.
        
        Args:
            data: Diccionario año -> cantidad de publicaciones
            
        Returns:
            bytes: Imagen del gráfico generado
        """
        pass

    @abstractmethod
    async def generate_subject_areas_chart(self, data: Dict[str, int]) -> bytes:
        """
        Genera gráfico de áreas temáticas.
        
        Args:
            data: Diccionario área -> cantidad de publicaciones
            
        Returns:
            bytes: Imagen del gráfico generado
        """
        pass

    @abstractmethod
    async def generate_quartile_distribution_chart(self, data: Dict[str, int]) -> bytes:
        """
        Genera gráfico de distribución por cuartiles SJR.
        
        Args:
            data: Diccionario cuartil -> cantidad de publicaciones
            
        Returns:
            bytes: Imagen del gráfico generado
        """
        pass

    @abstractmethod
    async def generate_document_types_chart(self, data: Dict[str, int]) -> bytes:
        """
        Genera gráfico de tipos de documentos.
        
        Args:
            data: Diccionario tipo -> cantidad de publicaciones
            
        Returns:
            bytes: Imagen del gráfico generado
        """
        pass


class EmailService(ABC):
    """
    Interface para el servicio de notificaciones por email.
    
    Define los contratos para envío de notificaciones.
    """

    @abstractmethod
    async def send_report_generated_notification(self, recipient: str, report_path: str) -> bool:
        """
        Envía notificación de reporte generado.
        
        Args:
            recipient: Email del destinatario
            report_path: Ruta del reporte generado
            
        Returns:
            bool: True si se envió correctamente
        """
        pass

    @abstractmethod
    async def send_sync_completed_notification(self, recipient: str, stats: Dict) -> bool:
        """
        Envía notificación de sincronización completada.
        
        Args:
            recipient: Email del destinatario
            stats: Estadísticas de la sincronización
            
        Returns:
            bool: True si se envió correctamente
        """
        pass