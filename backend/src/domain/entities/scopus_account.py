from dataclasses import dataclass


@dataclass
class ScopusAccount:
    """Entidad que representa una cuenta de Scopus asociada a un autor."""
    scopus_id: str
    scopus_user: str
    author_id: str
    
    def __post_init__(self):
        """Validaciones post-inicialización."""
        if not self.scopus_id or not self.author_id:
            raise ValueError("scopus_id y author_id son requeridos")
        
        if not self.scopus_user:
            self.scopus_user = f"user_{self.scopus_id}"
    
    def __str__(self) -> str:
        """Representación en string de la cuenta Scopus."""
        return f"Scopus({self.scopus_id}): {self.scopus_user}"