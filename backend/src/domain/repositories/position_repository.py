from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.position import Position


class PositionRepository(ABC):
    """Interfaz del repositorio de cargos/posiciones."""
    
    @abstractmethod
    async def get_by_id(self, pos_id: str) -> Optional["Position"]:
        """Obtiene un cargo por su ID."""
        ...
    
    @abstractmethod
    async def get_all(self) -> List["Position"]:
        """Obtiene todos los cargos."""
        ...
    
    @abstractmethod
    async def create(self, position: "Position") -> "Position":
        """Crea un nuevo cargo."""
        ...
    
    @abstractmethod
    async def update(self, position: "Position") -> "Position":
        """Actualiza un cargo existente."""
        ...
    
    @abstractmethod
    async def delete(self, pos_id: str) -> bool:
        """Elimina un cargo por su ID."""
        ...
    
    @abstractmethod
    async def get_by_name(self, pos_name: str) -> Optional["Position"]:
        """Obtiene un cargo por su nombre."""
        ...