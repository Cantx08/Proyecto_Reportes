from typing import List, Optional

from ...domain.entities.publication import Publication
from ..external.scopus_api_client import ScopusApiClient
from ...domain.repositories.publications_repository import PublicationsRepository


class ScopusPublicationsRepository(PublicationsRepository):
    """Repositorio de publicaciones usando la API de Scopus."""
    
    def __init__(self, scopus_client: ScopusApiClient):
        self._client = scopus_client
    
    def _transform_entry_to_publication(self, entry: dict) -> Optional[Publication]:
        """Convierte un entry de Scopus a una entidad Publication."""
        try:
            title = entry.get("dc:title", "")
            year = self._get_year_from_date(entry.get("prism:coverDate", ""))
            source = entry.get("prism:publicationName", "")
            document_type = entry.get("subtypeDescription", "")
            affiliation = self._retrieve_affiliation(entry)
            doi = entry.get("prism:doi", "")
            return Publication(
                title=title,
                year=year,
                source=source,
                document_type=document_type,
                affiliation=affiliation,
                doi=doi
            )
        except RuntimeError:
            return None
    
    @staticmethod
    def _get_year_from_date(publication_date: str) -> str:
        """Extrae el año de una fecha."""
        return publication_date[:4] if publication_date else ""
    
    @staticmethod
    def _retrieve_affiliation(entry: dict) -> str:
        """Extrae la afiliación de un entry."""
        if "affiliation" in entry and entry["affiliation"]:
            affiliation = entry["affiliation"][0].get("affilname", "")
            if affiliation and "escuela politécnica nacional" in affiliation.lower():
                return affiliation
        return "Sin filiación"
    
    async def get_publications_by_author(self, author_id: str) -> List[Publication]:
        """Obtiene las publicaciones de un autor específico."""
        data = await self._client.get_publications_by_author(author_id)
        entries = data.get("search-results", {}).get("entry", [])
        
        publication_list = []
        for entry in entries:
            publication = self._transform_entry_to_publication(entry)
            if publication:
                publication_list.append(publication)
        
        return publication_list
    
    async def get_publication_details(self, scopus_id: str) -> Optional[dict]:
        """Obtiene los detalles completos de una publicación."""
        try:
            return await self._client.get_publication_details(scopus_id)
        except Exception:
            return None