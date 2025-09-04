"""
Implementación del repositorio de Scopus.
"""
import requests
from typing import List, Optional, Dict, Any
from ..domain.entities import Publicacion, AreaTematica
from ..domain.repositories import PublicacionesRepository, AreasTematicasRepository


class ScopusApiClient:
    """Cliente para la API de Scopus."""
    
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._base_url = "https://api.elsevier.com"
        self._headers = {
            "Accept": "application/json",
            "X-ELS-APIKey": self._api_key
        }
    
    def buscar_publicaciones_por_autor(self, author_id: str, count: int = 100) -> Dict[str, Any]:
        """Busca publicaciones de un autor en Scopus."""
        url = f"{self._base_url}/content/search/scopus"
        params = {
            "query": f"AU-ID({author_id})",
            "count": count
        }
        
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def obtener_detalles_abstract(self, scopus_id: str) -> Dict[str, Any]:
        """Obtiene detalles completos de una publicación."""
        url = f"{self._base_url}/content/abstract/scopus_id/{scopus_id}"
        
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()


class ScopusPublicacionesRepository(PublicacionesRepository):
    """Repositorio de publicaciones usando la API de Scopus."""
    
    def __init__(self, scopus_client: ScopusApiClient):
        self._client = scopus_client
    
    async def obtener_publicaciones_por_autor(self, author_id: str) -> List[Publicacion]:
        """Obtiene las publicaciones de un autor específico."""
        data = self._client.buscar_publicaciones_por_autor(author_id)
        entries = data.get("search-results", {}).get("entry", [])
        
        publicaciones = []
        for entry in entries:
            publicacion = self._convertir_entry_a_publicacion(entry)
            if publicacion:
                publicaciones.append(publicacion)
        
        return publicaciones
    
    async def obtener_detalles_publicacion(self, scopus_id: str) -> Optional[dict]:
        """Obtiene los detalles completos de una publicación."""
        try:
            return self._client.obtener_detalles_abstract(scopus_id)
        except Exception:
            return None
    
    def _convertir_entry_a_publicacion(self, entry: dict) -> Optional[Publicacion]:
        """Convierte un entry de Scopus a una entidad Publicacion."""
        try:
            titulo = entry.get("dc:title", "")
            anio = self._extraer_anio(entry.get("prism:coverDate", ""))
            fuente = entry.get("prism:publicationName", "")
            tipo_documento = entry.get("subtypeDescription", "")
            filiacion = self._extraer_filiacion(entry)
            doi = entry.get("prism:doi", "")
            
            return Publicacion(
                titulo=titulo,
                anio=anio,
                fuente=fuente,
                tipo_documento=tipo_documento,
                filiacion=filiacion,
                doi=doi
            )
        except Exception:
            return None
    
    def _extraer_anio(self, fecha: str) -> str:
        """Extrae el año de una fecha."""
        return fecha[:4] if fecha else ""
    
    def _extraer_filiacion(self, entry: dict) -> str:
        """Extrae la filiación de un entry."""
        if "affiliation" in entry and entry["affiliation"]:
            filiacion = entry["affiliation"][0].get("affilname", "")
            if filiacion and "escuela politécnica nacional" in filiacion.lower():
                return filiacion
        return "Sin filiación"


class ScopusAreasTematicasRepository(AreasTematicasRepository):
    """Repositorio de áreas temáticas usando la API de Scopus."""
    
    def __init__(self, scopus_client: ScopusApiClient):
        self._client = scopus_client
    
    async def obtener_areas_tematicas_por_autor(self, author_id: str) -> List[AreaTematica]:
        """Obtiene las áreas temáticas de un autor."""
        data = self._client.buscar_publicaciones_por_autor(author_id)
        entries = data.get("search-results", {}).get("entry", [])
        
        areas_tematicas = set()
        
        for entry in entries:
            areas = self._extraer_areas_tematicas_de_publicacion(entry)
            areas_tematicas.update(areas)
        
        return list(areas_tematicas)
    
    def obtener_todas_las_areas(self) -> List[AreaTematica]:
        """
        Obtiene todas las áreas temáticas disponibles.
        Implementación básica - devuelve lista vacía ya que Scopus no provee un endpoint directo.
        """
        return []
    
    def mapear_subarea_a_area_principal(self, subarea: str) -> str:
        """
        Mapeo básico de subáreas - debe ser sobrescrito por el repositorio de archivos.
        Esta implementación devuelve la misma subárea.
        """
        return subarea
    
    def _extraer_areas_tematicas_de_publicacion(self, entry: dict) -> List[AreaTematica]:
        """Extrae las áreas temáticas de una publicación."""
        scopus_id = entry.get("dc:identifier", "").replace("SCOPUS_ID:", "")
        if not scopus_id:
            return []
        
        try:
            detail_data = self._client.obtener_detalles_abstract(scopus_id)
            abstracts_retrieval = detail_data.get("abstracts-retrieval-response", {})
            subject_areas_data = abstracts_retrieval.get("subject-areas", {})
            
            areas = []
            if subject_areas_data and "subject-area" in subject_areas_data:
                subject_area_list = subject_areas_data["subject-area"]
                
                if isinstance(subject_area_list, list):
                    for sa in subject_area_list:
                        area_name = sa.get("$", "")
                        if area_name:
                            areas.append(AreaTematica(nombre=area_name))
                elif isinstance(subject_area_list, dict):
                    area_name = subject_area_list.get("$", "")
                    if area_name:
                        areas.append(AreaTematica(nombre=area_name))
            
            return areas
        except Exception:
            return []
