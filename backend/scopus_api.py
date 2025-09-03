import unicodedata
import requests
import pandas as pd
from models import Author, Publication
from config import SCOPUS_API_KEY
from config import SJR_CSV_PATH

def normalize_sjr(data):
    """
    Normaliza el texto para mejorar la coincidencia entre nombres de revistas.
    Elimina tildes, convierte a minúsculas, elimina símbolos y espacios extra.
    """
    if not isinstance(data, str):
        data = str(data)
    data = data.lower().strip()
    data = unicodedata.normalize('NFKD', data)
    data = ''.join(c for c in data if not unicodedata.combining(c))
    data = data.replace('&', 'and')
    data = ''.join(c for c in data if c.isalnum() or c.isspace())
    data = ' '.join(data.split())
    return data

try:
    """
    Cachear el DataFrame al cargar el módulo
    """
    SJR_DF = pd.read_csv(SJR_CSV_PATH, sep=';')
    SJR_DF['Title_norm'] = SJR_DF['Title'].apply(normalize_sjr)
except Exception:
    SJR_DF = None

def get_journal_categories(journal_name, year):
    """
    Busca las categorías de una revista en un año específico usando el DataFrame cacheado de SJR.
    Retorna las categorías si hay coincidencia, o un mensaje si no existe.
    """
    if SJR_DF is None:
        return "No disponible"
    year = str(year)
    normalized_journal_name = normalize_sjr(journal_name)
    match = SJR_DF[(SJR_DF['Title_norm'] == normalized_journal_name) & (SJR_DF['year'].astype(str) == year)]
    if not match.empty:
        return match.iloc[0]["Categories"]
    return "No indexada"

def count_documents_by_year(publications: list) -> dict:
    """
    Recibe una lista de publicaciones (dict o Publicacion) y retorna un dict {anio: cantidad}
    Incluye todos los años en el rango desde el primer año hasta el último año con publicaciones.
    Los años sin publicaciones aparecen con valor 0.
    """
    from collections import Counter
    years = []
    for pub in publications:
        year = getattr(pub, 'year', None) if hasattr(pub, 'year') else pub.get('year')
        if year and year.strip():  # Verificar que el año no esté vacío
            years.append(int(year))
    
    if not years:
        return {}
    
    # Contar publicaciones por año
    year_counts = Counter(years)
    
    # Obtener el rango completo de años
    min_year = min(years)
    max_year = max(years)
    
    # Crear diccionario con todos los años en el rango
    complete_years = {}
    for year in range(min_year, max_year + 1):
        complete_years[str(year)] = year_counts.get(year, 0)
    
    return complete_years

def get_scopus_publications(ids):
    """
    Obtiene las publicaciones de Scopus para una lista de IDs de autor.
    Retorna una lista de diccionarios con los datos estructurados por autor.
    """
    publications = []
    for author_id in ids:
        url = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({author_id})"
        headers = {"X-ELS-APIKey": SCOPUS_API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data.get("search-results", {}).get("entry", [])
            pubs = []
            for pub in results:
                title = pub.get("dc:title", "")
                year = pub.get("prism:coverDate", "")[:4] if pub.get("prism:coverDate") else ""
                source = pub.get("prism:publicationName", "")
                document_type = pub.get("subtypeDescription", "")
                affiliation = ""
                if "affiliation" in pub and pub["affiliation"]:
                    affiliation = pub["affiliation"][0].get("affilname", "")
                if not affiliation or "escuela politécnica nacional".lower() not in affiliation.lower():
                    affiliation = "Sin filiación"
                doi = pub.get("prism:doi", "")
                categories = get_journal_categories(source, year)
                pubs.append({
                    "title": title,
                    "source": source,
                    "document_type": document_type,
                    "affiliation": affiliation,
                    "year": year,
                    "doi": doi,
                    "categories": categories
                })
            publications.append({"author_id": author_id, "publicaciones": pubs})
        else:
            publications.append({"author_id": author_id, "error": response.text})
    return publications

def group_publications_by_author(scopus_data, ids):
    """
    Agrupa todas las publicaciones de los IDs en un solo autor.
    """
    all_publications = []
    error_list = []
    for autor in scopus_data:
        if "error" in autor:
            error_list.append(autor["error"])
        else:
            pubs = [Publication(**pub) for pub in autor["publicaciones"]]
            all_publications.extend(pubs)
    autor_id = ','.join(ids)
    autor_obj = Author(author_id=autor_id, publications=all_publications)
    if error_list:
        autor_obj.error = '; '.join(error_list)
    return autor_obj