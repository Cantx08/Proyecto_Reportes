import csv
import io
from typing import List, Dict
from uuid import UUID, uuid4

from fastapi import UploadFile

from .author_dto import AuthorResponseDTO, AuthorCreateDTO, AuthorUpdateDTO
from ..domain.author import Author
from ..domain.author_repository import IAuthorRepository
from ...departments.domain.department_repository import IDepartmentRepository
from ...job_positions.domain.job_position_repository import IJobPositionRepository


class AuthorService:
    """Servicio de aplicación para la gestión de autores."""

    def __init__(self, author_repo: IAuthorRepository, department_repo: IDepartmentRepository, position_repo: IJobPositionRepository):
        self.author_repo = author_repo
        self.department_repo = department_repo
        self.position_repo = position_repo

    async def get_all_authors(self) -> List[AuthorResponseDTO]:
        authors = await self.author_repo.get_all()
        return [AuthorResponseDTO.from_entity(author) for author in authors]

    async def get_authors_by_department(self, dep_code: str) -> List[AuthorResponseDTO]:
        if dep_code is None:
            raise ValueError("Se requiere las siglas del departamento.")

        authors = await self.author_repo.get_by_department(dep_code)
        return [AuthorResponseDTO.from_entity(author) for author in authors]

    async def get_author_by_id(self, author_id: UUID) -> AuthorResponseDTO:
        author = await self.author_repo.get_by_id(author_id)
        if not author:
            raise ValueError(f"El autor no fue encontrado.")
        return AuthorResponseDTO.from_entity(author)

    async def create_author(self, author: AuthorCreateDTO) -> AuthorResponseDTO:
        existing_author = await self.author_repo.get_by_email(author.institutional_email)
        if existing_author:
            raise ValueError(f"El correo ya fue asociado a otro autor.")
        new_author = Author(
            author_id=uuid4(),
            first_name=author.first_name,
            last_name=author.last_name,
            institutional_email=author.institutional_email,
            title=author.title,
            gender=author.gender,
            job_position_id=author.job_position_id,
            department_id=author.department_id
        )
        saved_author = await self.author_repo.create(new_author)
        return AuthorResponseDTO.from_entity(saved_author)

    async def update_author(self, researcher_id: UUID, author: AuthorUpdateDTO) -> AuthorResponseDTO:
        existing = await self.author_repo.get_by_id(researcher_id)
        if not existing:
            raise ValueError(f"El autor con ID {researcher_id} no existe.")

        updated_author = Author(
            author_id=researcher_id,
            first_name=author.first_name if author.first_name else existing.first_name,
            last_name=author.last_name if author.last_name else existing.last_name,
            institutional_email=existing.institutional_email,
            title=author.title if author.title else existing.title,
            gender=existing.gender,
            job_position_id=author.job_position_id if author.job_position_id else existing.job_position_id,
            department_id=author.department_id if author.department_id else existing.department_id
        )

        result = await self.author_repo.update(researcher_id, updated_author)

        return AuthorResponseDTO.from_entity(result)

    async def delete_author(self, author_id: UUID) -> bool:
        existing = await self.author_repo.get_by_id(author_id)
        if not existing:
            raise ValueError(f"El autor con ID {author_id} no existe.")

        return await self.author_repo.delete(author_id)

    async def import_authors_from_csv(self, file: UploadFile) -> dict:
        """
        Importa autores desde un archivo CSV.
        Espera columnas: first_name, last_name, email, title, gender, department_name, position_name
        """
        content = await file.read()

        # Detectar encoding (útil para tildes en español)
        try:
            decoded_content = content.decode('utf-8')
        except UnicodeDecodeError:
            decoded_content = content.decode('latin-1')

        # 1. PRE-CARGA (Caching): Traer todos los Departamentos y Cargos para mapear nombres a ID
        # Esto evita hacer 1 query por cada fila del CSV (N+1 problem)
        all_departments = await self.department_repo.get_all()
        all_positions = await self.position_repo.get_all()

        # Crear mapas de búsqueda rápida (Normalizamos a minúsculas para evitar errores de tipeo)
        # map: "nombre departamento" -> UUID
        dept_map: Dict[str, UUID] = {dept.dep_name.strip().lower(): dept.dep_id for dept in all_departments}
        # map: "siglas departamento" -> UUID (por si usan siglas en el CSV)
        dept_code_map: Dict[str, UUID] = {dept.dep_code.strip().lower(): dept.dep_id for dept in all_departments}

        # map: "nombre cargo" -> UUID
        pos_map: Dict[str, UUID] = {p.pos_name.strip().lower(): p.pos_id for p in all_positions}

        # 2. PROCESAR CSV
        csv_reader = csv.DictReader(io.StringIO(decoded_content), delimiter=',')
        # Si el delimitador falla (ej.: usa punto y coma), intentar detectar o forzar
        if not csv_reader.fieldnames or len(csv_reader.fieldnames) < 2:
            csv_reader = csv.DictReader(io.StringIO(decoded_content), delimiter=';')

        results = {"created": 0, "errors": []}
        row_idx = 1  # Para reportar errores

        for row in csv_reader:
            try:
                # Normalizar claves del CSV (quitar espacios extra en headers)
                row = {k.strip().lower().lstrip('\ufeff'): v.strip() for k, v in row.items() if k}

                # Extracción de datos básicos
                email = row.get('email') or row.get('institutional_email')
                if not email:
                    raise ValueError("Falta el correo electrónico")

                # Resolución de Departamento (Por nombre o siglas)
                dept_name_input = (row.get('department') or row.get('department_name') or "").strip().lower()
                dept_id = dept_map.get(dept_name_input) or dept_code_map.get(dept_name_input)

                if not dept_id:
                    results["errors"].append(
                        f"Fila {row_idx}: Departamento '{dept_name_input}' no existe en el sistema.")
                    row_idx += 1
                    continue

                # Resolución de Cargo
                pos_name_input = (row.get('position_name') or row.get('job_position_name') or "").strip().lower()
                pos_id = pos_map.get(pos_name_input)

                if not pos_id:
                    results["errors"].append(f"Fila {row_idx}: Cargo '{pos_name_input}' no existe en el sistema.")
                    row_idx += 1
                    continue

                # Verificar duplicado antes de intentar crear
                existing = await self.author_repo.get_by_email(email)
                if existing:
                    results["errors"].append(f"Fila {row_idx}: El autor con email {email} ya existe. Omitido.")
                    row_idx += 1
                    continue

                # Crear Objeto DTO
                author_dto = AuthorCreateDTO(
                    first_name=row.get('first_name', 'Unknown'),
                    last_name=row.get('last_name', 'Unknown'),
                    institutional_email=email,
                    title=row.get('title', ''),
                    gender=row.get('gender', 'Sin especificar'),
                    department_id=dept_id,
                    job_position_id=pos_id
                )

                # Se crea el author
                new_author = Author(
                    author_id=uuid4(),
                    first_name=author_dto.first_name,
                    last_name=author_dto.last_name,
                    institutional_email=author_dto.institutional_email,
                    title=author_dto.title,
                    gender=author_dto.gender,
                    job_position_id=author_dto.job_position_id,
                    department_id=author_dto.department_id
                )
                await self.author_repo.create(new_author)
                results["created"] += 1

            except Exception as e:
                results["errors"].append(f"Fila {row_idx}: Error inesperado - {str(e)}")

            row_idx += 1

        return results