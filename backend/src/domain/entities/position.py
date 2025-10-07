from dataclasses import dataclass


@dataclass
class Position:
    """Entidad que representa un cargo académico."""
    pos_id: str
    pos_name: str
    
    def __post_init__(self):
        """Validaciones post-inicialización."""
        if not self.pos_id or not self.pos_name:
            raise ValueError("ID y nombre del cargo son requeridos")
    
    def __str__(self) -> str:
        """Representación en string del cargo."""
        return self.pos_name