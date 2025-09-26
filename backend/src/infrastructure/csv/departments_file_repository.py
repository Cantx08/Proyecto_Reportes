import pandas as pd
from typing import List
from pathlib import Path
from src.infrastructure.dtos.department_dto import DepartmentDTO

class DepartmentsFileRepository:
    """Repositorio para leer departamentos desde archivo CSV."""
    
    def __init__(self, csv_path: str = "data/deps.csv"):
        """
        Inicializar repositorio con la ruta del archivo CSV.
        
        Args:
            csv_path: Ruta relativa al archivo CSV desde la raíz del proyecto
        """
        self.csv_path = Path(__file__).parent.parent.parent.parent / csv_path
    
    def get_all_departments(self) -> List[DepartmentDTO]:
        """
        Obtener todos los departamentos del archivo CSV.
        
        Returns:
            Lista de DTOs de departamentos
        """
        try:
            # Leer el CSV con el separador correcto
            df = pd.read_csv(self.csv_path, sep=';', encoding='utf-8')
            
            departments = []
            for _, row in df.iterrows():
                department = DepartmentDTO(
                    sigla=row['DEP_SIGLA'],
                    nombre=row['NOMBRE'],
                    facultad=row['FACULTAD_NOMBRE']
                )
                departments.append(department)
            
            # Ordenar por nombre del departamento
            departments.sort(key=lambda x: x.nombre)
            
            return departments
            
        except Exception as e:
            raise Exception(f"Error al leer el archivo de departamentos: {str(e)}")