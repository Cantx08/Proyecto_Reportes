from enum import Enum


class Faculty(Enum):
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
    def from_string(cls, faculty_name: str) -> "Faculty":
        """Convierte un string a un enum Faculty."""
        for faculty in cls:
            if faculty.value.lower() == faculty_name.lower():
                return faculty
        return cls.DESCONOCIDA