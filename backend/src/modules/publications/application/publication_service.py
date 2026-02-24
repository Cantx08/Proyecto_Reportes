"""
Servicio de aplicación para gestión de publicaciones.

Arquitectura (post-refactoring IP institucional):
  - El frontend llama a Scopus directamente (IP institucional).
  - El backend se encarga de transformar, enriquecer con SJR y cachear.
  - Los datos se devuelven desde la caché local.
"""

from typing import List, Dict, Optional
from uuid import UUID
import logging
from .publication_dto import PublicationResponseDTO, AuthorPublicationsResponseDTO
from ..domain.publication import Publication
from ..domain.publication_cache_repository import IPublicationCacheRepository
from ..domain.sjr_repository import ISJRRepository
from ...scopus_accounts.domain.scopus_account_repository import IScopusAccountRepository

logger = logging.getLogger(__name__)


class PublicationService:
    """
    Servicio de aplicación para gestión de publicaciones.

    Ya NO llama a la API de Scopus.  Recibe datos crudos del frontend
    (que usa la IP institucional) y los procesa / cachea localmente.
    """
    
    # Tiempo de validez de la caché en horas
    CACHE_MAX_AGE_HOURS = 24
    EPN_AFFILIATION_ID = "60072054"
    
    
    def __init__(
        self,
        cache_repo: Optional[IPublicationCacheRepository],
        sjr_repo: ISJRRepository,
        scopus_account_repo: IScopusAccountRepository
    ):
        self._cache_repo = cache_repo
        self._sjr_repo = sjr_repo
        self._scopus_account_repo = scopus_account_repo

    def _transform_raw_publication(self, raw: Dict, scopus_author_id: str) -> Publication:
        """
        Transforma y aplica la lógica de validación de filiación estricta.
        """
        cover_date = raw.get("prism:coverDate", "")
        year = int(cover_date[:4]) if cover_date and len(cover_date) >= 4 else 0
        
        # Lógica central: Determinar si este autor, en este paper, firmó como EPN
        affiliation_name, affiliation_id, is_epn = self._analyze_affiliation_link(
            raw, scopus_author_id
        )
        
        # Extracción del Sourceid de la revista/fuente
        raw_source_id = raw.get("source-id")
        source_id = str(raw_source_id).strip() if raw_source_id else None

        return Publication(
            scopus_id=raw.get("dc:identifier", "").replace("SCOPUS_ID:", ""),
            eid=raw.get("eid", ""),
            doi=raw.get("prism:doi"),
            source_id=source_id,
            title=raw.get("dc:title", "Sin título"),
            year=year,
            publication_date=cover_date,
            source_title=raw.get("prism:publicationName", ""),
            document_type=raw.get("subtypeDescription", raw.get("prism:aggregationType", "")),
            
            # Nuevos datos calculados
            affiliation_name=affiliation_name,
            affiliation_id=affiliation_id,
            is_epn_affiliated=is_epn, # <--- La verdad de la milanesa
            
            subject_areas=[],
            categories_with_quartiles=[],
            sjr_year_used=None
        )
    
    def _analyze_affiliation_link(self, raw: Dict, target_author_id: str) -> tuple[str, Optional[str], bool]:
        """
        Analiza si el author_id específico está vinculado al AF-ID de la EPN en este documento.
        Retorna: (Nombre Filiación, ID Filiación, Es_EPN_Boolean)
        """
        # 1. Obtener lista de autores del paper
        authors = raw.get("author", [])
        if isinstance(authors, dict): authors = [authors]
        
        # 2. Obtener lista de afiliaciones globales del paper (para buscar nombres)
        affiliations_metadata = raw.get("affiliation", [])
        if isinstance(affiliations_metadata, dict): affiliations_metadata = [affiliations_metadata]
        
        # Diccionario auxiliar para buscar nombres de afiliaciones por ID rápido
        aff_lookup = {
            aff.get("afid"): aff.get("affilname", "Desconocida") 
            for aff in affiliations_metadata if aff.get("afid")
        }

        # 3. Buscar al autor objetivo
        target_author = next((a for a in authors if a.get("authid") == target_author_id), None)

        if not target_author:
            # Caso raro: El paper salió en la búsqueda pero el autor no aparece en la lista explícita
            # Esto pasa en "Group Authors" a veces. Asumimos False por seguridad.
            return "Autor no listado explícitamente", None, False

        # 4. Obtener los IDs de filiación DE ESTE AUTOR en este paper
        # Scopus devuelve 'afid' como un array de objetos (view=COMPLETE) o string
        author_afids = []
        raw_afids = target_author.get("afid", [])
        
        if isinstance(raw_afids, list):
            # Formato: [{'@_fa': 'true', '$': '12345'}, ...] o ['12345']
            for item in raw_afids:
                if isinstance(item, dict):
                    author_afids.append(item.get("$", ""))
                else:
                    author_afids.append(str(item))
        elif isinstance(raw_afids, dict):
            author_afids.append(raw_afids.get("$", ""))
        elif isinstance(raw_afids, str):
            # A veces viene separado por espacios si no es array
            author_afids = raw_afids.split()

        # 5. VERIFICACIÓN MAESTRA: ¿Está el ID de la EPN en los IDs de este autor?
        is_epn = self.EPN_AFFILIATION_ID in author_afids

        # 6. Resolver nombre de afiliación para mostrar
        if is_epn:
            # Si es EPN, forzamos que se muestre como tal y devolvemos el ID de EPN
            return aff_lookup.get(self.EPN_AFFILIATION_ID, "Escuela Politécnica Nacional"), self.EPN_AFFILIATION_ID, True
        
        # Si no es EPN, devolvemos su primera afiliación (la principal externa)
        if author_afids:
            primary_afid = author_afids[0]
            return aff_lookup.get(primary_afid, "Filiación Externa"), primary_afid, False
            
        return "Sin filiación", None, False

    def _get_author_affiliation(self, raw: Dict, scopus_author_id: str) -> tuple[str, Optional[str]]:
        authors = raw.get("author", [])
        if isinstance(authors, dict):
            authors = [authors]
        
        for author in authors:
            authid = author.get("authid", "")
            if authid == scopus_author_id:
                afid = author.get("afid")
                if afid:
                    affiliations = raw.get("affiliation", [])
                    if isinstance(affiliations, dict):
                        affiliations = [affiliations]
                    
                    for aff in affiliations:
                        if aff.get("afid") == afid:
                            return aff.get("affilname", "Sin filiación"), afid
                    return "Afiliación ID: " + afid, afid
        
        affiliations = raw.get("affiliation", [])
        if isinstance(affiliations, dict):
            affiliations = [affiliations]
        
        if affiliations:
            first_aff = affiliations[0]
            return first_aff.get("affilname", "Sin filiación"), first_aff.get("afid")
        
        return "Sin filiación", None

    def _enrich_with_sjr(self, publication: Publication) -> Publication:
        """
        Enriquece usando Sourceid como búsqueda primaria, con fallback por nombre de revista.
        """
        areas, categories_with_quartiles, sjr_year_used = self._sjr_repo.get_journal_data(
            publication.source_id, 
            publication.year,
            publication.source_title
        )
        
        publication.subject_areas = areas
        publication.categories_with_quartiles = categories_with_quartiles
        publication.sjr_year_used = sjr_year_used
        
        return publication

    async def get_statistics_by_author(self, author_id: UUID) -> Dict:
        """
        Obtiene estadísticas de publicaciones desde la caché local.
        No llama a la API de Scopus.
        """
        author_pubs = await self.get_cached_publications_by_author(author_id)
        
        by_year: Dict[int, int] = {}
        by_type: Dict[str, int] = {}
        
        for pub in author_pubs.publications:
            by_year[pub.year] = by_year.get(pub.year, 0) + 1
            by_type[pub.document_type] = by_type.get(pub.document_type, 0) + 1
        
        return {
            "author_id": str(author_id),
            "total_publications": author_pubs.total_publications,
            "by_year": dict(sorted(by_year.items(), reverse=True)),
            "by_type": by_type
        }

    # ------------------------------------------------------------------
    # Métodos para el flujo frontend-Scopus (refactoring IP institucional)
    # El frontend llama a Scopus directamente con la IP institucional y
    # envía los datos crudos al backend para transformación, enriquecimiento
    # SJR y caché.
    # ------------------------------------------------------------------

    async def get_scopus_account_status(self, author_id: UUID) -> dict:
        """
        Devuelve las cuentas Scopus del autor con su estado de caché,
        SIN realizar ninguna llamada a la API de Scopus.

        Uso: el frontend llama a este endpoint primero para saber:
        - qué Scopus IDs debe consultar directamente
        - cuáles ya están en caché y no necesitan re-consulta
        """
        scopus_accounts = await self._scopus_account_repo.get_by_author(author_id)
        if not scopus_accounts:
            raise ValueError("El autor no tiene cuentas Scopus asociadas.")

        result = []
        for account in scopus_accounts:
            cache_valid = False
            if self._cache_repo:
                cache_valid = await self._cache_repo.is_cache_valid(
                    account.account_id, self.CACHE_MAX_AGE_HOURS
                )
            result.append({
                "account_id": str(account.account_id),
                "scopus_id": account.scopus_id,
                "cache_valid": cache_valid,
            })

        return {"author_id": str(author_id), "scopus_accounts": result}

    async def get_cached_publications_by_author(self, author_id: UUID) -> AuthorPublicationsResponseDTO:
        """
        Devuelve las publicaciones almacenadas en caché para el autor,
        fusionando y deduplicando todas sus cuentas Scopus.

        No realiza ninguna llamada a la API de Scopus.
        Útil cuando el frontend ya sabe que la caché es válida.
        """
        scopus_accounts = await self._scopus_account_repo.get_by_author(author_id)
        if not scopus_accounts:
            raise ValueError("El autor no tiene cuentas Scopus asociadas.")

        scopus_ids = [acc.scopus_id for acc in scopus_accounts]
        all_publications: List[Publication] = []

        for account in scopus_accounts:
            if self._cache_repo:
                cached = await self._cache_repo.get_by_scopus_account(account.account_id)
                all_publications.extend(cached)

        # Deduplicar por scopus_id
        seen: Dict[str, Publication] = {}
        for pub in all_publications:
            seen[pub.scopus_id] = pub
        unique_pubs = sorted(seen.values(), key=lambda p: p.year, reverse=True)

        return AuthorPublicationsResponseDTO(
            author_id=str(author_id),
            scopus_ids=scopus_ids,
            total_publications=len(unique_pubs),
            publications=[PublicationResponseDTO.from_entity(p) for p in unique_pubs],
        )

    async def process_account_publications(
        self,
        account_id: UUID,
        scopus_author_id: str,
        raw_publications: List[Dict],
    ) -> List[Publication]:
        """
        Transforma datos crudos de Scopus, los enriquece con SJR y los
        guarda en caché.

        Flujo esperado (llamado desde el frontend):
        1. Frontend obtiene entradas crudas de Scopus (view=COMPLETE)
        2. Envía account_id + scopus_author_id + raw_publications a este endpoint
        3. El backend transforma, enriquece y cachea
        4. Devuelve las publicaciones procesadas
        """
        publications: List[Publication] = []
        for raw in raw_publications:
            pub = self._transform_raw_publication(raw, scopus_author_id)
            pub = self._enrich_with_sjr(pub)
            publications.append(pub)

        if publications and self._cache_repo:
            await self._cache_repo.save_publications(publications, account_id)

        return publications

    async def process_raw_publications_preview(
        self,
        scopus_author_id: str,
        raw_publications: List[Dict],
    ) -> List[Publication]:
        """
        Transforma y enriquece datos crudos de Scopus SIN guardar en caché.

        Útil para previsualizar publicaciones de un Scopus ID que aún no
        está asociado como cuenta (no existe account_id).
        """
        publications: List[Publication] = []
        for raw in raw_publications:
            pub = self._transform_raw_publication(raw, scopus_author_id)
            pub = self._enrich_with_sjr(pub)
            publications.append(pub)
        publications.sort(key=lambda p: p.year, reverse=True)
        return publications
