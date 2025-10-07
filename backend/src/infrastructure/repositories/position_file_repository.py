import pandas as pd
from typing import List, Optional
from pathlib import Path
from ...domain.entities.position import Position
from ...domain.repositories.position_repository import PositionRepository


class PositionFileRepository(PositionRepository):
    """Implementación del repositorio de cargos usando archivos CSV."""
    
    def __init__(self, csv_path: str = None):
        # Buscar archivo de cargos existente o usar uno por defecto
        base_path = Path(__file__).parent.parent.parent / "data"
        possible_files = ["cargos.csv", "posiciones.csv", "positions.csv"]
        
        if csv_path:
            self.csv_path = csv_path
        else:
            # Buscar el primer archivo que exista
            self.csv_path = None
            for filename in possible_files:
                if (base_path / filename).exists():
                    self.csv_path = str(base_path / filename)
                    break
            
            # Si no existe ninguno, usar el primero como default
            if not self.csv_path:
                self.csv_path = str(base_path / possible_files[0])
        
        self._positions_cache = {}
        self._load_positions()
    
    def _load_positions(self):
        """Carga los cargos desde el archivo CSV."""
        try:
            if Path(self.csv_path).exists():
                df = pd.read_csv(self.csv_path, sep=';')
                self._positions_cache = {}
                
                for idx, row in df.iterrows():
                    # Generar ID si no existe
                    pos_id = str(row.get('pos_id', row.get('id', f'pos_{idx}')))
                    pos_name = str(row.get('pos_name', row.get('cargo', row.get('position', ''))))
                    
                    if pos_name:  # Solo crear si tiene nombre
                        position = Position(
                            pos_id=pos_id,
                            pos_name=pos_name
                        )
                        self._positions_cache[position.pos_id] = position
            else:
                # Crear algunos cargos por defecto si no existe el archivo
                default_positions = [
                    Position("1", "Profesor Principal"),
                    Position("2", "Profesor Agregado"),
                    Position("3", "Profesor Auxiliar"),
                    Position("4", "Profesor Ocasional"),
                    Position("5", "Profesor Invitado"),
                    Position("6", "Director de Departamento"),
                    Position("7", "Coordinador")
                ]
                
                for pos in default_positions:
                    self._positions_cache[pos.pos_id] = pos
                
                # Guardar los cargos por defecto
                self._save_positions()
                
        except Exception as e:
            print(f"Error loading positions from CSV: {e}")
            self._positions_cache = {}
    
    def _save_positions(self):
        """Guarda los cargos al archivo CSV."""
        try:
            data = []
            for pos in self._positions_cache.values():
                data.append({
                    'pos_id': pos.pos_id,
                    'pos_name': pos.pos_name
                })
            
            df = pd.DataFrame(data)
            df.to_csv(self.csv_path, sep=';', index=False)
        except Exception as e:
            print(f"Error saving positions to CSV: {e}")
    
    async def get_by_id(self, pos_id: str) -> Optional[Position]:
        """Obtiene un cargo por su ID."""
        return self._positions_cache.get(pos_id)
    
    async def get_all(self) -> List[Position]:
        """Obtiene todos los cargos."""
        return list(self._positions_cache.values())
    
    async def create(self, position: Position) -> Position:
        """Crea un nuevo cargo."""
        if position.pos_id in self._positions_cache:
            raise ValueError(f"Position with ID {position.pos_id} already exists")
        
        self._positions_cache[position.pos_id] = position
        self._save_positions()
        return position
    
    async def update(self, position: Position) -> Position:
        """Actualiza un cargo existente."""
        if position.pos_id not in self._positions_cache:
            raise ValueError(f"Position with ID {position.pos_id} not found")
        
        self._positions_cache[position.pos_id] = position
        self._save_positions()
        return position
    
    async def delete(self, pos_id: str) -> bool:
        """Elimina un cargo por su ID."""
        if pos_id in self._positions_cache:
            del self._positions_cache[pos_id]
            self._save_positions()
            return True
        return False
    
    async def get_by_name(self, pos_name: str) -> Optional[Position]:
        """Obtiene un cargo por su nombre."""
        for pos in self._positions_cache.values():
            if pos.pos_name.lower() == pos_name.lower():
                return pos
        return None