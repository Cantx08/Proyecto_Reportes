from ...infrastructure.repositories.cargos_file_repository import CargosFileRepository
from ..dtos.cargo_dto import CargosResponseDTO

class CargoService:
    """Servicio para manejar operaciones relacionadas con cargos."""
    
    def __init__(self, cargos_repository: CargosFileRepository):
        """
        Inicializar el servicio con el repositorio de cargos.
        
        Args:
            cargos_repository: Repositorio para acceder a los datos de cargos
        """
        self.cargos_repository = cargos_repository
    
    def get_all_cargos(self) -> CargosResponseDTO:
        """
        Obtener todos los cargos disponibles.
        
        Returns:
            DTO de respuesta con la lista de cargos
        """
        try:
            cargos = self.cargos_repository.get_all_cargos()
            
            return CargosResponseDTO(
                success=True,
                data=cargos,
                message=f"Se encontraron {len(cargos)} cargos"
            )
            
        except Exception as e:
            return CargosResponseDTO(
                success=False,
                data=[],
                message=f"Error al obtener cargos: {str(e)}"
            )