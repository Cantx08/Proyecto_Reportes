from pydantic import BaseModel
from typing import List, Optional

class Publicacion(BaseModel):
    titulo: str
    anio: str
    fuente: str
    tipo: str
    filiacion: str
    doi: str
    categorias: str = ""

    def formato_texto(self):
        return f'({self.anio}) "{self.titulo}". {self.fuente}. Indexada en SCOPUS - {self.categorias}. DOI: {self.doi} ({self.filiacion})'

class AutorPublicaciones(BaseModel):
    author_id: str
    publicaciones: Optional[List[Publicacion]] = None
    error: Optional[str] = None


class RespuestaPublicaciones(BaseModel):
    publicaciones: List[AutorPublicaciones]

