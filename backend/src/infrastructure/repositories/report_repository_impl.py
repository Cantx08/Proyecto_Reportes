"""
Implementación del repositorio de reportes usando SQLAlchemy.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, asc

from ...domain.entities.report import Report
from ...domain.repositories.report_repository import ReportRepository
from ...domain.enums import ReportStatus, ReportType
from ..database.models import ReportModel, AuthorModel, ReportPublicationModel
from ..database.connection import db_config


class SQLAlchemyReportRepository(ReportRepository):
    """Implementación del repositorio de reportes usando SQLAlchemy."""
    
    def __init__(self, session: Optional[Session] = None):
        self._session = session
    
    @property
    def session(self) -> Session:
        """Obtiene la sesión de base de datos."""
        if self._session is None:
            self._session = db_config.get_session_sync()
        return self._session
    
    def save(self, report: Report) -> Report:
        """Guarda un reporte en la base de datos."""
        if report.id:
            # Actualizar existente
            existing = self.session.query(ReportModel).filter(
                ReportModel.id == report.id
            ).first()
            
            if existing:
                self._update_report_model(existing, report)
                report_model = existing
            else:
                raise ValueError(f"Report with id {report.id} not found")
        else:
            # Crear nuevo
            report_model = self._create_report_model(report)
            self.session.add(report_model)
        
        self.session.commit()
        self.session.refresh(report_model)
        
        return self._map_to_domain(report_model)
    
    def find_by_id(self, report_id: int) -> Optional[Report]:
        """Busca un reporte por ID."""
        report_model = self.session.query(ReportModel).options(
            joinedload(ReportModel.author),
            joinedload(ReportModel.publications)
        ).filter(ReportModel.id == report_id).first()
        
        if not report_model:
            return None
        
        return self._map_to_domain(report_model)
    
    def find_by_author(self, author_dni: str) -> List[Report]:
        """Busca reportes por autor."""
        report_models = self.session.query(ReportModel).join(AuthorModel).options(
            joinedload(ReportModel.author),
            joinedload(ReportModel.publications)
        ).filter(AuthorModel.dni == author_dni).all()
        
        return [self._map_to_domain(model) for model in report_models]
    
    def find_by_period(self, start_year: int, end_year: int) -> List[Report]:
        """Busca reportes por período."""
        report_models = self.session.query(ReportModel).options(
            joinedload(ReportModel.author),
            joinedload(ReportModel.publications)
        ).filter(
            and_(
                ReportModel.start_year <= end_year,
                ReportModel.end_year >= start_year
            )
        ).all()
        
        return [self._map_to_domain(model) for model in report_models]
    
    def find_by_status(self, status: ReportStatus) -> List[Report]:
        """Busca reportes por estado."""
        report_models = self.session.query(ReportModel).options(
            joinedload(ReportModel.author),
            joinedload(ReportModel.publications)
        ).filter(ReportModel.status == status.value).all()
        
        return [self._map_to_domain(model) for model in report_models]
    
    def find_by_type(self, report_type: ReportType) -> List[Report]:
        """Busca reportes por tipo."""
        report_models = self.session.query(ReportModel).options(
            joinedload(ReportModel.author),
            joinedload(ReportModel.publications)
        ).filter(ReportModel.type == report_type.value).all()
        
        return [self._map_to_domain(model) for model in report_models]
    
    def find_recent(self, limit: int = 10) -> List[Report]:
        """Busca los reportes más recientes."""
        report_models = self.session.query(ReportModel).options(
            joinedload(ReportModel.author),
            joinedload(ReportModel.publications)
        ).order_by(desc(ReportModel.created_at)).limit(limit).all()
        
        return [self._map_to_domain(model) for model in report_models]
    
    def find_with_filters(self, filters: Dict[str, Any]) -> List[Report]:
        """Busca reportes con filtros múltiples."""
        query = self.session.query(ReportModel).options(
            joinedload(ReportModel.author),
            joinedload(ReportModel.publications)
        )
        
        # Aplicar filtros
        if 'author_dni' in filters:
            query = query.join(AuthorModel).filter(AuthorModel.dni == filters['author_dni'])
        
        if 'status' in filters:
            query = query.filter(ReportModel.status == filters['status'])
        
        if 'type' in filters:
            query = query.filter(ReportModel.type == filters['type'])
        
        if 'start_year' in filters:
            query = query.filter(ReportModel.start_year >= filters['start_year'])
        
        if 'end_year' in filters:
            query = query.filter(ReportModel.end_year <= filters['end_year'])
        
        if 'created_after' in filters:
            query = query.filter(ReportModel.created_at >= filters['created_after'])
        
        if 'created_before' in filters:
            query = query.filter(ReportModel.created_at <= filters['created_before'])
        
        # Ordenar
        order_by = filters.get('order_by', 'created_at')
        order_dir = filters.get('order_dir', 'desc')
        
        if order_by == 'created_at':
            order_field = ReportModel.created_at
        elif order_by == 'title':
            order_field = ReportModel.title
        elif order_by == 'status':
            order_field = ReportModel.status
        else:
            order_field = ReportModel.created_at
        
        if order_dir == 'desc':
            query = query.order_by(desc(order_field))
        else:
            query = query.order_by(asc(order_field))
        
        # Aplicar límite si se especifica
        if 'limit' in filters:
            query = query.limit(filters['limit'])
        
        if 'offset' in filters:
            query = query.offset(filters['offset'])
        
        report_models = query.all()
        return [self._map_to_domain(model) for model in report_models]
    
    def find_all(self) -> List[Report]:
        """Obtiene todos los reportes."""
        report_models = self.session.query(ReportModel).options(
            joinedload(ReportModel.author),
            joinedload(ReportModel.publications)
        ).all()
        
        return [self._map_to_domain(model) for model in report_models]
    
    def delete(self, report_id: int) -> bool:
        """Elimina un reporte por ID."""
        report_model = self.session.query(ReportModel).filter(
            ReportModel.id == report_id
        ).first()
        
        if not report_model:
            return False
        
        self.session.delete(report_model)
        self.session.commit()
        return True
    
    def count_by_author(self, author_dni: str) -> int:
        """Cuenta los reportes de un autor."""
        return self.session.query(ReportModel).join(AuthorModel).filter(
            AuthorModel.dni == author_dni
        ).count()
    
    def count_by_status(self, status: ReportStatus) -> int:
        """Cuenta los reportes por estado."""
        return self.session.query(ReportModel).filter(
            ReportModel.status == status.value
        ).count()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales de reportes."""
        total_reports = self.session.query(ReportModel).count()
        
        # Contar por estado
        status_counts = {}
        for status in ReportStatus:
            count = self.session.query(ReportModel).filter(
                ReportModel.status == status.value
            ).count()
            status_counts[status.value] = count
        
        # Contar por tipo
        type_counts = {}
        for report_type in ReportType:
            count = self.session.query(ReportModel).filter(
                ReportModel.type == report_type.value
            ).count()
            type_counts[report_type.value] = count
        
        return {
            'total_reports': total_reports,
            'by_status': status_counts,
            'by_type': type_counts
        }
    
    def _create_report_model(self, report: Report) -> ReportModel:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""
        report_model = ReportModel(
            title=report.title,
            description=report.description,
            author_dni=report.author_dni,
            type=report.type.value,
            status=report.status.value,
            start_year=report.start_year,
            end_year=report.end_year,
            include_charts=report.include_charts,
            include_abstracts=report.include_abstracts,
            template_config=report.template_config,
            pdf_path=report.pdf_path,
            generated_at=report.generated_at,
            notes=report.notes,
            created_at=report.created_at,
            updated_at=report.updated_at
        )
        
        return report_model
    
    def _update_report_model(self, report_model: ReportModel, report: Report):
        """Actualiza un modelo existente con datos de la entidad de dominio."""
        report_model.title = report.title
        report_model.description = report.description
        report_model.type = report.type.value
        report_model.status = report.status.value
        report_model.start_year = report.start_year
        report_model.end_year = report.end_year
        report_model.include_charts = report.include_charts
        report_model.include_abstracts = report.include_abstracts
        report_model.template_config = report.template_config
        report_model.pdf_path = report.pdf_path
        report_model.generated_at = report.generated_at
        report_model.notes = report.notes
        report_model.updated_at = report.updated_at
    
    def _map_to_domain(self, report_model: ReportModel) -> Report:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""
        return Report(
            id=report_model.id,
            title=report_model.title,
            description=report_model.description,
            author_dni=report_model.author_dni,
            type=ReportType(report_model.type),
            status=ReportStatus(report_model.status),
            start_year=report_model.start_year,
            end_year=report_model.end_year,
            publication_ids=[pub.publication_id for pub in report_model.publications],
            include_charts=report_model.include_charts,
            include_abstracts=report_model.include_abstracts,
            template_config=report_model.template_config,
            pdf_path=report_model.pdf_path,
            generated_at=report_model.generated_at,
            notes=report_model.notes,
            created_at=report_model.created_at,
            updated_at=report_model.updated_at
        )