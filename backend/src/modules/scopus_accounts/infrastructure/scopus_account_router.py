from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .db_scopus_account_repository import DBScopusAccountRepository
from ..application.scopus_account_dto import ScopusAccountResponseDTO, ScopusAccountCreateDTO
from ..application.scopus_account_service import ScopusAccountService
from ....shared.database import get_db

router = APIRouter(prefix="/scopus-accounts", tags=["Cuentas Scopus"])


def get_service(db: Session = Depends(get_db)):
    return ScopusAccountService(DBScopusAccountRepository(db))


@router.get("/author/{author_id}", response_model=List[ScopusAccountResponseDTO])
async def get_scopus_accounts_by_author(author_id: UUID, service: ScopusAccountService = Depends(get_service)):
    return await service.get_accounts_by_author(author_id)

@router.get("/{scopus_id}", response_model=ScopusAccountResponseDTO)
async def get_account_by_scopus_id(scopus_id: str, service: ScopusAccountService = Depends(get_service)):
    try:
        return await service.get_account_by_scopus_id(scopus_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("", response_model=ScopusAccountResponseDTO)
async def add_scopus_account(dto: ScopusAccountCreateDTO, service: ScopusAccountService = Depends(get_service)):
    try:
        return await service.create_account(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=404, detail="El autor especificado no fue encontrado.")


@router.delete("/{account_id}")
async def delete_scopus_account(account_id: UUID, service: ScopusAccountService = Depends(get_service)):
    deleted = await service.delete_account(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cuenta Scopus no encontrada.")
    return {"message": "Cuenta Scopus eliminada exitosamente."}
