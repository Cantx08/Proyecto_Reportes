from typing import List, Dict, Optional
from uuid import UUID

from .publication_dto import PublicationResponseDTO, AuthorPublicationsResponseDTO
from ..domain.publication import Publication, SJRMetric
from ..domain.publication_repository import IPublicationRepository
from ..domain.publication_cache_repository import IPublicationCacheRepository
from ..domain.sjr_repository import ISJRRepository
from ...scopus_accounts.domain.scopus_account import ScopusAccount
from ...scopus_accounts.domain.scopus_account_repository import IScopusAccountRepository


class PublicationService:
    """
    Servicio de aplicación para gestión de publicaciones.
    
    Orquesta la obtención de publicaciones desde Scopus con estrategia de caché
    y enriquecimiento con métricas SJR para las categorías temáticas.
    """
    
    # Tiempo de validez de la caché en horas
    CACHE_MAX_AGE_HOURS = 24
    
    def __init__(
        self, 
        publication_repo: IPublicationRepository,
        cache_repo: Optional[IPublicationCacheRepository],
        sjr_repo: ISJRRepository,
        scopus_account_repo: IScopusAccountRepository
    ):
        self._publication_repo = publication_repo
        self._cache_repo = cache_repo
        self._sjr_repo = sjr_repo
        self._scopus_account_repo = scopus_account_repo

    async def get_publications_by_author(
        self, 
        author_id: UUID,
        force_refresh: bool = False
    ) -> AuthorPublicationsResponseDTO:
        """
        Obtiene todas las publicaciones de un autor desde sus cuentas Scopus.
        
        Utiliza caché cuando está disponible para reducir llamadas a la API.
        
        Args:
            author_id: UUID del autor en el sistema
            force_refresh: Si True, ignora la caché y consulta Scopus directamente
            
        Returns:
            DTO con las publicaciones del autor enriquecidas con métricas SJR
        """
        # 1. Obtener las cuentas Scopus del autor
        scopus_accounts = await self._scopus_account_repo.get_by_author(author_id)
        
        if not scopus_accounts:
            raise ValueError(f"El autor no tiene cuentas Scopus asociadas.")
        
        scopus_ids = [account.scopus_id for account in scopus_accounts]
        
        # 2. Obtener publicaciones de todas las cuentas Scopus
        all_publications: List[Publication] = []
        seen_scopus_ids = set()  # Para evitar duplicados
        
        for account in scopus_accounts:
            # Intentar obtener desde caché primero
            publications = await self._get_publications_with_cache(
                account, 
                force_refresh=force_refresh
            )
            
            for pub in publications:
                # Evitar duplicados (un artículo puede aparecer en múltiples cuentas)
                if pub.scopus_id not in seen_scopus_ids:
                    seen_scopus_ids.add(pub.scopus_id)
                    all_publications.append(pub)
        
        # 3. Ordenar por año descendente
        all_publications.sort(key=lambda p: p.year, reverse=True)
        
        return AuthorPublicationsResponseDTO(
            author_id=str(author_id),
            scopus_ids=scopus_ids,
            total_publications=len(all_publications),
            publications=[PublicationResponseDTO.from_entity(p) for p in all_publications]
        )

    async def _get_publications_with_cache(
        self, 
        account: ScopusAccount,
        force_refresh: bool = False
    ) -> List[Publication]:
        """
        Obtiene publicaciones usando la estrategia de caché.
        
        1. Si hay caché válida y no se fuerza refresh, usa caché
        2. Si no hay caché o está expirada, consulta Scopus y actualiza caché
        """
        # Si no hay repositorio de caché, ir directo a Scopus
        if self._cache_repo is None:
            return await self._fetch_from_scopus(account.scopus_id)
        
        # Verificar si la caché es válida
        if not force_refresh:
            cache_valid = await self._cache_repo.is_cache_valid(
                account.account_id, 
                self.CACHE_MAX_AGE_HOURS
            )
            
            if cache_valid:
                # Usar caché
                cached_pubs = await self._cache_repo.get_by_scopus_account(account.account_id)
                if cached_pubs:
                    return cached_pubs
        
        # Caché no válida o forzar refresh: consultar Scopus
        publications = await self._fetch_from_scopus(account.scopus_id)
        
        # Guardar en caché
        if publications:
            await self._cache_repo.save_publications(publications, account.account_id)
        
        return publications

    async def _fetch_from_scopus(self, scopus_id: str) -> List[Publication]:
        """Obtiene publicaciones desde la API de Scopus y las enriquece con SJR."""
        raw_publications = await self._publication_repo.get_publications_by_scopus_id(scopus_id)
        
        publications = []
        for raw_pub in raw_publications:
            pub = self._transform_raw_publication(raw_pub)
            pub = self._enrich_with_sjr(pub)
            publications.append(pub)
        
        return publications

    async def get_publications_by_scopus_id(
        self, 
        scopus_id: str
    ) -> List[PublicationResponseDTO]:
        """
        Obtiene las publicaciones de una cuenta Scopus específica.
        
        Este método NO usa caché ya que no tiene el account_id.
        Útil para verificar publicaciones antes de vincular una cuenta.
        
        Args:
            scopus_id: ID de Scopus del autor
            
        Returns:
            Lista de DTOs de publicaciones
        """
        publications = await self._fetch_from_scopus(scopus_id)
        
        # Ordenar por año descendente
        publications.sort(key=lambda p: p.year, reverse=True)
        
        return [PublicationResponseDTO.from_entity(p) for p in publications]

    async def refresh_author_publications(self, author_id: UUID) -> AuthorPublicationsResponseDTO:
        """
        Fuerza la actualización de publicaciones desde Scopus.
        
        Invalida la caché existente y consulta Scopus directamente.
        
        Args:
            author_id: UUID del autor
            
        Returns:
            DTO con las publicaciones actualizadas
        """
        return await self.get_publications_by_author(author_id, force_refresh=True)

    def _transform_raw_publication(self, raw: Dict) -> Publication:
        """
        Transforma los datos crudos de Scopus a una entidad Publication.
        
        Args:
            raw: Diccionario con datos de la API de Scopus
            
        Returns:
            Entidad Publication
        """
        # Extraer año de la fecha de publicación
        cover_date = raw.get("prism:coverDate", "")
        year = int(cover_date[:4]) if cover_date and len(cover_date) >= 4 else 0
        
        # Extraer filiación (buscar la primera disponible)
        affiliations = raw.get("affiliation", [])
        if isinstance(affiliations, dict):
            affiliations = [affiliations]
        
        affiliation_name = "Sin filiación"
        affiliation_id = None
        if affiliations:
            first_aff = affiliations[0]
            affiliation_name = first_aff.get("affilname", "Sin filiación")
            affiliation_id = first_aff.get("afid")
        
        return Publication(
            scopus_id=raw.get("dc:identifier", "").replace("SCOPUS_ID:", ""),
            eid=raw.get("eid", ""),
            doi=raw.get("prism:doi"),
            title=raw.get("dc:title", "Sin título"),
            year=year,
            publication_date=cover_date,
            source_title=raw.get("prism:publicationName", ""),
            document_type=raw.get("subtypeDescription", raw.get("prism:aggregationType", "")),
            affiliation_name=affiliation_name,
            affiliation_id=affiliation_id,
            subject_areas=[],  # Se llenan en el enriquecimiento SJR
            sjr_metrics=[]     # Se llenan en el enriquecimiento SJR
        )

    def _enrich_with_sjr(self, publication: Publication) -> Publication:
        """
        Enriquece una publicación con métricas SJR.
        
        Mapea dinámicamente años futuros al último año disponible.
        
        Args:
            publication: Publicación a enriquecer
            
        Returns:
            Publicación con métricas SJR
        """
        # Obtener métricas SJR para la revista
        metrics = self._sjr_repo.get_journal_metrics(
            publication.source_title, 
            publication.year
        )
        
        # Obtener áreas temáticas
        areas = self._sjr_repo.get_subject_areas(
            publication.source_title,
            publication.year
        )
        
        publication.sjr_metrics = metrics
        publication.subject_areas = areas
        
        return publication

    async def get_statistics_by_author(self, author_id: UUID) -> Dict:
        """
        Obtiene estadísticas de publicaciones de un autor.
        
        Args:
            author_id: UUID del autor
            
        Returns:
            Diccionario con estadísticas por año y por tipo
        """
        author_pubs = await self.get_publications_by_author(author_id)
        
        by_year: Dict[int, int] = {}
        by_type: Dict[str, int] = {}
        by_quartile: Dict[str, int] = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0, "Sin cuartil": 0}
        
        for pub in author_pubs.publications:
            # Por año
            by_year[pub.year] = by_year.get(pub.year, 0) + 1
            
            # Por tipo
            by_type[pub.document_type] = by_type.get(pub.document_type, 0) + 1
            
            # Por mejor cuartil
            quartile = pub.best_quartile or "Sin cuartil"
            by_quartile[quartile] = by_quartile.get(quartile, 0) + 1
        
        return {
            "author_id": str(author_id),
            "total_publications": author_pubs.total_publications,
            "by_year": dict(sorted(by_year.items(), reverse=True)),
            "by_type": by_type,
            "by_quartile": by_quartile
        }