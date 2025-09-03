from pydantic import BaseModel
from typing import List, Optional

class Publication(BaseModel):
    title: str
    year: str
    source: str
    document_type: str
    affiliation: str
    doi: str
    categories: str = ""

    def text_format(self):
        return f'({self.year}) "{self.title}". {self.source}. Indexada en SCOPUS - {self.categories}. DOI: {self.doi} ({self.affiliation})'

class Author(BaseModel):
    author_id: str
    publications: Optional[List[Publication]] = None
    error: Optional[str] = None


class PublicationResponses(BaseModel):
    publicaciones: List[Author]

