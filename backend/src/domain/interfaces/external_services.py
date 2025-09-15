"""
Interfaces para servicios externos.

Define los contratos que deben implementar los servicios externos
como APIs de Scopus, generadores de PDF, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from datetime import datetime


class ScopusAPIInterface(ABC):
    """Interfaz para el servicio de API de Scopus."""
    
    @abstractmethod
    def search_author_publications(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Busca publicaciones de un autor en Scopus.
        
        Args:
            params: Parámetros de búsqueda:
                - author_id: str - ID de Scopus del autor
                - start_year: int (opcional) - Año de inicio
                - end_year: int (opcional) - Año de fin
                - max_results: int (opcional) - Número máximo de resultados
                - include_citations: bool (opcional) - Incluir información de citaciones
                
        Returns:
            List[Dict[str, Any]]: Lista de publicaciones desde Scopus
        """
        pass
    
    @abstractmethod
    def search_publications_by_keywords(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Busca publicaciones por palabras clave.
        
        Args:
            params: Parámetros de búsqueda:
                - keywords: List[str] - Palabras clave
                - start_year: int (opcional) - Año de inicio
                - end_year: int (opcional) - Año de fin
                - subject_area: str (opcional) - Área temática
                - max_results: int (opcional) - Número máximo de resultados
                
        Returns:
            List[Dict[str, Any]]: Lista de publicaciones encontradas
        """
        pass
    
    @abstractmethod
    def get_publication_details(self, scopus_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene los detalles completos de una publicación.
        
        Args:
            scopus_id: ID de Scopus de la publicación
            
        Returns:
            Optional[Dict[str, Any]]: Detalles de la publicación o None si no se encuentra
        """
        pass
    
    @abstractmethod
    def get_author_details(self, author_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene los detalles de un autor.
        
        Args:
            author_id: ID de Scopus del autor
            
        Returns:
            Optional[Dict[str, Any]]: Detalles del autor o None si no se encuentra
        """
        pass
    
    @abstractmethod
    def verify_author_id(self, author_id: str) -> bool:
        """
        Verifica si un ID de autor existe en Scopus.
        
        Args:
            author_id: ID de Scopus del autor
            
        Returns:
            bool: True si el autor existe
        """
        pass


class PDFGeneratorInterface(ABC):
    """Interfaz para el generador de PDFs."""
    
    @abstractmethod
    def generate_report(self, report_data: Dict[str, Any]) -> bytes:
        """
        Genera un reporte en formato PDF.
        
        Args:
            report_data: Datos del reporte:
                - title: str - Título del reporte
                - author_info: Dict - Información del autor
                - publications: List[Dict] - Lista de publicaciones
                - statistics: Dict - Estadísticas
                - template_config: Dict - Configuración de plantilla
                - include_charts: bool - Incluir gráficos
                - include_abstracts: bool - Incluir resúmenes
                
        Returns:
            bytes: Contenido del PDF generado
        """
        pass
    
    @abstractmethod
    def generate_certificate(self, certificate_data: Dict[str, Any]) -> bytes:
        """
        Genera un certificado en formato PDF.
        
        Args:
            certificate_data: Datos del certificado
            
        Returns:
            bytes: Contenido del PDF del certificado
        """
        pass


class ChartGeneratorInterface(ABC):
    """Interfaz para el generador de gráficos."""
    
    @abstractmethod
    def generate_publications_by_year_chart(
        self, 
        data: Dict[int, int], 
        config: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Genera un gráfico de publicaciones por año.
        
        Args:
            data: Diccionario con año -> número de publicaciones
            config: Configuración del gráfico (opcional)
            
        Returns:
            bytes: Imagen del gráfico en formato PNG
        """
        pass
    
    @abstractmethod
    def generate_publications_by_type_chart(
        self, 
        data: Dict[str, int], 
        config: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Genera un gráfico de publicaciones por tipo.
        
        Args:
            data: Diccionario con tipo -> número de publicaciones
            config: Configuración del gráfico (opcional)
            
        Returns:
            bytes: Imagen del gráfico en formato PNG
        """
        pass
    
    @abstractmethod
    def generate_citations_chart(
        self, 
        data: List[Dict[str, Any]], 
        config: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Genera un gráfico de citaciones.
        
        Args:
            data: Lista de datos de citaciones
            config: Configuración del gráfico (opcional)
            
        Returns:
            bytes: Imagen del gráfico en formato PNG
        """
        pass


class EmailServiceInterface(ABC):
    """Interfaz para el servicio de email."""
    
    @abstractmethod
    def send_report_notification(
        self, 
        recipient: str, 
        report_data: Dict[str, Any]
    ) -> bool:
        """
        Envía una notificación por email sobre un reporte.
        
        Args:
            recipient: Dirección de email del destinatario
            report_data: Datos del reporte
            
        Returns:
            bool: True si se envió correctamente
        """
        pass
    
    @abstractmethod
    def send_sync_notification(
        self, 
        recipient: str, 
        sync_result: Dict[str, Any]
    ) -> bool:
        """
        Envía una notificación sobre sincronización de publicaciones.
        
        Args:
            recipient: Dirección de email del destinatario
            sync_result: Resultado de la sincronización
            
        Returns:
            bool: True si se envió correctamente
        """
        pass


class FileStorageInterface(ABC):
    """Interfaz para el almacenamiento de archivos."""
    
    @abstractmethod
    def save_file(self, file_path: str, content: bytes) -> str:
        """
        Guarda un archivo.
        
        Args:
            file_path: Ruta del archivo
            content: Contenido del archivo
            
        Returns:
            str: URL o ruta del archivo guardado
        """
        pass
    
    @abstractmethod
    def get_file(self, file_path: str) -> Optional[bytes]:
        """
        Obtiene un archivo.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Optional[bytes]: Contenido del archivo o None si no existe
        """
        pass
    
    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """
        Elimina un archivo.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """
        Verifica si un archivo existe.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            bool: True si el archivo existe
        """
        pass


class SJRServiceInterface(ABC):
    """Interfaz para el servicio de rankings SJR."""
    
    @abstractmethod
    def get_journal_ranking(self, journal_name: str, year: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene el ranking SJR de una revista.
        
        Args:
            journal_name: Nombre de la revista
            year: Año del ranking
            
        Returns:
            Optional[Dict[str, Any]]: Información del ranking o None si no se encuentra
        """
        pass
    
    @abstractmethod
    def search_journals(self, query: str) -> List[Dict[str, Any]]:
        """
        Busca revistas en la base de datos SJR.
        
        Args:
            query: Término de búsqueda
            
        Returns:
            List[Dict[str, Any]]: Lista de revistas encontradas
        """
        pass
    
    @abstractmethod
    def get_categories_for_journal(self, journal_id: str, year: int) -> List[str]:
        """
        Obtiene las categorías de una revista.
        
        Args:
            journal_id: ID de la revista
            year: Año
            
        Returns:
            List[str]: Lista de categorías
        """
        pass


class NotificationServiceInterface(ABC):
    """Interfaz para el servicio de notificaciones."""
    
    @abstractmethod
    def send_notification(
        self, 
        recipient: str, 
        message: str, 
        notification_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Envía una notificación.
        
        Args:
            recipient: Destinatario de la notificación
            message: Mensaje de la notificación
            notification_type: Tipo de notificación (email, sms, push, etc.)
            metadata: Metadatos adicionales (opcional)
            
        Returns:
            bool: True si se envió correctamente
        """
        pass


class CacheServiceInterface(ABC):
    """Interfaz para el servicio de caché."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor del caché.
        
        Args:
            key: Clave del valor
            
        Returns:
            Optional[Any]: Valor almacenado o None si no existe
        """
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Almacena un valor en el caché.
        
        Args:
            key: Clave del valor
            value: Valor a almacenar
            ttl: Tiempo de vida en segundos (opcional)
            
        Returns:
            bool: True si se almacenó correctamente
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Elimina un valor del caché.
        
        Args:
            key: Clave del valor
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """
        Limpia todo el caché.
        
        Returns:
            bool: True si se limpió correctamente
        """
        pass