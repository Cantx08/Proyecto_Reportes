from pydantic import BaseModel, Field
from typing import List, Optional

class Publicacion(BaseModel):
    titulo: str
    anio: str
    fuente: str
    tipo_documento: str
    filiacion: str
    doi: str
    categorias: str = ""

class Autor(BaseModel):
    id_autor: str
    lista_publicaciones: Optional[List[Publicacion]] = None
    error: Optional[str] = None


class Publicaciones(BaseModel):
    publicaciones: List[Autor]

