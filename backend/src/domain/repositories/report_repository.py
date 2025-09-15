from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from ..entities.report import Report, ReportType, ReportStatus


class ReportRepository(ABC):
    """
    Interface para el repositorio de reportes.
    
    Define los contratos para el acceso a datos de reportes.
    """

    @abstractmethod
    async def save(self, report: Report) -> Report:
        """
        Guarda un reporte en el repositorio.
        
        Args:
            report: Entidad Report a guardar
            
        Returns:
            Report: El reporte guardado con ID asignado
        """
        pass

    @abstractmethod
    async def find_by_id(self, report_id: int) -> Optional[Report]:
        """
        Busca un reporte por su ID.
        
        Args:
            report_id: ID del reporte
            
        Returns:
            Optional[Report]: El reporte encontrado o None
        """
        pass

    @abstractmethod
    async def find_by_author(self, author_id: int) -> List[Report]:
        """
        Busca reportes por autor.
        
        Args:
            author_id: ID del autor
            
        Returns:
            List[Report]: Lista de reportes del autor
        """
        pass

    @abstractmethod
    async def find_by_status(self, status: ReportStatus) -> List[Report]:
        """
        Busca reportes por estado.
        
        Args:
            status: Estado del reporte
            
        Returns:
            List[Report]: Lista de reportes con el estado especificado
        """
        pass

    @abstractmethod
    async def find_by_type(self, report_type: ReportType) -> List[Report]:
        """
        Busca reportes por tipo.
        
        Args:
            report_type: Tipo de reporte
            
        Returns:
            List[Report]: Lista de reportes del tipo especificado
        """
        pass

    @abstractmethod
    async def find_recent_by_author(self, author_id: int, limit: int = 10) -> List[Report]:
        """
        Busca reportes recientes de un autor.
        
        Args:
            author_id: ID del autor
            limit: Límite de resultados
            
        Returns:
            List[Report]: Lista de reportes recientes
        """
        pass

    @abstractmethod
    async def find_all_completed(self) -> List[Report]:
        """
        Obtiene todos los reportes completados.
        
        Returns:
            List[Report]: Lista de reportes completados
        """
        pass

    @abstractmethod
    async def update(self, report: Report) -> Report:
        """
        Actualiza un reporte existente.
        
        Args:
            report: Entidad Report a actualizar
            
        Returns:
            Report: El reporte actualizado
        """
        pass

    @abstractmethod
    async def delete(self, report_id: int) -> bool:
        """
        Elimina un reporte.
        
        Args:
            report_id: ID del reporte a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass

    @abstractmethod
    async def count_by_author(self, author_id: int) -> int:
        """
        Cuenta reportes por autor.
        
        Args:
            author_id: ID del autor
            
        Returns:
            int: Número de reportes del autor
        """
        pass

    @abstractmethod
    async def get_statistics(self) -> Dict[str, int]:
        """
        Obtiene estadísticas de reportes.
        
        Returns:
            Dict[str, int]: Estadísticas (total, por tipo, por estado, etc.)
        """
        pass