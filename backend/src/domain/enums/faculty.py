"""
Lista de facultades de la Escuela Politécnica Nacional
"""
from enum import Enum
from typing import List


class Faculty(str, Enum):
    """Enumeración de las facultades de la EPN."""
    FIEE = "Facultad de Ingeniería Eléctrica y Electrónica"
    FC = "Facultad de Ciencias"
    FCA = "Facultad de Ciencias Administrativas"
    FIQA = "Facultad de Ingeniería Química y Agroindustria"
    CS = "Ciencias Sociales"
    DFB = "Formación Básica"
    FIGP = "Facultad de Geología y Petróleos"
    FIS = "Facultad de Ingeniería de Sistemas"
    FICA = "Facultad de Ingeniería Civil y Ambiental"
    FIM = "Facultad de Ingeniería Mecánica"
    ESFOT = "Escuela de Formación de Tecnólogos"
    IG = "Instituto Geofísico"
    DESCONOCIDA = "No encontrada"

    @classmethod
    def from_string(cls, fac_name:str) -> "Faculty":
        """Permite crear un enum a partir de un string."""
        if not isinstance(fac_name, str):
            fac_name = str(fac_name)

        for faculty in cls:
            if faculty.value.lower() == fac_name.lower():
                return faculty
            if faculty.name.lower() == fac_name.lower():
                return faculty
        return cls.DESCONOCIDA

    @classmethod
    def list_faculties(cls) -> List[dict]:
        """Retorna la lista de todas las facultades."""
        return [
            {"key": faculty.name, "value": faculty.value}
            for faculty in cls if faculty != cls.DESCONOCIDA
        ]

    def __str__(self) -> str:
        """Retorna el nombre de la facultad."""
        return self.value
