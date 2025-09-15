"""
Entidad ScopusAccount del dominio.

Representa una cuenta de Scopus asociada a un autor.
"""

from datetime import datetime
from typing import Optional

from ..value_objects.scopus_id import ScopusId


class ScopusAccount:
    """
    Entidad que representa una cuenta de Scopus de un autor.
    
    Un autor puede tener múltiples cuentas de Scopus (por ejemplo,
    si cambió de institución), pero solo una puede ser la principal.
    """
    
    def __init__(
        self,
        scopus_id: ScopusId,
        is_primary: bool = False,
        is_active: bool = True,
        verified_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        """
        Inicializa una cuenta de Scopus.
        
        Args:
            scopus_id: ID de Scopus
            is_primary: Si es la cuenta principal del autor
            is_active: Si la cuenta está activa
            verified_at: Fecha de verificación
            created_at: Fecha de creación
        """
        self._scopus_id = scopus_id
        self._is_primary = is_primary
        self._is_active = is_active
        self._verified_at = verified_at
        self._created_at = created_at or datetime.now()
        
        # Validaciones
        self._validate()
    
    @property
    def scopus_id(self) -> ScopusId:
        """Obtiene el ID de Scopus."""
        return self._scopus_id
    
    @property
    def is_primary(self) -> bool:
        """Indica si es la cuenta principal."""
        return self._is_primary
    
    @property
    def is_active(self) -> bool:
        """Indica si la cuenta está activa."""
        return self._is_active
    
    @property
    def verified_at(self) -> Optional[datetime]:
        """Obtiene la fecha de verificación."""
        return self._verified_at
    
    @property
    def created_at(self) -> datetime:
        """Obtiene la fecha de creación."""
        return self._created_at
    
    @property
    def is_verified(self) -> bool:
        """Indica si la cuenta ha sido verificada."""
        return self._verified_at is not None
    
    def set_as_primary(self) -> None:
        """Marca esta cuenta como principal."""
        self._is_primary = True
    
    def set_as_secondary(self) -> None:
        """Marca esta cuenta como secundaria."""
        self._is_primary = False
    
    def activate(self) -> None:
        """Activa la cuenta."""
        self._is_active = True
    
    def deactivate(self) -> None:
        """Desactiva la cuenta."""
        self._is_active = False
        # Si se desactiva la cuenta principal, ya no puede ser principal
        if self._is_primary:
            self._is_primary = False
    
    def verify(self, verification_date: Optional[datetime] = None) -> None:
        """
        Marca la cuenta como verificada.
        
        Args:
            verification_date: Fecha de verificación (usa la actual si no se especifica)
        """
        self._verified_at = verification_date or datetime.now()
    
    def unverify(self) -> None:
        """Quita la verificación de la cuenta."""
        self._verified_at = None
    
    def _validate(self) -> None:
        """Valida el estado de la cuenta."""
        if not isinstance(self._scopus_id, ScopusId):
            raise ValueError("scopus_id must be a ScopusId instance")
        
        if not isinstance(self._is_primary, bool):
            raise ValueError("is_primary must be a boolean")
        
        if not isinstance(self._is_active, bool):
            raise ValueError("is_active must be a boolean")
        
        if self._verified_at is not None and not isinstance(self._verified_at, datetime):
            raise ValueError("verified_at must be a datetime or None")
        
        if not isinstance(self._created_at, datetime):
            raise ValueError("created_at must be a datetime")
        
        # Una cuenta inactiva no puede ser principal
        if not self._is_active and self._is_primary:
            raise ValueError("An inactive account cannot be primary")
    
    def __eq__(self, other) -> bool:
        """Compara dos cuentas de Scopus por su ID."""
        if not isinstance(other, ScopusAccount):
            return False
        return self._scopus_id == other._scopus_id
    
    def __hash__(self) -> int:
        """Hash basado en el Scopus ID."""
        return hash(self._scopus_id)
    
    def __str__(self) -> str:
        """Representación en string."""
        status = []
        if self._is_primary:
            status.append("primary")
        if self._is_active:
            status.append("active")
        if self.is_verified:
            status.append("verified")
        
        status_str = ", ".join(status) if status else "inactive"
        return f"ScopusAccount({self._scopus_id}, {status_str})"
    
    def __repr__(self) -> str:
        """Representación detallada."""
        return (
            f"ScopusAccount("
            f"scopus_id={self._scopus_id}, "
            f"is_primary={self._is_primary}, "
            f"is_active={self._is_active}, "
            f"verified_at={self._verified_at}, "
            f"created_at={self._created_at})"
        )
    
    def to_dict(self) -> dict:
        """
        Convierte la cuenta a un diccionario.
        
        Returns:
            dict: Representación en diccionario
        """
        return {
            'scopus_id': str(self._scopus_id),
            'is_primary': self._is_primary,
            'is_active': self._is_active,
            'is_verified': self.is_verified,
            'verified_at': self._verified_at.isoformat() if self._verified_at else None,
            'created_at': self._created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ScopusAccount':
        """
        Crea una cuenta de Scopus desde un diccionario.
        
        Args:
            data: Diccionario con los datos
            
        Returns:
            ScopusAccount: Nueva instancia
        """
        verified_at = None
        if data.get('verified_at'):
            verified_at = datetime.fromisoformat(data['verified_at'])
        
        created_at = None
        if data.get('created_at'):
            created_at = datetime.fromisoformat(data['created_at'])
        
        return cls(
            scopus_id=ScopusId(data['scopus_id']),
            is_primary=data.get('is_primary', False),
            is_active=data.get('is_active', True),
            verified_at=verified_at,
            created_at=created_at
        )