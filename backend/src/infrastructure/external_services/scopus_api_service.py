"""
Implementación del servicio de API de Scopus.
"""

import requests
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from ...domain.interfaces.external_services import ScopusAPIInterface


class ScopusAPIService(ScopusAPIInterface):
    """Implementación del servicio de API de Scopus."""
    
    def __init__(self):
        self.api_key = os.getenv("SCOPUS_API_KEY")
        self.base_url = "https://api.elsevier.com"
        
        if not self.api_key:
            raise ValueError("SCOPUS_API_KEY environment variable is required")
    
    def search_author_publications(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Busca publicaciones de un autor en Scopus.
        
        Args:
            params: Parámetros de búsqueda
            
        Returns:
            List[Dict[str, Any]]: Lista de publicaciones desde Scopus
        """
        author_id = params.get('author_id')
        if not author_id:
            raise ValueError("author_id is required")
        
        # Construir query de búsqueda
        query_parts = [f"AU-ID({author_id})"]
        
        # Agregar filtros de año si se especifican
        if 'start_year' in params and 'end_year' in params:
            start_year = params['start_year']
            end_year = params['end_year']
            query_parts.append(f"PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}")
        
        query = " AND ".join(query_parts)
        
        # Parámetros de la API
        api_params = {
            'query': query,
            'count': min(params.get('max_results', 100), 200),  # Máximo 200 por request
            'start': 0,
            'sort': '-pubyear',
            'view': 'COMPLETE'
        }
        
        headers = {
            'X-ELS-APIKey': self.api_key,
            'Accept': 'application/json'
        }
        
        url = f"{self.base_url}/content/search/scopus"
        
        try:
            response = requests.get(url, params=api_params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            search_results = data.get('search-results', {})
            entries = search_results.get('entry', [])
            
            publications = []
            for entry in entries:
                publication = self._parse_scopus_entry(entry)
                if publication:
                    publications.append(publication)
            
            return publications
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Scopus API: {str(e)}")
            return []
        except Exception as e:
            print(f"Error parsing Scopus response: {str(e)}")
            return []
    
    def search_publications_by_keywords(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Busca publicaciones por palabras clave.
        
        Args:
            params: Parámetros de búsqueda
            
        Returns:
            List[Dict[str, Any]]: Lista de publicaciones encontradas
        """
        keywords = params.get('keywords', [])
        if not keywords:
            return []
        
        # Construir query con palabras clave
        keyword_query = " OR ".join([f'KEY("{keyword}")' for keyword in keywords])
        
        query_parts = [f"({keyword_query})"]
        
        # Agregar filtros adicionales
        if 'start_year' in params and 'end_year' in params:
            start_year = params['start_year']
            end_year = params['end_year']
            query_parts.append(f"PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}")
        
        if 'subject_area' in params:
            subject_area = params['subject_area']
            query_parts.append(f'SUBJAREA("{subject_area}")')
        
        query = " AND ".join(query_parts)
        
        # Parámetros de la API
        api_params = {
            'query': query,
            'count': min(params.get('max_results', 50), 100),
            'start': 0,
            'sort': '-citedby-count',
            'view': 'COMPLETE'
        }
        
        headers = {
            'X-ELS-APIKey': self.api_key,
            'Accept': 'application/json'
        }
        
        url = f"{self.base_url}/content/search/scopus"
        
        try:
            response = requests.get(url, params=api_params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            search_results = data.get('search-results', {})
            entries = search_results.get('entry', [])
            
            publications = []
            for entry in entries:
                publication = self._parse_scopus_entry(entry)
                if publication:
                    publications.append(publication)
            
            return publications
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Scopus API: {str(e)}")
            return []
        except Exception as e:
            print(f"Error parsing Scopus response: {str(e)}")
            return []
    
    def get_publication_details(self, scopus_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene los detalles completos de una publicación.
        
        Args:
            scopus_id: ID de Scopus de la publicación
            
        Returns:
            Optional[Dict[str, Any]]: Detalles de la publicación
        """
        headers = {
            'X-ELS-APIKey': self.api_key,
            'Accept': 'application/json'
        }
        
        url = f"{self.base_url}/content/abstract/scopus_id/{scopus_id}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            abstract_retrieval = data.get('abstracts-retrieval-response', {})
            
            return self._parse_detailed_entry(abstract_retrieval)
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting publication details: {str(e)}")
            return None
        except Exception as e:
            print(f"Error parsing publication details: {str(e)}")
            return None
    
    def get_author_details(self, author_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene los detalles de un autor.
        
        Args:
            author_id: ID de Scopus del autor
            
        Returns:
            Optional[Dict[str, Any]]: Detalles del autor
        """
        headers = {
            'X-ELS-APIKey': self.api_key,
            'Accept': 'application/json'
        }
        
        url = f"{self.base_url}/content/author/author_id/{author_id}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            author_retrieval = data.get('author-retrieval-response', [{}])[0]
            
            return self._parse_author_details(author_retrieval)
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting author details: {str(e)}")
            return None
        except Exception as e:
            print(f"Error parsing author details: {str(e)}")
            return None
    
    def verify_author_id(self, author_id: str) -> bool:
        """
        Verifica si un ID de autor existe en Scopus.
        
        Args:
            author_id: ID de Scopus del autor
            
        Returns:
            bool: True si el autor existe
        """
        author_details = self.get_author_details(author_id)
        return author_details is not None

    
    def _parse_scopus_entry(self, entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parsea una entrada de búsqueda de Scopus.
        
        Args:
            entry: Entrada de la API de Scopus
            
        Returns:
            Optional[Dict[str, Any]]: Datos parseados de la publicación
        """
        try:
            # Información básica
            scopus_id = entry.get('dc:identifier', '').replace('SCOPUS_ID:', '')
            title = entry.get('dc:title', '')
            
            if not scopus_id or not title:
                return None
            
            # Año de publicación
            cover_date = entry.get('prism:coverDate', '')
            year = None
            if cover_date:
                try:
                    year = int(cover_date.split('-')[0])
                except (ValueError, IndexError):
                    pass
            
            # DOI
            doi = entry.get('prism:doi', '')
            
            # Journal información
            journal_name = entry.get('prism:publicationName', '')
            volume = entry.get('prism:volume', '')
            issue = entry.get('prism:issueIdentifier', '')
            pages = entry.get('prism:pageRange', '')
            
            # Citaciones
            citation_count = 0
            if 'citedby-count' in entry:
                try:
                    citation_count = int(entry['citedby-count'])
                except (ValueError, TypeError):
                    citation_count = 0
            
            # Tipo de documento
            doc_type = entry.get('subtypeDescription', 'Article')
            
            # Abstract
            abstract = entry.get('dc:description', '')
            
            # URL
            url = None
            links = entry.get('link', [])
            for link in links:
                if link.get('@rel') == 'scopus':
                    url = link.get('@href')
                    break
            
            # Keywords (no siempre disponible en búsquedas)
            keywords = []
            if 'authkeywords' in entry:
                keywords_str = entry['authkeywords']
                if keywords_str:
                    keywords = [kw.strip() for kw in keywords_str.split('|')]
            
            # Open access
            is_open_access = entry.get('openaccess', '0') == '1'
            
            return {
                'scopus_id': scopus_id,
                'title': title,
                'year': year,
                'doi': doi,
                'journal_name': journal_name,
                'volume': volume,
                'issue': issue,
                'pages': pages,
                'citation_count': citation_count,
                'type': doc_type,
                'abstract': abstract,
                'keywords': keywords,
                'url': url,
                'is_open_access': is_open_access
            }
            
        except Exception as e:
            print(f"Error parsing Scopus entry: {str(e)}")
            return None
    
    def _parse_detailed_entry(self, abstract_retrieval: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parsea una respuesta detallada de Scopus.
        
        Args:
            abstract_retrieval: Respuesta de abstract retrieval
            
        Returns:
            Optional[Dict[str, Any]]: Datos parseados detallados
        """
        try:
            core_data = abstract_retrieval.get('coredata', {})
            
            scopus_id = core_data.get('dc:identifier', '').replace('SCOPUS_ID:', '')
            title = core_data.get('dc:title', '')
            
            if not scopus_id or not title:
                return None
            
            # Usar el parser básico y agregar información adicional
            basic_data = {
                'dc:identifier': core_data.get('dc:identifier', ''),
                'dc:title': title,
                'prism:coverDate': core_data.get('prism:coverDate', ''),
                'prism:doi': core_data.get('prism:doi', ''),
                'prism:publicationName': core_data.get('prism:publicationName', ''),
                'prism:volume': core_data.get('prism:volume', ''),
                'prism:issueIdentifier': core_data.get('prism:issueIdentifier', ''),
                'prism:pageRange': core_data.get('prism:pageRange', ''),
                'citedby-count': core_data.get('citedby-count', '0'),
                'subtypeDescription': core_data.get('subtypeDescription', 'Article'),
                'dc:description': core_data.get('dc:description', ''),
                'openaccess': core_data.get('openaccess', '0')
            }
            
            # Agregar links
            links = core_data.get('link', [])
            basic_data['link'] = links
            
            # Keywords desde la sección detallada
            authkeywords = abstract_retrieval.get('authkeywords', {})
            if 'author-keyword' in authkeywords:
                author_keywords = authkeywords['author-keyword']
                if isinstance(author_keywords, list):
                    keywords = [kw.get('$', '') for kw in author_keywords]
                else:
                    keywords = [author_keywords.get('$', '')]
                basic_data['authkeywords'] = '|'.join(keywords)
            
            return self._parse_scopus_entry(basic_data)
            
        except Exception as e:
            print(f"Error parsing detailed Scopus entry: {str(e)}")
            return None
    
    def _parse_author_details(self, author_retrieval: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parsea los detalles de un autor de Scopus.
        
        Args:
            author_retrieval: Respuesta de author retrieval
            
        Returns:
            Optional[Dict[str, Any]]: Datos parseados del autor
        """
        try:
            core_data = author_retrieval.get('coredata', {})
            author_profile = author_retrieval.get('author-profile', {})
            
            author_id = core_data.get('dc:identifier', '').replace('AUTHOR_ID:', '')
            
            # Nombre del autor
            preferred_name = author_profile.get('preferred-name', {})
            first_name = preferred_name.get('given-name', '')
            last_name = preferred_name.get('surname', '')
            
            # Información de afiliación
            affiliation_current = author_profile.get('affiliation-current', {})
            institution = affiliation_current.get('affiliation', {})
            institution_name = institution.get('ip-doc', {}).get('afdispname', '')
            
            # Estadísticas
            citation_count = core_data.get('citation-count', 0)
            document_count = core_data.get('document-count', 0)
            
            return {
                'author_id': author_id,
                'first_name': first_name,
                'last_name': last_name,
                'institution': institution_name,
                'citation_count': citation_count,
                'document_count': document_count
            }
            
        except Exception as e:
            print(f"Error parsing author details: {str(e)}")
            return None
