"""
Router para el módulo de certificados.
Define los endpoints para generar certificados de publicaciones académicas.

Nota: Ningún endpoint llama a la API de Scopus.
Las publicaciones se obtienen desde la caché local (previamente poblada por
el frontend que usa la IP institucional para consultar Elsevier).
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..application.report_dto import ReportRequestDTO
from ..application.report_service import ReportService
from ..application.draft_processor_service import DraftProcessorService
from ..application.report_metadata_service import ReportMetadataService
from ..application.report_metadata_dto import (
    SaveReportMetadataDTO,
    UpdateReportMetadataDTO,
    ReportMetadataResponseDTO,
)
from ..domain.report_repository import IReportGenerator
from ..domain.elaborador import Elaborador
from .db_report_metadata_repository import DBReportMetadataRepository
from .report.pdf_generator import ReportLabReportGenerator
from .report.content_builder import ReportLabContentBuilder
from .report.style_manager import ReportLabStyleManager
from .report.chart_generator import MatplotlibChartGenerator
from .report.publication_formatter import ReportLabPublicationFormatter
from .report.template_overlay_service import TemplateOverlayService
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


def get_draft_processor_service() -> DraftProcessorService:
    """
    Factory para crear el servicio de procesamiento de borradores.
    """
    template_service = TemplateOverlayService()
    return DraftProcessorService(template_service)


def get_report_metadata_service(db: Session = Depends(get_db)) -> ReportMetadataService:
    """
    Factory para crear el servicio de metadatos de reportes.
    """
    repo = DBReportMetadataRepository(db)
    return ReportMetadataService(repo)


def get_publication_service(db: Session = Depends(get_db)) -> PublicationService:
    """
    Factory para crear el servicio de publicaciones (sin Scopus).
    """
    container = get_container()

    cache_repo = DBPublicationCacheRepository(db)
    sjr_repo = SJRFileRepository(csv_path=container.settings.SJR_CSV_PATH)
    scopus_account_repo = DBScopusAccountRepository(db)

    return PublicationService(
        cache_repo=cache_repo,
        sjr_repo=sjr_repo,
        scopus_account_repo=scopus_account_repo,
    )


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
    publication_service: PublicationService = Depends(get_publication_service),
):
    """
    Endpoint para generar un certificado de publicaciones.

    Obtiene publicaciones desde la CACHÉ local (previamente poblada por el
    frontend usando la IP institucional).  Las áreas temáticas se reciben
    opcionalmente en el body del request; si no vienen, se extraen de las
    publicaciones cacheadas.
    """
    try:
        # Log de datos recibidos
        print(f"[CERT] Datos recibidos: {request.model_dump()}")
        print(f"[CERT] Nombre: {request.docente_nombre}")
        print(f"[CERT] Departamento: {request.departamento}")
        print(f"[CERT] Cargo: {request.cargo}")
        
        # Recolectar publicaciones de todos los author_ids desde CACHÉ
        all_publications: List[Publication] = []
        all_subject_areas: set = set()
        
        for author_id in request.author_ids:
            try:
                author_uuid = UUID(author_id)
                # Usar datos cacheados – NO llama a Scopus
                author_pubs = await publication_service.get_cached_publications_by_author(author_uuid)
                
                for pub_dto in author_pubs.publications:
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
                    
                    # Extraer subject areas de las publicaciones como fallback
                    for area in pub_dto.subject_areas:
                        all_subject_areas.add(area)

            except ValueError:
                # author_id no es UUID – ignorar (el flujo directo por
                # Scopus ID se maneja desde el frontend)
                print(f"[CERT] author_id '{author_id}' no es UUID, ignorando.")

        # Si el frontend envió subject_areas explícitamente, usarlas
        if request.subject_areas:
            all_subject_areas = set(request.subject_areas)
        
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
            documents_by_year=pubs_by_year,
            is_draft=request.is_draft
        )
        
        # Crear nombre del archivo
        prefix = "borrador" if request.is_draft else "certificado"
        file_name = f"{prefix}_{request.docente_nombre.replace(' ', '_')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={file_name}"}
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(ve)}")
    except Exception as e:
        import traceback
        print(f"[CERT ERROR] Traceback completo:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generando el certificado: {str(e)}")


@router.get(
    "/elaboradores",
    summary="Obtener opciones de elaboradores",
    description="Retorna la lista de elaboradores predefinidos disponibles para los certificados."
)
async def get_elaboradores():
    """Endpoint para obtener las opciones de elaboradores."""
    return Elaborador.get_options()


@router.post(
    "/process-draft",
    response_class=Response,
    summary="Procesar borrador PDF y aplicar plantilla institucional",
    description="""
    Recibe un archivo PDF borrador y le aplica la plantilla institucional (form.pdf)
    para generar el certificado final.
    
    El archivo debe ser un PDF válido con tamaño máximo de 10MB.
    """
)
async def process_draft(
    file: UploadFile = File(..., description="Archivo PDF borrador a procesar"),
    draft_service: DraftProcessorService = Depends(get_draft_processor_service)
):
    """Endpoint para procesar un borrador PDF y convertirlo en certificado final."""
    # Validar tipo de archivo
    if not file.content_type or 'pdf' not in file.content_type.lower():
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser un PDF"
        )

    # Leer contenido del archivo
    try:
        draft_pdf_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Error al leer el archivo: {str(e)}"
                            ) from e

    # Validar tamaño máximo (10MB)
    max_size = 10 * 1024 * 1024  # 10 MB
    if len(draft_pdf_bytes) > max_size:
        raise HTTPException(status_code=400,
                            detail="El archivo excede el tamaño máximo permitido (10MB)"
                            )

    # Procesar el borrador
    try:
        final_pdf_bytes = await draft_service.process_draft(draft_pdf_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400,
                            detail=str(e)
                            ) from e
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error al procesar el borrador: {str(e)}"
                            ) from e

    # Retornar PDF final
    return Response(
        content=final_pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=certificado_final.pdf"
        }
    )


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
        
        #elif source_name == "libro":
            #if ("book" in document_type_lower or 
                #"chapter" in document_type_lower or 
                #"libro" in source_lower or
                #"capítulo" in source_lower):
                #filtered.append(pub)
    
    return filtered


# ============================================================================
# Endpoints CRUD de metadatos de reportes
# ============================================================================

@router.post(
    "/metadata",
    response_model=ReportMetadataResponseDTO,
    summary="Guardar metadatos de un reporte",
    description="Almacena publicaciones, áreas temáticas y datos del formulario para regenerar "
                "el certificado sin repetir la búsqueda."
)
async def save_metadata(
    dto: SaveReportMetadataDTO,
    service: ReportMetadataService = Depends(get_report_metadata_service),
):
    """Endpoint para guardar metadatos de un reporte."""
    try:
        return await service.save(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar metadatos: {str(e)}") from e


@router.get(
    "/metadata",
    response_model=List[ReportMetadataResponseDTO],
    summary="Listar metadatos guardados",
    description="Retorna todos los reportes guardados, ordenados del más reciente al más antiguo."
)
async def list_metadata(
    service: ReportMetadataService = Depends(get_report_metadata_service),
):
    """Endpoint para listar todos los metadatos guardados."""
    return await service.get_all()


@router.get(
    "/metadata/{metadata_id}",
    response_model=ReportMetadataResponseDTO,
    summary="Obtener metadatos por ID",
)
async def get_metadata(
    metadata_id: UUID,
    service: ReportMetadataService = Depends(get_report_metadata_service),
):
    """Endpoint para obtener metadatos por su ID."""
    result = await service.get_by_id(metadata_id)
    if not result:
        raise HTTPException(status_code=404, detail="Metadatos no encontrados")
    return result


@router.put(
    "/metadata/{metadata_id}",
    response_model=ReportMetadataResponseDTO,
    summary="Actualizar metadatos editables",
    description="Actualiza solo los campos editables: memorando, firmante, fecha, elaborador."
)
async def update_metadata(
    metadata_id: UUID,
    dto: UpdateReportMetadataDTO,
    service: ReportMetadataService = Depends(get_report_metadata_service),
):
    """Endpoint para actualizar campos editables de metadatos."""
    try:
        return await service.update(metadata_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar metadatos: {str(e)}") from e


@router.delete(
    "/metadata/{metadata_id}",
    summary="Eliminar metadatos",
)
async def delete_metadata(
    metadata_id: UUID,
    service: ReportMetadataService = Depends(get_report_metadata_service),
):
    """Endpoint para eliminar metadatos por su ID."""
    deleted = await service.delete(metadata_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Metadatos no encontrados")
    return {"message": "Metadatos eliminados correctamente"}


@router.post(
    "/metadata/{metadata_id}/generate",
    response_class=Response,
    summary="Regenerar borrador desde metadatos guardados",
    description="Usa los datos guardados (publicaciones, áreas, etc.) y los metadatos editables "
                "actuales para regenerar el borrador PDF sin buscar publicaciones nuevamente."
)
async def regenerate_from_metadata(
    metadata_id: UUID,
    service: ReportMetadataService = Depends(get_report_metadata_service),
    report_service: ReportService = Depends(get_report_service),
):
    """Regenera un borrador PDF usando los metadatos almacenados."""
    metadata = await service.get_by_id(metadata_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Metadatos no encontrados")

    try:
        # Reconstruir publicaciones desde snapshots
        pubs = []
        for pub_dict in metadata.publications:
            pubs.append(Publication(
                scopus_id=pub_dict.get("scopus_id", ""),
                eid=pub_dict.get("eid", ""),
                doi=pub_dict.get("doi"),
                title=pub_dict.get("title", ""),
                year=pub_dict.get("year", 0),
                publication_date=pub_dict.get("publication_date", ""),
                source_title=pub_dict.get("source_title", ""),
                document_type=pub_dict.get("document_type", ""),
                affiliation_name=pub_dict.get("affiliation_name", ""),
                affiliation_id=pub_dict.get("affiliation_id"),
                source_id=pub_dict.get("source_id"),
                subject_areas=pub_dict.get("subject_areas", []),
                categories_with_quartiles=pub_dict.get("categories_with_quartiles", []),
                sjr_year_used=pub_dict.get("sjr_year_used"),
            ))

        # Clasificar publicaciones
        scopus_pubs = _filter_by_type(pubs, "scopus")
        wos_pubs = _filter_by_type(pubs, "wos")
        regional_pubs = _filter_by_type(pubs, "regional")
        memories = _filter_by_type(pubs, "memoria")
        book_chapters = _filter_by_type(pubs, "libro")

        pdf_bytes = report_service.generate_report(
            author_name=metadata.author_name,
            author_gender=metadata.author_gender,
            department=metadata.department,
            role=metadata.position,
            memorandum=metadata.memorandum or "",
            signatory=metadata.signatory,
            signatory_name=metadata.signatory_name or "",
            report_date=metadata.report_date or "",
            elaborador=metadata.elaborador or "M. Vásquez",
            scopus_publications=scopus_pubs,
            wos_publications=wos_pubs,
            regional_publications=regional_pubs,
            event_memory=memories,
            book_chapters=book_chapters,
            subject_areas=metadata.subject_areas,
            documents_by_year=metadata.documents_by_year,
            is_draft=True,
        )

        file_name = f"borrador_{metadata.author_name.replace(' ', '_')}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={file_name}"},
        )

    except Exception as e:
        import traceback
        print(f"[META-REGEN ERROR] {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error al regenerar borrador: {str(e)}") from e
