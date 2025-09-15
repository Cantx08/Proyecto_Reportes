# 🎓 Sistema de Reportes de Publicaciones Académicas - Backend

> **API REST completa para gestión y análisis de publicaciones académicas de Scopus con Clean Architecture, principios SOLID y enfoque corporativo**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a693?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat&logo=python&logoColor=white)](https://python.org)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-blue?style=flat)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![SOLID](https://img.shields.io/badge/Principles-SOLID-green?style=flat)](https://en.wikipedia.org/wiki/SOLID)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-316192?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)

## 📋 Tabla de Contenidos

- [🎯 Descripción](#descripción)
- [✨ Características](#características)
- [🏗️ Arquitectura](#arquitectura)
- [🗄️ Modelo de Base de Datos](#modelo-de-base-de-datos)
- [🎯 Principios Aplicados](#principios-aplicados)
- [🚀 Instalación](#instalación)
- [📚 Uso de la API](#uso-de-la-api)
- [🔧 Configuración](#configuración)
- [🧪 Testing](#testing)
- [📖 Documentación](#documentación)
- [🤝 Contribución](#contribución)
- [📄 Licencia](#licencia)
- [👥 Autores](#autores)
- [🙏 Agradecimientos](#agradecimientos)
- [📈 Beneficios de la Arquitectura](#beneficios-de-la-arquitectura)
- [📝 Notas Técnicas](#notas-técnicas)

---

## 🎯 Descripción

Sistema integral para la gestión y análisis de publicaciones académicas que permite consultar la base de datos **Scopus**, gestionar autores, sincronizar publicaciones y generar reportes académicos automatizados. Desarrollado con **Clean Architecture** y principios **SOLID** para garantizar escalabilidad, mantenibilidad y extensibilidad.

### Funcionalidades Principales

- 👤 **Gestión de Autores**: CRUD completo con soporte para múltiples IDs de Scopus
- 📄 **Gestión de Publicaciones**: Sincronización automática con Scopus y edición manual
- � **Búsqueda Avanzada**: Por ID de Scopus o nombre en base de datos local
- 📊 **Análisis Estadístico**: Tendencias por año, áreas temáticas y cuartiles SJR
- 📋 **Generación de Reportes**: Borradores y reportes finales en PDF
- � **Sincronización Inteligente**: Actualización incremental desde Scopus
- 🏷️ **Categorización Automática**: Mapeo con datos SJR y áreas temáticas

---

## ✨ Características

### Arquitectura y Calidad de Código

- **Clean Architecture**: Separación clara de responsabilidades en 4 capas
- **Principios SOLID**: Código mantenible, extensible y testeable
- **Inyección de Dependencias**: Desacoplamiento total entre capas
- **Domain-Driven Design**: Modelado rico del dominio académico
- **Repository Pattern**: Abstracción completa del acceso a datos
- **Use Cases**: Lógica de negocio encapsulada y reutilizable

### Funcionalidades Técnicas

- **API REST Completa**: Endpoints para todas las operaciones CRUD
- **Documentación Automática**: Swagger UI y ReDoc integrados
- **Validación Robusta**: Schemas Pydantic para entrada y salida
- **Manejo de Errores**: Gestión centralizada de excepciones
- **Logging Estructurado**: Trazabilidad completa de operaciones
- **Caching Inteligente**: Optimización de consultas frecuentes

---

## 🏗️ Arquitectura

### Estructura del Proyecto

La aplicación sigue los principios de **Clean Architecture** con las siguientes capas:

```
backend/
├── src/
│   ├── domain/                     # 🏛️ Capa de Dominio (Entities, Value Objects, Business Rules)
│   │   ├── entities/               # Entidades del dominio
│   │   │   ├── author.py          # Entidad Autor
│   │   │   ├── publication.py     # Entidad Publicación
│   │   │   ├── journal.py         # Entidad Revista
│   │   │   ├── report.py          # Entidad Reporte
│   │   │   ├── department.py      # Entidad Departamento
│   │   │   ├── scopus_account.py  # Entidad Cuenta Scopus
│   │   │   └── subject_area.py    # Entidad Área Temática
│   │   ├── value_objects/          # Value Objects inmutables
│   │   │   ├── scopus_id.py       # ID de Scopus
│   │   │   ├── doi.py             # DOI
│   │   │   ├── email.py           # Email
│   │   │   ├── publication_year.py # Año de publicación
│   │   │   └── quartile.py        # Cuartil SJR
│   │   ├── repositories/           # Interfaces de repositorios
│   │   │   ├── author_repository.py
│   │   │   ├── publication_repository.py
│   │   │   ├── journal_repository.py
│   │   │   ├── sjr_repository.py
│   │   │   └── report_repository.py
│   │   ├── services/               # Servicios del dominio
│   │   ├── exceptions/             # Excepciones del dominio
│   │   │   ├── author_exceptions.py
│   │   │   └── publication_exceptions.py
│   │   ├── enums.py                # Enumeraciones del dominio
│   │   └── interfaces/             # Interfaces de servicios externos
│   │       └── external_services.py
│   │
│   ├── application/                # 🚀 Capa de Aplicación (Use Cases, DTOs)
│   │   ├── use_cases/             # Casos de uso por entidad
│   │   │   ├── author/
│   │   │   │   ├── create_author.py
│   │   │   │   ├── search_authors.py
│   │   │   │   └── sync_scopus_data.py
│   │   │   ├── publication/
│   │   │   │   ├── search_scopus_publications.py
│   │   │   │   ├── sync_publications.py
│   │   │   │   └── edit_publication_data.py
│   │   │   └── report/
│   │   │       └── generate_report.py
│   │   ├── dtos/                  # Data Transfer Objects
│   │   ├── interfaces/            # Interfaces de servicios externos
│   │   │   └── external_services.py
│   │   └── main_application_service.py
│   │
│   ├── infrastructure/            # 🔧 Capa de Infraestructura (External APIs, Database, Files)
│   │   ├── database/              # Configuración de base de datos
│   │   │   ├── connection.py
│   │   │   └── models/            # Modelos SQLAlchemy (14 tablas)
│   │   ├── repositories/          # Implementaciones de repositorios
│   │   │   ├── author_repository_impl.py
│   │   │   ├── publication_repository_impl.py
│   │   │   └── report_repository_impl.py
│   │   ├── external_services/     # Servicios externos
│   │   │   ├── scopus_api_service.py
│   │   │   ├── pdf_generator_service.py
│   │   │   └── chart_generator_service.py
│   │   └── csv_loaders/           # Cargadores de datos CSV
│   │       ├── sjr_loader.py
│   │       └── areas_loader.py
│   │
│   └── presentation/              # 🌐 Capa de Presentación (Controllers, Routes, DTOs)
│       ├── api/                   # API REST
│       │   └── v1/                # Versión 1 de la API
│       │       ├── authors.py     # Endpoints de autores
│       │       ├── publications.py # Endpoints de publicaciones
│       │       ├── reports.py     # Endpoints de reportes
│       │       └── health.py      # Health check
│       ├── schemas/               # Schemas de validación (Pydantic)
│       │   ├── author_schemas.py
│       │   ├── publication_schemas.py
│       │   └── report_schemas.py
│       └── dependencies/          # Dependency injection
├── config/
│   ├── database.py               # Configuración de BD
│   ├── scopus.py                # Configuración de Scopus API
│   └── settings.py              # Configuración general
├── tests/                       # Tests por capas
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

### Flujo de Dependencias

```
Presentation → Application → Domain
     ↓              ↓
Infrastructure → Domain
```

- **Presentation** llama a **Application**
- **Application** orquesta **Domain** y define casos de uso
- **Infrastructure** implementa interfaces del **Domain**
- **Domain** no depende de nada (núcleo de la arquitectura)

---

## 🗄️ Modelo de Base de Datos

### Diseño Relacional

El sistema utiliza un modelo relacional normalizado con **14 tablas principales** que cubren todos los aspectos de la gestión académica:

#### Entidades Principales

1. **DEPARTMENTS** - Departamentos y facultades
2. **AUTHORS** - Autores/Docentes con información completa
3. **SCOPUS_ACCOUNTS** - Múltiples cuentas Scopus por autor
4. **SUBJECT_AREAS** - Áreas temáticas principales (ASJC)
5. **SUBJECT_SUBAREAS** - Subáreas temáticas específicas
6. **JOURNALS** - Revistas científicas
7. **SJR_RANKINGS** - Rankings SJR históricos por año
8. **CATEGORIES** - Categorías de clasificación SJR
9. **SJR_CATEGORIES** - Relación categorías-rankings con cuartiles
10. **PUBLICATIONS** - Publicaciones con metadatos completos
11. **PUBLICATION_AUTHORS** - Relación muchos a muchos autores-publicaciones
12. **PUBLICATION_SUBJECT_AREAS** - Áreas temáticas por publicación
13. **REPORTS** - Reportes generados
14. **REPORT_PUBLICATIONS** - Publicaciones incluidas en reportes

#### Características del Diseño

- **✅ Normalización Completa**: Evita redundancia de datos
- **✅ Soporte Multi-Scopus**: Múltiples IDs por autor
- **✅ Histórico SJR**: Datos temporales de rankings
- **✅ Flexibilidad de Fuentes**: Scopus, WOS, regionales
- **✅ Auditoría Completa**: Timestamps en todas las tablas
- **✅ Integridad Referencial**: Claves foráneas y constraints
- **✅ Escalabilidad**: Índices optimizados para consultas

#### Casos de Uso Cubiertos

- 🔍 Búsqueda por ID Scopus o nombre
- 👤 Gestión completa de autores y afiliaciones
- 📄 Sincronización incremental de publicaciones
- 🏷️ Categorización automática por áreas temáticas
- 📊 Análisis temporal y estadístico
- 📋 Generación de reportes personalizados
- ✏️ Edición manual de datos para reportes
- 🔄 Actualización desde múltiples fuentes

---

## 🎯 Principios Aplicados

### Clean Architecture

1. **Independencia de Frameworks**: El dominio no depende de FastAPI, SQLAlchemy o cualquier framework
2. **Independencia de UI**: La lógica de negocio está separada de la presentación
3. **Independencia de Base de Datos**: Los repositorios abstraen el acceso a datos
4. **Independencia de Agencias Externas**: Scopus API y servicios están abstraídos
5. **Testeable**: Cada capa se puede testear independientemente

### SOLID Principles

1. **Single Responsibility (SRP)**: Cada clase tiene una única responsabilidad
2. **Open/Closed (OCP)**: Abierto para extensión, cerrado para modificación
3. **Liskov Substitution (LSP)**: Las implementaciones son intercambiables
4. **Interface Segregation (ISP)**: Interfaces específicas y cohesivas
5. **Dependency Inversion (DIP)**: Dependencias hacia abstracciones

### Clean Code

- **Nombres Descriptivos**: Métodos y clases expresan su intención
- **Funciones Pequeñas**: Cada método hace una sola cosa
- **Comentarios Mínimos**: El código se autodocumenta
- **Manejo Consistente de Errores**: Validaciones explícitas y excepciones específicas

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.9 o superior
- Clave API de Scopus ([Obtener aquí](https://dev.elsevier.com))
- Archivo CSV de datos SJR

### Instalación

1. **Clonar el repositorio**
    ```bash
    git clone https://github.com/Cantx08/Proyecto_Reportes.git
    cd Proyecto_Reportes/backend
    ```

2. **Crear entorno virtual**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3. **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar variables de entorno**
    ```bash
    # Crear archivo .env
    echo "SCOPUS_API_KEY=tu_clave_api_scopus" > .env
    echo "SJR_CSV_PATH=data/tu_archivo.csv" >> .env
    ```

5. **Iniciar la aplicación**
    ```bash
    uvicorn main:app --reload
    ```

La API estará disponible en: `http://localhost:8000`

---

## 📚 Uso de la API

### Endpoints Disponibles

#### 📄 Obtener Publicaciones
```http
GET /scopus/publications?ids=00000000000&ids=12345678901
```
**Respuesta:**
```json
{
  "publicaciones": [
    {
      "id_autor": "00000000000,12345678901",
      "lista_publicaciones": [
        {
          "titulo": "Título de la publicación",
          "anio": "2025",
          "fuente": "Revista",
          "tipo_documento": "Articulo/Conferencia",
          "filiacion": "Institución",
          "doi": "10.1000/xyz123",
          "categorias": "Categoría 1 (Q1); Categoría 2 (Q2)"
        }
      ]
    }
  ]
}
```

#### 📊 Estadísticas por Año
```http
GET /scopus/docs_by_year?ids=00000000000
```
**Respuesta:**
```json
{
  "author_ids": ["00000000000"],
  "documentos_por_anio": {
    "2020": 3,
    "2021": 5,
    "2022": 2,
    "2023": 4,
    "2024": 1
  }
}
```

#### 🏷️ Áreas Temáticas
```http
GET /scopus/subject_areas?ids=00000000000
```
**Respuesta:**
```json
{
  "author_ids": ["00000000000"],
  "subject_areas": [
    "Area 1",
    "Area 2",
    "Area 3",
    "Area 4"
  ]
}
```

#### 🩺 Verificar Salud
```http
GET /health
```
**Respuesta:**
```json
{
  "status": "healthy",
  "message": "API funcionando correctamente"
}
```

### Documentación Interactiva

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🔧 Configuración

### Variables de Entorno

| Variable         | Descripción                | Ejemplo                |
|------------------|---------------------------|------------------------|
| `SCOPUS_API_KEY` | Clave API de Scopus       | `abc123def456...`      |
| `SJR_CSV_PATH`   | Ruta al archivo CSV SJR   | `data/archivo.csv`     |

### Archivos de Datos

- **`data/archivo.csv`**: Datos SJR para categorización de revistas
- **`data/areas_subareas.csv`**: Mapeo de áreas y subáreas temáticas

---

## 🏗️ Componentes Principales

### Value Objects
```python
@dataclass(frozen=True)
class DocenteInfo:
    """Value Object inmutable para información del docente."""
    nombre: str
    genero: Genero
    departamento: str
    cargo: str
```

### Interfaces
```python
class IReportGenerator(ABC):
    """Interface principal para generación de reportes."""
    
    @abstractmethod
    def generar_reporte(self, docente: DocenteInfo, ...) -> bytes:
        pass
```

### Servicios de Aplicación
```python
class ReportApplicationService:
    """Servicio de aplicación que orquesta la generación de reportes."""
    
    def generar_reporte_certificacion(self, ...):
        # Validaciones
        # Transformaciones
        # Orquestación
```

---

## 🧪 Testing

### Ventajas de la Arquitectura para Testing

```python
# Ejemplo de test unitario
class MockScopusRepository(PublicacionesRepository):
    async def obtener_publicaciones_por_autor(self, author_id):
        return [PublicacionMock()]

# Test del servicio
def test_obtener_publicaciones():
    mock_repo = MockScopusRepository()
    service = PublicacionesService(mock_repo, mock_sjr_repo)
    result = await service.obtener_publicaciones_agrupadas(["123"])
    assert len(result.autores) == 1
```

### Ejecutar Tests
```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio

# Ejecutar tests
pytest tests/
```

---

## 📖 Documentación

### Casos de Uso Principales

1. **Investigador Individual**: Consultar publicaciones y tendencias de un autor
2. **Análisis Colaborativo**: Combinar publicaciones de múltiples coautores  
3. **Estudio Institucional**: Analizar producción académica de una institución
4. **Análisis Temático**: Identificar áreas de investigación predominantes

### Ejemplos de Uso

#### Consulta Simple
```bash
curl "http://localhost:8000/scopus/publications?ids=00000000000"
```

#### Múltiples Autores
```bash
curl "http://localhost:8000/scopus/subject_areas?ids=00000000000&ids=12345678901"
```

#### Análisis Temporal
```bash
curl "http://localhost:8000/scopus/docs_by_year?ids=00000000000"
```

---

## 🤝 Contribución

### Guía para Contribuir

1. **Fork** el repositorio
2. **Crear** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Seguir** los principios de Clean Code y SOLID
4. **Escribir** tests para tu código
5. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
6. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
7. **Crear** un Pull Request

### Estándares de Código

- Seguir principios SOLID
- Aplicar Clean Code
- Documentar funciones complejas
- Escribir tests unitarios
- Mantener cobertura de tests > 80%

### Reportar Bugs

Usa el [sistema de issues](https://github.com/Cantx08/Proyecto_Reportes/issues) incluyendo:

- Descripción detallada del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Información del entorno (OS, Python version, etc.)

---

## 👥 Autores

- **Andrés Cantuña** - *Desarrollo inicial* - [GitHub](https://github.com/Cantx08)

---

<div align="center">

**¿Te gustó el proyecto?** ⭐ ¡Dale una estrella en GitHub!

[📚 Documentación](http://localhost:8000/docs) • [🐛 Reportar Bug](https://github.com/Cantx08/Proyecto_Reportes/issues) • [💡 Solicitar Feature](https://github.com/Cantx08/Proyecto_Reportes/issues)

</div>

---

## 📈 Beneficios de la Arquitectura

1. **Mantenibilidad**: Código fácil de modificar y extender
2. **Testabilidad**: Componentes aislados y mockeables
3. **Reutilización**: Componentes intercambiables
4. **Separación de Responsabilidades**: Cada capa tiene su propósito
5. **Independencia de Frameworks**: La lógica de negocio no depende de tecnologías específicas

---

## 📝 Notas Técnicas

- **Inmutabilidad**: Los Value Objects son inmutables (frozen dataclasses)
- **Validación**: Validaciones en la capa de aplicación
- **Error Handling**: Excepciones específicas (`ValueError` para datos inválidos)
- **Inyección de Dependencias**: Configuración manual en el servicio de aplicación
