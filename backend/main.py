


from fastapi import FastAPI, Query
from typing import List
from models import RespuestaPublicaciones, AutorPublicaciones, Publicacion
from scopus_api import obtener_publicaciones_scopus, contar_documentos_por_anio

app = FastAPI()

def agrupar_publicaciones_por_autor(scopus_data, ids):
    """
    Agrupa todas las publicaciones de los IDs en un solo autor.
    """
    todas_publicaciones = []
    errores = []
    for autor in scopus_data:
        if "error" in autor:
            errores.append(autor["error"])
        else:
            publicaciones = [Publicacion(**pub) for pub in autor["publicaciones"]]
            todas_publicaciones.extend(publicaciones)
    autor_id = ','.join(ids)
    autor_obj = AutorPublicaciones(author_id=autor_id, publicaciones=todas_publicaciones)
    if errores:
        autor_obj.error = '; '.join(errores)
    return autor_obj


@app.get("/scopus/publicaciones", response_model=RespuestaPublicaciones)
def obtener_publicaciones(ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus")):
    """
    Obtiene publicaciones de uno o varios IDs de autor Scopus.
    Agrupa todas las publicaciones bajo un solo autor.
    """
    scopus_data = obtener_publicaciones_scopus(ids)
    autor_obj = agrupar_publicaciones_por_autor(scopus_data, ids)
    return RespuestaPublicaciones(publicaciones=[autor_obj])

# Nuevo endpoint para documentos por año
@app.get("/scopus/documentos_por_anio")
def documentos_por_anio(ids: List[str] = Query(..., description="Lista de IDs de autor de Scopus")):
    """
    Devuelve el conteo de documentos por año para uno o varios IDs de autor Scopus.
    """
    scopus_data = obtener_publicaciones_scopus(ids)
    publicaciones = []
    for autor in scopus_data:
        if "publicaciones" in autor:
            publicaciones.extend(autor["publicaciones"])
    conteo = contar_documentos_por_anio(publicaciones)
    return conteo
