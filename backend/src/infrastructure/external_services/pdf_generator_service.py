"""
Implementación del generador de PDF para reportes.
"""

import io
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from ...domain.interfaces.external_services import PDFGeneratorInterface


class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado con numeración de páginas."""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, page_state) in enumerate(self._saved_page_states):
            self.__dict__.update(page_state)
            self.draw_page_number(page_num + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_number(self, page_num, total_pages):
        """Dibuja el número de página en formato X/Y."""
        self.setFont("Helvetica", 9)
        self.drawRightString(
            A4[0] - 2*cm, 
            1*cm, 
            f"{page_num}/{total_pages}"
        )


class PDFGeneratorService(PDFGeneratorInterface):
    """Implementación del generador de PDF usando ReportLab."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para el PDF."""
        # Estilo para títulos principales
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        ))
        
        # Estilo para secciones
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20
        ))
        
        # Estilo para subsecciones
        self.styles.add(ParagraphStyle(
            name='SubSectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=10,
            spaceBefore=15
        ))
    
    def generate_report_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF del reporte con los datos proporcionados.
        
        Args:
            data: Datos del reporte incluyendo autor, publicaciones, estadísticas
            
        Returns:
            bytes: Contenido del PDF generado
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Construir el contenido del documento
        story = self._build_story(data)
        
        # Generar PDF con numeración de páginas
        doc.build(story, canvasmaker=NumberedCanvas)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Valida que los datos sean suficientes para generar el PDF.
        
        Args:
            data: Datos a validar
            
        Returns:
            bool: True si los datos son válidos
        """
        required_fields = ['author', 'publications', 'report_metadata']
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validar estructura del autor
        author = data.get('author', {})
        if not author.get('first_name') or not author.get('last_name'):
            return False
        
        # Validar que hay publicaciones
        publications = data.get('publications', [])
        if not isinstance(publications, list):
            return False
        
        return True
    
    def _build_story(self, data: Dict[str, Any]) -> list:
        """
        Construye el contenido completo del documento.
        
        Args:
            data: Datos del reporte
            
        Returns:
            list: Lista de elementos para ReportLab
        """
        story = []
        
        # Encabezado del reporte
        story.extend(self._build_header(data))
        
        # Información del autor
        story.extend(self._build_author_section(data.get('author', {})))
        
        # Resumen ejecutivo
        story.extend(self._build_summary_section(data))
        
        # Análisis de publicaciones
        story.extend(self._build_publications_section(data.get('publications', [])))
        
        # Estadísticas
        story.extend(self._build_statistics_section(data.get('statistics', {})))
        
        # Conclusiones
        story.extend(self._build_conclusions_section(data))
        
        return story
    
    def _build_header(self, data: Dict[str, Any]) -> list:
        """Construye el encabezado del reporte."""
        elements = []
        
        # Título principal
        metadata = data.get('report_metadata', {})
        title = metadata.get('title', 'Reporte de Publicaciones Científicas')
        elements.append(Paragraph(title, self.styles['MainTitle']))
        elements.append(Spacer(1, 20))
        
        # Fecha del reporte
        report_date = metadata.get('generated_date', 'Fecha no especificada')
        elements.append(Paragraph(f"Fecha del reporte: {report_date}", self.styles['Normal']))
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _build_author_section(self, author: Dict[str, Any]) -> list:
        """Construye la sección de información del autor."""
        elements = []
        
        elements.append(Paragraph("Información del Autor", self.styles['SectionHeader']))
        
        # Nombre completo
        first_name = author.get('first_name', '')
        last_name = author.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip()
        elements.append(Paragraph(f"<b>Nombre:</b> {full_name}", self.styles['Normal']))
        
        # Email si está disponible
        if author.get('email'):
            elements.append(Paragraph(f"<b>Email:</b> {author['email']}", self.styles['Normal']))
        
        # Departamento
        if author.get('department'):
            elements.append(Paragraph(f"<b>Departamento:</b> {author['department']}", self.styles['Normal']))
        
        # IDs de Scopus
        scopus_accounts = author.get('scopus_accounts', [])
        if scopus_accounts:
            scopus_ids = ', '.join([acc.get('scopus_id', '') for acc in scopus_accounts])
            elements.append(Paragraph(f"<b>IDs de Scopus:</b> {scopus_ids}", self.styles['Normal']))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_summary_section(self, data: Dict[str, Any]) -> list:
        """Construye la sección de resumen ejecutivo."""
        elements = []
        
        elements.append(Paragraph("Resumen Ejecutivo", self.styles['SectionHeader']))
        
        publications = data.get('publications', [])
        statistics = data.get('statistics', {})
        
        # Estadísticas básicas
        total_pubs = len(publications)
        total_citations = statistics.get('total_citations', 0)
        
        summary_text = f"""
        Este reporte presenta un análisis completo de la producción científica del autor.
        Se han identificado un total de <b>{total_pubs} publicaciones</b> con 
        <b>{total_citations} citaciones</b> acumuladas.
        """
        
        elements.append(Paragraph(summary_text, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_publications_section(self, publications: list) -> list:
        """Construye la sección de análisis de publicaciones."""
        elements = []
        
        elements.append(Paragraph("Análisis de Publicaciones", self.styles['SectionHeader']))
        
        if not publications:
            elements.append(Paragraph("No se encontraron publicaciones.", self.styles['Normal']))
            return elements
        
        # Agrupar por año
        publications_by_year = {}
        for pub in publications:
            year = pub.get('year', 'Sin año')
            if year not in publications_by_year:
                publications_by_year[year] = []
            publications_by_year[year].append(pub)
        
        # Mostrar por año (más reciente primero)
        sorted_years = sorted(publications_by_year.keys(), reverse=True)
        
        for year in sorted_years:
            elements.append(Paragraph(f"Publicaciones {year}", self.styles['SubSectionHeader']))
            
            year_pubs = publications_by_year[year]
            for i, pub in enumerate(year_pubs, 1):
                title = pub.get('title', 'Sin título')
                journal = pub.get('journal_name', 'Sin revista')
                citations = pub.get('citation_count', 0)
                
                pub_text = f"""
                {i}. <b>{title}</b><br/>
                Revista: {journal}<br/>
                Citaciones: {citations}
                """
                
                elements.append(Paragraph(pub_text, self.styles['Normal']))
                elements.append(Spacer(1, 10))
        
        return elements
    
    def _build_statistics_section(self, statistics: Dict[str, Any]) -> list:
        """Construye la sección de estadísticas."""
        elements = []
        
        elements.append(Paragraph("Estadísticas", self.styles['SectionHeader']))
        
        # Métricas principales
        metrics = [
            ('Total de publicaciones', statistics.get('total_publications', 0)),
            ('Total de citaciones', statistics.get('total_citations', 0)),
            ('Promedio de citaciones por publicación', statistics.get('avg_citations', 0)),
            ('Publicaciones Q1', statistics.get('q1_publications', 0)),
            ('Publicaciones Q2', statistics.get('q2_publications', 0)),
        ]
        
        for metric_name, value in metrics:
            elements.append(Paragraph(f"<b>{metric_name}:</b> {value}", self.styles['Normal']))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_conclusions_section(self, data: Dict[str, Any]) -> list:
        """Construye la sección de conclusiones."""
        elements = []
        
        elements.append(Paragraph("Conclusiones", self.styles['SectionHeader']))
        
        publications = data.get('publications', [])
        statistics = data.get('statistics', {})
        
        # Generar conclusiones automáticas basadas en los datos
        conclusions = []
        
        total_pubs = len(publications)
        if total_pubs > 0:
            conclusions.append(f"El autor ha demostrado una productividad científica significativa con {total_pubs} publicaciones.")
        
        total_citations = statistics.get('total_citations', 0)
        if total_citations > 0:
            avg_citations = total_citations / total_pubs if total_pubs > 0 else 0
            conclusions.append(f"Sus trabajos han recibido un total de {total_citations} citaciones, con un promedio de {avg_citations:.1f} citaciones por publicación.")
        
        q1_pubs = statistics.get('q1_publications', 0)
        if q1_pubs > 0:
            conclusions.append(f"Se destacan {q1_pubs} publicaciones en revistas Q1, indicando alta calidad en su investigación.")
        
        # Agregar conclusiones al documento
        for conclusion in conclusions:
            elements.append(Paragraph(f"• {conclusion}", self.styles['Normal']))
        
        elements.append(Spacer(1, 30))
        
        # Información de generación
        elements.append(Paragraph("Este reporte fue generado automáticamente por el Sistema de Análisis de Publicaciones Científicas.", self.styles['Normal']))
        
        return elements
