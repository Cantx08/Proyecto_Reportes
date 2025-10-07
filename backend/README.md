# 🎓 Sistema de Publicaciones Académicas

> **API REST para consultar y analizar publicaciones académicas de Scopus con arquitectura limpia y principios SOLID**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a693?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat&logo=python&logoColor=white)](https://python.org)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-blue?style=flat)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![SOLID](https://img.shields.io/badge/Principles-SOLID-green?style=flat)](https://en.wikipedia.org/wiki/SOLID)

## 📋 Tabla de Contenidos

- [🎯 Descripción](#descripción)
- [✨ Características](#características)
- [🏗️ Arquitectura](#arquitectura)
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

Este sistema permite consultar y analizar publicaciones académicas de la base de datos **Scopus** de manera eficiente y escalable. Desarrollado con **Clean Architecture** y principios **SOLID**, proporciona endpoints REST para:

- 📄 Obtener publicaciones de autores
- 📊 Generar estadísticas por año
- 🏷️ Extraer áreas temáticas (subject areas)
- 📈 Analizar tendencias de investigación

---

## ✨ Características

### Funcionalidades Principales

- **Consulta de Publicaciones**: Obtiene publicaciones completas de uno o múltiples autores
- **Análisis Temporal**: Estadísticas de publicaciones por año con rangos completos
- **Categorización Temática**: Extracción de subject areas de publicaciones
- **Enriquecimiento de Datos**: Integración con datos SJR para categorías de revistas
- **Manejo de Múltiples IDs**: Soporte para autores con múltiples identificadores Scopus

### Arquitectura y Calidad

- **Clean Architecture**: Separación clara de responsabilidades por capas
- **Principios SOLID**: Código mantenible y extensible
- **Inyección de Dependencias**: Desacoplamiento y testabilidad
- **Documentación Automática**: Swagger UI integrado
- **Manejo de Errores**: Gestión robusta de excepciones
- **Código Autodocumentado**: Nombres descriptivos y funciones enfocadas

---

## 🏗️ Arquitectura

La aplicación sigue los principios de **Clean Architecture** con las siguientes capas:

```
backend/src/
├── domain/              # Capa de Dominio (Entidades y Reglas de Negocio)
│   ├── entities.py      # Entidades del dominio
│   ├── value_objects.py # Value Objects inmutables
│   ├── interfaces.py    # Contratos/Interfaces
│   └── repositories.py  # Interfaces de repositorios
├── application/         # Capa de Aplicación (Casos de Uso)
│   ├── services.py      # Servicios de aplicación existentes
│   └── report_application_service.py # Nuevo servicio de reportes
├── infrastructure/     # Capa de Infraestructura (Implementaciones)
│   ├── chart_generator.py       # Generador de gráficos (matplotlib)
│   ├── style_manager.py         # Manejador de estilos (ReportLab)
│   ├── publication_formatter.py # Formateador de publicaciones
│   ├── content_builder.py       # Constructor de contenido
│   ├── pdf_generator.py         # Generador principal de PDF
│   └── ... (otros repositorios)
└── presentation/       # Capa de Presentación (Controladores/API)
    ├── controllers.py
    ├── report_controller.py # Controlador refactorizado
    └── dtos.py
```

---

## 🎯 Principios Aplicados

### Clean Code

- **Nombres descriptivos**: Métodos y clases con nombres que expresan su intención (`obtener_subject_areas` vs `get_data`)
- **Funciones pequeñas**: Cada método hace una sola cosa
- **Comentarios mínimos**: El código se autodocumenta
- **Manejo consistente de errores**: Validaciones explícitas y excepciones específicas

### SOLID Principles

1. **Single Responsibility Principle (SRP)**: Cada clase tiene una única responsabilidad bien definida
2. **Open/Closed Principle (OCP)**: Las interfaces permiten extensión sin modificación
3. **Liskov Substitution Principle (LSP)**: Las implementaciones son intercambiables a través de sus interfaces
4. **Interface Segregation Principle (ISP)**: Interfaces específicas y cohesivas
5. **Dependency Inversion Principle (DIP)**: Dependencias hacia abstracciones, no hacia concreciones

### Clean Architecture

- **Independencia de frameworks**: Lógica de negocio sin dependencias externas
- **Testabilidad**: Cada capa puede testearse independientemente
- **Flexibilidad**: Cambio de implementaciones sin afectar el negocio

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
- **`data/areas_categories.csv`**: Mapeo de áreas y subáreas temáticas

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
    """Interfaz principal para generación de reportes."""
    
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

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👥 Autores

- **Cantx08** - *Desarrollo inicial* - [GitHub](https://github.com/Cantx08)

---

## 🙏 Agradecimientos

- **Elsevier/Scopus** - Por proporcionar la API de datos académicos
- **SCImago Journal Rank** - Por los datos de clasificación de revistas
- **FastAPI Community** - Por el excelente framework web

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
