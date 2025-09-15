"""
Servicio principal de aplicación que integra todas las capas - Nueva Arquitectura.

Este servicio maneja la lógica de aplicación principal integrando
los casos de uso, repositorios y servicios externos.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from ..domain.entities.author import Author
from ..domain.entities.publication import Publication
from ..domain.entities.report import Report
from ..domain.repositories.author_repository import AuthorRepository
from ..domain.repositories.publication_repository import PublicationRepository
from ..domain.repositories.report_repository import ReportRepository
from ..domain.value_objects.scopus_id import ScopusId
from ..domain.value_objects.email import Email
from ..domain.enums import ReportType, ReportStatus

from .use_cases.author.create_author_use_case import CreateAuthorUseCase
from .use_cases.author.search_authors_use_case import SearchAuthorsUseCase
from .use_cases.publication.search_scopus_publications_use_case import SearchScopusPublicationsUseCase
from .use_cases.publication.sync_publications_use_case import SyncPublicationsUseCase
from .use_cases.report.generate_report_use_case import GenerateReportUseCase

from ..infrastructure.repositories.author_repository_impl import SQLAlchemyAuthorRepository
from ..infrastructure.repositories.publication_repository_impl import SQLAlchemyPublicationRepository
from ..infrastructure.repositories.report_repository_impl import SQLAlchemyReportRepository
from ..infrastructure.external_services.scopus_api_service import ScopusAPIService
from ..infrastructure.external_services.pdf_generator_service import PDFGeneratorService
from ..infrastructure.external_services.chart_generator_service import ChartGeneratorService
from ..infrastructure.database.connection import get_database_session


class ApplicationService:
    """
    Servicio principal de aplicación que coordina todas las operaciones.
    
    Este servicio actúa como una fachada que simplifica la interacción
    con el sistema desde la capa de presentación.
    """
    
    def __init__(self, session: Optional[Session] = None):
        """
        Inicializa el servicio de aplicación.
        
        Args:
            session: Sesión de base de datos opcional
        """
        self.session = session
        
        # Repositorios
        self.author_repository = SQLAlchemyAuthorRepository(session)
        self.publication_repository = SQLAlchemyPublicationRepository(session)
        self.report_repository = SQLAlchemyReportRepository(session)
        
        # Servicios externos
        self.scopus_service = ScopusAPIService()
        self.pdf_service = PDFGeneratorService()
        self.chart_service = ChartGeneratorService()
        
        # Casos de uso
        self._initialize_use_cases()
    
    def _initialize_use_cases(self):
        """Inicializa los casos de uso con sus dependencias."""
        self.create_author_use_case = CreateAuthorUseCase(self.author_repository)
        self.search_authors_use_case = SearchAuthorsUseCase(self.author_repository)
        
        self.search_scopus_publications_use_case = SearchScopusPublicationsUseCase(
            self.scopus_service, self.publication_repository
        )
        self.sync_publications_use_case = SyncPublicationsUseCase(
            self.scopus_service, self.publication_repository, self.author_repository
        )
        
        self.generate_report_use_case = GenerateReportUseCase(
            self.report_repository, 
            self.publication_repository,
            self.author_repository,
            self.pdf_service,
            self.chart_service
        )
    
    # Métodos para manejo de autores
    
    def create_author(self, author_data: Dict[str, Any]) -> Author:
        """
        Crea un nuevo autor.
        
        Args:
            author_data: Datos del autor
            
        Returns:
            Author: El autor creado
        """
        return self.create_author_use_case.execute(author_data)
    
    def get_author_by_dni(self, dni: str) -> Optional[Author]:
        """
        Obtiene un autor por DNI.
        
        Args:
            dni: DNI del autor
            
        Returns:
            Optional[Author]: El autor si existe
        """
        return self.author_repository.find_by_dni(dni)
    
    def get_author_by_scopus_id(self, scopus_id: str) -> Optional[Author]:
        """
        Obtiene un autor por Scopus ID.
        
        Args:
            scopus_id: ID de Scopus
            
        Returns:
            Optional[Author]: El autor si existe
        """
        return self.author_repository.find_by_scopus_id(ScopusId(scopus_id))
    
    def search_authors(self, query: str) -> List[Author]:
        """
        Busca autores por nombre.
        
        Args:
            query: Término de búsqueda
            
        Returns:
            List[Author]: Lista de autores encontrados
        """
        return self.search_authors_use_case.execute(query)
    
    def get_all_authors(self) -> List[Author]:
        """
        Obtiene todos los autores.
        
        Returns:
            List[Author]: Lista de todos los autores
        """
        return self.author_repository.find_all()
    
    # Métodos para manejo de publicaciones
    
    def search_scopus_publications(self, scopus_id: str, year_range: Optional[tuple] = None) -> List[Publication]:
        """
        Busca publicaciones en Scopus para un autor.
        
        Args:
            scopus_id: ID de Scopus del autor
            year_range: Rango de años opcional (inicio, fin)
            
        Returns:
            List[Publication]: Lista de publicaciones encontradas
        """
        search_params = {'scopus_id': scopus_id}
        if year_range:
            search_params['year_range'] = year_range
            
        return self.search_scopus_publications_use_case.execute(search_params)
    
    def sync_author_publications(self, author_dni: str) -> Dict[str, Any]:
        """
        Sincroniza las publicaciones de un autor desde Scopus.
        
        Args:
            author_dni: DNI del autor
            
        Returns:
            Dict[str, Any]: Resultado de la sincronización
        """
        return self.sync_publications_use_case.execute({'author_dni': author_dni})
    
    def get_publications_by_author(self, author_dni: str) -> List[Publication]:
        """
        Obtiene las publicaciones de un autor.
        
        Args:
            author_dni: DNI del autor
            
        Returns:
            List[Publication]: Lista de publicaciones
        """
        return self.publication_repository.find_by_author(author_dni)
    
    def get_publications_by_year_range(self, start_year: int, end_year: int) -> List[Publication]:
        """
        Obtiene publicaciones por rango de años.
        
        Args:
            start_year: Año de inicio
            end_year: Año de fin
            
        Returns:
            List[Publication]: Lista de publicaciones
        """
        return self.publication_repository.find_by_year_range(start_year, end_year)
    
    def search_publications(self, filters: Dict[str, Any]) -> List[Publication]:
        """
        Busca publicaciones con filtros.
        
        Args:
            filters: Filtros de búsqueda
            
        Returns:
            List[Publication]: Lista de publicaciones
        """
        return self.publication_repository.find_with_filters(filters)
    
    def update_publication(self, publication: Publication) -> Publication:
        """
        Actualiza una publicación.
        
        Args:
            publication: Publicación a actualizar
            
        Returns:
            Publication: Publicación actualizada
        """
        return self.publication_repository.save(publication)
    
    # Métodos para manejo de reportes
    
    def generate_report(self, report_params: Dict[str, Any]) -> Report:
        """
        Genera un nuevo reporte.
        
        Args:
            report_params: Parámetros del reporte
            
        Returns:
            Report: El reporte generado
        """
        return self.generate_report_use_case.execute(report_params)
    
    def get_report_by_id(self, report_id: int) -> Optional[Report]:
        """
        Obtiene un reporte por ID.
        
        Args:
            report_id: ID del reporte
            
        Returns:
            Optional[Report]: El reporte si existe
        """
        return self.report_repository.find_by_id(report_id)
    
    def get_reports_by_author(self, author_dni: str) -> List[Report]:
        """
        Obtiene los reportes de un autor.
        
        Args:
            author_dni: DNI del autor
            
        Returns:
            List[Report]: Lista de reportes
        """
        return self.report_repository.find_by_author(author_dni)
    
    def get_recent_reports(self, limit: int = 10) -> List[Report]:
        """
        Obtiene los reportes más recientes.
        
        Args:
            limit: Número máximo de reportes
            
        Returns:
            List[Report]: Lista de reportes recientes
        """
        return self.report_repository.find_recent(limit)
    
    def search_reports(self, filters: Dict[str, Any]) -> List[Report]:
        """
        Busca reportes con filtros.
        
        Args:
            filters: Filtros de búsqueda
            
        Returns:
            List[Report]: Lista de reportes
        """
        return self.report_repository.find_with_filters(filters)
    
    def update_report_status(self, report_id: int, status: ReportStatus) -> Optional[Report]:
        """
        Actualiza el estado de un reporte.
        
        Args:
            report_id: ID del reporte
            status: Nuevo estado
            
        Returns:
            Optional[Report]: El reporte actualizado
        """
        report = self.report_repository.find_by_id(report_id)
        if not report:
            return None
        
        report.status = status
        report.updated_at = datetime.now()
        
        return self.report_repository.save(report)
    
    def delete_report(self, report_id: int) -> bool:
        """
        Elimina un reporte.
        
        Args:
            report_id: ID del reporte
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.report_repository.delete(report_id)
    
    # Métodos de estadísticas y análisis
    
    def get_dashboard_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas para el dashboard.
        
        Returns:
            Dict[str, Any]: Estadísticas del sistema
        """
        total_authors = len(self.author_repository.find_all())
        total_publications = len(self.publication_repository.find_all())
        report_stats = self.report_repository.get_statistics()
        
        # Publicaciones por año (últimos 5 años)
        current_year = datetime.now().year
        publications_by_year = {}
        for year in range(current_year - 4, current_year + 1):
            count = self.publication_repository.count_by_year(year)
            publications_by_year[year] = count
        
        return {
            'total_authors': total_authors,
            'total_publications': total_publications,
            'total_reports': report_stats['total_reports'],
            'reports_by_status': report_stats['by_status'],
            'reports_by_type': report_stats['by_type'],
            'publications_by_year': publications_by_year
        }
    
    def get_author_statistics(self, author_dni: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de un autor específico.
        
        Args:
            author_dni: DNI del autor
            
        Returns:
            Dict[str, Any]: Estadísticas del autor
        """
        author = self.author_repository.find_by_dni(author_dni)
        if not author:
            return {}
        
        publications = self.publication_repository.find_by_author(author_dni)
        reports = self.report_repository.find_by_author(author_dni)
        
        # Publicaciones por año
        publications_by_year = {}
        for pub in publications:
            year = pub.year.value
            publications_by_year[year] = publications_by_year.get(year, 0) + 1
        
        # Publicaciones por tipo
        publications_by_type = {}
        for pub in publications:
            pub_type = pub.type.value
            publications_by_type[pub_type] = publications_by_type.get(pub_type, 0) + 1
        
        # Citaciones totales
        total_citations = sum(pub.citation_count for pub in publications)
        
        return {
            'author_info': {
                'dni': author.dni,
                'name': f"{author.first_name} {author.last_name}",
                'email': str(author.email),
                'scopus_accounts': len(author.scopus_accounts)
            },
            'total_publications': len(publications),
            'total_citations': total_citations,
            'total_reports': len(reports),
            'publications_by_year': publications_by_year,
            'publications_by_type': publications_by_type,
            'h_index': self._calculate_h_index(publications)
        }
    
    def _calculate_h_index(self, publications: List[Publication]) -> int:
        """
        Calcula el índice H de un conjunto de publicaciones.
        
        Args:
            publications: Lista de publicaciones
            
        Returns:
            int: Índice H
        """
        if not publications:
            return 0
        
        # Ordenar por número de citaciones (descendente)
        citations = sorted([pub.citation_count for pub in publications], reverse=True)
        
        h_index = 0
        for i, citation_count in enumerate(citations, 1):
            if citation_count >= i:
                h_index = i
            else:
                break
        
        return h_index


# Factory function para crear el servicio con dependencias inyectadas
def create_application_service(session: Optional[Session] = None) -> ApplicationService:
    """
    Factory para crear una instancia del servicio de aplicación.
    
    Args:
        session: Sesión de base de datos opcional
        
    Returns:
        ApplicationService: Instancia del servicio
    """
    return ApplicationService(session)