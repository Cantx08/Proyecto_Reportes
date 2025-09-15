"""
Controladores para los endpoints de la API.
"""
from typing import List
from ..application.services import PublicacionesService, AreasTematicasService
from ..domain.entities import Autor, Publicacion
from .dtos import (
    PublicacionesResponseDTO, 
    DocumentosPorAnioResponseDTO, 
    AreasTematicasResponseDTO,
    AutorDTO,
    PublicacionDTO
)


class PublicacionesController:
    """Controlador para endpoints de publicaciones."""
    
    def __init__(self, publicaciones_service: PublicacionesService):
        self._publicaciones_service = publicaciones_service
    
    async def obtener_publicaciones(self, author_ids: List[str]) -> PublicacionesResponseDTO:
        """Obtiene publicaciones de autores."""
        collection = await self._publicaciones_service.obtener_publicaciones_agrupadas(author_ids)
        
        autores_dto = []
        for autor in collection.autores:
            autor_dto = self._convertir_autor_a_dto(autor)
            autores_dto.append(autor_dto)
        
        return PublicacionesResponseDTO(publicaciones=autores_dto)
    
    async def obtener_documentos_por_anio(self, author_ids: List[str]) -> DocumentosPorAnioResponseDTO:
        """Obtiene estadísticas de documentos por año."""
        estadisticas = await self._publicaciones_service.obtener_estadisticas_por_anio(author_ids)
        
        return DocumentosPorAnioResponseDTO(
            author_ids=author_ids,
            documentos_por_anio=estadisticas
        )
    
    def _convertir_autor_a_dto(self, autor: Autor) -> AutorDTO:
        """Convierte una entidad Autor a DTO."""
        publicaciones_dto = []
        
        if autor.lista_publicaciones:
            for pub in autor.lista_publicaciones:
                pub_dto = PublicacionDTO(
                    titulo=pub.titulo,
                    anio=pub.anio,
                    fuente=pub.fuente,
                    tipo_documento=pub.tipo_documento,
                    filiacion=pub.filiacion,
                    doi=pub.doi,
                    categorias=pub.categorias
                )
                publicaciones_dto.append(pub_dto)
        
        return AutorDTO(
            id_autor=autor.id_autor,
            lista_publicaciones=publicaciones_dto,
            error=autor.error
        )


class AreasTematicasController:
    """Controlador para endpoints de áreas temáticas."""
    
    def __init__(self, areas_tematicas_service: AreasTematicasService):
        self._areas_tematicas_service = areas_tematicas_service
    
    async def obtener_areas_tematicas(self, author_ids: List[str]) -> AreasTematicasResponseDTO:
        """Obtiene las áreas temáticas principales (generales) de autores."""
        areas = await self._areas_tematicas_service.obtener_areas_tematicas_principales(author_ids)
        
        return AreasTematicasResponseDTO(
            author_ids=author_ids,
            areas_tematicas=areas
        )
