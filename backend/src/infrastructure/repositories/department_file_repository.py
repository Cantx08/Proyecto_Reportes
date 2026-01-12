import pandas as pd
from typing import List, Optional
from pathlib import Path
from ...domain.entities.department import Department
from backend.src.domain.enums.faculty import Faculty
from ...domain.repositories.department_repository import IDepartmentRepository


class DepartmentFileRepository(IDepartmentRepository):
    """Implementación del repositorio de departamentos usando archivos CSV."""
    
    def __init__(self, csv_path: str = None):
        self.csv_path = csv_path or Path(__file__).parent.parent.parent / "data" / "deps.csv"
        self._departments_cache = {}
        self._load_departments()
    
    def _load_departments(self):
        """Carga los departamentos desde el archivo CSV."""
        try:
            if Path(self.csv_path).exists():
                df = pd.read_csv(self.csv_path, sep=';')
                self._departments_cache = {}
                
                for _, row in df.iterrows():
                    # Generar ID único si no existe
                    dep_id = str(row.get('DEP_ID', row.get('DEP_SIGLA', '')))
                    
                    department = Department(
                        dep_id=dep_id,
                        dep_code=str(row.get('DEP_SIGLA', '')),
                        dep_name=str(row.get('NOMBRE', '')),
                        faculty=Faculty.from_string(str(row.get('FACULTAD_NOMBRE', '')))
                    )
                    self._departments_cache[department.dep_id] = department
        except Exception as e:
            print(f"Error loading departments from CSV: {e}")
            self._departments_cache = {}
    
    def _save_departments(self):
        """Guarda los departamentos al archivo CSV."""
        try:
            data = []
            for dept in self._departments_cache.values():
                data.append({
                    'DEP_SIGLA': dept.dep_code,
                    'NOMBRE': dept.dep_name,
                    'FACULTAD_NOMBRE': dept.fac_name.value
                })
            
            df = pd.DataFrame(data)
            df.to_csv(self.csv_path, sep=';', index=False)
        except Exception as e:
            print(f"Error saving departments to CSV: {e}")
    
    async def get_by_id(self, dep_id: str) -> Optional[Department]:
        """Obtiene un departamento por su ID."""
        return self._departments_cache.get(dep_id)
    
    async def get_by_name(self, dep_code: str) -> Optional[Department]:
        """Obtiene un departamento por su código/sigla."""
        for dept in self._departments_cache.values():
            if dept.dep_code.upper() == dep_code.upper():
                return dept
        return None
    
    async def get_all(self) -> List[Department]:
        """Obtiene todos los departamentos."""
        return list(self._departments_cache.values())
    
    async def create(self, department: Department) -> Department:
        """Crea un nuevo departamento."""
        if department.dep_id in self._departments_cache:
            raise ValueError(f"Department with ID {department.dep_id} already exists")
        
        self._departments_cache[department.dep_id] = department
        self._save_departments()
        return department
    
    async def update(self, department: Department) -> Department:
        """Actualiza un departamento existente."""
        if department.dep_id not in self._departments_cache:
            raise ValueError(f"Department with ID {department.dep_id} not found")
        
        self._departments_cache[department.dep_id] = department
        self._save_departments()
        return department
    
    async def delete(self, dep_id: str) -> bool:
        """Elimina un departamento por su ID."""
        if dep_id in self._departments_cache:
            del self._departments_cache[dep_id]
            self._save_departments()
            return True
        return False
    
    async def get_by_faculty(self, faculty_name: str) -> List[Department]:
        """Obtiene departamentos por facultad."""
        faculty = Faculty.from_string(faculty_name)
        return [dept for dept in self._departments_cache.values() 
                if dept.fac_name == faculty]