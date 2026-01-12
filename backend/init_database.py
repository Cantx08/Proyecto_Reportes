"""
Script para inicializar la base de datos PostgreSQL.
Crea los tipos enum y todas las tablas necesarias.
"""

from sqlalchemy import text
from src.infrastructure.database.connection import DatabaseConfig
from src.infrastructure.database.models.base import Base

# Importar todos los modelos para que SQLAlchemy los registre
from src.infrastructure.database.models.author import (
    AuthorModel, ScopusAccountModel,
    SubjectAreaModel, SubjectCategoryModel
)
from backend.src.infrastructure.database.models import DepartmentModel
from src.infrastructure.database.models.position import PositionModel
from src.infrastructure.database.models.publication import PublicationModel
from src.infrastructure.database.models.journal import (
    JournalModel, CategoryModel, SJRRankingModel, SJRCategoryModel
)
from src.infrastructure.database.models.report import ReportModel


def create_enums():
    """Crea los tipos enum en PostgreSQL."""
    db_config = DatabaseConfig()
    
    # Lista de enums a crear
    enums = [
        ('GenderEnum', "CREATE TYPE genderenum AS ENUM ('M', 'F', 'O');", 'GenderEnum'),
        ('DocumentTypeEnum', "CREATE TYPE documenttypeenum AS ENUM ('ar', 'cp', 'ch', 're', 'bk', 'er', 'no', 'sh', 'le', 'ed');", 'DocumentTypeEnum'),
        ('SourceTypeEnum', "CREATE TYPE sourcetypeenum AS ENUM ('j', 'b', 'k', 'c', 'p', 'd', 'n', 'r', 't');", 'SourceTypeEnum'),
        ('ReportTypeEnum', "CREATE TYPE reporttypeenum AS ENUM ('DRAFT', 'FINAL', 'MEMO');", 'ReportTypeEnum'),
        ('ReportStatusEnum', "CREATE TYPE reportstatusenum AS ENUM ('GENERATING', 'COMPLETED', 'ERROR');", 'ReportStatusEnum'),
    ]
    
    for enum_name, sql, display_name in enums:
        try:
            with db_config.engine.begin() as conn:
                conn.execute(text(sql))
            print(f"✓ {display_name} creado exitosamente")
        except Exception as e:
            if "already exists" in str(e) or "ya existe" in str(e):
                print(f"ℹ {display_name} ya existe")
            else:
                print(f"✗ Error al crear {display_name}: {e}")
                raise


def create_tables():
    """Crea todas las tablas en la base de datos."""
    db_config = DatabaseConfig()
    
    try:
        print("\n📊 Creando tablas...")
        Base.metadata.create_all(db_config.engine)
        print("✓ Todas las tablas creadas exitosamente")
        
        # Mostrar tablas creadas
        print("\n📋 Tablas en la base de datos:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
    except Exception as e:
        print(f"✗ Error al crear tablas: {e}")
        raise


def main():
    """Función principal."""
    print("=" * 60)
    print("INICIALIZACIÓN DE BASE DE DATOS")
    print("=" * 60)
    
    print("\n🔧 Paso 1: Creando tipos enum...")
    create_enums()
    
    print("\n🔧 Paso 2: Creando tablas...")
    create_tables()
    
    print("\n" + "=" * 60)
    print("✓ INICIALIZACIÓN COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    main()
