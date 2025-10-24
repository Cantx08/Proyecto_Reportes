import os
from contextlib import contextmanager
from typing import Generator
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models.base import Base


class DatabaseConfig:
    """Configuración de la base de datos."""

    def __init__(self):
        self.database_url = self._build_database_url()
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    @staticmethod
    def _build_database_url() -> str:
        """Construye la URL de conexión a la base de datos."""
        # Variables de entorno para la conexión
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "P@ssw0rd")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "reportes_publicaciones_epn")

        # Si la contraseña ya está escapada (contiene %), no escapar
        # Si contiene caracteres especiales sin escapar, escapar
        if '%' in db_password:
            db_password_escaped = db_password
        else:
            db_password_escaped = quote_plus(db_password)
        
        return f'postgresql://{db_user}:{db_password_escaped}@{db_host}:{db_port}/{db_name}'

    def create_tables(self):
        """Crea todas las tablas en la base de datos."""
        Base.metadata.create_all(bind=self.engine)

    def drop_tables(self):
        """Elimina todas las tablas de la base de datos."""
        Base.metadata.drop_all(bind=self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager para obtener una sesión de base de datos.
        
        Yields:
            Session: Sesión de SQLAlchemy
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_session_sync(self) -> Session:
        """
        Obtiene una sesión síncrona.
        
        Returns:
            Session: Sesión de SQLAlchemy
        """
        return self.SessionLocal()


# Instancia global de configuración
db_config = DatabaseConfig()


def get_database_session() -> Generator[Session, None, None]:
    """
    Dependency para FastAPI que proporciona una sesión de base de datos.
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    with db_config.get_session() as session:
        yield session


def init_database():
    """Inicializa la base de datos creando las tablas."""
    db_config.create_tables()


def reset_database():
    """Resetea la base de datos eliminando y creando las tablas."""
    db_config.drop_tables()
    db_config.create_tables()