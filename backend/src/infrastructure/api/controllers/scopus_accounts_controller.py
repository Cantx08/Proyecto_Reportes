from fastapi import HTTPException
from ....application.services.scopus_account_service import ScopusAccountService
from ....domain.entities.scopus_account import ScopusAccount
from ....application.dto import (
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
                author_id=account.author_id,
                is_active=account.is_active
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
                    author_id=account.author_id,
                    is_active=account.is_active
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
                    author_id=account.author_id,
                    is_active=account.is_active
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
                author_id=account_create.author_id,
                is_active=account_create.is_active
            )
            
            created_account = await self.scopus_account_service.create_account(account)
            
            account_dto = ScopusAccountDTO(
                scopus_id=created_account.scopus_id,
                author_id=created_account.author_id,
                is_active=created_account.is_active
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
                author_id=account_update.author_id if account_update.author_id is not None else existing_account.author_id,
                is_active=account_update.is_active if account_update.is_active is not None else existing_account.is_active
            )
            
            result_account = await self.scopus_account_service.update_account(updated_account)
            
            account_dto = ScopusAccountDTO(
                scopus_id=result_account.scopus_id,
                author_id=result_account.author_id,
                is_active=result_account.is_active
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
            created_accounts, existing_scopus_ids = await self.scopus_account_service.link_author_to_scopus(
                link_data.author_id, 
                link_data.scopus_ids
            )
            
            # Obtener todas las cuentas del autor para retornar el estado completo
            all_accounts = await self.scopus_account_service.get_accounts_by_author_id(link_data.author_id)
            
            accounts_dto = [
                ScopusAccountDTO(
                    scopus_id=account.scopus_id,
                    author_id=account.author_id,
                    is_active=account.is_active
                )
                for account in all_accounts
            ]
            
            # Crear mensaje descriptivo
            message_parts = []
            if created_accounts:
                message_parts.append(f"Created {len(created_accounts)} new Scopus accounts")
            if existing_scopus_ids:
                message_parts.append(f"{len(existing_scopus_ids)} accounts already existed")
            
            message = ". ".join(message_parts) if message_parts else "No changes made"
            message += f" for author {link_data.author_id}"
            
            return ScopusAccountsResponseDTO(
                success=True,
                data=accounts_dto,
                message=message,
                total=len(accounts_dto)
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
    
    async def get_scopus_ids_by_author(self, author_id: str) -> dict:
        """Obtiene los ID de Scopus asociados a un autor."""
        try:
            scopus_ids = await self.scopus_account_service.get_scopus_ids_by_author_id(author_id)
            return {
                "success": True,
                "data": scopus_ids,
                "message": f"Found {len(scopus_ids)} Scopus IDs for author {author_id}",
                "total": len(scopus_ids)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e