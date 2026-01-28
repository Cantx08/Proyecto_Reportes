from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from uuid import UUID


@dataclass
class Department:
    """Entidad que representa un departamento académico."""
    dep_id: UUID
    dep_code: str
    dep_name: str
    faculty: Faculty


class Faculty(str, Enum):
    """ Enum que representa las facultades de la EPN. """
    FIEE = "FIEE"
    FC = "FC"
    FCA = "FCA"
    FIQA = "FIQA"
    CS = "CS"
    DFB = "DFB"
    FIGP = "FIGP"
    FIS = "FIS"
    FICA = "FICA"
    FIM = "FIM"
    ESFOT = "ESFOT"
    IG = "IG"

    @property
    def fac_code(self) -> str:
        return self.value

    @property
    def fac_name(self) -> str:
        # Mapa de nombres completos
        names = {
            "FIEE": "Facultad de Ingeniería Eléctrica y Electrónica",
            "FC": "Facultad de Ciencias",
            "FCA": "Facultad de Ciencias Administrativas",
            "FIQA": "Facultad de Ingeniería Química y Agroindustria",
            "CS": "Ciencias Sociales",
            "DFB": "Formación Básica",
            "FIGP": "Facultad de Geología y Petróleos",
            "FIS": "Facultad de Ingeniería de Sistemas",
            "FICA": "Facultad de Ingeniería Civil y Ambiental",
            "FIM": "Facultad de Ingeniería Mecánica",
            "ESFOT": "Escuela de Formación de Tecnólogos",
            "IG": "Instituto Geofísico"
        }
        return names.get(self.value, "Facultad No Encontrada")


class IDepartmentRepository(ABC):
    """Interfaz del repositorio de departamentos."""

    @abstractmethod
    async def get_all(self) -> List[Department]:
        """Obtiene todos los departamentos."""

    @abstractmethod
    async def get_by_faculty(self, faculty: Faculty) -> List[Department]:
        """Obtiene departamentos por facultad."""

    @abstractmethod
    async def get_by_id(self, dep_id: UUID) -> Optional[Department]:
        """Obtiene un departamento por su ID."""

    @abstractmethod
    async def create(self, department: Department) -> Department:
        """Crea un nuevo departamento."""

    @abstractmethod
    async def update(self, dep_id: UUID, department: Department) -> Department:
        """Actualiza un departamento existente."""

    @abstractmethod
    async def delete(self, dep_id: UUID) -> bool:
        """Elimina un departamento por su ID."""
