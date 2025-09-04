"""
Entidades del dominio para el sistema de publicaciones académicas.
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Publicacion:
    """Entidad que representa una publicación académica."""
    titulo: str
    anio: str
    fuente: str
    tipo_documento: str
    filiacion: str
    doi: str
    categorias: str = ""

    def es_valida(self) -> bool:
        """Valida si la publicación tiene los datos mínimos requeridos."""
        return bool(self.titulo and self.anio and self.fuente)

    def tiene_filiacion_epn(self) -> bool:
        """Verifica si la publicación tiene filiación con la EPN."""
        return "escuela politécnica nacional" in self.filiacion.lower()


@dataclass
class Autor:
    """Entidad que representa un autor académico."""
    id_autor: str
    lista_publicaciones: Optional[List[Publicacion]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.lista_publicaciones is None:
            self.lista_publicaciones = []

    def agregar_publicacion(self, publicacion: Publicacion) -> None:
        """Agrega una publicación a la lista del autor."""
        if publicacion.es_valida():
            self.lista_publicaciones.append(publicacion)

    def obtener_publicaciones_por_anio(self, anio: str) -> List[Publicacion]:
        """Obtiene las publicaciones de un año específico."""
        return [pub for pub in self.lista_publicaciones if pub.anio == anio]

    def contar_publicaciones(self) -> int:
        """Cuenta el total de publicaciones del autor."""
        return len(self.lista_publicaciones)


@dataclass
class AreaTematica:
    """Entidad que representa un área temática principal con sus subáreas."""
    nombre: str
    clave: Optional[str] = None
    subareas: Optional[List[str]] = None

    def __post_init__(self):
        if self.subareas is None:
            self.subareas = []

    def contiene_subarea(self, subarea: str) -> bool:
        """Verifica si una subárea pertenece a esta área temática."""
        subarea_normalizada = subarea.lower().strip()
        
        # Verificar si es multidisciplinary (caso especial)
        if self.clave == "MULT" and "multidisciplinary" in subarea_normalizada:
            return True
        
        # Buscar en la lista de subáreas
        for sub in self.subareas:
            if subarea_normalizada in sub.lower():
                return True
        
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, AreaTematica):
            return self.nombre.lower() == other.nombre.lower()
        return False

    def __hash__(self) -> int:
        return hash(self.nombre.lower())


@dataclass
class PublicacionesCollection:
    """Colección de publicaciones con métodos de análisis."""
    autores: List[Autor]

    def obtener_todas_las_publicaciones(self) -> List[Publicacion]:
        """Obtiene todas las publicaciones de todos los autores."""
        publicaciones = []
        for autor in self.autores:
            publicaciones.extend(autor.lista_publicaciones)
        return publicaciones

    def contar_publicaciones_por_anio(self) -> dict[str, int]:
        """Cuenta las publicaciones agrupadas por año."""
        publicaciones = self.obtener_todas_las_publicaciones()
        conteo = {}
        
        anios_con_publicaciones = [int(pub.anio) for pub in publicaciones if pub.anio.strip()]
        
        if not anios_con_publicaciones:
            return {}
        
        primer_anio = min(anios_con_publicaciones)
        ultimo_anio = max(anios_con_publicaciones)
        
        # Inicializar todos los años con 0
        for anio in range(primer_anio, ultimo_anio + 1):
            conteo[str(anio)] = 0
        
        # Contar publicaciones reales
        for pub in publicaciones:
            if pub.anio.strip():
                conteo[pub.anio] = conteo.get(pub.anio, 0) + 1
                
        return conteo
