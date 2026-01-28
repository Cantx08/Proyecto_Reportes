from enum import Enum


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
