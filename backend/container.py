from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv

# Importamos componentes compartidos
from shared.database import db_config
# from src.shared.scopus_client import ScopusApiClient

load_dotenv()


class Settings:
    """Configuración centralizada de la aplicación."""
    PROJECT_NAME: str = "Sistema de Publicaciones Académicas (EPN)"
    VERSION: str = "2.1.0"
    API_PREFIX: str = ""

    # Base de Datos
    DB_ECHO: bool = os.getenv("SQL_ECHO", "False").lower() == "true"

    # Scopus & External APIs
    SCOPUS_API_KEY: str = os.getenv("SCOPUS_API_KEY", "")

    # Rutas de Archivos (Data estática)
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    SJR_CSV_PATH: str = os.getenv("SJR_CSV_PATH", str(DATA_DIR / "df_sjr_24_04_2025.csv"))
    AREAS_CSV_PATH: str = os.getenv("AREAS_CSV_PATH", str(DATA_DIR / "areas_categories.csv"))


class Container:
    """
    Contenedor de dependencias Globales.
    Aquí viven las instancias que se comparten entre TODOS los módulos.
    """

    def __init__(self):
        self.settings = Settings()
        self.db_handler = db_config

        # Inicializar Cliente Scopus
        # self.scopus_client = ScopusApiClient(self.settings.SCOPUS_API_KEY)

        # Aquí podrías inicializar Redis, Logging centralizado, etc.


@lru_cache()
def get_container() -> Container:
    """Proveedor del contenedor para inyección de dependencias."""
    return Container()