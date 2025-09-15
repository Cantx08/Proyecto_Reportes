import pandas as pd
from typing import List, Optional
from ...domain.entities.subject_area import SubjectArea
from ...application.repositories.subject_areas_repository import SubjectAreasRepository


class SubjectAreasFileRepository(SubjectAreasRepository):
    """Repositorio de áreas temáticas basado en archivo CSV."""
    
    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        self._areas: Optional[List[SubjectArea]] = None
        self._load_areas()
    
    def _load_areas(self) -> None:
        """Carga las áreas temáticas del archivo CSV."""
        try:
            df = pd.read_csv(self._csv_path, sep=';')
            self._areas = []
            
            for _, row in df.iterrows():
                area_code = row['CLAVE']
                subject_area = row['AREA TEMATICA']
                subareas = row['SUBAREAS']
                
                # Procesar subáreas
                subareas = []
                if pd.notna(subareas) and subareas.strip():
                    # Dividir por ';' y limpiar espacios
                    subareas = [sub.strip() for sub in subareas.split(';') if sub.strip()]
                
                area = SubjectArea(
                    area_key=area_code,
                    name=subject_area,
                    subareas=subareas
                )
                self._areas.append(area)
                
        except Exception as e:
            print(f"Error cargando áreas temáticas: {str(e)}")
            self._areas = []

    def _normalize_text(self, texto: str) -> str:
        """Normaliza un texto para comparación."""
        return texto.lower().strip()
    
    def _belongs_to_subject_area(self, normalized_subarea: str, area: SubjectArea) -> bool:
        """Verifica si una subárea normalizada pertenece a un área temática."""
        # Buscar coincidencias exactas o parciales en las subáreas
        for subarea in area.subareas:
            normalized_subarea = self._normalize_text(subarea)
            
            # Coincidencia exacta
            if normalized_subarea == normalized_subarea:
                return True
            
            # Coincidencia parcial (la subárea está contenida en la definición)
            if normalized_subarea in normalized_subarea:
                return True
            
            # Coincidencia parcial inversa (la definición está contenida en la subárea)
            if normalized_subarea in normalized_subarea:
                return True
        
        return False

    async def get_subject_areas_by_author(self, author_id: str) -> List[SubjectArea]:
        """
        Obtiene las áreas temáticas de un autor.
        Esta implementación del repositorio de archivos no puede obtener datos por autor,
        ya que es un repositorio de mapeo. Devuelve lista vacía.
        """
        return []
    
    def get_all_subject_areas(self) -> List[SubjectArea]:
        """Obtiene todas las áreas temáticas con sus subáreas."""
        return self._areas if self._areas else []
    
    def map_subarea_to_area(self, subarea: str) -> Optional[str]:
        """
        Mapea una subárea específica a su área temática principal.
        Args:
            subarea: El nombre de la subárea a mapear (ej: "Computer Science Applications")
        Returns:
            El nombre del área temática principal (ej: "Computer Science") o None si no se encuentra
        """
        if not self._areas or not subarea:
            return None
        
        normalized_subarea = self._normalize_text(subarea)
        
        # Area Multidisciplinary
        if "multidisciplinary" in normalized_subarea:
            return "Multidisciplinary"
        
        # Buscar en todas las áreas temáticas
        for area in self._areas:
            if self._belongs_to_subject_area(normalized_subarea, area):
                return area.nombre
        
        return None