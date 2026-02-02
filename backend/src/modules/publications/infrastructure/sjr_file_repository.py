import unicodedata
import pandas as pd
from typing import Dict, Tuple, List, Any
from backend.src.modules.publications.domain.sjr_repository import SJRRepository


class SJRFileRepository(SJRRepository):
    """Repositorio de datos SJR con cálculo automático de percentiles y fallback de año."""

    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        # Cache: (nombre_normalizado, año) -> Lista de diccionarios con info detallada
        self._data_cache: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
        self._max_year_available = 0  # Almacenará el año más reciente encontrado en el CSV
        self._load_data()

    def _load_data(self) -> None:
        """Carga datos, calcula percentiles y detecta el año más reciente."""
        try:
            df = pd.read_csv(self._csv_path, sep=';', decimal=',')

            # Normalizar títulos
            df['Title_norm'] = df['Title'].apply(self.normalize_journal_name)

            if 'SJR' in df.columns:
                df['SJR'] = pd.to_numeric(df['SJR'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
            else:
                print("Error Crítico: No se encontró la columna 'SJR'.")
                return

            categories_map = {}
            max_year_found = 0

            # --- PASO 1: Agrupar revistas ---
            for _, row in df.iterrows():
                title_norm = row['Title_norm']
                sjr_score = row['SJR']
                categories_str = str(row['Categories'])
                raw_year = row.get('year', '2023')

                # Detectar año máximo dinámicamente
                try:
                    year_int = int(raw_year)
                    if year_int > max_year_found:
                        max_year_found = year_int
                except ValueError:
                    pass

                year = str(raw_year)

                parsed_cats = self._parse_categories_string(categories_str)

                for cat_data in parsed_cats:
                    cat_name = cat_data['name']
                    quartile = cat_data['quartile']

                    if cat_name not in categories_map:
                        categories_map[cat_name] = []

                    categories_map[cat_name].append({
                        'sjr': sjr_score,
                        'title': title_norm,
                        'quartile': quartile,
                        'year': year
                    })

            self._max_year_available = max_year_found
            print(f"SJR cargado correctamente. Año más reciente detectado: {self._max_year_available}")

            # --- PASO 2: Calcular Percentiles ---
            result_builder = {}

            for cat_name, items in categories_map.items():
                items.sort(key=lambda x: x['sjr'], reverse=True)
                total_journals = len(items)

                for rank, item in enumerate(items, 1):
                    percentile = (rank / total_journals) * 100
                    key = (item['title'], item['year'])

                    if key not in result_builder:
                        result_builder[key] = []

                    result_builder[key].append({
                        'name': cat_name,
                        'quartile': item['quartile'],
                        'percentile': round(percentile, 1),
                        'rank': rank,
                        'total': total_journals
                    })

            self._data_cache = result_builder

        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo SJR en {self._csv_path}")
            self._data_cache = {}
        except Exception as e:
            print(f"Error procesando SJR: {e}")
            self._data_cache = {}

    def get_journal_categories(self, journal_name: str, year: str) -> Any:
        """
        Devuelve la lista estructurada de categorías.
        Si el año solicitado es mayor al disponible, usa el último año disponible.
        """
        if not self._data_cache:
            return "No disponible"

        normalized_journal = self.normalize_journal_name(journal_name)
        target_year = str(year)

        if self._max_year_available > 0:
            try:
                if int(target_year) > self._max_year_available:
                    target_year = str(self._max_year_available)
            except ValueError:
                pass

        return self._data_cache.get((normalized_journal, target_year), "No indexada")

    @staticmethod
    def _parse_categories_string(cat_str: str) -> List[Dict[str, str]]:
        if not isinstance(cat_str, str) or not cat_str:
            return []
        results = []
        parts = cat_str.split(';')
        for part in parts:
            part = part.strip()
            if not part: continue
            quartile = "Q4"
            name = part
            if "(Q1)" in part:
                quartile, name = "Q1", part.replace("(Q1)", "")
            elif "(Q2)" in part:
                quartile, name = "Q2", part.replace("(Q2)", "")
            elif "(Q3)" in part:
                quartile, name = "Q3", part.replace("(Q3)", "")
            elif "(Q4)" in part:
                quartile, name = "Q4", part.replace("(Q4)", "")
            results.append({'name': name.strip(), 'quartile': quartile})
        return results

    def normalize_journal_name(self, name: str) -> str:
        if not isinstance(name, str): name = str(name)
        name = name.lower().strip()
        name = unicodedata.normalize('NFKD', name)
        name = ''.join(c for c in name if not unicodedata.combining(c))
        name = name.replace('&', 'and')
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        name = ' '.join(name.split())
        return name