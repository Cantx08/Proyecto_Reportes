import pandas as pd
from typing import List
from pathlib import Path
from src.infrastructure.dtos.cargo_dto import CargoDTO

class CargosFileRepository:
    """Repositorio para leer cargos desde archivo CSV."""
    
    def __init__(self, csv_path: str = "data/categorias.csv"):
        """
        Inicializar repositorio con la ruta del archivo CSV.
        
        Args:
            csv_path: Ruta relativa al archivo CSV desde la raíz del proyecto
        """
        self.csv_path = Path(__file__).parent.parent.parent.parent / csv_path
    
    def get_all_cargos(self) -> List[CargoDTO]:
        """
        Obtener todos los cargos del archivo CSV.
        
        Returns:
            Lista de DTOs de cargos
        """
        try:
            # Leer el CSV con el separador correcto
            df = pd.read_csv(self.csv_path, sep=';', encoding='utf-8')
            
            cargos = []
            for _, row in df.iterrows():
                cargo = CargoDTO(
                    cargo=row['CARGO'],
                    tiempo=row['TIEMPO']
                )
                cargos.append(cargo)
            
            # Ordenar por nombre del cargo
            cargos.sort(key=lambda x: x.cargo)
            
            return cargos
            
        except Exception as e:
            raise Exception(f"Error al leer el archivo de cargos: {str(e)}")