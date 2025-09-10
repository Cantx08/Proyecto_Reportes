"""
Value Objects para el dominio de reportes.
"""
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from enum import Enum

from .entities import Publicacion


class Genero(Enum):
    """Enum para el género del docente."""
    MASCULINO = "M"
    FEMENINO = "F"


class TipoFirmante(Enum):
    """Enum para el tipo de firmante."""
    DIRECTORA_INVESTIGACION = 1
    VICERRECTOR_INVESTIGACION = 2


@dataclass(frozen=True)
class DocenteInfo:
    """Value Object para la información básica del docente."""
    nombre: str
    genero: Genero
    departamento: str
    cargo: str
    
    def obtener_articulo(self) -> str:
        """Retorna el artículo apropiado según el género."""
        return "El" if self.genero == Genero.MASCULINO else "La"
    
    def obtener_autor_coautor(self) -> str:
        """Retorna la forma apropiada de autor/coautor según el género."""
        return "autor/co-autor" if self.genero == Genero.MASCULINO else "autora/co-autora"


@dataclass(frozen=True)
class ConfiguracionReporte:
    """Value Object para la configuración del reporte."""
    memorando: str
    firmante: TipoFirmante
    fecha: str
    
    @classmethod
    def crear_con_fecha_actual(cls, memorando: str = "", firmante: TipoFirmante = TipoFirmante.DIRECTORA_INVESTIGACION):
        """Factory method para crear configuración con fecha actual."""
        fecha = datetime.now().strftime("%d de %B de %Y")
        return cls(memorando, firmante, fecha)


@dataclass(frozen=True)
class EstadisticasPublicaciones:
    """Value Object para las estadísticas de publicaciones."""
    areas_tematicas: List[str]
    documentos_por_anio: Dict[str, int]
    
    def tiene_suficientes_datos_para_grafico(self) -> bool:
        """Verifica si hay suficientes datos para mostrar un gráfico."""
        return len(self.documentos_por_anio) > 1


@dataclass(frozen=True)
class ColeccionesPublicaciones:
    """Value Object que agrupa todas las colecciones de publicaciones."""
    scopus: List[Publicacion]
    wos: List[Publicacion]
    regionales: List[Publicacion]
    memorias: List[Publicacion]
    libros: List[Publicacion]
    
    def total_publicaciones(self) -> int:
        """Calcula el total de publicaciones."""
        return (len(self.scopus) + len(self.wos) + len(self.regionales) + 
                len(self.memorias) + len(self.libros))
    
    def tiene_publicaciones_scopus(self) -> bool:
        """Verifica si hay publicaciones Scopus."""
        return len(self.scopus) > 0
