from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SubjectArea:
    """Entidad que representa un área temática principal con sus subáreas."""
    name: str
    area_key: Optional[str] = None
    subareas: Optional[List[str]] = None

    def __post_init__(self):
        if self.subareas is None:
            self.subareas = []

    def contains_subarea(self, subarea: str) -> bool:
        """Verifica si una subárea pertenece a esta área temática."""
        subarea_normalized = subarea.lower().strip()
        
        # Verificar si es multidisciplinary (caso especial)
        if self.area_key == "MULT" and "multidisciplinary" in subarea_normalized:
            return True
        
        # Buscar en la lista de subáreas
        for sub in self.subareas:
            if subarea_normalized in sub.lower():
                return True
        
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, SubjectArea):
            return self.name.lower() == other.name.lower()
        return False

    def __hash__(self) -> int:
        return hash(self.name.lower())