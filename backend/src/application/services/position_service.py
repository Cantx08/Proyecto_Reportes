from typing import List, Optional
from ...domain.entities.position import Position
from ...domain.repositories.position_repository import PositionRepository


class PositionService:
    """Servicio de aplicación para la gestión de cargos/posiciones."""
    
    def __init__(self, position_repository: PositionRepository):
        self._position_repository = position_repository
    
    async def get_position_by_id(self, pos_id: str) -> Optional[Position]:
        """Obtiene un cargo por su ID."""
        if not pos_id:
            raise ValueError("Position ID is required")
        return await self._position_repository.get_by_id(pos_id)
    
    async def get_position_by_name(self, pos_name: str) -> Optional[Position]:
        """Obtiene un cargo por su nombre."""
        if not pos_name:
            raise ValueError("Position name is required")
        return await self._position_repository.get_by_name(pos_name)
    
    async def get_all_positions(self) -> List[Position]:
        """Obtiene todos los cargos."""
        return await self._position_repository.get_all()
    
    async def create_position(self, position: Position) -> Position:
        """Crea un nuevo cargo."""
        if not position.pos_id:
            raise ValueError("Position ID is required")
        
        # Verificar que no exista ya
        existing_pos = await self._position_repository.get_by_id(position.pos_id)
        if existing_pos:
            raise ValueError(f"Position with ID {position.pos_id} already exists")
        
        # Verificar que no exista el nombre
        existing_name = await self._position_repository.get_by_name(position.pos_name)
        if existing_name:
            raise ValueError(f"Position with name {position.pos_name} already exists")
        
        return await self._position_repository.create(position)
    
    async def update_position(self, position: Position) -> Position:
        """Actualiza un cargo existente."""
        if not position.pos_id:
            raise ValueError("Position ID is required")
        
        # Verificar que existe
        existing_pos = await self._position_repository.get_by_id(position.pos_id)
        if not existing_pos:
            raise ValueError(f"Position with ID {position.pos_id} not found")
        
        return await self._position_repository.update(position)
    
    async def delete_position(self, pos_id: str) -> bool:
        """Elimina un cargo por su ID."""
        if not pos_id:
            raise ValueError("Position ID is required")
        
        # Verificar que existe
        existing_pos = await self._position_repository.get_by_id(pos_id)
        if not existing_pos:
            raise ValueError(f"Position with ID {pos_id} not found")
        
        return await self._position_repository.delete(pos_id)