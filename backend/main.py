from fastapi import FastAPI, Query
from typing import List
from models import Publicaciones
from scopus_api import agrupar_publicaciones_por_autor, obtener_publicaciones, obtener_documentos_por_anio, obtener_areas_tematicas

app = FastAPI()

@app.get("/scopus/publications", response_model=Publicaciones)
def get_publications(ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus")):
    """
    Obtiene publicaciones de uno o varios IDs de autor Scopus.
    Agrupa todas las publicaciones bajo un solo autor.
    """
    scopus_data = obtener_publicaciones(ids)
    autor_obj = agrupar_publicaciones_por_autor(scopus_data, ids)
    return Publicaciones(publicaciones=[autor_obj])

@app.get("/scopus/docs_by_year")
def get_documents_by_year(ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus")):
    """
    Obtiene el número de publicaciones por año realizadas por un autor que tiene uno o varios IDs.
    """
    scopus_data = obtener_publicaciones(ids)
    publicaciones = []
    for autor in scopus_data:
        if "publicaciones" in autor:
            publicaciones.extend(autor["publicaciones"])
    conteo = obtener_documentos_por_anio(publicaciones)
    return conteo

@app.get("/scopus/subject_areas")
def get_subject_areas(ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus")):
    """
    Obtiene las áreas temáticas generales del análisis de resultados de las publicaciones del autor.
    """
    scopus_data = obtener_publicaciones(ids)
    publicaciones = []
    for autor in scopus_data:
        if "publicaciones" in autor:
            publicaciones.extend(autor["publicaciones"])
    areas = obtener_areas_tematicas(publicaciones)
    return areas

