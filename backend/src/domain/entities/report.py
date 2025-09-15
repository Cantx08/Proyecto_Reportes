from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class ReportType(Enum):
    """Tipos de reportes disponibles."""
    DRAFT = "draft"  # Borrador sin encabezados institucionales
    FINAL = "final"  # Reporte final con encabezados institucionales


class ReportStatus(Enum):
    """Estados del reporte."""
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Report:
    """
    Entidad que representa un reporte generado.
    
    Contiene toda la información del reporte incluyendo
    configuración, metadatos y referencias a publicaciones.
    """
    
    # Identificadores
    id: Optional[int] = None
    
    # Información básica
    title: str = ""
    author_id: Optional[int] = None
    report_type: ReportType = ReportType.DRAFT
    
    # Configuración del reporte
    memo_number: Optional[str] = None
    memo_date: Optional[datetime] = None
    signatory: Optional[str] = None  # Persona que firma
    generated_by: Optional[int] = None  # ID del usuario que genera
    
    # Archivos y rutas
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    
    # Metadatos y configuración
    metadata: Dict = field(default_factory=dict)
    publication_ids: List[int] = field(default_factory=list)
    
    # Estado
    status: ReportStatus = ReportStatus.GENERATING
    error_message: Optional[str] = None
    
    # Auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    generated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones posteriores a la inicialización."""
        self._validate()

    def _validate(self) -> None:
        """Valida los datos del reporte."""
        if not self.title or len(self.title.strip()) < 3:
            raise ValueError("Report title must be at least 3 characters long")
        
        if self.author_id is None:
            raise ValueError("Author ID is required")

    @property
    def is_draft(self) -> bool:
        """Verifica si es un reporte borrador."""
        return self.report_type == ReportType.DRAFT

    @property
    def is_final(self) -> bool:
        """Verifica si es un reporte final."""
        return self.report_type == ReportType.FINAL

    @property
    def is_completed(self) -> bool:
        """Verifica si el reporte está completado."""
        return self.status == ReportStatus.COMPLETED

    @property
    def is_generating(self) -> bool:
        """Verifica si el reporte se está generando."""
        return self.status == ReportStatus.GENERATING

    @property
    def has_failed(self) -> bool:
        """Verifica si la generación falló."""
        return self.status == ReportStatus.FAILED

    @property
    def has_file(self) -> bool:
        """Verifica si el reporte tiene archivo asociado."""
        return bool(self.file_path)

    @property
    def publication_count(self) -> int:
        """Retorna el número de publicaciones incluidas."""
        return len(self.publication_ids)

    def set_metadata(self, key: str, value) -> None:
        """Establece un metadato del reporte."""
        self.metadata[key] = value
        self.updated_at = datetime.now()

    def get_metadata(self, key: str, default=None):
        """Obtiene un metadato del reporte."""
        return self.metadata.get(key, default)

    def add_publication(self, publication_id: int) -> None:
        """Agrega una publicación al reporte."""
        if publication_id not in self.publication_ids:
            self.publication_ids.append(publication_id)
            self.updated_at = datetime.now()

    def remove_publication(self, publication_id: int) -> None:
        """Elimina una publicación del reporte."""
        if publication_id in self.publication_ids:
            self.publication_ids.remove(publication_id)
            self.updated_at = datetime.now()

    def clear_publications(self) -> None:
        """Limpia todas las publicaciones del reporte."""
        self.publication_ids.clear()
        self.updated_at = datetime.now()

    def start_generation(self) -> None:
        """Marca el reporte como en proceso de generación."""
        self.status = ReportStatus.GENERATING
        self.error_message = None
        self.updated_at = datetime.now()

    def complete_generation(self, file_path: str, file_name: str) -> None:
        """Marca el reporte como completado."""
        self.status = ReportStatus.COMPLETED
        self.file_path = file_path
        self.file_name = file_name
        self.generated_at = datetime.now()
        self.updated_at = datetime.now()
        self.error_message = None

    def fail_generation(self, error_message: str) -> None:
        """Marca el reporte como fallido."""
        self.status = ReportStatus.FAILED
        self.error_message = error_message
        self.updated_at = datetime.now()

    def update_configuration(self,
                           title: Optional[str] = None,
                           memo_number: Optional[str] = None,
                           memo_date: Optional[datetime] = None,
                           signatory: Optional[str] = None) -> None:
        """Actualiza la configuración del reporte."""
        if title is not None:
            self.title = title
        if memo_number is not None:
            self.memo_number = memo_number
        if memo_date is not None:
            self.memo_date = memo_date
        if signatory is not None:
            self.signatory = signatory
        
        self.updated_at = datetime.now()
        self._validate()

    def convert_to_final(self) -> None:
        """Convierte el reporte a tipo final."""
        if self.is_draft:
            self.report_type = ReportType.FINAL
            self.updated_at = datetime.now()

    def convert_to_draft(self) -> None:
        """Convierte el reporte a tipo borrador."""
        if self.is_final:
            self.report_type = ReportType.DRAFT
            self.updated_at = datetime.now()

    def __eq__(self, other) -> bool:
        """Compara reportes por ID."""
        if not isinstance(other, Report):
            return False
        
        if self.id and other.id:
            return self.id == other.id
        
        return False

    def __hash__(self) -> int:
        """Hash basado en ID."""
        if self.id:
            return hash(self.id)
        return hash(f"{self.title}_{self.author_id}")

    def __str__(self) -> str:
        """Representación string del reporte."""
        return f"Report(id={self.id}, title='{self.title}', status={self.status.value})"