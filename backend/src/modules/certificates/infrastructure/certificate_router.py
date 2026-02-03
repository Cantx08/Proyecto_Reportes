"""
Router para el módulo de certificados.
Define los endpoints para generar certificados de publicaciones académicas.
"""
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..application.report_dto import ReportRequestDTO, ProcessDraftRequestDTO
from ..application.report_service import ReportService
from ..application.draft_processor_service import DraftProcessorService
from ..domain.report_repository import IReportGenerator
from ..domain.template_overlay_repository import ITemplateOverlayService
from ..domain.elaborador import Elaborador
from .report.pdf_generator import ReportLabReportGenerator
from .report.content_builder import ReportLabContentBuilder
from .report.style_manager import ReportLabStyleManager
from .report.chart_generator import MatplotlibChartGenerator
from .report.publication_formatter import ReportLabPublicationFormatter
from .report.template_overlay_service import TemplateOverlayService
from ...publications.infrastructure.scopus_publication_repository import ScopusPublicationRepository
from ...publications.infrastructure.sjr_file_repository import SJRFileRepository
from ...publications.infrastructure.db_publication_cache_repository import DBPublicationCacheRepository
from ...publications.application.publication_service import PublicationService
from ...publications.domain.publication import Publication
from ...scopus_accounts.infrastructure.db_scopus_account_repository import DBScopusAccountRepository
from ....shared.database import get_db
from ....container import get_container

router = APIRouter(prefix="/certificates", tags=["Certificados"])


def get_report_service() -> ReportService:
    """
    Factory para crear el servicio de reportes con sus dependencias.
    """
    # Crear componentes del generador de reportes
    style_manager = ReportLabStyleManager()
    chart_generator = MatplotlibChartGenerator()
    publication_formatter = ReportLabPublicationFormatter(style_manager)
    content_builder = ReportLabContentBuilder(style_manager, chart_generator, publication_formatter)
    
    # Crear generador de reportes
    report_generator: IReportGenerator = ReportLabReportGenerator(content_builder)
    
    return ReportService(report_generator)


def get_publication_service(db: Session = Depends(get_db)) -> PublicationService:
    """
    Factory para crear el servicio de publicaciones con sus dependencias.
    """
    container = get_container()
    
    publication_repo = ScopusPublicationRepository(
        api_key=container.settings.SCOPUS_API_KEY
    )
    cache_repo = DBPublicationCacheRepository(db)
    sjr_repo = SJRFileRepository(csv_path=container.settings.SJR_CSV_PATH)
    scopus_account_repo = DBScopusAccountRepository(db)
    
    return PublicationService(
        publication_repo=publication_repo,
        cache_repo=cache_repo,
        sjr_repo=sjr_repo,
        scopus_account_repo=scopus_account_repo
    )


def get_draft_processor_service() -> DraftProcessorService:
    """
    Factory para crear el servicio de procesamiento de borradores.
    """
    template_service: ITemplateOverlayService = TemplateOverlayService()
    return DraftProcessorService(template_service)


