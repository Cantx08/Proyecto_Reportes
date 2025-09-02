import unicodedata
import requests
import pandas as pd
from config import SCOPUS_API_KEY
from config import SJR_CSV_PATH

def normalizar_texto(texto):
    """
    Normaliza el texto para mejorar la coincidencia entre nombres de revistas.
    Elimina tildes, convierte a minúsculas, elimina símbolos y espacios extra.
    """
    if not isinstance(texto, str):
        texto = str(texto)
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = texto.replace('&', 'and')
    texto = ''.join(c for c in texto if c.isalnum() or c.isspace())
    texto = ' '.join(texto.split())
    return texto

# Cachear el DataFrame al cargar el módulo
try:
    SJR_DF = pd.read_csv(SJR_CSV_PATH, sep=';')
    SJR_DF['Title_norm'] = SJR_DF['Title'].apply(normalizar_texto)
except Exception:
    SJR_DF = None

def obtener_categorias_revista(nombre_revista, anio):
    """
    Busca las categorías de una revista en un año específico usando el DataFrame cacheado de SJR.
    Retorna las categorías si hay coincidencia, o un mensaje si no existe.
    """
    if SJR_DF is None:
        return "No disponible"
    anio = str(anio)
    nombre_revista_norm = normalizar_texto(nombre_revista)
    match = SJR_DF[(SJR_DF['Title_norm'] == nombre_revista_norm) & (SJR_DF['year'].astype(str) == anio)]
    if not match.empty:
        return match.iloc[0]["Categories"]
    return "No indexada"

def contar_documentos_por_anio(publicaciones: list) -> dict:
    """
    Recibe una lista de publicaciones (dict o Publicacion) y retorna un dict {anio: cantidad}
    """
    from collections import Counter
    anios = []
    for pub in publicaciones:
        anio = getattr(pub, 'anio', None) if hasattr(pub, 'anio') else pub.get('anio')
        if anio:
            anios.append(anio)
    return dict(Counter(anios))

def obtener_publicaciones_scopus(ids):
    """
    Obtiene las publicaciones de Scopus para una lista de IDs de autor.
    Retorna una lista de diccionarios con los datos estructurados por autor.
    """
    publicaciones = []
    for author_id in ids:
        url = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({author_id})"
        headers = {"X-ELS-APIKey": SCOPUS_API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data.get("search-results", {}).get("entry", [])
            publicaciones_autor = []
            for pub in results:
                titulo = pub.get("dc:title", "")
                anio = pub.get("prism:coverDate", "")[:4] if pub.get("prism:coverDate") else ""
                fuente = pub.get("prism:publicationName", "")
                tipo = pub.get("subtypeDescription", "")
                filiacion = ""
                if "affiliation" in pub and pub["affiliation"]:
                    filiacion = pub["affiliation"][0].get("affilname", "")
                if not filiacion or "escuela politécnica nacional".lower() not in filiacion.lower():
                    filiacion = "Sin filiación"
                doi = pub.get("prism:doi", "")
                categorias = obtener_categorias_revista(fuente, anio)
                publicaciones_autor.append({
                    "titulo": titulo,
                    "fuente": fuente,
                    "tipo": tipo,
                    "filiacion": filiacion,
                    "anio": anio,
                    "doi": doi,
                    "categorias": categorias
                })
            publicaciones.append({"author_id": author_id, "publicaciones": publicaciones_autor})
        else:
            publicaciones.append({"author_id": author_id, "error": response.text})
    return publicaciones