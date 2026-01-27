import unicodedata
import pandas as pd
from typing import Dict, Tuple, List, Any
from ...domain.repositories.sjr_repository import SJRRepository

class SJRFileRepository(SJRRepository):
    """Repositorio de datos SJR con cálculo automático de percentiles por categoría."""
    
    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        # Cache: (nombre_normalizado, año) -> Lista de diccionarios con info detallada
        self._data_cache: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Carga datos y calcula percentiles reales procesando todo el dataset."""
        try:
            # Asegurarse de que el separador sea el correcto (SJR suele usar ';')
            # Necesitamos la columna 'SJR' para ordenar. Si tiene comas decimales, hay que manejarlas.
            df = pd.read_csv(self._csv_path, sep=';', decimal=',') 
            
            # Normalizar títulos una sola vez
            df['Title_norm'] = df['Title'].apply(self.normalize_journal_name)
            
            # Convertir SJR a numérico si no lo es (a veces viene como string en pandas)
            if 'SJR' in df.columns:
                 # Limpiar posibles strings vacíos o nulos
                df['SJR'] = pd.to_numeric(df['SJR'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
            else:
                print("Error Crítico: No se encontró la columna 'SJR' para calcular rankings.")
                return

            # --- PASO 1: Agrupar revistas por Categoría ---
            # Estructura temporal: {'Ecology': [(sjr_score, title_norm, quartile), ...]}
            categories_map = {} 
            
            # Diccionario auxiliar para guardar los cuartiles crudos de cada revista
            # journal_raw_data[(title_norm, year)] = row
            
            # Iteramos una sola vez para explotar las categorías
            for _, row in df.iterrows():
                title_norm = row['Title_norm']
                sjr_score = row['SJR']
                categories_str = str(row['Categories'])
                year = str(row.get('year', '2023')) # Ajustar si tu CSV no tiene año explícito
                
                # Parsear categorías: "Ecology (Q1); Biology (Q2)"
                parsed_cats = self._parse_categories_string(categories_str)
                
                for cat_data in parsed_cats:
                    cat_name = cat_data['name']
                    quartile = cat_data['quartile']
                    
                    if cat_name not in categories_map:
                        categories_map[cat_name] = []
                    
                    # Guardamos la info necesaria para rankear
                    categories_map[cat_name].append({
                        'sjr': sjr_score,
                        'title': title_norm,
                        'quartile': quartile,
                        'year': year
                    })

            # --- PASO 2: Calcular Percentiles por Categoría ---
            # Ahora que tenemos todas las revistas de "Ecology" juntas, las ordenamos.
            
            # Cache temporal para ir construyendo el resultado final por revista
            # result_builder[(title, year)] = [ {cat_info}, {cat_info} ]
            result_builder = {}

            for cat_name, items in categories_map.items():
                # Ordenar por SJR descendente (Mayor impacto primero)
                items.sort(key=lambda x: x['sjr'], reverse=True)
                
                total_journals = len(items)
                
                for rank, item in enumerate(items, 1):
                    # Calcular percentil exacto (Top 1% es 1.0, Top 10% es 10.0)
                    percentile = (rank / total_journals) * 100
                    
                    key = (item['title'], item['year'])
                    
                    if key not in result_builder:
                        result_builder[key] = []
                    
                    result_builder[key].append({
                        'name': cat_name,
                        'quartile': item['quartile'],
                        'percentile': round(percentile, 1), # Ej: 5.3
                        'rank': rank,
                        'total': total_journals
                    })
            
            # --- PASO 3: Guardar en Caché Final ---
            self._data_cache = result_builder
                
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo SJR en {self._csv_path}")
            self._data_cache = {}
        except Exception as e:
            print(f"Error procesando SJR: {e}")
            self._data_cache = {}

    def get_journal_categories(self, journal_name: str, year: str) -> Any:
        """Devuelve la lista estructurada de categorías con percentiles."""
        if not self._data_cache:
            return "No disponible"
        
        edition_year = str(year)
        normalized_journal = self.normalize_journal_name(journal_name)
        
        # Retorna la lista de dicts o un string default
        return self._data_cache.get((normalized_journal, edition_year), "No indexada")

    def _parse_categories_string(self, cat_str: str) -> List[Dict[str, str]]:
        """Convierte 'Cat A (Q1); Cat B (Q2)' en lista de dicts."""
        if not isinstance(cat_str, str) or not cat_str:
            return []
            
        results = []
        parts = cat_str.split(';')
        
        for part in parts:
            part = part.strip()
            if not part: continue
            
            quartile = "Q4" # Default
            name = part
            
            # Extraer Q
            if "(Q1)" in part: 
                quartile = "Q1"
                name = part.replace("(Q1)", "")
            elif "(Q2)" in part: 
                quartile = "Q2"
                name = part.replace("(Q2)", "")
            elif "(Q3)" in part: 
                quartile = "Q3"
                name = part.replace("(Q3)", "")
            elif "(Q4)" in part: 
                quartile = "Q4"
                name = part.replace("(Q4)", "")
                
            results.append({
                'name': name.strip(),
                'quartile': quartile
            })
        return results

    def normalize_journal_name(self, name: str) -> str:
        # ... (Tu código de normalización existente se mantiene igual) ...
        if not isinstance(name, str):
            name = str(name)
        name = name.lower().strip()
        name = unicodedata.normalize('NFKD', name)
        name = ''.join(c for c in name if not unicodedata.combining(c))
        name = name.replace('&', 'and')
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        name = ' '.join(name.split())
        return name