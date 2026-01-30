from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from pydantic import EmailStr

from .gender import Gender


@dataclass
class Author:
    """Entidad que representa un autor académico."""
    author_id: UUID
    first_name: str
    last_name: str
    institutional_email: EmailStr
    title: Optional[str]
    gender: Optional[Gender]
    job_position_id: UUID
    department_id: UUID
