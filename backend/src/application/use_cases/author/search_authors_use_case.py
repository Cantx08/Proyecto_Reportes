"""
Caso de uso para buscar autores.
"""

from typing import List, Dict, Any

from ....domain.entities.author import Author
from ....domain.repositories.author_repository import AuthorRepository


class SearchAuthorsUseCase:
    """Caso de uso para buscar autores."""
    
    def __init__(self, author_repository: AuthorRepository):
        self.author_repository = author_repository
    
    def execute(self, query: str) -> List[Author]:
        """
        Ejecuta la búsqueda de autores.
        
        Args:
            query: Término de búsqueda (nombre, DNI, etc.)
            
        Returns:
            List[Author]: Lista de autores encontrados
        """
        if not query or not query.strip():
            return []
        
        query = query.strip()
        
        # Si parece ser un DNI, buscar por DNI exacto
        if self._looks_like_dni(query):
            author = self.author_repository.find_by_dni(query)
            return [author] if author else []
        
        # Si parece ser un email, buscar por email exacto
        if self._looks_like_email(query):
            try:
                from ....domain.value_objects.email import Email
                author = self.author_repository.find_by_email(Email(query))
                return [author] if author else []
            except ValueError:
                # Si no es un email válido, continuar con búsqueda por nombre
                pass
        
        # Si parece ser un Scopus ID, buscar por Scopus ID
        if self._looks_like_scopus_id(query):
            try:
                from ....domain.value_objects.scopus_id import ScopusId
                author = self.author_repository.find_by_scopus_id(ScopusId(query))
                return [author] if author else []
            except ValueError:
                # Si no es un Scopus ID válido, continuar con búsqueda por nombre
                pass
        
        # Búsqueda por nombre
        return self.author_repository.search_by_name(query)
    
    def search_with_filters(self, filters: Dict[str, Any]) -> List[Author]:
        """
        Busca autores con filtros específicos.
        
        Args:
            filters: Diccionario con filtros:
                - name: str (opcional) - Búsqueda por nombre
                - department_id: int (opcional) - Filtrar por departamento
                - is_active: bool (opcional) - Filtrar por estado activo
                - has_scopus: bool (opcional) - Filtrar por tener cuenta Scopus
                
        Returns:
            List[Author]: Lista de autores filtrados
        """
        # Si hay búsqueda por nombre
        if 'name' in filters and filters['name']:
            authors = self.author_repository.search_by_name(filters['name'])
        else:
            authors = self.author_repository.find_all()
        
        # Aplicar filtros adicionales
        filtered_authors = []
        
        for author in authors:
            # Filtro por departamento
            if 'department_id' in filters and filters['department_id'] is not None:
                if author.department_id != filters['department_id']:
                    continue
            
            # Filtro por estado activo
            if 'is_active' in filters and filters['is_active'] is not None:
                if author.is_active != filters['is_active']:
                    continue
            
            # Filtro por tener cuenta Scopus
            if 'has_scopus' in filters and filters['has_scopus'] is not None:
                has_scopus = len(author.scopus_accounts) > 0
                if has_scopus != filters['has_scopus']:
                    continue
            
            filtered_authors.append(author)
        
        return filtered_authors
    
    def _looks_like_dni(self, query: str) -> bool:
        """Determina si la consulta parece ser un DNI."""
        # DNI típicamente son números entre 8 y 20 caracteres
        return query.isdigit() and 8 <= len(query) <= 20
    
    def _looks_like_email(self, query: str) -> bool:
        """Determina si la consulta parece ser un email."""
        return '@' in query and '.' in query
    
    def _looks_like_scopus_id(self, query: str) -> bool:
        """Determina si la consulta parece ser un Scopus ID."""
        # Scopus IDs típicamente son números de 10-11 dígitos
        return query.isdigit() and 10 <= len(query) <= 11