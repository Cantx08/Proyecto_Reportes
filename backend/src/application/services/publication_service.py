from typing import List
from ...domain.entities.author_publications import AuthorPublications
from ...domain.entities.publication import PublicationsCollection
from ...domain.repositories.publications_repository import PublicationsRepository
from ...domain.repositories.sjr_repository import SJRRepository
from ...domain.repositories.scopus_account_repository import ScopusAccountRepository


class PublicationService:
    """Servicio para manejo de publicaciones."""
    
    def __init__(
        self, 
        publications_repository: PublicationsRepository,
        sjr_repository: SJRRepository,
        scopus_account_repository: ScopusAccountRepository
    ):
        self._publications_repository = publications_repository
        self._sjr_repository = sjr_repository
        self._scopus_account_repository = scopus_account_repository

    async def _resolve_scopus_ids(self, mixed_ids: List[str]) -> List[str]:
        """
        Resuelve una lista mezclada de IDs (Scopus IDs o Author IDs) a solo Scopus IDs.
        
        Args:
            mixed_ids: Lista que puede contener Scopus IDs (numéricos) o Author IDs (cualquier formato)
            
        Returns:
            Lista de Scopus IDs únicos
        """
        scopus_ids = []
        
        for id_value in mixed_ids:
            # Si es numérico y tiene 11 dígitos, probablemente es un Scopus ID
            if id_value.isdigit() and len(id_value) == 11:
                scopus_ids.append(id_value)
            else:
                # Intentar buscar como Author ID en la base de datos
                try:
                    accounts = await self._scopus_account_repository.get_by_author_id(id_value)
                    for account in accounts:
                        if account.is_active:
                            scopus_ids.append(account.scopus_id)
                except Exception:
                    # Si no se encuentra, asumir que es un Scopus ID de todas formas
                    scopus_ids.append(id_value)
        
        # Retornar lista única de IDs
        return list(set(scopus_ids))

    async def fetch_grouped_publications(self, mixed_ids: List[str]) -> PublicationsCollection:
        """
        Obtiene y agrupa publicaciones de múltiples autores.
        
        Args:
            mixed_ids: Lista que puede contener Scopus IDs o Author IDs de la base de datos
        """
        # Resolver todos los IDs a Scopus IDs
        scopus_ids = await self._resolve_scopus_ids(mixed_ids)
        
        authors = []
        
        for scopus_id in scopus_ids:
            try:
                publication_list = await self._publications_repository.get_publications_by_author(scopus_id)
                
                # Enriquecer publicaciones con categorías SJR
                for pub in publication_list:
                    if not pub.categories:
                        pub.categories = self._sjr_repository.get_journal_categories(pub.source, pub.year)

                author = AuthorPublications(author_id=scopus_id, publications_list=publication_list)
                authors.append(author)
                
            except Exception as e:
                author_with_error = AuthorPublications(author_id=scopus_id, publications_list=[], error=str(e))
                authors.append(author_with_error)
        
        return PublicationsCollection(authors=authors)

    async def get_statistics_by_year(self, author_ids: List[str]) -> dict[str, int]:
        """Obtiene estadísticas de publicaciones por año."""
        collection = await self.fetch_grouped_publications(author_ids)
        return collection.count_publications_by_year()