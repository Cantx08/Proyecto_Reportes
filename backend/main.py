from fastapi import FastAPI, Query
from typing import List
from models import PublicationResponses
from scopus_api import group_publications_by_author, get_scopus_publications, count_documents_by_year

app = FastAPI()

@app.get("/scopus/publicaciones", response_model=PublicationResponses)
def get_publications(ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus")):
    """
    Obtiene publicaciones de uno o varios IDs de autor Scopus.
    Agrupa todas las publicaciones bajo un solo autor.
    """
    scopus_data = get_scopus_publications(ids)
    autor_obj = group_publications_by_author(scopus_data, ids)
    return PublicationResponses(publicaciones=[autor_obj])

# Nuevo endpoint para documentos por año
@app.get("/scopus/documentos_por_anio")
def get_documents_by_year(ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus")):
    """
    Devuelve el conteo de documentos por año para uno o varios IDs de autor Scopus.
    """
    scopus_data = get_scopus_publications(ids)
    publicaciones = []
    for autor in scopus_data:
        if "publicaciones" in autor:
            publicaciones.extend(autor["publicaciones"])
    conteo = count_documents_by_year(publicaciones)
    return conteo
