from dataclasses import dataclass
from uuid import UUID


@dataclass
class JobPosition:
    """
    Entidad que representa un cargo/posición.
    """
    pos_id: UUID
    pos_name: str

    def is_full_time(self) -> bool:
        """Indica si el cargo es a tiempo completo."""
        return "Tiempo Completo" in self.pos_name
