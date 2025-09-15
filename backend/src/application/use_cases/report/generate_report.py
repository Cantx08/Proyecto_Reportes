"""
Casos de uso relacionados con la gestión de reportes.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

from ...domain.entities import Report, ReportType, Author, Publication
from ...domain.repositories import ReportRepository, AuthorRepository, PublicationRepository
from ...application.interfaces.external_services import PDFService, ChartService


@dataclass
class GenerateReportRequest:
    """Request para generar un reporte."""
    author_id: int
    title: str
    report_type: ReportType
    memo_number: Optional[str] = None
    memo_date: Optional[datetime] = None
    signatory: Optional[str] = None
    publication_ids: Optional[List[int]] = None
    generated_by: Optional[int] = None


@dataclass
class GenerateReportResponse:
    """Response de generación de reporte."""
    report_id: int
    file_path: str
    file_name: str
    status: str
    message: str


class GenerateReportUseCase:
    """
    Caso de uso para generar reportes de publicaciones.
    
    Este caso de uso orquesta la generación completa de un reporte
    incluyendo la recopilación de datos, generación de gráficos y PDF.
    """

    def __init__(self,
                 report_repository: ReportRepository,
                 author_repository: AuthorRepository,
                 publication_repository: PublicationRepository,
                 pdf_service: PDFService,
                 chart_service: ChartService):
        self._report_repository = report_repository
        self._author_repository = author_repository
        self._publication_repository = publication_repository
        self._pdf_service = pdf_service
        self._chart_service = chart_service

    async def execute(self, request: GenerateReportRequest) -> GenerateReportResponse:
        """
        Ejecuta la generación del reporte.
        
        Args:
            request: Datos necesarios para generar el reporte
            
        Returns:
            GenerateReportResponse: Resultado de la generación
            
        Raises:
            ValueError: Si los datos de entrada son inválidos
            RuntimeError: Si hay errores en la generación
        """
        # Validar entrada
        await self._validate_request(request)
        
        # Crear entidad de reporte
        report = self._create_report_entity(request)
        
        # Guardar reporte inicial
        report = await self._report_repository.save(report)
        
        try:
            # Marcar como en proceso
            report.start_generation()
            await self._report_repository.update(report)
            
            # Obtener datos del autor
            author = await self._author_repository.find_by_id(request.author_id)
            if not author:
                raise ValueError(f"Author with ID {request.author_id} not found")
            
            # Obtener publicaciones
            publications = await self._get_publications(request, author)
            report.publication_ids = [pub.id for pub in publications if pub.id]
            
            # Generar gráficos
            charts_data = await self._generate_charts(publications)
            
            # Preparar datos para PDF
            pdf_data = self._prepare_pdf_data(author, publications, charts_data, request)
            
            # Generar PDF
            if request.report_type == ReportType.DRAFT:
                pdf_content = await self._pdf_service.generate_draft_report(pdf_data)
            else:
                pdf_content = await self._pdf_service.generate_final_report(pdf_data)
            
            # Guardar archivo
            file_path, file_name = await self._save_report_file(report, pdf_content)
            
            # Completar reporte
            report.complete_generation(file_path, file_name)
            await self._report_repository.update(report)
            
            return GenerateReportResponse(
                report_id=report.id,
                file_path=file_path,
                file_name=file_name,
                status="completed",
                message="Report generated successfully"
            )
            
        except Exception as e:
            # Marcar como fallido
            report.fail_generation(str(e))
            await self._report_repository.update(report)
            
            return GenerateReportResponse(
                report_id=report.id,
                file_path="",
                file_name="",
                status="failed",
                message=f"Report generation failed: {str(e)}"
            )

    async def _validate_request(self, request: GenerateReportRequest) -> None:
        """Valida la request de generación."""
        if not request.title or len(request.title.strip()) < 3:
            raise ValueError("Report title must be at least 3 characters long")
        
        if request.author_id <= 0:
            raise ValueError("Valid author ID is required")

    def _create_report_entity(self, request: GenerateReportRequest) -> Report:
        """Crea la entidad de reporte."""
        return Report(
            title=request.title,
            author_id=request.author_id,
            report_type=request.report_type,
            memo_number=request.memo_number,
            memo_date=request.memo_date,
            signatory=request.signatory,
            generated_by=request.generated_by,
            publication_ids=request.publication_ids or [],
            created_at=datetime.now()
        )

    async def _get_publications(self, request: GenerateReportRequest, author: Author) -> List[Publication]:
        """Obtiene las publicaciones para el reporte."""
        if request.publication_ids:
            # Obtener publicaciones específicas
            publications = []
            for pub_id in request.publication_ids:
                pub = await self._publication_repository.find_by_id(pub_id)
                if pub and pub.is_included_in_report:
                    publications.append(pub)
            return publications
        else:
            # Obtener todas las publicaciones del autor incluidas en reportes
            all_publications = await self._publication_repository.find_by_author_scopus_ids(
                author.scopus_accounts
            )
            return [pub for pub in all_publications if pub.is_included_in_report]

    async def _generate_charts(self, publications: List[Publication]) -> Dict:
        """Genera los gráficos para el reporte."""
        charts_data = {}
        
        # Gráfico de publicaciones por año
        year_counts = {}
        for pub in publications:
            if pub.year:
                year_counts[pub.year] = year_counts.get(pub.year, 0) + 1
        
        if year_counts:
            charts_data['publications_by_year'] = await self._chart_service.generate_publications_by_year_chart(year_counts)
        
        # Gráfico de áreas temáticas
        area_counts = {}
        for pub in publications:
            for area in pub.subject_areas:
                area_counts[area] = area_counts.get(area, 0) + 1
        
        if area_counts:
            charts_data['subject_areas'] = await self._chart_service.generate_subject_areas_chart(area_counts)
        
        # Distribución por cuartiles
        quartile_counts = {}
        for pub in publications:
            quartile = pub.best_sjr_quartile
            if quartile:
                quartile_counts[quartile] = quartile_counts.get(quartile, 0) + 1
        
        if quartile_counts:
            charts_data['quartile_distribution'] = await self._chart_service.generate_quartile_distribution_chart(quartile_counts)
        
        return charts_data

    def _prepare_pdf_data(self, author: Author, publications: List[Publication], 
                         charts_data: Dict, request: GenerateReportRequest) -> Dict:
        """Prepara los datos para la generación del PDF."""
        return {
            'author': {
                'name': author.full_name,
                'title': author.title,
                'position': author.position,
                'department_id': author.department_id,
                'gender': author.gender.value if author.gender else None
            },
            'report': {
                'title': request.title,
                'memo_number': request.memo_number,
                'memo_date': request.memo_date,
                'signatory': request.signatory,
                'type': request.report_type.value
            },
            'publications': [
                {
                    'title': pub.display_title,
                    'year': pub.year,
                    'journal': pub.journal_name,
                    'doi': pub.doi.value if pub.doi else None,
                    'document_type': pub.document_type.value,
                    'categories': pub.sjr_categories,
                    'subject_areas': pub.subject_areas
                }
                for pub in publications
            ],
            'statistics': {
                'total_publications': len(publications),
                'publications_by_year': self._group_publications_by_year(publications),
                'publications_by_type': self._group_publications_by_type(publications),
                'subject_areas': self._get_unique_subject_areas(publications)
            },
            'charts': charts_data
        }

    def _group_publications_by_year(self, publications: List[Publication]) -> Dict[int, int]:
        """Agrupa publicaciones por año."""
        year_counts = {}
        for pub in publications:
            if pub.year:
                year_counts[pub.year] = year_counts.get(pub.year, 0) + 1
        return year_counts

    def _group_publications_by_type(self, publications: List[Publication]) -> Dict[str, int]:
        """Agrupa publicaciones por tipo."""
        type_counts = {}
        for pub in publications:
            doc_type = pub.document_type.value
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        return type_counts

    def _get_unique_subject_areas(self, publications: List[Publication]) -> List[str]:
        """Obtiene áreas temáticas únicas."""
        areas = set()
        for pub in publications:
            areas.update(pub.subject_areas)
        return sorted(list(areas))

    async def _save_report_file(self, report: Report, pdf_content: bytes) -> tuple[str, str]:
        """Guarda el archivo del reporte y retorna la ruta y nombre."""
        import os
        from datetime import datetime
        
        # Crear directorio si no existe
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"report_{report.id}_{timestamp}.pdf"
        file_path = os.path.join(reports_dir, file_name)
        
        # Guardar archivo
        with open(file_path, 'wb') as f:
            f.write(pdf_content)
        
        return file_path, file_name