from typing import List
from fastapi import HTTPException
from ....application.services.scopus_account_service import ScopusAccountService
from ....domain.entities.scopus_account import ScopusAccount
from ....application.dtos import (
    ScopusAccountDTO, ScopusAccountCreateDTO, ScopusAccountUpdateDTO,
    ScopusAccountsResponseDTO, ScopusAccountResponseDTO, LinkAuthorScopusDTO
)


class ScopusAccountsController:
    """Controlador para manejar endpoints relacionados con cuentas Scopus."""
    
    def __init__(self, scopus_account_service: ScopusAccountService):
        self.scopus_account_service = scopus_account_service
    
    async def get_account_by_scopus_id(self, scopus_id: str) -> ScopusAccountResponseDTO:
        """Obtiene una cuenta Scopus por su ID de Scopus."""
        try:
            account = await self.scopus_account_service.get_account_by_scopus_id(scopus_id)
            if not account:
                return ScopusAccountResponseDTO(
                    success=False,
                    data=None,
                    message=f"Scopus account with ID {scopus_id} not found"
                )
            
            account_dto = ScopusAccountDTO(
                scopus_id=account.scopus_id,
                scopus_user=account.scopus_user,
                author_id=account.author_id
            )
            
            return ScopusAccountResponseDTO(
                success=True,
                data=account_dto,
                message="Scopus account retrieved successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
    
    async def get_accounts_by_author_id(self, author_id: str) -> ScopusAccountsResponseDTO:
        """Obtiene todas las cuentas Scopus de un autor."""
        try:
            accounts = await self.scopus_account_service.get_accounts_by_author_id(author_id)
            
            accounts_dto = [
                ScopusAccountDTO(
                    scopus_id=account.scopus_id,
                    scopus_user=account.scopus_user,
                    author_id=account.author_id
                )
                for account in accounts
            ]
            
            return ScopusAccountsResponseDTO(
                success=True,
                data=accounts_dto,
                message=f"Found {len(accounts)} Scopus accounts for author {author_id}",
                total=len(accounts)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
    
    async def get_all_accounts(self) -> ScopusAccountsResponseDTO:
        """Obtiene todas las cuentas Scopus."""
        try:
            accounts = await self.scopus_account_service.get_all_accounts()
            
            accounts_dto = [
                ScopusAccountDTO(
                    scopus_id=account.scopus_id,
                    scopus_user=account.scopus_user,
                    author_id=account.author_id
                )
                for account in accounts
            ]
            
            return ScopusAccountsResponseDTO(
                success=True,
                data=accounts_dto,
                message=f"Retrieved {len(accounts)} Scopus accounts successfully",
                total=len(accounts)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
    
    async def create_account(self, account_create: ScopusAccountCreateDTO) -> ScopusAccountResponseDTO:
        """Crea una nueva cuenta Scopus."""
        try:
            account = ScopusAccount(
                scopus_id=account_create.scopus_id,
                scopus_user=account_create.scopus_user,
                author_id=account_create.author_id
            )
            
            created_account = await self.scopus_account_service.create_account(account)
            
            account_dto = ScopusAccountDTO(
                scopus_id=created_account.scopus_id,
                scopus_user=created_account.scopus_user,
                author_id=created_account.author_id
            )
            
            return ScopusAccountResponseDTO(
                success=True,
                data=account_dto,
                message="Scopus account created successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
    
    async def update_account(self, scopus_id: str, account_update: ScopusAccountUpdateDTO) -> ScopusAccountResponseDTO:
        """Actualiza una cuenta Scopus existente."""
        try:
            # Obtener la cuenta actual
            existing_account = await self.scopus_account_service.get_account_by_scopus_id(scopus_id)
            if not existing_account:
                raise HTTPException(status_code=404, detail=f"Scopus account with ID {scopus_id} not found")
            
            # Actualizar solo los campos proporcionados
            updated_account = ScopusAccount(
                scopus_id=existing_account.scopus_id,
                scopus_user=account_update.scopus_user if account_update.scopus_user is not None else existing_account.scopus_user,
                author_id=account_update.author_id if account_update.author_id is not None else existing_account.author_id
            )
            
            result_account = await self.scopus_account_service.update_account(updated_account)
            
            account_dto = ScopusAccountDTO(
                scopus_id=result_account.scopus_id,
                scopus_user=result_account.scopus_user,
                author_id=result_account.author_id
            )
            
            return ScopusAccountResponseDTO(
                success=True,
                data=account_dto,
                message="Scopus account updated successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
    
    async def delete_account(self, scopus_id: str) -> ScopusAccountResponseDTO:
        """Elimina una cuenta Scopus por su ID de Scopus."""
        try:
            deleted = await self.scopus_account_service.delete_account(scopus_id)
            if not deleted:
                raise HTTPException(status_code=404, detail=f"Scopus account with ID {scopus_id} not found")
            
            return ScopusAccountResponseDTO(
                success=True,
                data=None,
                message="Scopus account deleted successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
    
    async def link_author_to_scopus(self, link_data: LinkAuthorScopusDTO) -> ScopusAccountsResponseDTO:
        """Vincula un autor con múltiples cuentas Scopus."""
        try:
            created_accounts = await self.scopus_account_service.link_author_to_scopus(
                link_data.author_id, 
                link_data.scopus_ids
            )
            
            accounts_dto = [
                ScopusAccountDTO(
                    scopus_id=account.scopus_id,
                    scopus_user=account.scopus_user,
                    author_id=account.author_id
                )
                for account in created_accounts
            ]
            
            return ScopusAccountsResponseDTO(
                success=True,
                data=accounts_dto,
                message=f"Successfully linked {len(created_accounts)} Scopus accounts to author {link_data.author_id}",
                total=len(created_accounts)
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
    
    async def get_scopus_ids_by_author(self, author_id: str) -> List[str]:
        """Obtiene los ID de Scopus asociados a un autor."""
        try:
            scopus_ids = await self.scopus_account_service.get_scopus_ids_by_author_id(author_id)
            return scopus_ids
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e