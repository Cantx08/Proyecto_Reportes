# Arquitectura Limpia - Sistema de Reportes de Publicaciones

## Estructura Propuesta

```
backend/
├── src/
│   ├── domain/                     # Capa de Dominio (Entities, Value Objects, Business Rules)
│   │   ├── __init__.py
│   │   ├── entities/               # Entidades del dominio
│   │   │   ├── __init__.py
│   │   │   ├── author.py          # Entidad Autor
│   │   │   ├── publication.py     # Entidad Publicación
│   │   │   ├── journal.py         # Entidad Revista
│   │   │   ├── report.py          # Entidad Reporte
│   │   │   ├── category.py        # Entidad Categoría
│   │   │   └── department.py      # Entidad Departamento
│   │   ├── value_objects/          # Value Objects
│   │   │   ├── __init__.py
│   │   │   ├── scopus_id.py       # ID de Scopus
│   │   │   ├── doi.py             # DOI
│   │   │   ├── publication_year.py # Año de publicación
│   │   │   ├── email.py           # Email
│   │   │   └── quartile.py        # Cuartil SJR
│   │   ├── repositories/           # Interfaces de repositorios
│   │   │   ├── __init__.py
│   │   │   ├── author_repository.py
│   │   │   ├── publication_repository.py
│   │   │   ├── journal_repository.py
│   │   │   ├── sjr_repository.py
│   │   │   └── report_repository.py
│   │   ├── services/               # Servicios del dominio
│   │   │   ├── __init__.py
│   │   │   ├── publication_domain_service.py
│   │   │   ├── author_domain_service.py
│   │   │   └── report_domain_service.py
│   │   └── exceptions/             # Excepciones del dominio
│   │       ├── __init__.py
│   │       ├── author_exceptions.py
│   │       ├── publication_exceptions.py
│   │       └── report_exceptions.py
│   │
│   ├── application/                # Capa de Aplicación (Use Cases, DTOs)
│   │   ├── __init__.py
│   │   ├── use_cases/             # Casos de uso
│   │   │   ├── __init__.py
│   │   │   ├── author/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_author.py
│   │   │   │   ├── get_author_publications.py
│   │   │   │   └── sync_scopus_data.py
│   │   │   ├── publication/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── search_scopus_publications.py
│   │   │   │   ├── map_sjr_categories.py
│   │   │   │   ├── edit_publication_data.py
│   │   │   │   └── get_publications_by_year.py
│   │   │   └── report/
│   │   │       ├── __init__.py
│   │   │       ├── generate_report.py
│   │   │       ├── generate_draft_report.py
│   │   │       └── generate_charts.py
│   │   ├── dtos/                  # Data Transfer Objects
│   │   │   ├── __init__.py
│   │   │   ├── author_dto.py
│   │   │   ├── publication_dto.py
│   │   │   ├── report_dto.py
│   │   │   └── chart_dto.py
│   │   └── interfaces/            # Interfaces de servicios externos
│   │       ├── __init__.py
│   │       ├── scopus_service.py
│   │       ├── pdf_service.py
│   │       ├── chart_service.py
│   │       └── email_service.py
│   │
│   ├── infrastructure/            # Capa de Infraestructura (External APIs, Database, Files)
│   │   ├── __init__.py
│   │   ├── database/              # Configuración de base de datos
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   ├── models/            # Modelos SQLAlchemy
│   │   │   │   ├── __init__.py
│   │   │   │   ├── author_model.py
│   │   │   │   ├── publication_model.py
│   │   │   │   ├── journal_model.py
│   │   │   │   └── report_model.py
│   │   │   └── migrations/        # Migraciones Alembic
│   │   │       └── versions/
│   │   ├── repositories/          # Implementaciones de repositorios
│   │   │   ├── __init__.py
│   │   │   ├── sqlalchemy_author_repository.py
│   │   │   ├── sqlalchemy_publication_repository.py
│   │   │   ├── csv_sjr_repository.py
│   │   │   └── file_report_repository.py
│   │   ├── external_services/     # Servicios externos
│   │   │   ├── __init__.py
│   │   │   ├── scopus_api_service.py
│   │   │   ├── pdf_generator_service.py
│   │   │   ├── chart_generator_service.py
│   │   │   └── email_notification_service.py
│   │   └── csv_loaders/           # Cargadores de CSV
│   │       ├── __init__.py
│   │       ├── sjr_loader.py
│   │       ├── areas_loader.py
│   │       └── departments_loader.py
│   │
│   └── presentation/              # Capa de Presentación (Controllers, Routes, DTOs)
│       ├── __init__.py
│       ├── api/                   # API REST
│       │   ├── __init__.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── authors.py     # Endpoints de autores
│       │   │   ├── publications.py # Endpoints de publicaciones
│       │   │   ├── reports.py     # Endpoints de reportes
│       │   │   └── health.py      # Health check
│       │   └── middleware/
│       │       ├── __init__.py
│       │       ├── cors_middleware.py
│       │       ├── auth_middleware.py
│       │       └── error_handler.py
│       ├── schemas/               # Schemas de validación (Pydantic)
│       │   ├── __init__.py
│       │   ├── author_schemas.py
│       │   ├── publication_schemas.py
│       │   └── report_schemas.py
│       └── dependencies/          # Dependency injection
│           ├── __init__.py
│           └── container.py
├── config/
│   ├── __init__.py
│   ├── database.py               # Configuración de BD
│   ├── scopus.py                # Configuración de Scopus API
│   └── settings.py              # Configuración general
├── tests/                       # Tests
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/
│   └── e2e/
├── requirements.txt
├── alembic.ini                  # Configuración de migraciones
├── docker-compose.yml           # Para desarrollo local
├── Dockerfile
└── main.py                      # Punto de entrada
```

## Principios de Clean Architecture Aplicados

### 1. **Independencia de Frameworks**
- El dominio no depende de FastAPI, SQLAlchemy o cualquier framework
- Se puede cambiar de framework sin afectar la lógica de negocio

### 2. **Independencia de UI**
- La lógica de negocio está separada de la presentación
- Se puede cambiar de REST API a GraphQL sin modificar casos de uso

### 3. **Independencia de Base de Datos**
- Los repositorios abstraen el acceso a datos
- Se puede cambiar de PostgreSQL a MongoDB sin afectar el dominio

### 4. **Independencia de Agencias Externas**
- Scopus API, generadores de PDF están abstraídos mediante interfaces
- Fácil testing con mocks

### 5. **Testeable**
- Cada capa se puede testear independientemente
- Dependency injection facilita el testing

## Flujo de Dependencias

```
Presentation → Application → Domain
     ↓              ↓
Infrastructure → Domain
```

- **Presentation** llama a **Application**
- **Application** llama a **Domain**
- **Infrastructure** implementa interfaces del **Domain**
- **Domain** no depende de nada (centro de la arquitectura)

## Beneficios de esta Arquitectura

1. **Mantenibilidad**: Código organizado y fácil de entender
2. **Escalabilidad**: Fácil agregar nuevas funcionalidades
3. **Testabilidad**: Testing fácil con mocks e interfaces
4. **Flexibilidad**: Cambiar implementaciones sin afectar lógica de negocio
5. **Reutilización**: Casos de uso reutilizables en diferentes interfaces