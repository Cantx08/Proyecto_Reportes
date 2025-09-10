"""
Generador principal de reportes PDF usando ReportLab.
"""
import io
from typing import List, Any
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from ..domain.interfaces import IReportGenerator, IContentBuilder
from ..domain.value_objects import DocenteInfo, ConfiguracionReporte, ColeccionesPublicaciones, EstadisticasPublicaciones


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


class ReportLabReportGenerator(IReportGenerator):
    """Generador de reportes PDF usando ReportLab."""
    
    def __init__(self, content_builder: IContentBuilder):
        self._content_builder = content_builder
    
    def generar_reporte(self, docente: DocenteInfo, config: ConfiguracionReporte,
                       publicaciones: ColeccionesPublicaciones, 
                       estadisticas: EstadisticasPublicaciones) -> bytes:
        """Genera el reporte completo en formato PDF."""
        buffer = io.BytesIO()
        doc = self._crear_documento(buffer)
        
        # Construir el contenido del documento
        story = self._construir_story(docente, config, publicaciones, estadisticas)
        
        # Construir PDF con numeración de páginas
        doc.build(story, canvasmaker=NumberedCanvas)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _crear_documento(self, buffer: io.BytesIO) -> SimpleDocTemplate:
        """Crea el documento PDF con configuración básica."""
        return SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
    
    def _construir_story(self, docente: DocenteInfo, config: ConfiguracionReporte,
                        publicaciones: ColeccionesPublicaciones, 
                        estadisticas: EstadisticasPublicaciones) -> List[Any]:
        """Construye la historia completa del documento."""
        story = []
        
        # Título principal
        story.extend(self._content_builder.construir_encabezado(docente, config))
        
        # Sección Resumen
        story.extend(self._content_builder.construir_resumen(docente, config, publicaciones))
        
        # Sección Informe Técnico
        story.extend(self._content_builder.construir_informe_tecnico(docente, publicaciones, estadisticas))
        
        # Sección Conclusión
        story.extend(self._content_builder.construir_conclusion(docente, config, publicaciones))
        
        # Firmas y tabla al final
        story.extend(self._content_builder.construir_firmas(config))
        
        return story
