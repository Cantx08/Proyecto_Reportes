"""
Script para eliminar todas las tablas y tipos de la base de datos.
"""

from sqlalchemy import text
from src.infrastructure.database.connection import DatabaseConfig


def drop_all_tables():
    """Elimina todas las tablas de la base de datos."""
    db_config = DatabaseConfig()
    
    print("=" * 60)
    print("ELIMINANDO TODAS LAS TABLAS")
    print("=" * 60)
    
    # Obtener todas las tablas
    with db_config.engine.begin() as conn:
        result = conn.execute(text("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        tables = [row[0] for row in result]
        
        if not tables:
            print("\n✓ No hay tablas para eliminar")
            return
        
        print(f"\n📋 Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table}")
        
        # Eliminar todas las tablas con CASCADE
        print("\n🗑️  Eliminando tablas...")
        for table in tables:
            try:
                conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                print(f"  ✓ {table} eliminada")
            except Exception as e:
                print(f"  ✗ Error al eliminar {table}: {e}")
    
    print("\n" + "=" * 60)
    print("✓ TABLAS ELIMINADAS")
    print("=" * 60)


def drop_all_types():
    """Elimina todos los tipos enum de la base de datos."""
    db_config = DatabaseConfig()
    
    print("\n" + "=" * 60)
    print("ELIMINANDO TIPOS ENUM")
    print("=" * 60)
    
    enum_types = [
        'genderenum',
        'documenttypeenum',
        'sourcetypeenum',
        'reporttypeenum',
        'reportstatusenum'
    ]
    
    with db_config.engine.begin() as conn:
        for enum_type in enum_types:
            try:
                conn.execute(text(f'DROP TYPE IF EXISTS {enum_type} CASCADE'))
                print(f"  ✓ {enum_type} eliminado")
            except Exception as e:
                print(f"  ✗ Error al eliminar {enum_type}: {e}")
    
    print("\n" + "=" * 60)
    print("✓ TIPOS ENUM ELIMINADOS")
    print("=" * 60)


def main():
    """Función principal."""
    print("\n⚠️  ADVERTENCIA: Esta operación eliminará TODAS las tablas y tipos")
    print("⚠️  Se perderán TODOS los datos existentes\n")
    
    response = input("¿Estás seguro que deseas continuar? (escribe 'SI' para confirmar): ")
    
    if response != 'SI':
        print("\n❌ Operación cancelada")
        return
    
    drop_all_tables()
    drop_all_types()
    
    print("\n✓ Base de datos limpiada completamente")
    print("Ahora puedes ejecutar: python init_database.py")


if __name__ == "__main__":
    main()
