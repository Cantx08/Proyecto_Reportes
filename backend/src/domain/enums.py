"""
Enumeraciones para el dominio.

Define los valores constantes utilizados en todo el sistema.
"""

from enum import Enum


class PublicationType(Enum):
    """Tipos de publicación."""
    ARTICLE = "article"
    BOOK = "book"
    BOOK_CHAPTER = "book_chapter"
    CONFERENCE_PAPER = "conference_paper"
    REVIEW = "review"
    EDITORIAL = "editorial"
    LETTER = "letter"
    NOTE = "note"
    SHORT_SURVEY = "short_survey"
    ERRATUM = "erratum"
    CONFERENCE_REVIEW = "conference_review"
    RETRACTED = "retracted"


class SJRQuartile(Enum):
    """Cuartiles SJR."""
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"
    NOT_RANKED = "not_ranked"


class ReportType(Enum):
    """Tipos de reporte."""
    INDIVIDUAL = "individual"
    DEPARTMENTAL = "departmental"
    INSTITUTIONAL = "institutional"
    ANNUAL = "annual"
    CUSTOM = "custom"


class ReportStatus(Enum):
    """Estados de reporte."""
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"


class PublicationSource(Enum):
    """Fuentes de publicaciones."""
    SCOPUS = "scopus"
    WOS = "wos"
    REGIONAL = "regional"
    MEMORIES = "memories"
    BOOKS = "books"
    MANUAL = "manual"


class AuthorRole(Enum):
    """Roles del autor en una publicación."""
    FIRST_AUTHOR = "first_author"
    CORRESPONDING_AUTHOR = "corresponding_author"
    CO_AUTHOR = "co_author"
    LAST_AUTHOR = "last_author"


class DepartmentType(Enum):
    """Tipos de departamento."""
    ACADEMIC = "academic"
    RESEARCH = "research"
    ADMINISTRATIVE = "administrative"


class SJRCategory(Enum):
    """Categorías principales de SJR."""
    PHYSICAL_SCIENCES = "Physical Sciences"
    HEALTH_SCIENCES = "Health Sciences"
    LIFE_SCIENCES = "Life Sciences"
    SOCIAL_SCIENCES = "Social Sciences and Humanities"


class Gender(Enum):
    """Género."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ChartType(Enum):
    """Tipos de gráficos."""
    BAR = "bar"
    PIE = "pie"
    LINE = "line"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"


class NotificationType(Enum):
    """Tipos de notificación."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class ImportStatus(Enum):
    """Estados de importación."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExportFormat(Enum):
    """Formatos de exportación."""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    XML = "xml"


class ValidationLevel(Enum):
    """Niveles de validación."""
    STRICT = "strict"
    MODERATE = "moderate"
    LENIENT = "lenient"


class SyncFrequency(Enum):
    """Frecuencia de sincronización."""
    MANUAL = "manual"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class AccessLevel(Enum):
    """Niveles de acceso."""
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"
    PRIVATE = "private"


class LanguageCode(Enum):
    """Códigos de idioma."""
    ES = "es"  # Español
    EN = "en"  # Inglés
    PT = "pt"  # Portugués
    FR = "fr"  # Francés
    DE = "de"  # Alemán
    IT = "it"  # Italiano


class Priority(Enum):
    """Niveles de prioridad."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(Enum):
    """Estados de tareas."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class LogLevel(Enum):
    """Niveles de log."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class FileType(Enum):
    """Tipos de archivo."""
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    XML = "xml"
    PDF = "pdf"
    IMAGE = "image"
    TEXT = "text"


class OperationType(Enum):
    """Tipos de operación."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    IMPORT = "import"
    EXPORT = "export"
    SYNC = "sync"
    GENERATE = "generate"