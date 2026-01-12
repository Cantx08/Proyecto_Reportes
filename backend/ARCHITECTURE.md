# Arquitectura del Backend - Clean Architecture

## Visión General

Este backend sigue los principios de **Clean Architecture** (también conocida como Onion Architecture o Hexagonal Architecture) propuesta por Robert C. Martin (Uncle Bob).

```
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    APPLICATION                            │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │                    DOMAIN                        │    │    │
│  │  │                                                  │    │    │
│  │  │   Entities, Value Objects, Interfaces           │    │    │
│  │  │                                                  │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │                                                          │    │
│  │   Services (Use Cases)                                   │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│   Controllers, Repositories, External APIs, Database            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Estructura de Carpetas

```
src/
├── domain/                    # Capa de Dominio (Núcleo)
│   ├── entities/             # Entidades de negocio
│   ├── enums/                # Enumeraciones del dominio
│   ├── repositories/         # INTERFACES de repositorios (contratos)
│   ├── value_objects/        # Objetos de valor
│   └── exceptions.py         # Excepciones de dominio
│
├── application/              # Capa de Aplicación
│   ├── dto/                  # Data Transfer Objects
│   └── services/             # Servicios de aplicación (casos de uso)
│
└── infrastructure/           # Capa de Infraestructura
    ├── api/
    │   └── controllers/      # Controladores HTTP (FastAPI)
    ├── database/             # Configuración de base de datos
    ├── external/             # Clientes de APIs externas (Scopus)
    ├── repositories/         # IMPLEMENTACIONES de repositorios
    └── dependencies.py       # Composition Root (DI Container)
```

## Principios Aplicados

### 1. Dependency Rule (Regla de Dependencia)
Las dependencias **solo apuntan hacia adentro**:
- `infrastructure` → `application` → `domain`
- El dominio NO conoce nada de las otras capas

### 2. Inversión de Dependencias (DIP)
Los servicios de aplicación dependen de **abstracciones** (interfaces), no de implementaciones:

```python
# ✅ CORRECTO - Depende de abstracción
class ReportService:
    def __init__(self, report_generator: IReportGenerator):
        self._report_generator = report_generator

# ❌ INCORRECTO - Dependía de implementación
class ReportService:
    def __init__(self):
        self._report_generator = ReportLabReportGenerator()  # Acoplamiento
```

### 3. Single Responsibility (SRP)
Cada clase tiene una única responsabilidad:
- `DepartmentService`: Lógica de negocio de departamentos
- `DBDepartmentRepository`: Acceso a datos de departamentos en PostgreSQL
- `DepartmentsController`: Manejo de peticiones HTTP

### 4. Open/Closed (OCP)
El sistema está abierto a extensión pero cerrado a modificación:
- Para agregar un nuevo tipo de repositorio (ej: MongoDB), solo implementas la interfaz
- No modificas los servicios de aplicación

## Flujo de una Petición

```
HTTP Request
    │
    ▼
┌───────────────────┐
│   Controller      │  ← Infrastructure (maneja HTTP)
│   (FastAPI)       │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   Service         │  ← Application (orquesta lógica)
│   (Use Case)      │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   Repository      │  ← Infrastructure (implementación)
│   (Database/API)  │     Pero el Service ve la Interface (Domain)
└─────────┬─────────┘
          │
          ▼
    Base de Datos
    o API Externa
```

## Composition Root (dependencies.py)

El archivo `dependencies.py` es el **único lugar** donde se crean instancias concretas:

```python
class DependencyContainer:
    def _setup_dependencies(self):
        # 1. Infraestructura base
        self._setup_infrastructure()
        
        # 2. Repositorios (implementan interfaces de Domain)
        self._setup_repositories()
        
        # 3. Servicios de aplicación (reciben abstracciones)
        self._setup_application_services()
        
        # 4. Controladores (reciben servicios)
        self._setup_controllers()
```

## Interfaces en Domain

Las interfaces definen **contratos** que la infraestructura debe cumplir:

```python
# domain/repositories/department_repository.py
class IDepartmentRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Department]:
        """Obtiene todos los departamentos."""
        
    @abstractmethod
    async def create(self, department: Department) -> Department:
        """Crea un nuevo departamento."""
```

## Beneficios de esta Arquitectura

1. **Testeable**: Los servicios pueden probarse con mocks de repositorios
2. **Mantenible**: Cambios en una capa no afectan a otras
3. **Escalable**: Fácil agregar nuevas funcionalidades
4. **Independiente del Framework**: El dominio no conoce FastAPI ni SQLAlchemy
5. **Flexible**: Cambiar de PostgreSQL a MongoDB solo requiere nueva implementación

## Cómo Agregar una Nueva Funcionalidad

### Ejemplo: Agregar entidad "Proyecto"

1. **Domain** - Crear entidad e interfaz:
   ```
   domain/entities/project.py
   domain/repositories/project_repository.py  # Interface
   ```

2. **Application** - Crear servicio y DTOs:
   ```
   application/dto/project_dto.py
   application/services/project_service.py
   ```

3. **Infrastructure** - Crear implementación:
   ```
   infrastructure/repositories/project_db_repository.py
   infrastructure/api/controllers/projects_controller.py
   ```

4. **Registrar en DependencyContainer**:
   ```python
   self._project_repo = ProjectDatabaseRepository(self._db_config)
   self._project_service = ProjectService(self._project_repo)
   self._projects_controller = ProjectsController(self._project_service)
   ```

5. **Agregar rutas en main.py**
