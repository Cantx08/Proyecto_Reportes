import asyncio
from typing import List
from backend.src.modules.publications.domain.subject_areas_repository import SubjectAreasRepository
from ...domain.repositories.scopus_account_repository import ScopusAccountRepository


class SubjectAreaService:
    """Servicio para manejo de áreas temáticas."""

    def __init__(
        self, 
        scopus_repository: SubjectAreasRepository, 
        mapping_repository: SubjectAreasRepository,
        scopus_account_repository: ScopusAccountRepository
    ):
        self._scopus_repository = scopus_repository  # Para obtener datos de Scopus
        self._mapping_repository = mapping_repository  # Para mapear usando CSV
        self._scopus_account_repository = scopus_account_repository

    async def _resolve_scopus_ids(self, mixed_ids: List[str]) -> List[str]:
        """
        Resuelve una lista mezclada de IDs (Scopus IDs o Author IDs) a solo Scopus IDs.
        
        Args:
            mixed_ids: Lista que puede contener Scopus IDs (numéricos) o Author IDs (cualquier formato)
            
        Returns:
            Lista de Scopus IDs únicos
        """
        scopus_ids = []
        
        for id_value in mixed_ids:
            # Si es numérico y tiene 11 dígitos, probablemente es un Scopus ID
            if id_value.isdigit() and len(id_value) == 11:
                scopus_ids.append(id_value)
            else:
                # Intentar buscar como Author ID en la base de datos
                try:
                    accounts = await self._scopus_account_repository.get_by_author_id(id_value)
                    for account in accounts:
                        if account.is_active:
                            scopus_ids.append(account.scopus_id)
                except Exception:
                    # Si no se encuentra, asumir que es un Scopus ID de todas formas
                    scopus_ids.append(id_value)
        
        # Retornar lista única de IDs
        return list(set(scopus_ids))

    async def get_subject_areas(self, mixed_ids: List[str]) -> List[str]:
        """
        Obtiene las áreas temáticas principales (generales) de múltiples autores.
        Mapea las subáreas específicas a áreas temáticas generales usando el CSV.
        
        Args:
            mixed_ids: Lista que puede contener Scopus IDs o Author IDs de la base de datos
        """
        # Resolver todos los IDs a Scopus IDs
        scopus_ids = await self._resolve_scopus_ids(mixed_ids)
        
        categories = set()

        # Obtener todas las subáreas específicas de Scopus
        async def fetch_author_areas(scopus_id):
            try:
                areas = await self._scopus_repository.get_subject_areas_by_author(scopus_id)
                return areas
            except Exception as e:
                print(f"Error obteniendo áreas para autor {scopus_id}: {e}")
                return []
            
        tasks = [fetch_author_areas(sid) for sid in scopus_ids]
        results = await asyncio.gather(*tasks)

        for areas_list in results:
            for area in areas_list:
                categories.add(area.name)
        
        # Mapear subáreas a áreas temáticas principales
        subject_areas = set()
        for category in categories:
            subject_area = self._mapping_repository.map_category_to_area(category)
            if subject_area:
                subject_areas.add(subject_area)

        return sorted(list(subject_areas))
