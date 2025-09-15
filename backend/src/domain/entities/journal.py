from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Journal:
    """
    Entidad que representa una revista académica.
    
    Contiene información básica de la revista y metadatos
    necesarios para el mapeo con SJR.
    """
    
    # Identificadores
    id: Optional[int] = None
    
    # Información básica
    title: str = ""
    issn: Optional[str] = None
    e_issn: Optional[str] = None
    publisher: Optional[str] = None
    
    # Clasificación
    source_type: str = "Journal"  # Journal, Book Series, Conference Proceeding
    
    # Estado
    is_active: bool = True
    
    # Auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones posteriores a la inicialización."""
        self._validate()

    def _validate(self) -> None:
        """Valida los datos de la revista."""
        if not self.title or len(self.title.strip()) < 2:
            raise ValueError("Journal title must be at least 2 characters long")

    @property
    def display_title(self) -> str:
        """Retorna el título para mostrar."""
        return self.title.strip()

    @property
    def has_issn(self) -> bool:
        """Verifica si tiene ISSN."""
        return bool(self.issn or self.e_issn)

    @property
    def primary_issn(self) -> Optional[str]:
        """Retorna el ISSN principal (preferible e-ISSN)."""
        return self.e_issn or self.issn

    def update_info(self, 
                   title: Optional[str] = None,
                   issn: Optional[str] = None,
                   e_issn: Optional[str] = None,
                   publisher: Optional[str] = None) -> None:
        """Actualiza la información de la revista."""
        if title is not None:
            self.title = title
        if issn is not None:
            self.issn = issn
        if e_issn is not None:
            self.e_issn = e_issn
        if publisher is not None:
            self.publisher = publisher
        
        self.updated_at = datetime.now()
        self._validate()

    def deactivate(self) -> None:
        """Desactiva la revista."""
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Activa la revista."""
        self.is_active = True
        self.updated_at = datetime.now()

    def __eq__(self, other) -> bool:
        """Compara revistas por ID o título."""
        if not isinstance(other, Journal):
            return False
        
        if self.id and other.id:
            return self.id == other.id
        
        return self.title.lower().strip() == other.title.lower().strip()

    def __hash__(self) -> int:
        """Hash basado en ID o título."""
        if self.id:
            return hash(self.id)
        return hash(self.title.lower().strip())

    def __str__(self) -> str:
        """Representación string de la revista."""
        return f"Journal(id={self.id}, title='{self.title}')"