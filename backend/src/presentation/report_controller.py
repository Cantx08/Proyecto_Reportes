"""
Controlador para la generación de reportes de certificación.
"""
from typing import List
from fastapi import HTTPException
from fastapi.responses import Response

from ..application.services import PublicacionesService, AreasTematicasService
from ..application.report_application_service import ReportApplicationService
from ..domain.entities import Publicacion
from .dtos import ReportRequestDTO


class ReportController:
    """Controlador para endpoints de generación de reportes."""
    
    def __init__(
        self, 
        publicaciones_service: PublicacionesService,
        areas_service: AreasTematicasService
    ):
        self._publicaciones_service = publicaciones_service
        self._areas_service = areas_service
        self._report_service = ReportApplicationService()
    
    async def generar_reporte_certificacion(self, request: ReportRequestDTO) -> Response:
        """Genera un reporte de certificación de publicaciones en PDF."""
        try:
            # Obtener datos de publicaciones
            collection = await self._publicaciones_service.obtener_publicaciones_agrupadas(
                request.author_ids
            )
            
            # Obtener áreas temáticas
            areas_tematicas = await self._areas_service.obtener_areas_tematicas_principales(
                request.author_ids
            )
            
            # Obtener estadísticas por año
            stats_por_anio = await self._publicaciones_service.obtener_estadisticas_por_anio(
                request.author_ids
            )
            
            # Consolidar todas las publicaciones de todos los autores
            todas_publicaciones = []
            for autor in collection.autores:
                if autor.lista_publicaciones:
                    todas_publicaciones.extend(autor.lista_publicaciones)
            
            # Clasificar publicaciones por tipo/fuente
            publicaciones_scopus = self._filtrar_publicaciones_por_tipo(
                todas_publicaciones, "scopus"
            )
            publicaciones_wos = self._filtrar_publicaciones_por_tipo(
                todas_publicaciones, "wos"
            )
            publicaciones_regionales = self._filtrar_publicaciones_por_tipo(
                todas_publicaciones, "regional"
            )
            memorias_eventos = self._filtrar_publicaciones_por_tipo(
                todas_publicaciones, "conferencia"
            )
            libros_capitulos = self._filtrar_publicaciones_por_tipo(
                todas_publicaciones, "libro"
            )
            
            # Generar PDF usando el nuevo servicio de aplicación
            pdf_bytes = self._report_service.generar_reporte_certificacion(
                docente_nombre=request.docente_nombre,
                docente_genero=request.docente_genero,
                departamento=request.departamento,
                cargo=request.cargo,
                memorando=request.memorando or "",
                firmante=request.firmante,
                fecha=request.fecha or "",
                publicaciones_scopus=publicaciones_scopus,
                publicaciones_wos=publicaciones_wos,
                publicaciones_regionales=publicaciones_regionales,
                memorias_eventos=memorias_eventos,
                libros_capitulos=libros_capitulos,
                areas_tematicas=areas_tematicas,
                documentos_por_anio=stats_por_anio
            )
            
            # Crear nombre del archivo
            nombre_archivo = f"certificacion_{request.docente_nombre.replace(' ', '_')}.pdf"
            
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename={nombre_archivo}"
                }
            )
            
        except ValueError as ve:
            raise HTTPException(
                status_code=400,
                detail=f"Datos inválidos: {str(ve)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generando el reporte: {str(e)}"
            )
    
    def _filtrar_publicaciones_por_tipo(
        self, 
        publicaciones: List[Publicacion], 
        tipo: str
    ) -> List[Publicacion]:
        """Filtra publicaciones por tipo/fuente."""
        filtradas = []
        
        for pub in publicaciones:
            fuente_lower = (pub.fuente or "").lower()
            tipo_lower = (pub.tipo_documento or "").lower()
            categorias_lower = (pub.categorias or "").lower()
            
            if tipo == "scopus":
                # Publicaciones indexadas en Scopus - criterio más amplio
                if (any(keyword in fuente_lower for keyword in 
                       ["elsevier", "springer", "ieee", "nature", "science", "journal", "review"]) or
                    any(keyword in categorias_lower for keyword in 
                       ["scopus", "q1", "q2", "q3", "q4"]) or
                    pub.doi):  # La mayoría de publicaciones Scopus tienen DOI
                    filtradas.append(pub)
            
            elif tipo == "wos":
                # Publicaciones Web of Science - criterio específico
                if ("web of science" in fuente_lower or 
                    "wos" in fuente_lower or
                    "conference proceedings citation index" in categorias_lower):
                    filtradas.append(pub)
            
            elif tipo == "regional":
                # Publicaciones regionales/locales
                if any(keyword in fuente_lower for keyword in 
                      ["scielo", "redalyc", "latindex"]):
                    filtradas.append(pub)
            
            elif tipo == "conferencia":
                # Memorias de eventos/conferencias - solo las que NO son Scopus
                if (("conference" in tipo_lower or 
                     "proceeding" in fuente_lower or
                     "symposium" in fuente_lower or
                     "workshop" in fuente_lower) and
                    not any(keyword in categorias_lower for keyword in 
                           ["scopus", "q1", "q2", "q3", "q4"]) and
                    not pub.doi):
                    filtradas.append(pub)
            
            elif tipo == "libro":
                # Libros y capítulos
                if ("book" in tipo_lower or 
                    "chapter" in tipo_lower or 
                    "libro" in fuente_lower or
                    "capítulo" in fuente_lower):
                    filtradas.append(pub)
        
        return filtradas
