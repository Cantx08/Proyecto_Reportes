from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .publication_dto import PublicationDTO


class AuthorDTO(BaseModel):
    """DTO para autor."""
    author_id: str
    publications_list: Optional[List["PublicationDTO"]] = None
    error: Optional[str] = None
