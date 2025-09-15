"""
Manejador de estilos para documentos PDF.
"""
from typing import Any
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors

from ..domain.interfaces import IStyleManager


class ReportLabStyleManager(IStyleManager):
    """Implementación de manejador de estilos usando ReportLab."""
    
    def __init__(self):
        self._styles = getSampleStyleSheet()
        self.configurar_estilos_personalizados()
    
    def obtener_estilo(self, nombre: str) -> Any:
        """Obtiene un estilo por nombre."""
        return self._styles[nombre]
    
    def configurar_estilos_personalizados(self) -> None:
        """Configura estilos personalizados para el documento."""
        self._crear_estilo_titulo_principal()
        self._crear_estilo_subtitulo()
        self._crear_estilo_texto_justificado()
        self._crear_estilo_publicaciones()
        self._crear_estilo_caption_centrado()
        self._crear_estilo_firma()
        self._crear_estilo_tabla_elaboracion()
    
    def _crear_estilo_titulo_principal(self) -> None:
        """Crea el estilo para el título principal."""
        self._styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self._styles['Title'],
            fontSize=20,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        ))
    
    def _crear_estilo_subtitulo(self) -> None:
        """Crea el estilo para subtítulos."""
        self._styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self._styles['Heading2'],
            fontSize=12,
            spaceAfter=10,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
    
    def _crear_estilo_texto_justificado(self) -> None:
        """Crea el estilo para texto justificado."""
        self._styles.add(ParagraphStyle(
            name='Justified',
            parent=self._styles['Normal'],
            fontSize=12,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            fontName='Times-Roman'
        ))
    
    def _crear_estilo_publicaciones(self) -> None:
        """Crea el estilo para publicaciones."""
        self._styles.add(ParagraphStyle(
            name='Publication',
            parent=self._styles['Normal'],
            fontSize=12,
            leftIndent=20,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Times-Roman'
        ))
    
    def _crear_estilo_caption_centrado(self) -> None:
        """Crea el estilo para captions centrados."""
        self._styles.add(ParagraphStyle(
            name='CaptionCenter',
            parent=self._styles['Normal'],
            alignment=TA_CENTER,
            fontSize=10,
            textColor=colors.black,
            fontName='Times-Roman'
        ))
    
    def _crear_estilo_firma(self) -> None:
        """Crea el estilo para firmas."""
        self._styles.add(ParagraphStyle(
            name='Firma',
            parent=self._styles['Normal'],
            fontSize=12,
            alignment=TA_LEFT,
            fontName='Times-Roman',
            textColor=colors.black
        ))
    
    def _crear_estilo_tabla_elaboracion(self) -> None:
        """Crea el estilo para la tabla de elaboración."""
        self._styles.add(ParagraphStyle(
            name='TablaElaboracion',
            parent=self._styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            fontName='Times-Roman',
            textColor=colors.black
        ))
