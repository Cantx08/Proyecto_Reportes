"""
Router de publicaciones – flujo frontend-Scopus (IP institucional).

Ningún endpoint de este router llama a la API de Scopus.
El frontend obtiene los datos directamente desde Elsevier usando la IP
institucional del navegador y los envía aquí para transformación, SJR y caché.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .sjr_file_repository import SJRFileRepository
from .db_publication_cache_repository import DBPublicationCacheRepository
from ..application.publication_dto import (
    AuthorPublicationsResponseDTO,
    AuthorScopusStatusResponseDTO,
    PreviewPublicationsRequestDTO,
    ProcessAccountRequestDTO,
    ProcessAccountResponseDTO,
    PublicationResponseDTO,
)
from ..application.publication_service import PublicationService
from ...scopus_accounts.infrastructure.db_scopus_account_repository import DBScopusAccountRepository
from ....shared.database import get_db
from ....container import get_container

router = APIRouter(prefix="/publications", tags=["Publicaciones"])


# ---------------------------------------------------------------------------
# Factory – ya NO depende de repositorios Scopus
# ---------------------------------------------------------------------------

def get_service(db: Session = Depends(get_db)) -> PublicationService:
    """Factory para crear el servicio de publicaciones (sin Scopus)."""
    container = get_container()

    cache_repo = DBPublicationCacheRepository(db)
    sjr_repo = SJRFileRepository(csv_path=container.settings.SJR_CSV_PATH)
    scopus_account_repo = DBScopusAccountRepository(db)

    return PublicationService(
        cache_repo=cache_repo,
        sjr_repo=sjr_repo,
        scopus_account_repo=scopus_account_repo,
    )


# ---------------------------------------------------------------------------
# Endpoints – ninguno llama a la API de Scopus
# ---------------------------------------------------------------------------

@router.get(
    "/author/{author_id}/scopus-ids",
    response_model=AuthorScopusStatusResponseDTO,
    summary="Obtener cuentas Scopus del autor con estado de caché",
    description="""
    Devuelve las cuentas Scopus asociadas al autor junto con el estado de
    su caché (válida / expirada).

    **Este endpoint NO realiza ninguna llamada a la API de Scopus.**

    El frontend lo usa para saber:
    - Qué Scopus IDs debe consultar directamente usando la IP institucional.
    - Cuáles ya tienen datos en caché y no requieren re-consulta.
    """,
)
async def get_author_scopus_ids(
    author_id: UUID,
    service: PublicationService = Depends(get_service),
):
    """Devuelve cuentas Scopus del autor y estado de caché."""
    try:
        return await service.get_scopus_account_status(author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener cuentas Scopus: {str(e)}",
        )


@router.get(
    "/author/{author_id}/from-cache",
    response_model=AuthorPublicationsResponseDTO,
    summary="Obtener publicaciones del autor desde caché local",
    description="""
    Devuelve las publicaciones almacenadas en la base de datos local,
    fusionando y deduplicando todas las cuentas Scopus del autor.

    **No realiza ninguna llamada a la API de Scopus.**

    Úsalo después de que el frontend haya procesado las cuentas con
    ``POST /publications/process-account`` para obtener el resultado final
    consolidado.
    """,
)
async def get_cached_publications(
    author_id: UUID,
    service: PublicationService = Depends(get_service),
):
    """Devuelve publicaciones cacheadas del autor."""
    try:
        return await service.get_cached_publications_by_author(author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener publicaciones desde caché: {str(e)}",
        )


@router.get(
    "/author/{author_id}/stats",
    summary="Obtener estadísticas de publicaciones (desde caché)",
    description="""
    Obtiene estadísticas de publicaciones por año y tipo desde la caché local.

    **No realiza ninguna llamada a la API de Scopus.**
    """,
)
async def get_publication_stats(
    author_id: UUID,
    service: PublicationService = Depends(get_service),
):
    """Estadísticas del autor calculadas sobre la caché local."""
    try:
        return await service.get_statistics_by_author(author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas: {str(e)}",
        )


@router.post(
    "/process-account",
    response_model=ProcessAccountResponseDTO,
    summary="Procesar publicaciones crudas de Scopus",
    description="""
    Recibe datos crudos de la API de Scopus (obtenidos por el frontend con la
    IP institucional), los transforma, enriquece con datos SJR y los almacena
    en caché.

    **Flujo esperado:**
    1. Frontend obtiene ``scopus_ids`` vía ``GET /publications/author/{id}/scopus-ids``
    2. Frontend consulta ``https://api.elsevier.com/content/search/scopus?query=AU-ID({id})``
       directamente desde el navegador (IP institucional).
    3. Frontend envía las entradas crudas (``entry[]`` del JSON de Scopus) aquí.
    4. El backend aplica transformación de filiación, enriquecimiento SJR y caché.
    5. El frontend llama a ``GET /publications/author/{id}/from-cache`` para el
       resultado final consolidado.
    """,
)
async def process_account_publications(
    body: ProcessAccountRequestDTO,
    service: PublicationService = Depends(get_service),
):
    """Transforma datos crudos de Scopus, enriquece con SJR y guarda en caché."""
    try:
        account_uuid = UUID(body.account_id)
        publications = await service.process_account_publications(
            account_id=account_uuid,
            scopus_author_id=body.scopus_author_id,
            raw_publications=body.raw_publications,
        )
        return ProcessAccountResponseDTO(
            account_id=body.account_id,
            scopus_author_id=body.scopus_author_id,
            total_processed=len(publications),
            publications=[PublicationResponseDTO.from_entity(p) for p in publications],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar publicaciones: {str(e)}",
        )


@router.post(
    "/process-preview",
    response_model=List[PublicationResponseDTO],
    summary="Previsualizar publicaciones crudas de Scopus (sin caché)",
    description="""
    Recibe datos crudos de la API de Scopus, los transforma y enriquece
    con datos SJR, pero **NO los guarda en caché**.

    Útil para verificar publicaciones de un Scopus ID *antes* de asociar
    la cuenta a un autor en el sistema.

    **No realiza ninguna llamada a la API de Scopus.**
    """,
)
async def process_preview_publications(
    body: PreviewPublicationsRequestDTO,
    service: PublicationService = Depends(get_service),
):
    """Transforma + enriquece datos crudos de Scopus sin cachear."""
    try:
        publications = await service.process_raw_publications_preview(
            scopus_author_id=body.scopus_author_id,
            raw_publications=body.raw_publications,
        )
        return [PublicationResponseDTO.from_entity(p) for p in publications]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar publicaciones: {str(e)}",
        )