from typing import List
from ...domain.entities.author import Author
from ...domain.entities.publication import PublicationsCollection
from ...domain.repositories.publications_repository import PublicationsRepository
from ...domain.repositories.sjr_repository import SJRRepository


class PublicationService:
    """Servicio para manejo de publicaciones."""
    
    def __init__(
        self, 
        publications_repository: PublicationsRepository,
        sjr_repository: SJRRepository
    ):
        self._publications_repository = publications_repository
        self._sjr_repository = sjr_repository

    async def fetch_grouped_publications(self, author_ids: List[str]) -> PublicationsCollection:
        """Obtiene y agrupa publicaciones de múltiples autores."""
        authors = []
        
        for author_id in author_ids:
            try:
                publication_list = await self._publications_repository.get_publications_by_author(author_id)
                
                # Enriquecer publicaciones con categorías SJR
                for pub in publication_list:
                    if not pub.categories:
                        pub.categories = self._sjr_repository.get_journal_categories(pub.source, pub.year)

                author = Author(author_id=author_id, publications_list=publication_list)
                authors.append(author)
                
            except Exception as e:
                author_with_error = Author(author_id=author_id, error=str(e))
                authors.append(author_with_error)
        
        return PublicationsCollection(authors=authors)

    async def get_statistics_by_year(self, author_ids: List[str]) -> dict[str, int]:
        """Obtiene estadísticas de publicaciones por año."""
        collection = await self.fetch_grouped_publications(author_ids)
        return collection.count_publications_by_year()