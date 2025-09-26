from typing import List
from src.infrastructure.csv.departments_file_repository import DepartmentsFileRepository
from src.infrastructure.dtos.department_dto import DepartmentDTO, DepartmentsResponseDTO

class DepartmentService:
    """Servicio para manejar operaciones relacionadas con departamentos."""
    
    def __init__(self, departments_repository: DepartmentsFileRepository):
        """
        Inicializar el servicio con el repositorio de departamentos.
        
        Args:
            departments_repository: Repositorio para acceder a los datos de departamentos
        """
        self.departments_repository = departments_repository
    
    def get_all_departments(self) -> DepartmentsResponseDTO:
        """
        Obtener todos los departamentos disponibles.
        
        Returns:
            DTO de respuesta con la lista de departamentos
        """
        try:
            departments = self.departments_repository.get_all_departments()
            
            return DepartmentsResponseDTO(
                success=True,
                data=departments,
                message=f"Se encontraron {len(departments)} departamentos"
            )
            
        except Exception as e:
            return DepartmentsResponseDTO(
                success=False,
                data=[],
                message=f"Error al obtener departamentos: {str(e)}"
            )