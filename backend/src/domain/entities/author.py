from dataclasses import dataclass, field
from typing import List, Optional, Set
from datetime import datetime
from enum import Enum

from ..value_objects.scopus_id import ScopusId
from ..value_objects.email import Email
from ..exceptions.author_exceptions import InvalidAuthorDataError


class Gender(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "Other"


@dataclass
class Author:
    """
    Entidad que representa un autor académico.
    
    Esta entidad contiene toda la información personal y profesional
    de un docente/investigador, incluyendo sus cuentas de Scopus.
    """
    
    # Identificadores únicos
    id: Optional[int] = None
    dni: Optional[str] = None
    
    # Información personal
    first_name: str = ""
    last_name: str = ""
    email: Optional[Email] = None
    gender: Optional[Gender] = None
    
    # Información profesional
    title: str = ""  # Dr., PhD, Ing., etc.
    position: str = ""  # Cargo/puesto
    department_id: Optional[int] = None
    
    # Cuentas Scopus
    scopus_accounts: List[ScopusId] = field(default_factory=list)
    primary_scopus_id: Optional[ScopusId] = None
    
    # Estado
    is_active: bool = True
    
    # Auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones posteriores a la inicialización."""
        self._validate()

    def _validate(self) -> None:
        """Valida los datos del autor."""
        if not self.first_name or not self.last_name:
            raise InvalidAuthorDataError("First name and last name are required")
        
        if self.email and not isinstance(self.email, Email):
            raise InvalidAuthorDataError("Email must be a valid Email value object")

    @property
    def full_name(self) -> str:
        """Retorna el nombre completo del autor."""
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def display_name(self) -> str:
        """Retorna el nombre para mostrar con título."""
        if self.title:
            return f"{self.title} {self.full_name}"
        return self.full_name

    def add_scopus_account(self, scopus_id: ScopusId) -> None:
        """
        Agrega una cuenta de Scopus al autor.
        
        Args:
            scopus_id: ID de Scopus validado
            
        Raises:
            InvalidAuthorDataError: Si el ID ya existe
        """
        if scopus_id in self.scopus_accounts:
            raise InvalidAuthorDataError(f"Scopus ID {scopus_id.value} already exists for this author")
        
        self.scopus_accounts.append(scopus_id)
        
        # Si es la primera cuenta, establecerla como principal
        if not self.primary_scopus_id:
            self.primary_scopus_id = scopus_id

    def set_primary_scopus_account(self, scopus_id: ScopusId) -> None:
        """
        Establece una cuenta de Scopus como principal.
        
        Args:
            scopus_id: ID de Scopus que será principal
            
        Raises:
            InvalidAuthorDataError: Si el ID no existe en las cuentas del autor
        """
        if scopus_id not in self.scopus_accounts:
            raise InvalidAuthorDataError(f"Scopus ID {scopus_id.value} not found in author's accounts")
        
        self.primary_scopus_id = scopus_id

    def remove_scopus_account(self, scopus_id: ScopusId) -> None:
        """
        Elimina una cuenta de Scopus del autor.
        
        Args:
            scopus_id: ID de Scopus a eliminar
            
        Raises:
            InvalidAuthorDataError: Si es la única cuenta o la cuenta principal
        """
        if len(self.scopus_accounts) <= 1:
            raise InvalidAuthorDataError("Cannot remove the only Scopus account")
        
        if scopus_id not in self.scopus_accounts:
            raise InvalidAuthorDataError(f"Scopus ID {scopus_id.value} not found")
        
        self.scopus_accounts.remove(scopus_id)
        
        # Si era la cuenta principal, establecer una nueva
        if self.primary_scopus_id == scopus_id:
            self.primary_scopus_id = self.scopus_accounts[0] if self.scopus_accounts else None

    def get_all_scopus_ids(self) -> List[str]:
        """Retorna todos los IDs de Scopus como strings."""
        return [scopus_id.value for scopus_id in self.scopus_accounts]

    def has_scopus_account(self, scopus_id: str) -> bool:
        """Verifica si el autor tiene una cuenta de Scopus específica."""
        return any(account.value == scopus_id for account in self.scopus_accounts)

    def update_personal_info(self, 
                           first_name: Optional[str] = None,
                           last_name: Optional[str] = None,
                           email: Optional[Email] = None,
                           gender: Optional[Gender] = None) -> None:
        """Actualiza la información personal del autor."""
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
        if gender:
            self.gender = gender
        
        self.updated_at = datetime.now()
        self._validate()

    def update_professional_info(self,
                               title: Optional[str] = None,
                               position: Optional[str] = None,
                               department_id: Optional[int] = None) -> None:
        """Actualiza la información profesional del autor."""
        if title is not None:
            self.title = title
        if position is not None:
            self.position = position
        if department_id is not None:
            self.department_id = department_id
        
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """Desactiva el autor."""
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Activa el autor."""
        self.is_active = True
        self.updated_at = datetime.now()

    def __eq__(self, other) -> bool:
        """Compara autores por ID o DNI."""
        if not isinstance(other, Author):
            return False
        
        if self.id and other.id:
            return self.id == other.id
        
        if self.dni and other.dni:
            return self.dni == other.dni
        
        return False

    def __hash__(self) -> int:
        """Hash basado en ID o DNI."""
        if self.id:
            return hash(self.id)
        if self.dni:
            return hash(self.dni)
        return hash(self.full_name)