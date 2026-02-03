from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .scopus_publication_repository import ScopusPublicationRepository
from .sjr_file_repository import SJRFileRepository
from .db_publication_cache_repository import DBPublicationCacheRepository
from ..application.publication_dto import (
    PublicationResponseDTO, 
    AuthorPublicationsResponseDTO
)
from ..application.publication_service import PublicationService
from ...scopus_accounts.infrastructure.db_scopus_account_repository import DBScopusAccountRepository
from ....shared.database import get_db
from ....container import get_container

router = APIRouter(prefix="/publications", tags=["Publicaciones"])


def get_service(db: Session = Depends(get_db)) -> PublicationService:
    """
    Factory para crear el servicio de publicaciones con sus dependencias.
    """
    container = get_container()
    
    # Repositorio de publicaciones (Scopus API)
    publication_repo = ScopusPublicationRepository(
        api_key=container.settings.SCOPUS_API_KEY
    )
    
    # Repositorio de caché (base de datos)
    cache_repo = DBPublicationCacheRepository(db)
    
    # Repositorio SJR (archivo CSV)
    sjr_repo = SJRFileRepository(
        csv_path=container.settings.SJR_CSV_PATH
    )
    
    # Repositorio de cuentas Scopus (base de datos)
    scopus_account_repo = DBScopusAccountRepository(db)
    
    return PublicationService(
        publication_repo=publication_repo,
        cache_repo=cache_repo,
        sjr_repo=sjr_repo,
        scopus_account_repo=scopus_account_repo
    )


@router.get(
    "/author/{author_id}", 
    response_model=AuthorPublicationsResponseDTO,
    summary="Obtener publicaciones de un autor",
    description="""
    Obtiene todas las publicaciones de un autor desde sus cuentas Scopus asociadas.
    
    Las publicaciones incluyen:
    - Información básica (título, año, DOI, tipo de documento)
    - Filiación institucional al momento de la publicación
    - Áreas temáticas
    - Categorías con cuartiles SJR del año correspondiente
    
    **Estrategia de caché:** Las publicaciones se almacenan en BD por 24 horas.
    Use `refresh=true` para forzar actualización desde Scopus.
    
    Si el año de publicación es mayor al último disponible en el histórico SJR,
    se utiliza el último año disponible para las métricas.
    """
)
async def get_publications_by_author(
    author_id: UUID,
    refresh: bool = Query(False, description="Forzar actualización desde Scopus"),
    service: PublicationService = Depends(get_service)
):
    """Endpoint para obtener publicaciones de un autor por su ID del sistema."""
    try:
        return await service.get_publications_by_author(author_id, force_refresh=refresh)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener publicaciones: {str(e)}"
        )


@router.get(
    "/scopus/{scopus_id}",
    response_model=List[PublicationResponseDTO],
    summary="Obtener publicaciones por Scopus ID",
    description="""
    Obtiene las publicaciones directamente desde una cuenta Scopus específica.
    
    Útil para verificar publicaciones antes de asociar una cuenta Scopus a un autor.
    """
)
async def get_publications_by_scopus_id(
    scopus_id: str,
    service: PublicationService = Depends(get_service)
):
    """Endpoint para obtener publicaciones por Scopus ID directamente."""
    try:
        return await service.get_publications_by_scopus_id(scopus_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener publicaciones de Scopus: {str(e)}"
        )


@router.get(
    "/author/{author_id}/stats",
    summary="Obtener estadísticas de publicaciones",
    description="Obtiene estadísticas de publicaciones por año, tipo y cuartil."
)
async def get_publication_stats(
    author_id: UUID,
    service: PublicationService = Depends(get_service)
):
    """Endpoint para obtener estadísticas de un autor."""
    try:
        return await service.get_statistics_by_author(author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )
