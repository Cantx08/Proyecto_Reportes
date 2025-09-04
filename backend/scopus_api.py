import unicodedata
import requests
import pandas as pd
from models import Autor, Publicacion
from config import SCOPUS_API_KEY
from config import SJR_CSV_PATH
from collections import Counter

def normalizar_sjr(datos_sjr):
    """
    Normaliza el texto para mejorar la coincidencia entre nombres de revistas.
    Elimina tildes, convierte a minúsculas, elimina símbolos y espacios extra.
    """
    if not isinstance(datos_sjr, str):
        datos_sjr = str(datos_sjr)
    datos_sjr = datos_sjr.lower().strip()
    datos_sjr = unicodedata.normalize('NFKD', datos_sjr)
    datos_sjr = ''.join(c for c in datos_sjr if not unicodedata.combining(c))
    datos_sjr = datos_sjr.replace('&', 'and')
    datos_sjr = ''.join(c for c in datos_sjr if c.isalnum() or c.isspace())
    datos_sjr = ' '.join(datos_sjr.split())
    return datos_sjr

try:
    """
    Cachear el DataFrame al cargar el módulo
    """
    SJR_DF = pd.read_csv(SJR_CSV_PATH, sep=';')
    SJR_DF['Title_norm'] = SJR_DF['Title'].apply(normalizar_sjr)
except Exception:
    SJR_DF = None

def obtener_publicaciones(ids):
    """
    Obtiene las publicaciones de Scopus para una lista de IDs de autor.
    Retorna una lista de diccionarios con los datos estructurados por autor.
    """
    lista_final_publicaciones = []
    for id_autor in ids:
        url = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({id_autor})"
        headers = {"X-ELS-APIKey": SCOPUS_API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data.get("search-results", {}).get("entry", [])
            publicaciones_autor = []  # Lista específica para este autor
            for publicacion in results:
                titulo = publicacion.get("dc:title", "")
                anio = publicacion.get("prism:coverDate", "")[:4] if publicacion.get("prism:coverDate") else ""
                fuente = publicacion.get("prism:publicationName", "")
                tipo_documento = publicacion.get("subtypeDescription", "")
                filiacion = ""
                if "affiliation" in publicacion and publicacion["affiliation"]:
                    filiacion = publicacion["affiliation"][0].get("affilname", "")
                if not filiacion or "escuela politécnica nacional".lower() not in filiacion.lower():
                    filiacion = "Sin filiación"
                doi = publicacion.get("prism:doi", "")
                categorias = obtener_categorias(fuente, anio)
                publicaciones_autor.append({
                    "titulo": titulo,
                    "fuente": fuente,
                    "tipo_documento": tipo_documento,
                    "filiacion": filiacion,
                    "anio": anio,
                    "doi": doi,
                    "categorias": categorias
                })
            lista_final_publicaciones.append({"author_id": id_autor, "publicaciones": publicaciones_autor})
        else:
            lista_final_publicaciones.append({"author_id": id_autor, "error": response.text})
    return lista_final_publicaciones


def agrupar_publicaciones_por_autor(datos_scopus, ids):
    """
    Agrupa todas las publicaciones de los IDs en un solo autor.
    """
    lista_publicaciones = []
    errores = []
    for autor in datos_scopus:
        if "error" in autor:
            errores.append(autor["error"])
        else:
            pubs = [Publicacion(**pub) for pub in autor["publicaciones"]]
            lista_publicaciones.extend(pubs)
    autor_id = ','.join(ids)
    lista_final_publicaciones = Autor(id_autor=autor_id, lista_publicaciones=lista_publicaciones)
    if errores:
        lista_final_publicaciones.error = '; '.join(errores)
    return lista_final_publicaciones


def obtener_categorias(nombre_fuente, anio):
    """
    Busca las categorías de una revista en un año específico usando el DataFrame cacheado de SJR.
    Retorna las categorías si hay coincidencia, o un mensaje si no existe.
    """
    if SJR_DF is None:
        return "No disponible"
    anio = str(anio)
    fuente_normalizada = normalizar_sjr(nombre_fuente)
    match = SJR_DF[(SJR_DF['Title_norm'] == fuente_normalizada) & (SJR_DF['year'].astype(str) == anio)]
    if not match.empty:
        return match.iloc[0]["Categories"]
    return "No indexada"


def obtener_documentos_por_anio(publicaciones: list) -> dict:
    """
    Recibe una lista de publicaciones (dict o Publicacion) y retorna un dict {anio: cantidad}
    Incluye todos los años en el rango desde el primer año hasta el último año con publicaciones.
    Los años sin publicaciones aparecen con valor 0.
    """
    anios = []
    for publicacion in publicaciones:
        anio = getattr(publicacion, 'anio', None) if hasattr(publicacion, 'anio') else publicacion.get('anio')
        if anio and anio.strip():  # Verificar que el año no esté vacío
            anios.append(int(anio))
    
    if not anios:
        return {}
    
    # Contar publicaciones por año
    contador_anios = Counter(anios)
    
    # Obtener el rango completo de años
    primer_anio = min(anios)
    ultimo_anio = max(anios)
    
    # Crear diccionario con todos los años en el rango
    publicaciones_por_anio = {}
    for anio in range(primer_anio, ultimo_anio + 1):
        publicaciones_por_anio[str(anio)] = contador_anios.get(anio, 0)
    
    return publicaciones_por_anio


def obtener_areas_tematicas(publicaciones: list) -> dict:
    """
    Extrae y cuenta las subject areas de las publicaciones.
    Retorna un diccionario con las subject areas y su conteo.
    """
    areas_tematicas = []
    
    for publicaciones in publicaciones:
        categorias = getattr(publicaciones, 'categorias', None) if hasattr(publicaciones, 'categorias') else publicaciones.get('categorias', '')

        if categorias and categorias != "No indexada" and categorias != "No disponible":
            # Las categorías pueden venir separadas por ';' o por otros delimitadores
            # Ejemplo: "Engineering (Q2); Materials Science (Q1)"
            areas = categorias.split(';')
            for area in areas:
                area = area.strip()
                if area:
                    # Extraer solo el nombre del área (sin el ranking Q1, Q2, etc.)
                    # Buscar paréntesis y tomar solo lo que está antes
                    if '(' in area:
                        area = area.split('(')[0].strip()
                    areas_tematicas.append(area)
    
    # Contar las subject areas
    contador_areas = Counter(areas_tematicas)
    
    # Ordenar por conteo descendente
    areas_ordenadas = dict(sorted(contador_areas.items(), key=lambda x: x[1], reverse=True))

    return areas_ordenadas