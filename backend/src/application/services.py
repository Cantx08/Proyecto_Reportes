"""
Servicios de aplicación que orquestan la lógica de negocio.
"""
from typing import List
from ..domain.entities import Autor, Publicacion, PublicacionesCollection, AreaTematica
from ..domain.repositories import PublicacionesRepository, AreasTematicasRepository, SJRRepository


class PublicacionesService:
    """Servicio para manejo de publicaciones."""
    
    def __init__(
        self, 
        publicaciones_repo: PublicacionesRepository,
        sjr_repo: SJRRepository
    ):
        self._publicaciones_repo = publicaciones_repo
        self._sjr_repo = sjr_repo
    
    async def obtener_publicaciones_agrupadas(self, author_ids: List[str]) -> PublicacionesCollection:
        """Obtiene y agrupa publicaciones de múltiples autores."""
        autores = []
        
        for author_id in author_ids:
            try:
                publicaciones = await self._publicaciones_repo.obtener_publicaciones_por_autor(author_id)
                
                # Enriquecer publicaciones con categorías SJR
                for pub in publicaciones:
                    if not pub.categorias:
                        pub.categorias = self._sjr_repo.obtener_categorias_revista(pub.fuente, pub.anio)
                
                autor = Autor(id_autor=author_id, lista_publicaciones=publicaciones)
                autores.append(autor)
                
            except Exception as e:
                autor_con_error = Autor(id_autor=author_id, error=str(e))
                autores.append(autor_con_error)
        
        return PublicacionesCollection(autores=autores)
    
    async def obtener_estadisticas_por_anio(self, author_ids: List[str]) -> dict[str, int]:
        """Obtiene estadísticas de publicaciones por año."""
        collection = await self.obtener_publicaciones_agrupadas(author_ids)
        return collection.contar_publicaciones_por_anio()


class AreasTematicasService:
    """Servicio para manejo de áreas temáticas."""
    
    def __init__(self, scopus_repo: AreasTematicasRepository, mapping_repo: AreasTematicasRepository):
        self._scopus_repo = scopus_repo  # Para obtener datos de Scopus
        self._mapping_repo = mapping_repo  # Para mapear usando CSV
    
    async def obtener_areas_tematicas_principales(self, author_ids: List[str]) -> List[str]:
        """
        Obtiene las áreas temáticas principales (generales) de múltiples autores.
        Mapea las subáreas específicas a áreas temáticas generales usando el CSV.
        """
        todas_las_subareas = set()
        
        # Obtener todas las subáreas específicas de Scopus
        for author_id in author_ids:
            try:
                areas = await self._scopus_repo.obtener_areas_tematicas_por_autor(author_id)
                for area in areas:
                    todas_las_subareas.add(area.nombre)
            except Exception as e:
                # Log error silently and continue
                print(f"Error obteniendo áreas para autor {author_id}: {e}")
                continue
        
        # Mapear subáreas a áreas temáticas principales
        areas_principales = set()
        for subarea in todas_las_subareas:
            area_principal = self._mapping_repo.mapear_subarea_a_area_principal(subarea)
            if area_principal:
                areas_principales.add(area_principal)
        
        return sorted(list(areas_principales))
