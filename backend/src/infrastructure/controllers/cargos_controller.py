from src.infrastructure.dtos.cargo_dto import CargosResponseDTO
from src.application.services.cargo_service import CargoService

class CargosController:
    """Controlador para manejar endpoints relacionados con cargos."""
    
    def __init__(self, cargo_service: CargoService):
        """
        Inicializar el controlador con el servicio de cargos.
        
        Args:
            cargo_service: Servicio de cargos
        """
        self.cargo_service = cargo_service
    
    async def get_cargos(self) -> CargosResponseDTO:
        """
        Obtener todos los cargos disponibles.
        
        Returns:
            DTO de respuesta con la lista de cargos
        """
        return self.cargo_service.get_all_cargos()