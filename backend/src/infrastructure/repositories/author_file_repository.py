import pandas as pd
from typing import List, Optional
from pathlib import Path
from datetime import datetime, date
from ...domain.entities.author import Author
from ...domain.repositories.author_repository import AuthorRepository


class AuthorFileRepository(AuthorRepository):
    """Implementación del repositorio de autores usando archivos CSV."""
    
    def __init__(self, csv_path: str = None):
        self.csv_path = csv_path or Path(__file__).parent.parent.parent / "data" / "docentes.csv"
        self._authors_cache = {}
        # No cargar automáticamente - los autores se inyectarán manualmente
        # self._load_authors()
    
    def _load_authors(self):
        """Carga los autores desde el archivo CSV."""
        try:
            if Path(self.csv_path).exists():
                df = pd.read_csv(self.csv_path, sep=';')
                self._authors_cache = {}
                
                for _, row in df.iterrows():
                    author = Author(
                        author_id=str(row.get('author_id', row.get('id', ''))),
                        name=str(row.get('name', row.get('nombre', ''))),
                        surname=str(row.get('surname', row.get('apellido', ''))),
                        dni=str(row.get('dni', row.get('cedula', ''))),
                        title=str(row.get('title', row.get('titulo', ''))),
                        birth_date=self._parse_date(row.get('birth_date', row.get('fecha_nacimiento'))),
                        gender=str(row.get('gender', row.get('genero', 'M'))),
                        position=str(row.get('position', row.get('cargo', ''))),
                        department=str(row.get('department', row.get('departamento', '')))
                    )
                    self._authors_cache[author.author_id] = author
        except Exception as e:
            print(f"Error loading authors from CSV: {e}")
            self._authors_cache = {}
    
    def load_authors_from_csv(self):
        """Método público para cargar autores desde CSV cuando sea necesario."""
        self._load_authors()
    
    def _parse_date(self, date_value) -> Optional[date]:
        """Parsea una fecha desde el CSV."""
        if pd.isna(date_value) or not date_value:
            return None
        try:
            if isinstance(date_value, str):
                return datetime.strptime(date_value, '%Y-%m-%d').date()
            return date_value
        except (ValueError, TypeError):
            return None
    
    def _save_authors(self):
        """Guarda los autores al archivo CSV."""
        try:
            data = []
            for author in self._authors_cache.values():
                data.append({
                    'author_id': author.author_id,
                    'name': author.name,
                    'surname': author.surname,
                    'dni': author.dni,
                    'title': author.title,
                    'birth_date': author.birth_date.isoformat() if author.birth_date else '',
                    'gender': author.gender,
                    'position': author.position,
                    'department': author.department
                })
            
            df = pd.DataFrame(data)
            df.to_csv(self.csv_path, sep=';', index=False)
        except Exception as e:
            print(f"Error saving authors to CSV: {e}")
    
    async def get_by_id(self, author_id: str) -> Optional[Author]:
        """Obtiene un autor por su ID."""
        return self._authors_cache.get(author_id)
    
    async def get_all(self) -> List[Author]:
        """Obtiene todos los autores."""
        return list(self._authors_cache.values())
    
    async def create(self, author: Author) -> Author:
        """Crea un nuevo autor."""
        if author.author_id in self._authors_cache:
            raise ValueError(f"Author with ID {author.author_id} already exists")
        
        self._authors_cache[author.author_id] = author
        self._save_authors()
        return author
    
    async def update(self, author: Author) -> Author:
        """Actualiza un autor existente."""
        if author.author_id not in self._authors_cache:
            raise ValueError(f"Author with ID {author.author_id} not found")
        
        self._authors_cache[author.author_id] = author
        self._save_authors()
        return author
    
    async def delete(self, author_id: str) -> bool:
        """Elimina un autor por su ID."""
        if author_id in self._authors_cache:
            del self._authors_cache[author_id]
            self._save_authors()
            return True
        return False
    
    async def get_by_department(self, department: str) -> List[Author]:
        """Obtiene autores por departamento."""
        return [author for author in self._authors_cache.values() 
                if author.department.lower() == department.lower()]
    
    async def get_by_position(self, position: str) -> List[Author]:
        """Obtiene autores por cargo."""
        return [author for author in self._authors_cache.values() 
                if author.position.lower() == position.lower()]
    
    async def search_by_name(self, search_term: str) -> List[Author]:
        """Busca autores por nombre o apellido."""
        search_term = search_term.lower()
        return [author for author in self._authors_cache.values() 
                if search_term in author.name.lower() or search_term in author.surname.lower()]