@router.post(
    "/generate",
    response_class=Response,
    summary="Generar certificado de publicaciones",
    description="""
    Genera un certificado PDF de publicaciones académicas para un docente.
    
    El certificado incluye:
    - Información del docente (nombre, departamento, cargo)
    - Lista de publicaciones Scopus con categorías y cuartiles
    - Gráfico de tendencia de publicaciones por año
    - Áreas temáticas de investigación
    - Firma digital de la autoridad correspondiente
    
    **Etiquetas de indexación por tipo de documento:**
    - Article → "Indexada en Scopus"
    - Conference Paper → "Conferencia indexada en Scopus"
    - Book Chapter → "Cap. Libro indexado en Scopus"
    - Review → "Review indexado en Scopus"
    """
)
async def generate_certificate(
    request: ReportRequestDTO,
    report_service: ReportService = Depends(get_report_service),
    publication_service: PublicationService = Depends(get_publication_service)
):
    """Endpoint para generar un certificado de publicaciones."""
    try:
        # Recolectar publicaciones de todos los author_ids
        all_publications: List[Publication] = []
        all_subject_areas: set = set()
        
        for author_id in request.author_ids:
            try:
                # Intentar como UUID
                author_uuid = UUID(author_id)
                author_pubs = await publication_service.get_publications_by_author(author_uuid)
                
                for pub_dto in author_pubs.publications:
                    # Convertir DTO a Publication entity
                    pub = Publication(
                        scopus_id=pub_dto.scopus_id,
                        eid=pub_dto.eid,
                        doi=pub_dto.doi,
                        title=pub_dto.title,
                        year=pub_dto.year,
                        publication_date=pub_dto.publication_date,
                        source_title=pub_dto.source_title,
                        document_type=pub_dto.document_type,
                        affiliation_name=pub_dto.affiliation_name,
                        affiliation_id=pub_dto.affiliation_id,
                        subject_areas=pub_dto.subject_areas,
                        categories_with_quartiles=pub_dto.categories_with_quartiles,
                        sjr_year_used=pub_dto.sjr_year_used
                    )
                    all_publications.append(pub)
                    all_subject_areas.update(pub_dto.subject_areas)
                    
            except ValueError:
                # Si no es UUID, intentar como Scopus ID directamente
                pubs = await publication_service.get_publications_by_scopus_id(author_id)
                for pub_dto in pubs:
                    pub = Publication(
                        scopus_id=pub_dto.scopus_id,
                        eid=pub_dto.eid,
                        doi=pub_dto.doi,
                        title=pub_dto.title,
                        year=pub_dto.year,
                        publication_date=pub_dto.publication_date,
                        source_title=pub_dto.source_title,
                        document_type=pub_dto.document_type,
                        affiliation_name=pub_dto.affiliation_name,
                        affiliation_id=pub_dto.affiliation_id,
                        subject_areas=pub_dto.subject_areas,
                        categories_with_quartiles=pub_dto.categories_with_quartiles,
                        sjr_year_used=pub_dto.sjr_year_used
                    )
                    all_publications.append(pub)
                    all_subject_areas.update(pub_dto.subject_areas)
        
        # Eliminar duplicados basados en scopus_id
        seen_ids = set()
        unique_publications = []
        for pub in all_publications:
            if pub.scopus_id not in seen_ids:
                seen_ids.add(pub.scopus_id)
                unique_publications.append(pub)
        
        # Ordenar por año descendente
        unique_publications.sort(key=lambda p: p.year, reverse=True)
        
        # Calcular estadísticas por año
        pubs_by_year = {}
        for pub in unique_publications:
            year_str = str(pub.year)
            pubs_by_year[year_str] = pubs_by_year.get(year_str, 0) + 1
        
        # Clasificar publicaciones por tipo/fuente
        scopus_pubs = _filter_by_type(unique_publications, "scopus")
        wos_pubs = _filter_by_type(unique_publications, "wos")
        regional_pubs = _filter_by_type(unique_publications, "regional")
        memories = _filter_by_type(unique_publications, "memoria")
        book_chapters = _filter_by_type(unique_publications, "libro")
        
        # Generar PDF
        pdf_bytes = report_service.generate_report(
            author_name=request.docente_nombre,
            author_gender=request.docente_genero,
            department=request.departamento,
            role=request.cargo,
            memorandum=request.memorando or "",
            signatory=request.firmante,
            signatory_name=request.firmante_nombre or "",
            report_date=request.fecha or "",
            elaborador=request.elaborador or "M. Vásquez",
            scopus_publications=scopus_pubs,
            wos_publications=wos_pubs,
            regional_publications=regional_pubs,
            event_memory=memories,
            book_chapters=book_chapters,
            subject_areas=sorted(list(all_subject_areas)),
            documents_by_year=pubs_by_year
        )
        
        # Crear nombre del archivo
        file_name = f"certificado_{request.docente_nombre.replace(' ', '_')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={file_name}"}
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando el certificado: {str(e)}")


