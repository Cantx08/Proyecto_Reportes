from dataclasses import dataclass
from ..value_objects.faculty import Faculty


@dataclass
class Department:
    """Entidad que representa un departamento académico."""
    dep_id: str
    dep_code: str
    dep_name: str
    fac_name: Faculty

    def __post_init__(self):
        """Validaciones post-inicialización."""
        if not self.dep_id or not self.dep_code or not self.dep_name:
            raise ValueError("Todos los campos del departamento son requeridos")

        # Convertir string a Faculty enum si es necesario
        if isinstance(self.fac_name, str):
            self.fac_name = Faculty.from_string(self.fac_name)

    def get_full_name(self) -> str:
        """Retorna el nombre completo del departamento con su sigla."""
        return f"{self.dep_name} ({self.dep_code})"

    def belongs_to_faculty(self, faculty: Faculty) -> bool:
        """Verifica si el departamento pertenece a una facultad específica."""
        return self.fac_name == faculty
