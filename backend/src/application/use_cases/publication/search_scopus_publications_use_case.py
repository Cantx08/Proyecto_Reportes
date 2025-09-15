"""
Caso de uso para buscar publicaciones en Scopus.
"""

from typing import List, Dict, Any, Optional

from ....domain.entities.publication import Publication
from ....domain.repositories.publication_repository import PublicationRepository
from ....domain.interfaces.external_services import ScopusAPIInterface
from ....domain.enums import PublicationType


class SearchScopusPublicationsUseCase:
    """Caso de uso para buscar publicaciones en Scopus."""
    
    def __init__(
        self, 
        scopus_service: ScopusAPIInterface,
        publication_repository: PublicationRepository
    ):
        self.scopus_service = scopus_service
        self.publication_repository = publication_repository
    
    def execute(self, search_params: Dict[str, Any]) -> List[Publication]:
        """
        Ejecuta la búsqueda de publicaciones en Scopus.
        
        Args:
            search_params: Parámetros de búsqueda:
                - scopus_id: str - ID de Scopus del autor
                - year_range: tuple (opcional) - (año_inicio, año_fin)
                - max_results: int (opcional) - Número máximo de resultados
                - include_citations: bool (opcional) - Incluir información de citaciones
                
        Returns:
            List[Publication]: Lista de publicaciones encontradas
        """
        scopus_id = search_params.get('scopus_id')
        if not scopus_id:
            raise ValueError("scopus_id is required")
        
        # Validar Scopus ID
        from ....domain.value_objects.scopus_id import ScopusId
        try:
            scopus_id_vo = ScopusId(scopus_id)
        except ValueError as e:
            raise ValueError(f"Invalid Scopus ID: {str(e)}")
        
        # Preparar parámetros para la API
        api_params = {
            'author_id': str(scopus_id_vo),
            'max_results': search_params.get('max_results', 100),
            'include_citations': search_params.get('include_citations', True)
        }
        
        # Agregar filtro de años si se especifica
        if 'year_range' in search_params and search_params['year_range']:
            year_range = search_params['year_range']
            if isinstance(year_range, (list, tuple)) and len(year_range) == 2:
                api_params['start_year'] = year_range[0]
                api_params['end_year'] = year_range[1]
        
        # Buscar en Scopus
        scopus_publications = self.scopus_service.search_author_publications(api_params)
        
        # Convertir a entidades de dominio
        publications = []
        for scopus_pub in scopus_publications:
            publication = self._convert_scopus_to_domain(scopus_pub)
            if publication:
                publications.append(publication)
        
        return publications
    
    def search_by_keywords(self, keywords: List[str], filters: Optional[Dict[str, Any]] = None) -> List[Publication]:
        """
        Busca publicaciones por palabras clave.
        
        Args:
            keywords: Lista de palabras clave
            filters: Filtros adicionales (año, área, etc.)
            
        Returns:
            List[Publication]: Lista de publicaciones encontradas
        """
        if not keywords:
            return []
        
        # Preparar parámetros para la API
        api_params = {
            'keywords': keywords,
            'max_results': filters.get('max_results', 50) if filters else 50
        }
        
        if filters:
            if 'year_range' in filters:
                year_range = filters['year_range']
                if isinstance(year_range, (list, tuple)) and len(year_range) == 2:
                    api_params['start_year'] = year_range[0]
                    api_params['end_year'] = year_range[1]
            
            if 'subject_area' in filters:
                api_params['subject_area'] = filters['subject_area']
        
        # Buscar en Scopus
        scopus_publications = self.scopus_service.search_publications_by_keywords(api_params)
        
        # Convertir a entidades de dominio
        publications = []
        for scopus_pub in scopus_publications:
            publication = self._convert_scopus_to_domain(scopus_pub)
            if publication:
                publications.append(publication)
        
        return publications
    
    def get_publication_details(self, scopus_id: str) -> Optional[Publication]:
        """
        Obtiene los detalles completos de una publicación específica.
        
        Args:
            scopus_id: ID de Scopus de la publicación
            
        Returns:
            Optional[Publication]: La publicación si se encuentra
        """
        # Primero verificar si ya está en nuestra base de datos
        from ....domain.value_objects.scopus_id import ScopusId
        try:
            scopus_id_vo = ScopusId(scopus_id)
            existing_publication = self.publication_repository.find_by_scopus_id(scopus_id_vo)
            if existing_publication:
                return existing_publication
        except ValueError:
            return None
        
        # Si no está en la BD, buscar en Scopus
        scopus_publication = self.scopus_service.get_publication_details(scopus_id)
        if not scopus_publication:
            return None
        
        return self._convert_scopus_to_domain(scopus_publication)
    
    def _convert_scopus_to_domain(self, scopus_data: Dict[str, Any]) -> Optional[Publication]:
        """
        Convierte datos de Scopus a una entidad Publication del dominio.
        
        Args:
            scopus_data: Datos de la publicación desde Scopus
            
        Returns:
            Optional[Publication]: La publicación convertida
        """
        try:
            from ....domain.value_objects.scopus_id import ScopusId
            from ....domain.value_objects.doi import DOI
            from ....domain.value_objects.publication_year import PublicationYear
            from ....domain.enums import PublicationType
            
            # Extraer datos básicos
            title = scopus_data.get('title', '').strip()
            if not title:
                return None
            
            # Año de publicación
            year = scopus_data.get('year')
            if not year:
                return None
            
            try:
                year_vo = PublicationYear(int(year))
            except (ValueError, TypeError):
                return None
            
            # Tipo de publicación
            pub_type_str = scopus_data.get('type', 'article').lower()
            pub_type = self._map_scopus_type_to_domain(pub_type_str)
            
            # IDs
            scopus_id = None
            if scopus_data.get('scopus_id'):
                try:
                    scopus_id = ScopusId(scopus_data['scopus_id'])
                except ValueError:
                    pass
            
            doi = None
            if scopus_data.get('doi'):
                try:
                    doi = DOI(scopus_data['doi'])
                except ValueError:
                    pass
            
            # Crear la entidad Publication
            publication = Publication(
                title=title,
                abstract=scopus_data.get('abstract', ''),
                year=year_vo,
                type=pub_type,
                scopus_id=scopus_id,
                doi=doi,
                pages=scopus_data.get('pages'),
                volume=scopus_data.get('volume'),
                issue=scopus_data.get('issue'),
                citation_count=scopus_data.get('citation_count', 0),
                keywords=scopus_data.get('keywords', []),
                is_open_access=scopus_data.get('is_open_access', False),
                url=scopus_data.get('url'),
                source='scopus'
            )
            
            return publication
            
        except Exception as e:
            # Log el error pero no fallar completamente
            print(f"Error converting Scopus data to domain: {str(e)}")
            return None
    
    def _map_scopus_type_to_domain(self, scopus_type: str) -> PublicationType:
        """
        Mapea tipos de publicación de Scopus a los del dominio.
        
        Args:
            scopus_type: Tipo de publicación en Scopus
            
        Returns:
            PublicationType: Tipo correspondiente en el dominio
        """
        from ....domain.enums import PublicationType
        
        mapping = {
            'ar': PublicationType.ARTICLE,
            'article': PublicationType.ARTICLE,
            'bk': PublicationType.BOOK,
            'book': PublicationType.BOOK,
            'ch': PublicationType.BOOK_CHAPTER,
            'chapter': PublicationType.BOOK_CHAPTER,
            'cp': PublicationType.CONFERENCE_PAPER,
            'conference paper': PublicationType.CONFERENCE_PAPER,
            're': PublicationType.REVIEW,
            'review': PublicationType.REVIEW,
            'ed': PublicationType.EDITORIAL,
            'editorial': PublicationType.EDITORIAL,
            'le': PublicationType.LETTER,
            'letter': PublicationType.LETTER,
            'no': PublicationType.NOTE,
            'note': PublicationType.NOTE,
            'sh': PublicationType.SHORT_SURVEY,
            'short survey': PublicationType.SHORT_SURVEY,
            'er': PublicationType.ERRATUM,
            'erratum': PublicationType.ERRATUM,
            'cr': PublicationType.CONFERENCE_REVIEW,
            'conference review': PublicationType.CONFERENCE_REVIEW,
            'retracted': PublicationType.RETRACTED
        }
        
        return mapping.get(scopus_type.lower(), PublicationType.ARTICLE)