@router.post(
    "/process-draft",
    response_class=Response,
    summary="Procesar borrador PDF",
    description="""
    Procesa un PDF externo y le aplica la plantilla institucional.
    
    Útil para convertir documentos PDF existentes en certificados oficiales
    con el formato y membrete institucional de la EPN.
    """
)
async def process_draft(
    file: UploadFile = File(..., description="Archivo PDF a procesar"),
    memorando: Optional[str] = Form(None, description="Número de memorando"),
    firmante: Optional[int] = Form(None, description="Tipo de firmante (1=Directora, 2=Vicerrector)"),
    firmante_nombre: Optional[str] = Form(None, description="Nombre del firmante personalizado"),
    fecha: Optional[str] = Form(None, description="Fecha del certificado"),
    draft_service: DraftProcessorService = Depends(get_draft_processor_service)
):
    """Endpoint para procesar un borrador PDF y aplicar plantilla institucional."""
    # Validar tipo de archivo
    if not file.content_type or 'pdf' not in file.content_type.lower():
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    
    # Leer contenido del archivo
    try:
        draft_pdf_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer el archivo: {str(e)}")
    
    # Validar tamaño máximo (10MB)
    max_size = 10 * 1024 * 1024
    if len(draft_pdf_bytes) > max_size:
        raise HTTPException(status_code=400, detail="El archivo excede el tamaño máximo permitido (10MB)")
    
    # Crear DTO con metadatos
    metadata = ProcessDraftRequestDTO(
        memorando=memorando,
        firmante=firmante,
        firmante_nombre=firmante_nombre,
        fecha=fecha
    )
    
    # Procesar el borrador
    try:
        final_pdf_bytes = await draft_service.process_draft(draft_pdf_bytes, metadata)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el borrador: {str(e)}")
    
    return Response(
        content=final_pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=certificado_final.pdf"}
    )


@router.get(
    "/elaboradores",
    summary="Obtener opciones de elaboradores",
    description="Retorna la lista de elaboradores predefinidos disponibles para los certificados."
)
async def get_elaboradores():
    """Endpoint para obtener las opciones de elaboradores."""
    return Elaborador.get_options()


def _filter_by_type(publications: List[Publication], source_name: str) -> List[Publication]:
    """Filtra publicaciones por tipo/fuente."""
    filtered = []
    
    for pub in publications:
        source_lower = (pub.source_title or "").lower()
        document_type_lower = (pub.document_type or "").lower()
        categories_str = ""
        if pub.categories_with_quartiles:
            if isinstance(pub.categories_with_quartiles, list):
                categories_str = " ".join(pub.categories_with_quartiles).lower()
            else:
                categories_str = str(pub.categories_with_quartiles).lower()
        
        if source_name == "scopus":
            # TODAS las publicaciones se consideran Scopus por defecto,
            # a menos que sean explícitamente de otro tipo
            is_book = ("book" in document_type_lower or 
                      "chapter" in document_type_lower or 
                      "libro" in source_lower)
            is_wos = ("web of science" in source_lower or "wos" in source_lower)
            is_regional = any(kw in source_lower for kw in ["scielo", "redalyc", "latindex"])
            
            if not (is_book or is_wos or is_regional):
                filtered.append(pub)
        
        elif source_name == "wos":
            if ("web of science" in source_lower or 
                "wos" in source_lower or
                "conference proceedings citation index" in categories_str):
                filtered.append(pub)
        
        elif source_name == "regional":
            if any(keyword in source_lower for keyword in ["scielo", "redalyc", "latindex"]):
                filtered.append(pub)
        
        elif source_name == "memoria":
            if "memoria_manual" in categories_str:
                filtered.append(pub)
        
        elif source_name == "libro":
            if ("book" in document_type_lower or 
                "chapter" in document_type_lower or 
                "libro" in source_lower or
                "capítulo" in source_lower):
                filtered.append(pub)
    
    return filtered
