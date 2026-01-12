"""
Módulo que define los Departamentos que pertenecen a la Escuela Politécnica Nacional.
Cada departamento está asociado a una facultad específica.
"""

from dataclasses import dataclass, field
from typing import Optional
from ..enums.faculty import Faculty
from ..exceptions import InvalidEntityData

MIN_CODE_LENGTH = 2
MAX_CODE_LENGTH = 10


@dataclass
class Department:
    """Entidad que representa un departamento académico."""
    dep_id: Optional[int] = field(default=None, kw_only=True)
    dep_code: str
    dep_name: str
    fac_name: Faculty

    def __post_init__(self):
        """Validaciones post-inicialización."""
        if not self.dep_name or not self.dep_name.strip():
            raise InvalidEntityData("El campo nombre del departamento no puede estar vacío.")

        if not self.dep_code or not self.dep_code.strip():
            raise InvalidEntityData("El campo siglas del departamento no puede estar vacío.")

        code_len = len(self.dep_code)
        if not MIN_CODE_LENGTH <= code_len <= MAX_CODE_LENGTH:
            raise InvalidEntityData(
                f"La sigla del departamento debe tener entre {MIN_CODE_LENGTH} y "
                f"{MAX_CODE_LENGTH} caracteres."
            )

        if self.dep_id is not None and self.dep_id <= 0:
            raise InvalidEntityData("ID de departamento incorrecto.")

        if isinstance(self.fac_name, str):
            self.fac_name = Faculty.from_string(self.fac_name)

            self.dep_name = self.dep_name.strip()
            self.dep_code = self.dep_code.strip()

    def update_details(self, dep_code: str, dep_name: str, faculty: Faculty):
        """Actualiza la información de un departamento."""
        if not dep_name or not dep_name.strip():
            raise InvalidEntityData("El campo nombre del departamento no puede estar vacío.")
        if not dep_code or not dep_code.strip():
            raise InvalidEntityData("El campo siglas del departamento no puede estar vacío.")

        if isinstance(faculty, str):
            faculty = Faculty.from_string(faculty)

        self.dep_name = dep_name.strip()
        self.dep_code = dep_code.strip()
        self.fac_name = faculty

    def belongs_to_faculty(self, faculty: Faculty) -> bool:
        """Verifica si el departamento pertenece a una facultad específica."""
        return self.fac_name == faculty
