from ....application.dtos.legacy_department_dto import LegacyDepartmentsResponseDTO
from ....application.services.legacy_department_service import LegacyDepartmentService

class DepartmentsController:
    """Controlador para manejar endpoints relacionados con departamentos."""
    
    def __init__(self, department_service: LegacyDepartmentService):
        """
        Inicializar el controlador con el servicio de departamentos.
        
        Args:
            department_service: Servicio de departamentos
        """
        self.department_service = department_service
    
    async def get_departments(self) -> LegacyDepartmentsResponseDTO:
        """
        Obtener todos los departamentos disponibles.
        
        Returns:
            DTO de respuesta con la lista de departamentos
        """
        return await self.department_service.get_all_departments()