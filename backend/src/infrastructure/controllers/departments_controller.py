from src.infrastructure.csv.departments_file_repository import DepartmentsFileRepository
from src.infrastructure.dtos.department_dto import DepartmentsResponseDTO
from src.application.services.department_service import DepartmentService

class DepartmentsController:
    """Controlador para manejar endpoints relacionados con departamentos."""
    
    def __init__(self, department_service: DepartmentService):
        """
        Inicializar el controlador con el servicio de departamentos.
        
        Args:
            department_service: Servicio de departamentos
        """
        self.department_service = department_service
    
    async def get_departments(self) -> DepartmentsResponseDTO:
        """
        Obtener todos los departamentos disponibles.
        
        Returns:
            DTO de respuesta con la lista de departamentos
        """
        return self.department_service.get_all_departments()