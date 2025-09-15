from typing import List
from fastapi import HTTPException
from fastapi.responses import Response
from ...application.services.publication_service import PublicationService
from ...application.services.subject_area_service import SubjectAreaService
from ...application.services.report_service import ReportService
from ...domain.entities.publication import Publication
from ..dtos.publication_dto import ReportRequestDTO


class ReportController:
    """Controlador para endpoints de generación de reportes."""
    def __init__(self, publication_service: PublicationService, subject_area_service: SubjectAreaService):
        self._publication_service = publication_service
        self._subject_area_service = subject_area_service
        self._report_service = ReportService()
    
    async def generate_report(self, request: ReportRequestDTO) -> Response:
        """Genera un reporte de certificación de publicaciones en PDF."""
        try:
            # Obtener datos de publicaciones
            collection = await self._publication_service.fetch_grouped_publications(request.author_ids)
            
            # Obtener áreas temáticas
            subject_areas = await self._subject_area_service.get_subject_areas(request.author_ids)
            
            # Obtener estadísticas por año
            pubs_by_year = await self._publication_service.get_statistics_by_year(request.author_ids)
            
            # Consolidar todas las publicaciones de todos los autores
            publications_list = []
            for author in collection.authors:
                if author.publications_list:
                    publications_list.extend(author.publications_list)
            
            # Clasificar publicaciones por tipo/fuente
            scopus_pubs = self._filter_by_type(publications_list, "scopus")
            wos_pubs = self._filter_by_type(publications_list, "wos")
            regional_pubs = self._filter_by_type(publications_list, "regional")
            memories = self._filter_by_type(publications_list, "memoria")
            book_chapters = self._filter_by_type(publications_list, "libro")
            
            # Generar PDF usando el nuevo servicio de aplicación
            pdf_bytes = self._report_service.generate_report(
                author_name=request.docente_nombre,
                author_gender=request.docente_genero,
                department=request.departamento,
                role=request.cargo,
                memorandum=request.memorando or "",
                signatory=request.firmante,
                report_date=request.fecha or "",
                scopus_publications=scopus_pubs,
                wos_publications=wos_pubs,
                regional_publications=regional_pubs,
                event_memory=memories,
                book_chapters=book_chapters,
                subject_areas=subject_areas,
                documents_by_year=pubs_by_year
            )
            
            # Crear nombre del archivo
            file_name = f"certificacion_{request.docente_nombre.replace(' ', '_')}.pdf"
            
            return Response(content=pdf_bytes, media_type="application/pdf", 
                            headers={"Content-Disposition": f"attachment; filename={file_name}"})
            
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(ve)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generando el reporte: {str(e)}")

    def _filter_by_type(self, publications: List[Publication], type: str) -> List[Publication]:
        """Filtra publicaciones por tipo/fuente."""
        filtered = []
        
        for pub in publications:
            source_lower = (pub.source or "").lower()
            document_type_lower = (pub.document_type or "").lower()
            categories_lower = (pub.categories or "").lower()
            
            if type == "scopus":
                # Publicaciones indexadas en Scopus - criterio más amplio
                if (any(keyword in source_lower for keyword in 
                       ["elsevier", "springer", "ieee", "nature", "science", "journal", "review"]) or
                    any(keyword in categories_lower for keyword in 
                       ["scopus", "q1", "q2", "q3", "q4"]) or
                    pub.doi):  # La mayoría de publicaciones Scopus tienen DOI
                    filtered.append(pub)
            
            elif type == "wos":
                # Publicaciones Web of Science - criterio específico
                if ("web of science" in source_lower or 
                    "wos" in source_lower or
                    "conference proceedings citation index" in categories_lower):
                    filtered.append(pub)
            
            elif type == "regional":
                # Publicaciones regionales/locales
                if any(keyword in source_lower for keyword in 
                      ["scielo", "redalyc", "latindex"]):
                    filtered.append(pub)
            
            elif type == "memoria":
                # Memorias de eventos/conferencias - solo las que NO son Scopus
                if (("proceeding" in source_lower or
                     "symposium" in source_lower or
                     "workshop" in source_lower) and
                    not any(keyword in categories_lower for keyword in 
                           ["scopus", "q1", "q2", "q3", "q4"]) and
                    not pub.doi):
                    filtered.append(pub)
            
            elif type == "libro":
                # Libros y capítulos
                if ("book" in document_type_lower or 
                    "chapter" in document_type_lower or 
                    "libro" in source_lower or
                    "capítulo" in source_lower):
                    filtered.append(pub)
        return filtered