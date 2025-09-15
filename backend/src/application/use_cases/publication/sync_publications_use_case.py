"""
Caso de uso para sincronizar publicaciones desde Scopus.
"""

from typing import Dict, Any, List
from datetime import datetime

from ....domain.entities.author import Author
from ....domain.entities.publication import Publication
from ....domain.repositories.author_repository import AuthorRepository
from ....domain.repositories.publication_repository import PublicationRepository
from ....domain.interfaces.external_services import ScopusAPIInterface


class SyncPublicationsUseCase:
    """Caso de uso para sincronizar publicaciones desde Scopus."""
    
    def __init__(
        self,
        scopus_service: ScopusAPIInterface,
        publication_repository: PublicationRepository,
        author_repository: AuthorRepository
    ):
        self.scopus_service = scopus_service
        self.publication_repository = publication_repository
        self.author_repository = author_repository
    
    def execute(self, sync_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta la sincronización de publicaciones.
        
        Args:
            sync_params: Parámetros de sincronización:
                - author_dni: str - DNI del autor
                - force_update: bool (opcional) - Forzar actualización de existentes
                - year_range: tuple (opcional) - (año_inicio, año_fin)
                - max_results: int (opcional) - Número máximo de resultados
                
        Returns:
            Dict[str, Any]: Resultado de la sincronización
        """
        author_dni = sync_params.get('author_dni')
        if not author_dni:
            raise ValueError("author_dni is required")
        
        # Buscar el autor
        author = self.author_repository.find_by_dni(author_dni)
        if not author:
            raise ValueError(f"Author with DNI {author_dni} not found")
        
        # Verificar que el autor tenga cuentas de Scopus activas
        active_scopus_accounts = [
            acc for acc in author.scopus_accounts 
            if acc.is_active
        ]
        
        if not active_scopus_accounts:
            return {
                'success': False,
                'message': 'Author has no active Scopus accounts',
                'stats': {
                    'total_found': 0,
                    'new_publications': 0,
                    'updated_publications': 0,
                    'skipped_publications': 0,
                    'errors': 0
                }
            }
        
        # Estadísticas de sincronización
        sync_stats = {
            'total_found': 0,
            'new_publications': 0,
            'updated_publications': 0,
            'skipped_publications': 0,
            'errors': 0
        }
        
        errors = []
        all_publications = []
        
        # Sincronizar publicaciones para cada cuenta de Scopus activa
        for scopus_account in active_scopus_accounts:
            try:
                account_publications = self._sync_scopus_account_publications(
                    scopus_account.scopus_id,
                    sync_params,
                    sync_stats
                )
                all_publications.extend(account_publications)
            except Exception as e:
                error_msg = f"Error syncing Scopus account {scopus_account.scopus_id}: {str(e)}"
                errors.append(error_msg)
                sync_stats['errors'] += 1
        
        # Resultado final
        result = {
            'success': sync_stats['errors'] == 0 or len(all_publications) > 0,
            'message': 'Synchronization completed',
            'stats': sync_stats,
            'publications': len(all_publications)
        }
        
        if errors:
            result['errors'] = errors
        
        return result
    
    def _sync_scopus_account_publications(
        self,
        scopus_id,
        sync_params: Dict[str, Any],
        sync_stats: Dict[str, int]
    ) -> List[Publication]:
        """
        Sincroniza publicaciones para una cuenta de Scopus específica.
        
        Args:
            scopus_id: ID de Scopus
            sync_params: Parámetros de sincronización
            sync_stats: Estadísticas de sincronización (se modifica in-place)
            
        Returns:
            List[Publication]: Lista de publicaciones sincronizadas
        """
        # Preparar parámetros para la API de Scopus
        api_params = {
            'author_id': str(scopus_id),
            'max_results': sync_params.get('max_results', 200),
            'include_citations': True
        }
        
        # Agregar filtro de años si se especifica
        if 'year_range' in sync_params and sync_params['year_range']:
            year_range = sync_params['year_range']
            if isinstance(year_range, (list, tuple)) and len(year_range) == 2:
                api_params['start_year'] = year_range[0]
                api_params['end_year'] = year_range[1]
        
        # Buscar publicaciones en Scopus
        scopus_publications = self.scopus_service.search_author_publications(api_params)
        sync_stats['total_found'] += len(scopus_publications)
        
        synchronized_publications = []
        force_update = sync_params.get('force_update', False)
        
        for scopus_pub in scopus_publications:
            try:
                publication = self._process_scopus_publication(scopus_pub, force_update, sync_stats)
                if publication:
                    synchronized_publications.append(publication)
            except Exception as e:
                print(f"Error processing publication {scopus_pub.get('scopus_id', 'unknown')}: {str(e)}")
                sync_stats['errors'] += 1
        
        return synchronized_publications
    
    def _process_scopus_publication(
        self,
        scopus_data: Dict[str, Any],
        force_update: bool,
        sync_stats: Dict[str, int]
    ) -> Publication:
        """
        Procesa una publicación de Scopus y la guarda en la base de datos.
        
        Args:
            scopus_data: Datos de la publicación desde Scopus
            force_update: Si se debe forzar la actualización
            sync_stats: Estadísticas de sincronización
            
        Returns:
            Publication: La publicación procesada
        """
        # Convertir datos de Scopus a entidad de dominio
        publication = self._convert_scopus_to_domain(scopus_data)
        if not publication:
            sync_stats['skipped_publications'] += 1
            return None
        
        # Verificar si la publicación ya existe
        existing_publication = None
        
        # Buscar por Scopus ID si está disponible
        if publication.scopus_id:
            existing_publication = self.publication_repository.find_by_scopus_id(
                publication.scopus_id
            )
        
        # Si no se encontró por Scopus ID, buscar por DOI
        if not existing_publication and publication.doi:
            existing_publication = self.publication_repository.find_by_doi(publication.doi)
        
        if existing_publication:
            if force_update:
                # Actualizar la publicación existente con nuevos datos
                self._update_existing_publication(existing_publication, publication)
                updated_publication = self.publication_repository.save(existing_publication)
                sync_stats['updated_publications'] += 1
                return updated_publication
            else:
                # Publicación ya existe y no se fuerza actualización
                sync_stats['skipped_publications'] += 1
                return existing_publication
        else:
            # Nueva publicación
            new_publication = self.publication_repository.save(publication)
            sync_stats['new_publications'] += 1
            return new_publication
    
    def _convert_scopus_to_domain(self, scopus_data: Dict[str, Any]) -> Publication:
        """
        Convierte datos de Scopus a una entidad Publication del dominio.
        
        Args:
            scopus_data: Datos de la publicación desde Scopus
            
        Returns:
            Publication: La publicación convertida
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
                source='scopus',
                is_editable=False,  # Las publicaciones de Scopus no son editables por defecto
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            return publication
            
        except Exception as e:
            print(f"Error converting Scopus data to domain: {str(e)}")
            return None
    
    def _map_scopus_type_to_domain(self, scopus_type: str):
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
    
    def _update_existing_publication(self, existing: Publication, new_data: Publication) -> None:
        """
        Actualiza una publicación existente con nuevos datos.
        
        Args:
            existing: Publicación existente
            new_data: Nuevos datos de la publicación
        """
        # Actualizar campos que pueden cambiar
        if new_data.citation_count > existing.citation_count:
            existing.citation_count = new_data.citation_count
        
        # Actualizar abstract si no existía
        if not existing.abstract and new_data.abstract:
            existing.abstract = new_data.abstract
        
        # Actualizar keywords si no existían
        if not existing.keywords and new_data.keywords:
            existing.keywords = new_data.keywords
        
        # Actualizar URL si no existía
        if not existing.url and new_data.url:
            existing.url = new_data.url
        
        # Actualizar información de acceso abierto
        if new_data.is_open_access and not existing.is_open_access:
            existing.is_open_access = new_data.is_open_access
        
        # Actualizar timestamp
        existing.updated_at = datetime.now()