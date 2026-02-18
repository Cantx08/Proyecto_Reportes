"""Servicio para obtener áreas temáticas de un autor desde Scopus Author Retrieval."""

import asyncio
import logging
from typing import List
from uuid import UUID

from ..domain.author_subject_area_repository import IAuthorSubjectAreaRepository
from ...scopus_accounts.domain.scopus_account_repository import IScopusAccountRepository

logger = logging.getLogger(__name__)


class SubjectAreaService:
    """
    Servicio para obtener las áreas temáticas de un autor.
    
    Flujo:
    1. Recibe el ID interno del autor (UUID).
    2. Busca todas sus cuentas Scopus (scopus_id).
    3. Consulta la API de Author Retrieval para cada scopus_id.
    4. Fusiona las áreas temáticas eliminando duplicados.
    """

    def __init__(
        self,
        author_sa_repo: IAuthorSubjectAreaRepository,
        scopus_account_repo: IScopusAccountRepository
    ):
        self._author_sa_repo = author_sa_repo
        self._scopus_account_repo = scopus_account_repo

    async def get_subject_areas_by_author(self, author_id: UUID) -> List[str]:
        """
        Obtiene las áreas temáticas fusionadas de todas las cuentas Scopus de un autor.
        
        Args:
            author_id: UUID del autor en el sistema
            
        Returns:
            Lista ordenada de áreas temáticas únicas
            
        Raises:
            ValueError: Si el autor no tiene cuentas Scopus asociadas
        """
        # 1. Buscar cuentas Scopus del autor
        scopus_accounts = await self._scopus_account_repo.get_by_author(author_id)

        if not scopus_accounts:
            logger.warning("Autor %s no tiene cuentas Scopus asociadas", author_id)
            raise ValueError("El autor no tiene cuentas Scopus asociadas.")

        scopus_ids = [account.scopus_id for account in scopus_accounts]
        logger.info(
            "Obteniendo subject areas para autor %s con %d cuenta(s) Scopus",
            author_id, len(scopus_ids)
        )

        # 2. Consultar Author Retrieval para cada cuenta en paralelo
        tasks = [
            self._author_sa_repo.get_subject_areas_by_scopus_id(sid)
            for sid in scopus_ids
        ]
        results = await asyncio.gather(*tasks)

        # 3. Fusionar eliminando duplicados
        merged_areas: set[str] = set()
        for areas_list in results:
            for area in areas_list:
                merged_areas.add(area)

        sorted_areas = sorted(merged_areas)
        logger.info(
            "Autor %s: %d áreas temáticas únicas obtenidas de %d cuentas",
            author_id, len(sorted_areas), len(scopus_ids)
        )

        return sorted_areas

    async def get_subject_areas_by_scopus_id(self, scopus_id: str) -> List[str]:
        """
        Obtiene las áreas temáticas de una sola cuenta Scopus.
        
        Args:
            scopus_id: ID del autor en Scopus
            
        Returns:
            Lista ordenada de áreas temáticas
        """
        areas = await self._author_sa_repo.get_subject_areas_by_scopus_id(scopus_id)
        return sorted(set(areas))

