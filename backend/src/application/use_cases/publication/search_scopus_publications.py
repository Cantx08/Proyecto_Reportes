"""
Casos de uso relacionados con la búsqueda y sincronización de publicaciones desde Scopus.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

from ...domain.entities import Publication, Author
from ...domain.repositories import PublicationRepository, AuthorRepository, JournalRepository, SJRRepository
from ...domain.value_objects import ScopusId
from ...application.interfaces.external_services import ScopusService


@dataclass
class SearchScopusPublicationsRequest:
    """Request para búsqueda de publicaciones en Scopus."""
    scopus_ids: List[str]
    update_existing: bool = False
    map_sjr_categories: bool = True


@dataclass
class SearchScopusPublicationsResponse:
    """Response de búsqueda de publicaciones en Scopus."""
    publications_found: int
    publications_new: int
    publications_updated: int
    publications: List[Publication]
    errors: List[str]


class SearchScopusPublicationsUseCase:
    """
    Caso de uso para buscar publicaciones en Scopus.
    
    Este caso de uso maneja la búsqueda de publicaciones desde Scopus,
    la creación/actualización en la base de datos local y el mapeo
    con categorías SJR.
    """

    def __init__(self,
                 publication_repository: PublicationRepository,
                 author_repository: AuthorRepository,
                 journal_repository: JournalRepository,
                 sjr_repository: SJRRepository,
                 scopus_service: ScopusService):
        self._publication_repository = publication_repository
        self._author_repository = author_repository
        self._journal_repository = journal_repository
        self._sjr_repository = sjr_repository
        self._scopus_service = scopus_service

    async def execute(self, request: SearchScopusPublicationsRequest) -> SearchScopusPublicationsResponse:
        """
        Ejecuta la búsqueda de publicaciones en Scopus.
        
        Args:
            request: Parámetros de búsqueda
            
        Returns:
            SearchScopusPublicationsResponse: Resultado de la búsqueda
        """
        all_publications = []
        publications_new = 0
        publications_updated = 0
        errors = []

        for scopus_id_str in request.scopus_ids:
            try:
                # Validar y crear ScopusId
                scopus_id = ScopusId.create(scopus_id_str)
                
                # Buscar publicaciones en Scopus
                scopus_publications = await self._scopus_service.get_author_publications(scopus_id)
                
                for scopus_pub in scopus_publications:
                    try:
                        # Verificar si ya existe
                        existing_pub = None
                        if scopus_pub.scopus_id:
                            existing_pub = await self._publication_repository.find_by_scopus_id(scopus_pub.scopus_id)
                        elif scopus_pub.doi:
                            existing_pub = await self._publication_repository.find_by_doi(scopus_pub.doi.value)
                        
                        if existing_pub:
                            if request.update_existing:
                                # Actualizar publicación existente
                                updated_pub = await self._update_publication(existing_pub, scopus_pub)
                                if request.map_sjr_categories:
                                    await self._map_sjr_categories(updated_pub)
                                all_publications.append(updated_pub)
                                publications_updated += 1
                            else:
                                all_publications.append(existing_pub)
                        else:
                            # Crear nueva publicación
                            new_pub = await self._create_publication(scopus_pub)
                            if request.map_sjr_categories:
                                await self._map_sjr_categories(new_pub)
                            all_publications.append(new_pub)
                            publications_new += 1
                            
                    except Exception as e:
                        errors.append(f"Error processing publication {scopus_pub.title[:50]}...: {str(e)}")
                        
            except Exception as e:
                errors.append(f"Error processing Scopus ID {scopus_id_str}: {str(e)}")

        return SearchScopusPublicationsResponse(
            publications_found=len(all_publications),
            publications_new=publications_new,
            publications_updated=publications_updated,
            publications=all_publications,
            errors=errors
        )

    async def _create_publication(self, scopus_publication: Publication) -> Publication:
        """Crea una nueva publicación en la base de datos."""
        # Buscar o crear revista
        if scopus_publication.journal_name:
            journal = await self._journal_repository.find_by_title(scopus_publication.journal_name)
            if journal:
                scopus_publication.journal_id = journal.id
        
        # Guardar publicación
        return await self._publication_repository.save(scopus_publication)

    async def _update_publication(self, existing: Publication, scopus_data: Publication) -> Publication:
        """Actualiza una publicación existente con datos de Scopus."""
        # Actualizar campos específicos manteniendo datos editados
        if not existing.custom_data.get('title'):
            existing.title = scopus_data.title
        
        if not existing.custom_data.get('abstract'):
            existing.abstract = scopus_data.abstract
        
        # Actualizar métricas
        existing.citation_count = scopus_data.citation_count
        existing.is_open_access = scopus_data.is_open_access
        
        # Actualizar áreas temáticas si no han sido editadas manualmente
        if not existing.custom_data.get('subject_areas'):
            existing.subject_areas = scopus_data.subject_areas
            existing.subject_subareas = scopus_data.subject_subareas
        
        return await self._publication_repository.update(existing)

    async def _map_sjr_categories(self, publication: Publication) -> None:
        """Mapea las categorías SJR para una publicación."""
        if not publication.journal_name or not publication.year:
            return
        
        try:
            # Buscar datos SJR
            sjr_data = await self._sjr_repository.find_journal_by_name_and_year(
                publication.journal_name, 
                publication.year
            )
            
            if sjr_data:
                # Obtener categorías
                categories = await self._sjr_repository.get_categories_by_journal_and_year(
                    publication.journal_name,
                    publication.year
                )
                
                # Limpiar categorías existentes
                publication.clear_sjr_categories()
                
                # Agregar nuevas categorías
                for category in categories:
                    publication.add_sjr_category(
                        name=category.get('name', ''),
                        quartile=category.get('quartile', ''),
                        rank=category.get('rank')
                    )
                
                # Actualizar en base de datos
                await self._publication_repository.update(publication)
                
        except Exception as e:
            # Log error pero no fallar todo el proceso
            print(f"Error mapping SJR categories for publication {publication.id}: {str(e)}")


@dataclass
class MapSJRCategoriesRequest:
    """Request para mapear categorías SJR."""
    publication_ids: Optional[List[int]] = None
    author_ids: Optional[List[int]] = None
    year_range: Optional[tuple[int, int]] = None
    force_remap: bool = False


@dataclass 
class MapSJRCategoriesResponse:
    """Response de mapeo de categorías SJR."""
    publications_processed: int
    publications_mapped: int
    errors: List[str]


class MapSJRCategoriesUseCase:
    """
    Caso de uso para mapear categorías SJR a publicaciones existentes.
    
    Este caso de uso mapea las categorías SJR basándose en el nombre
    de la revista y el año de publicación.
    """

    def __init__(self,
                 publication_repository: PublicationRepository,
                 sjr_repository: SJRRepository):
        self._publication_repository = publication_repository
        self._sjr_repository = sjr_repository

    async def execute(self, request: MapSJRCategoriesRequest) -> MapSJRCategoriesResponse:
        """
        Ejecuta el mapeo de categorías SJR.
        
        Args:
            request: Parámetros de mapeo
            
        Returns:
            MapSJRCategoriesResponse: Resultado del mapeo
        """
        publications = await self._get_publications_to_process(request)
        publications_mapped = 0
        errors = []

        for publication in publications:
            try:
                # Verificar si ya tiene categorías y no es forzado
                if publication.has_sjr_categories and not request.force_remap:
                    continue
                
                # Mapear categorías
                mapped = await self._map_publication_categories(publication)
                if mapped:
                    publications_mapped += 1
                    
            except Exception as e:
                errors.append(f"Error mapping publication {publication.id}: {str(e)}")

        return MapSJRCategoriesResponse(
            publications_processed=len(publications),
            publications_mapped=publications_mapped,
            errors=errors
        )

    async def _get_publications_to_process(self, request: MapSJRCategoriesRequest) -> List[Publication]:
        """Obtiene las publicaciones a procesar."""
        publications = []
        
        if request.publication_ids:
            for pub_id in request.publication_ids:
                pub = await self._publication_repository.find_by_id(pub_id)
                if pub:
                    publications.append(pub)
        
        elif request.author_ids:
            for author_id in request.author_ids:
                # Necesitaríamos obtener los scopus_ids del autor
                # Por simplicidad, asumimos que tenemos una forma de obtener las publicaciones por autor
                author_pubs = await self._publication_repository.get_statistics_by_author(author_id)
                publications.extend(author_pubs)
        
        elif request.year_range:
            start_year, end_year = request.year_range
            for year in range(start_year, end_year + 1):
                year_pubs = await self._publication_repository.find_by_year_range(year, year)
                publications.extend(year_pubs)
        
        return publications

    async def _map_publication_categories(self, publication: Publication) -> bool:
        """Mapea las categorías SJR para una publicación específica."""
        if not publication.journal_name or not publication.year:
            return False
        
        try:
            categories = await self._sjr_repository.get_categories_by_journal_and_year(
                publication.journal_name,
                publication.year
            )
            
            if categories:
                # Limpiar categorías existentes
                publication.clear_sjr_categories()
                
                # Agregar nuevas categorías
                for category in categories:
                    publication.add_sjr_category(
                        name=category.get('name', ''),
                        quartile=category.get('quartile', ''),
                        rank=category.get('rank')
                    )
                
                # Actualizar en base de datos
                await self._publication_repository.update(publication)
                return True
            
        except Exception:
            raise
        
        return False