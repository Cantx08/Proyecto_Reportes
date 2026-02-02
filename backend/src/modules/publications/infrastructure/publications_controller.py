from typing import List, Union
from ....application.dto import AuthorDTO, DocumentsByYearResponseDTO, PublicationDTO, PublicationsResponseDTO
from backend.src.modules.publications.application.publication_service import PublicationService
from backend.src.modules.authors.domain.author import Author
from ....domain.entities.author_publications import AuthorPublications


class PublicationsController:
    """Controlador para endpoints de publicaciones."""

    def __init__(self, publication_service: PublicationService):
        self._publication_service = publication_service

    async def get_publications(self, author_ids: List[str]) -> PublicationsResponseDTO:
        """Obtiene publicaciones de autores."""
        collection = await self._publication_service.fetch_grouped_publications(author_ids)

        authors_dto = []
        for author in collection.authors:
            author_dto = self._map_author_to_dto(author)
            authors_dto.append(author_dto)

        return PublicationsResponseDTO(publications=authors_dto)

    async def get_documents_by_year(self, author_ids: List[str]) -> DocumentsByYearResponseDTO:
        """Obtiene estadísticas de documentos por año."""
        statistics = await self._publication_service.get_statistics_by_year(author_ids)

        return DocumentsByYearResponseDTO(
            author_ids=author_ids,
            documents_by_year=statistics
        )

    @staticmethod
    def _map_author_to_dto(author: Union[Author, AuthorPublications]) -> AuthorDTO:
        """Convierte una entidad Autor a DTO."""
        publications_dto = []

        if author.publications_list:
            for pub in author.publications_list:
                pub_dto = PublicationDTO(
                    title=pub.title,
                    year=pub.year,
                    source=pub.source,
                    document_type=pub.document_type,
                    affiliation=pub.affiliation,
                    doi=pub.doi,
                    categories=pub.categories
                )
                publications_dto.append(pub_dto)

        # Si es un AuthorPublications (solo publicaciones de Scopus)
        if isinstance(author, AuthorPublications):
            return AuthorDTO(
                author_id=author.author_id,
                name="",  # No disponible desde Scopus
                surname="",  # No disponible desde Scopus
                dni="",  # No disponible desde Scopus
                publications_list=publications_dto,
                error=author.error
            )
        
        # Si es un Author completo
        return AuthorDTO(
            author_id=author.author_id or "",
            name=author.name,
            surname=author.surname,
            dni=author.dni,
            title=author.title,
            birth_date=author.birth_date,
            gender=author.gender,
            position=author.position,
            department=author.department,
            publications_list=publications_dto,
            error=author.error
        )
