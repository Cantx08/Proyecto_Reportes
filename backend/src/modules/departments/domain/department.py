from dataclasses import dataclass
from uuid import UUID

from .faculty import Faculty


@dataclass
class Department:
    """Entidad que representa un departamento académico."""
    dep_id: UUID
    dep_code: str
    dep_name: str
    faculty: Faculty
