"""
Interfaces de repositorios para el dominio.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .entities import Autor, Publicacion, AreaTematica
else:
    from .entities import Autor, Publicacion, AreaTematica


class PublicacionesRepository(ABC):
    """Interface para el repositorio de publicaciones."""
    
    @abstractmethod
    async def obtener_publicaciones_por_autor(self, author_id: str) -> List[Publicacion]:
        """Obtiene las publicaciones de un autor específico."""
        pass
    
    @abstractmethod
    async def obtener_detalles_publicacion(self, scopus_id: str) -> Optional[dict]:
        """Obtiene los detalles completos de una publicación."""
        pass


class AreasTematicasRepository(ABC):
    """Interface para el repositorio de áreas temáticas."""
    
    @abstractmethod
    async def obtener_areas_tematicas_por_autor(self, author_id: str) -> List[AreaTematica]:
        """Obtiene las áreas temáticas de un autor."""
        pass
    
    @abstractmethod
    def obtener_todas_las_areas(self) -> List[AreaTematica]:
        """Obtiene todas las áreas temáticas con sus subáreas."""
        pass
    
    @abstractmethod
    def mapear_subarea_a_area_principal(self, subarea: str) -> Optional[str]:
        """Mapea una subárea específica a su área temática principal."""
        pass


class SJRRepository(ABC):
    """Interface para el repositorio de datos SJR."""
    
    @abstractmethod
    def obtener_categorias_revista(self, nombre_revista: str, anio: str) -> str:
        """Obtiene las categorías de una revista en un año específico."""
        pass
    
    @abstractmethod
    def normalizar_nombre_revista(self, nombre: str) -> str:
        """Normaliza el nombre de una revista para búsqueda."""
        pass
