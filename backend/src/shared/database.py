import os
from pathlib import Path
from typing import Generator
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Cargar variables de entorno
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
load_dotenv()  # Carga backup por si acaso

# 1. Definir la Base Declarativa aquí para que sea compartida por TODOS los modelos
Base = declarative_base()


class DatabaseConfig:
    """
    Configuración de la conexión a base de datos.
    Responsabilidad única: Gestionar el Engine y la SessionFactory.
    """

    def __init__(self):
        self.database_url = self._build_database_url()

        # Configuración del Engine
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,  # Verifica si la conexión está viva antes de usarla
            pool_recycle=300,  # Recicla conexiones cada 5 min para evitar timeouts
            pool_size=10,  # Tamaño base del pool
            max_overflow=20,  # Conexiones extra si el pool se llena
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    @staticmethod
    def _build_database_url() -> str:
        """Construye y valida la URL de conexión."""
        db_user = os.getenv("DB_USER", "postgres")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "reportes_publicaciones_epn")
        db_password = os.getenv("DB_PASSWORD")

        if not db_password:
            raise ValueError(
                "❌ ERROR CRÍTICO: 'DB_PASSWORD' no definida en variables de entorno."
            )

        # Manejo seguro de caracteres especiales en la contraseña
        db_password_escaped = quote_plus(db_password) if '%' not in db_password else db_password

        return f'postgresql://{db_user}:{db_password_escaped}@{db_host}:{db_port}/{db_name}'

    def get_session_local(self) -> Session:
        """Crea una nueva sesión."""
        return self.SessionLocal()


# Instancia global
db_config = DatabaseConfig()


# ============================================================================
# Inyección de dependencias
# ============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para inyectar la sesión de BD en los enrutadores.
    Maneja automáticamente el cierre de la sesión (yield/finally).
    """
    session = db_config.get_session_local()
    try:
        yield session
    finally:
        session.close()