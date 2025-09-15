from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Department:
    """
    Entidad que representa un departamento de la institución.
    
    Contiene información básica del departamento y su facultad.
    """
    
    # Identificadores
    id: Optional[int] = None
    
    # Información básica
    name: str = ""
    faculty: Optional[str] = None
    
    # Auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones posteriores a la inicialización."""
        self._validate()

    def _validate(self) -> None:
        """Valida los datos del departamento."""
        if not self.name or len(self.name.strip()) < 2:
            raise ValueError("Department name must be at least 2 characters long")

    @property
    def display_name(self) -> str:
        """Retorna el nombre para mostrar."""
        return self.name.strip()

    @property
    def full_name(self) -> str:
        """Retorna el nombre completo con facultad si existe."""
        if self.faculty:
            return f"{self.name} - {self.faculty}"
        return self.name

    def update_info(self, 
                   name: Optional[str] = None,
                   faculty: Optional[str] = None) -> None:
        """Actualiza la información del departamento."""
        if name is not None:
            self.name = name
        if faculty is not None:
            self.faculty = faculty
        
        self.updated_at = datetime.now()
        self._validate()

    def __eq__(self, other) -> bool:
        """Compara departamentos por ID o nombre."""
        if not isinstance(other, Department):
            return False
        
        if self.id and other.id:
            return self.id == other.id
        
        return self.name.lower().strip() == other.name.lower().strip()

    def __hash__(self) -> int:
        """Hash basado en ID o nombre."""
        if self.id:
            return hash(self.id)
        return hash(self.name.lower().strip())

    def __str__(self) -> str:
        """Representación string del departamento."""
        return f"Department(id={self.id}, name='{self.name}')"


@dataclass
class Category:
    """
    Entidad que representa una categoría SJR.
    
    Contiene información de las categorías utilizadas en el ranking SJR.
    """
    
    # Identificadores
    id: Optional[int] = None
    
    # Información básica
    name: str = ""
    description: Optional[str] = None
    
    # Auditoría
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones posteriores a la inicialización."""
        self._validate()

    def _validate(self) -> None:
        """Valida los datos de la categoría."""
        if not self.name or len(self.name.strip()) < 2:
            raise ValueError("Category name must be at least 2 characters long")

    @property
    def display_name(self) -> str:
        """Retorna el nombre para mostrar."""
        return self.name.strip()

    def __eq__(self, other) -> bool:
        """Compara categorías por ID o nombre."""
        if not isinstance(other, Category):
            return False
        
        if self.id and other.id:
            return self.id == other.id
        
        return self.name.lower().strip() == other.name.lower().strip()

    def __hash__(self) -> int:
        """Hash basado en ID o nombre."""
        if self.id:
            return hash(self.id)
        return hash(self.name.lower().strip())

    def __str__(self) -> str:
        """Representación string de la categoría."""
        return f"Category(id={self.id}, name='{self.name}')"