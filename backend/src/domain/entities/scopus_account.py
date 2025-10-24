from dataclasses import dataclass


@dataclass
class ScopusAccount:
    """Entidad que representa una cuenta de Scopus asociada a un autor."""
    scopus_id: str
    author_id: str
    is_active: bool = True
    
    def __post_init__(self):
        """Validaciones post-inicialización."""
        if not self.scopus_id or not self.author_id:
            raise ValueError("scopus_id y author_id son requeridos")
    
    def __str__(self) -> str:
        """Representación en string de la cuenta Scopus."""
        return f"Scopus({self.scopus_id}): {'Active' if self.is_active else 'Inactive'}"