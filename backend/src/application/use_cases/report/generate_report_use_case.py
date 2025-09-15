"""
Caso de uso para generar reportes.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from ....domain.entities.report import Report
from ....domain.entities.author import Author
from ....domain.entities.publication import Publication
from ....domain.repositories.report_repository import ReportRepository
from ....domain.repositories.publication_repository import PublicationRepository
from ....domain.repositories.author_repository import AuthorRepository
from ....domain.interfaces.external_services import PDFGeneratorInterface, ChartGeneratorInterface
from ....domain.enums import ReportType, ReportStatus


class GenerateReportUseCase:
    """Caso de uso para generar reportes."""
    
    def __init__(
        self,
        report_repository: ReportRepository,
        publication_repository: PublicationRepository,
        author_repository: AuthorRepository,
        pdf_service: PDFGeneratorInterface,
        chart_service: ChartGeneratorInterface
    ):
        self.report_repository = report_repository
        self.publication_repository = publication_repository
        self.author_repository = author_repository
        self.pdf_service = pdf_service
        self.chart_service = chart_service
    
    def execute(self, report_params: Dict[str, Any]) -> Report:
        """
        Ejecuta la generación de un reporte.
        
        Args:
            report_params: Parámetros del reporte:
                - title: str - Título del reporte
                - description: str (opcional) - Descripción
                - author_dni: str - DNI del autor
                - type: str - Tipo de reporte
                - start_year: int - Año de inicio
                - end_year: int - Año de fin
                - publication_ids: List[int] (opcional) - IDs específicos de publicaciones
                - include_charts: bool (opcional) - Incluir gráficos
                - include_abstracts: bool (opcional) - Incluir resúmenes
                - template_config: Dict (opcional) - Configuración de plantilla
                
        Returns:
            Report: El reporte generado
        """
        # Validar parámetros requeridos
        self._validate_report_params(report_params)
        
        # Obtener el autor
        author_dni = report_params['author_dni']
        author = self.author_repository.find_by_dni(author_dni)
        if not author:
            raise ValueError(f"Author with DNI {author_dni} not found")
        
        # Crear entidad de reporte inicial
        report = self._create_report_entity(report_params, author)
        
        # Guardar el reporte como borrador
        report = self.report_repository.save(report)
        
        try:
            # Cambiar estado a generando
            report.status = ReportStatus.GENERATING
            report = self.report_repository.save(report)
            
            # Obtener publicaciones para el reporte
            publications = self._get_publications_for_report(report_params, author)
            
            # Actualizar IDs de publicaciones en el reporte
            report.publication_ids = [pub.id for pub in publications]
            report = self.report_repository.save(report)
            
            # Generar el PDF del reporte
            pdf_content = self._generate_pdf_report(report, author, publications)
            
            # Guardar el PDF y actualizar el reporte
            pdf_path = self._save_pdf_file(report.id, pdf_content)
            report.pdf_path = pdf_path
            report.status = ReportStatus.COMPLETED
            report.generated_at = datetime.now()
            
            # Guardar reporte completado
            report = self.report_repository.save(report)
            
            return report
            
        except Exception as e:
            # En caso de error, marcar el reporte como fallido
            report.status = ReportStatus.ERROR
            report.notes = f"Error generating report: {str(e)}"
            self.report_repository.save(report)
            raise
    
    def _validate_report_params(self, params: Dict[str, Any]) -> None:
        """
        Valida los parámetros del reporte.
        
        Args:
            params: Parámetros a validar
            
        Raises:
            ValueError: Si algún parámetro es inválido
        """
        required_fields = ['title', 'author_dni', 'type', 'start_year', 'end_year']
        
        for field in required_fields:
            if field not in params or params[field] is None:
                raise ValueError(f"Field '{field}' is required")
        
        # Validar título
        title = params['title'].strip()
        if len(title) < 3 or len(title) > 200:
            raise ValueError("Title must be between 3 and 200 characters")
        
        # Validar tipo de reporte
        try:
            ReportType(params['type'])
        except ValueError:
            raise ValueError(f"Invalid report type: {params['type']}")
        
        # Validar años
        start_year = params['start_year']
        end_year = params['end_year']
        
        if not isinstance(start_year, int) or not isinstance(end_year, int):
            raise ValueError("Years must be integers")
        
        if start_year < 1950 or end_year < 1950:
            raise ValueError("Years must be 1950 or later")
        
        if start_year > end_year:
            raise ValueError("Start year must be less than or equal to end year")
        
        current_year = datetime.now().year
        if end_year > current_year:
            raise ValueError(f"End year cannot be greater than current year ({current_year})")
    
    def _create_report_entity(self, params: Dict[str, Any], author: Author) -> Report:
        """
        Crea la entidad Report inicial.
        
        Args:
            params: Parámetros del reporte
            author: Autor del reporte
            
        Returns:
            Report: Entidad de reporte creada
        """
        return Report(
            title=params['title'].strip(),
            description=params.get('description', '').strip(),
            author_dni=author.dni,
            type=ReportType(params['type']),
            status=ReportStatus.DRAFT,
            start_year=params['start_year'],
            end_year=params['end_year'],
            publication_ids=[],  # Se llenará después
            include_charts=params.get('include_charts', True),
            include_abstracts=params.get('include_abstracts', False),
            template_config=params.get('template_config', {}),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    def _get_publications_for_report(
        self, 
        params: Dict[str, Any], 
        author: Author
    ) -> List[Publication]:
        """
        Obtiene las publicaciones para incluir en el reporte.
        
        Args:
            params: Parámetros del reporte
            author: Autor del reporte
            
        Returns:
            List[Publication]: Lista de publicaciones
        """
        # Si se especificaron IDs específicos de publicaciones
        if 'publication_ids' in params and params['publication_ids']:
            # TODO: Implementar método para obtener publicaciones por IDs
            # publications = self.publication_repository.find_by_ids(params['publication_ids'])
            # Por ahora, usar filtros
            publications = []
        else:
            # Buscar publicaciones del autor en el rango de años
            filters = {
                'author_dni': author.dni,
                'year_start': params['start_year'],
                'year_end': params['end_year'],
                'order_by': 'year',
                'order_dir': 'desc'
            }
            
            publications = self.publication_repository.find_with_filters(filters)
        
        return publications
    
    def _generate_pdf_report(
        self, 
        report: Report, 
        author: Author, 
        publications: List[Publication]
    ) -> bytes:
        """
        Genera el PDF del reporte.
        
        Args:
            report: Entidad del reporte
            author: Autor del reporte
            publications: Lista de publicaciones
            
        Returns:
            bytes: Contenido del PDF generado
        """
        # Preparar datos para el generador de PDF
        report_data = {
            'title': report.title,
            'description': report.description,
            'type': report.type.value,
            'period': f"{report.start_year} - {report.end_year}",
            'generated_at': report.generated_at or datetime.now(),
            'author_info': {
                'name': f"{author.first_name} {author.last_name}",
                'dni': author.dni,
                'email': str(author.email),
                'department_id': author.department_id
            },
            'publications': self._format_publications_for_pdf(publications),
            'statistics': self._calculate_statistics(publications),
            'template_config': report.template_config,
            'include_charts': report.include_charts,
            'include_abstracts': report.include_abstracts
        }
        
        # Generar gráficos si se solicita
        if report.include_charts:
            report_data['charts'] = self._generate_charts(publications)
        
        # Generar PDF
        return self.pdf_service.generate_report(report_data)
    
    def _format_publications_for_pdf(self, publications: List[Publication]) -> List[Dict[str, Any]]:
        """
        Formatea las publicaciones para el PDF.
        
        Args:
            publications: Lista de publicaciones
            
        Returns:
            List[Dict[str, Any]]: Publicaciones formateadas
        """
        formatted_publications = []
        
        for pub in publications:
            formatted_pub = {
                'title': pub.title,
                'year': pub.year.value,
                'type': pub.type.value,
                'citation_count': pub.citation_count,
                'journal_info': {},  # TODO: Obtener información del journal
                'authors': [],  # TODO: Obtener información de autores
                'doi': str(pub.doi) if pub.doi else None,
                'scopus_id': str(pub.scopus_id) if pub.scopus_id else None,
                'url': pub.url,
                'keywords': pub.keywords
            }
            
            if pub.abstract:
                formatted_pub['abstract'] = pub.abstract
            
            formatted_publications.append(formatted_pub)
        
        return formatted_publications
    
    def _calculate_statistics(self, publications: List[Publication]) -> Dict[str, Any]:
        """
        Calcula estadísticas de las publicaciones.
        
        Args:
            publications: Lista de publicaciones
            
        Returns:
            Dict[str, Any]: Estadísticas calculadas
        """
        if not publications:
            return {
                'total_publications': 0,
                'total_citations': 0,
                'publications_by_year': {},
                'publications_by_type': {},
                'h_index': 0,
                'average_citations': 0
            }
        
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
        
        # Citaciones
        total_citations = sum(pub.citation_count for pub in publications)
        average_citations = total_citations / len(publications) if publications else 0
        
        # Calcular índice H
        h_index = self._calculate_h_index(publications)
        
        return {
            'total_publications': len(publications),
            'total_citations': total_citations,
            'publications_by_year': publications_by_year,
            'publications_by_type': publications_by_type,
            'h_index': h_index,
            'average_citations': round(average_citations, 2)
        }
    
    def _calculate_h_index(self, publications: List[Publication]) -> int:
        """
        Calcula el índice H.
        
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
    
    def _generate_charts(self, publications: List[Publication]) -> Dict[str, bytes]:
        """
        Genera gráficos para el reporte.
        
        Args:
            publications: Lista de publicaciones
            
        Returns:
            Dict[str, bytes]: Gráficos generados
        """
        charts = {}
        
        if not publications:
            return charts
        
        # Gráfico de publicaciones por año
        publications_by_year = {}
        for pub in publications:
            year = pub.year.value
            publications_by_year[year] = publications_by_year.get(year, 0) + 1
        
        if publications_by_year:
            charts['publications_by_year'] = self.chart_service.generate_publications_by_year_chart(
                publications_by_year
            )
        
        # Gráfico de publicaciones por tipo
        publications_by_type = {}
        for pub in publications:
            pub_type = pub.type.value
            publications_by_type[pub_type] = publications_by_type.get(pub_type, 0) + 1
        
        if publications_by_type:
            charts['publications_by_type'] = self.chart_service.generate_publications_by_type_chart(
                publications_by_type
            )
        
        return charts
    
    def _save_pdf_file(self, report_id: int, pdf_content: bytes) -> str:
        """
        Guarda el archivo PDF del reporte.
        
        Args:
            report_id: ID del reporte
            pdf_content: Contenido del PDF
            
        Returns:
            str: Ruta del archivo guardado
        """
        import os
        from datetime import datetime
        
        # Crear directorio de reportes si no existe
        reports_dir = os.path.join('data', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{report_id}_{timestamp}.pdf"
        file_path = os.path.join(reports_dir, filename)
        
        # Guardar archivo
        with open(file_path, 'wb') as f:
            f.write(pdf_content)
        
        return file_path