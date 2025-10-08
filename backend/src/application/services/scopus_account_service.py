from typing import List, Optional
from ...domain.entities.scopus_account import ScopusAccount
from ...domain.repositories.scopus_account_repository import ScopusAccountRepository


class ScopusAccountService:
    """Servicio de aplicación para la gestión de cuentas Scopus."""
    
    def __init__(self, scopus_account_repository: ScopusAccountRepository):
        self._scopus_account_repository = scopus_account_repository
    
    async def get_account_by_scopus_id(self, scopus_id: str) -> Optional[ScopusAccount]:
        """Obtiene una cuenta Scopus por su ID de Scopus."""
        if not scopus_id:
            raise ValueError("Scopus ID is required")
        return await self._scopus_account_repository.get_by_scopus_id(scopus_id)
    
    async def get_accounts_by_author_id(self, author_id: str) -> List[ScopusAccount]:
        """Obtiene todas las cuentas Scopus de un autor."""
        if not author_id:
            raise ValueError("Author ID is required")
        return await self._scopus_account_repository.get_by_author_id(author_id)
    
    async def get_all_accounts(self) -> List[ScopusAccount]:
        """Obtiene todas las cuentas Scopus."""
        return await self._scopus_account_repository.get_all()
    
    async def create_account(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """Crea una nueva cuenta Scopus."""
        if not scopus_account.scopus_id:
            raise ValueError("Scopus ID is required")
        
        # Verificar que no exista ya
        existing_account = await self._scopus_account_repository.get_by_scopus_id(scopus_account.scopus_id)
        if existing_account:
            raise ValueError(f"Scopus account with ID {scopus_account.scopus_id} already exists")
        
        return await self._scopus_account_repository.create(scopus_account)
    
    async def update_account(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """Actualiza una cuenta Scopus existente."""
        if not scopus_account.scopus_id:
            raise ValueError("Scopus ID is required")
        
        # Verificar que existe
        existing_account = await self._scopus_account_repository.get_by_scopus_id(scopus_account.scopus_id)
        if not existing_account:
            raise ValueError(f"Scopus account with ID {scopus_account.scopus_id} not found")
        
        return await self._scopus_account_repository.update(scopus_account)
    
    async def delete_account(self, scopus_id: str) -> bool:
        """Elimina una cuenta Scopus por su ID de Scopus."""
        if not scopus_id:
            raise ValueError("Scopus ID is required")
        
        # Verificar que existe
        existing_account = await self._scopus_account_repository.get_by_scopus_id(scopus_id)
        if not existing_account:
            raise ValueError(f"Scopus account with ID {scopus_id} not found")
        
        return await self._scopus_account_repository.delete(scopus_id)
    
    async def delete_accounts_by_author_id(self, author_id: str) -> bool:
        """Elimina todas las cuentas Scopus de un autor."""
        if not author_id:
            raise ValueError("Author ID is required")
        
        # Verificar que el autor tiene cuentas
        accounts = await self._scopus_account_repository.get_by_author_id(author_id)
        if not accounts:
            raise ValueError(f"No Scopus accounts found for author {author_id}")
        
        return await self._scopus_account_repository.delete_by_author_id(author_id)
    
    async def link_author_to_scopus(self, author_id: str, scopus_ids: List[str]) -> tuple[List[ScopusAccount], List[str]]:
        """Vincula un autor con múltiples cuentas Scopus.
        
        Returns:
            tuple: (created_accounts, existing_scopus_ids)
        """
        if not author_id:
            raise ValueError("Author ID is required")
        if not scopus_ids:
            raise ValueError("At least one Scopus ID is required")
        
        created_accounts = []
        existing_scopus_ids = []
        
        for scopus_id in scopus_ids:
            try:
                # Verificar si ya existe
                existing_account = await self._scopus_account_repository.get_by_scopus_id(scopus_id)
                if existing_account and existing_account.author_id == author_id:
                    existing_scopus_ids.append(scopus_id)
                    continue
                
                account = ScopusAccount(
                    scopus_id=scopus_id,
                    scopus_user=f"user_{scopus_id}",
                    author_id=author_id
                )
                created_account = await self.create_account(account)
                created_accounts.append(created_account)
            except ValueError as e:
                # Si ya existe, continuar con el siguiente
                if "already exists" in str(e):
                    existing_scopus_ids.append(scopus_id)
                    continue
                raise e
        
        return created_accounts, existing_scopus_ids
    
    async def get_scopus_ids_by_author_id(self, author_id: str) -> List[str]:
        """Obtiene los IDs de Scopus asociados a un autor."""
        accounts = await self.get_accounts_by_author_id(author_id)
        return [account.scopus_id for account in accounts]