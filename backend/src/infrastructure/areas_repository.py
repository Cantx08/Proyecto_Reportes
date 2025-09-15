"""
Implementación del repositorio de áreas temáticas.
"""
import pandas as pd
from typing import List, Optional
from ..domain.entities import AreaTematica
from ..domain.repositories import AreasTematicasRepository


class AreasTematicasFileRepository(AreasTematicasRepository):
    """Repositorio de áreas temáticas basado en archivo CSV."""
    
    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        self._areas: Optional[List[AreaTematica]] = None
        self._cargar_areas()
    
    def _cargar_areas(self) -> None:
        """Carga las áreas temáticas del archivo CSV."""
        try:
            df = pd.read_csv(self._csv_path, sep=';')
            self._areas = []
            
            for _, row in df.iterrows():
                clave = row['CLAVE']
                nombre = row['AREA TEMATICA']
                subareas_str = row['SUBAREAS']
                
                # Procesar subáreas
                subareas = []
                if pd.notna(subareas_str) and subareas_str.strip():
                    # Dividir por ';' y limpiar espacios
                    subareas = [sub.strip() for sub in subareas_str.split(';') if sub.strip()]
                
                area = AreaTematica(
                    clave=clave,
                    nombre=nombre,
                    subareas=subareas
                )
                self._areas.append(area)
                
        except Exception as e:
            print(f"Error cargando áreas temáticas: {str(e)}")
            self._areas = []
    
    async def obtener_areas_tematicas_por_autor(self, author_id: str) -> List[AreaTematica]:
        """
        Obtiene las áreas temáticas de un autor.
        Esta implementación del repositorio de archivos no puede obtener datos por autor,
        ya que es un repositorio de mapeo. Devuelve lista vacía.
        """
        return []
    
    def obtener_todas_las_areas(self) -> List[AreaTematica]:
        """Obtiene todas las áreas temáticas con sus subáreas."""
        return self._areas if self._areas else []
    
    def mapear_subarea_a_area_principal(self, subarea: str) -> Optional[str]:
        """
        Mapea una subárea específica a su área temática principal.
        
        Args:
            subarea: El nombre de la subárea a mapear (ej: "Computer Science Applications")
            
        Returns:
            El nombre del área temática principal (ej: "Computer Science") o None si no se encuentra
        """
        if not self._areas or not subarea:
            return None
        
        subarea_limpia = self._normalizar_texto(subarea)
        
        # Caso especial para Multidisciplinary
        if "multidisciplinary" in subarea_limpia:
            return "Multidisciplinary"
        
        # Buscar en todas las áreas temáticas
        for area in self._areas:
            if self._subarea_pertenece_a_area(subarea_limpia, area):
                return area.nombre
        
        return None
    
    def _normalizar_texto(self, texto: str) -> str:
        """Normaliza un texto para comparación."""
        return texto.lower().strip()
    
    def _subarea_pertenece_a_area(self, subarea_normalizada: str, area: AreaTematica) -> bool:
        """Verifica si una subárea normalizada pertenece a un área temática."""
        # Buscar coincidencias exactas o parciales en las subáreas
        for sub in area.subareas:
            sub_normalizada = self._normalizar_texto(sub)
            
            # Coincidencia exacta
            if subarea_normalizada == sub_normalizada:
                return True
            
            # Coincidencia parcial (la subárea está contenida en la definición)
            if subarea_normalizada in sub_normalizada:
                return True
            
            # Coincidencia parcial inversa (la definición está contenida en la subárea)
            if sub_normalizada in subarea_normalizada:
                return True
        
        return False
