import requests
from typing import Dict, Any


class ScopusApiClient:
    """Cliente para la API de Scopus."""

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._base_url = "https://api.elsevier.com"
        self._headers = {
            "Accept": "application/json",
            "X-ELS-APIKey": self._api_key
        }

    def get_publications_by_author(self, author_id: str) -> Dict[str, Any]:
        """Busca publicaciones de un autor en Scopus."""
        url = f"{self._base_url}/content/search/scopus"
        start = 0
        count = 200
        params = {
            "query": f"AU-ID({author_id})",
            "start": start,
            "count": count
        }

        response = requests.get(url, headers=self._headers, params=params, timeout=180)
        response.raise_for_status()
        return response.json()

    def get_publication_details(self, scopus_id: str) -> Dict[str, Any]:
        """Obtiene detalles completos de una publicación."""
        url = f"{self._base_url}/content/abstract/scopus_id/{scopus_id}"

        response = requests.get(url, headers=self._headers, timeout=180)
        response.raise_for_status()
        return response.json()
