"""
Caso de uso para crear un nuevo autor.
"""

from typing import Dict, Any
from datetime import datetime

from ....domain.entities.author import Author
from ....domain.entities.scopus_account import ScopusAccount
from ....domain.repositories.author_repository import AuthorRepository
from ....domain.value_objects.email import Email
from ....domain.value_objects.scopus_id import ScopusId
from ....domain.exceptions.author_exceptions import (
    AuthorAlreadyExistsException,
    InvalidAuthorDataException
)


class CreateAuthorUseCase:
    """Caso de uso para crear un nuevo autor."""
    
    def __init__(self, author_repository: AuthorRepository):
        self.author_repository = author_repository
    
    def execute(self, author_data: Dict[str, Any]) -> Author:
        """
        Ejecuta el caso de uso para crear un autor.
        
        Args:
            author_data: Diccionario con los datos del autor
                - dni: str
                - first_name: str
                - last_name: str
                - email: str
                - department_id: int
                - scopus_accounts: List[Dict] (opcional)
        
        Returns:
            Author: El autor creado
            
        Raises:
            AuthorAlreadyExistsException: Si el autor ya existe
            InvalidAuthorDataException: Si los datos son inválidos
        """
        # Validar datos requeridos
        self._validate_author_data(author_data)
        
        # Verificar que no exista un autor con el mismo DNI
        dni = author_data['dni']
        existing_author = self.author_repository.find_by_dni(dni)
        if existing_author:
            raise AuthorAlreadyExistsException(f"Author with DNI {dni} already exists")
        
        # Verificar que no exista un autor con el mismo email
        email_str = author_data['email']
        existing_author_by_email = self.author_repository.find_by_email(Email(email_str))
        if existing_author_by_email:
            raise AuthorAlreadyExistsException(f"Author with email {email_str} already exists")
        
        # Crear cuentas de Scopus si se proporcionan
        scopus_accounts = []
        if 'scopus_accounts' in author_data and author_data['scopus_accounts']:
            scopus_accounts = self._create_scopus_accounts(author_data['scopus_accounts'])
        
        # Crear la entidad Author
        author = Author(
            dni=dni,
            first_name=author_data['first_name'],
            last_name=author_data['last_name'],
            email=Email(email_str),
            department_id=author_data['department_id'],
            scopus_accounts=scopus_accounts,
            is_active=author_data.get('is_active', True),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Guardar en el repositorio
        return self.author_repository.save(author)
    
    def _validate_author_data(self, author_data: Dict[str, Any]) -> None:
        """
        Valida los datos del autor.
        
        Args:
            author_data: Datos del autor a validar
            
        Raises:
            InvalidAuthorDataException: Si algún dato es inválido
        """
        required_fields = ['dni', 'first_name', 'last_name', 'email', 'department_id']
        
        # Verificar campos requeridos
        for field in required_fields:
            if field not in author_data or not author_data[field]:
                raise InvalidAuthorDataException(f"Field '{field}' is required")
        
        # Validar DNI
        dni = author_data['dni'].strip()
        if len(dni) < 8 or len(dni) > 20:
            raise InvalidAuthorDataException("DNI must be between 8 and 20 characters")
        
        # Validar nombres
        first_name = author_data['first_name'].strip()
        last_name = author_data['last_name'].strip()
        
        if len(first_name) < 2 or len(first_name) > 100:
            raise InvalidAuthorDataException("First name must be between 2 and 100 characters")
        
        if len(last_name) < 2 or len(last_name) > 100:
            raise InvalidAuthorDataException("Last name must be between 2 and 100 characters")
        
        # Validar email
        try:
            Email(author_data['email'])
        except ValueError as e:
            raise InvalidAuthorDataException(f"Invalid email: {str(e)}")
        
        # Validar department_id
        try:
            department_id = int(author_data['department_id'])
            if department_id <= 0:
                raise InvalidAuthorDataException("Department ID must be a positive integer")
        except (ValueError, TypeError):
            raise InvalidAuthorDataException("Department ID must be a valid integer")
        
        # Validar cuentas de Scopus si se proporcionan
        if 'scopus_accounts' in author_data and author_data['scopus_accounts']:
            self._validate_scopus_accounts(author_data['scopus_accounts'])
    
    def _validate_scopus_accounts(self, scopus_accounts_data: list) -> None:
        """
        Valida los datos de las cuentas de Scopus.
        
        Args:
            scopus_accounts_data: Lista de datos de cuentas de Scopus
            
        Raises:
            InvalidAuthorDataException: Si algún dato es inválido
        """
        if not isinstance(scopus_accounts_data, list):
            raise InvalidAuthorDataException("Scopus accounts must be a list")
        
        primary_count = 0
        scopus_ids = set()
        
        for i, account_data in enumerate(scopus_accounts_data):
            if not isinstance(account_data, dict):
                raise InvalidAuthorDataException(f"Scopus account {i} must be a dictionary")
            
            if 'scopus_id' not in account_data:
                raise InvalidAuthorDataException(f"Scopus account {i} must have 'scopus_id'")
            
            # Validar Scopus ID
            try:
                scopus_id = ScopusId(account_data['scopus_id'])
                scopus_id_str = str(scopus_id)
            except ValueError as e:
                raise InvalidAuthorDataException(f"Invalid Scopus ID in account {i}: {str(e)}")
            
            # Verificar duplicados
            if scopus_id_str in scopus_ids:
                raise InvalidAuthorDataException(f"Duplicate Scopus ID: {scopus_id_str}")
            scopus_ids.add(scopus_id_str)
            
            # Contar cuentas primarias
            if account_data.get('is_primary', False):
                primary_count += 1
        
        # Debe haber exactamente una cuenta primaria
        if len(scopus_accounts_data) > 0 and primary_count != 1:
            raise InvalidAuthorDataException("Exactly one Scopus account must be marked as primary")
    
    def _create_scopus_accounts(self, scopus_accounts_data: list) -> list:
        """
        Crea las entidades ScopusAccount a partir de los datos.
        
        Args:
            scopus_accounts_data: Lista de datos de cuentas de Scopus
            
        Returns:
            List[ScopusAccount]: Lista de cuentas de Scopus creadas
        """
        scopus_accounts = []
        
        for account_data in scopus_accounts_data:
            # Verificar que no exista otra cuenta con el mismo Scopus ID
            scopus_id = ScopusId(account_data['scopus_id'])
            existing_author = self.author_repository.find_by_scopus_id(scopus_id)
            if existing_author:
                raise AuthorAlreadyExistsException(
                    f"Scopus ID {scopus_id} is already associated with author {existing_author.dni}"
                )
            
            account = ScopusAccount(
                scopus_id=scopus_id,
                is_primary=account_data.get('is_primary', False),
                is_active=account_data.get('is_active', True),
                verified_at=account_data.get('verified_at'),
                created_at=datetime.now()
            )
            scopus_accounts.append(account)
        
        return scopus_accounts