"""
Constructor de contenido para reportes PDF.
"""
import io
from typing import List, Any
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import cm
from reportlab.lib import colors

from ..domain.interfaces import IContentBuilder, IStyleManager, IChartGenerator, IPublicationFormatter
from ..domain.value_objects import DocenteInfo, ConfiguracionReporte, EstadisticasPublicaciones, ColeccionesPublicaciones, TipoFirmante


class ReportLabContentBuilder(IContentBuilder):
    """Constructor de contenido usando ReportLab."""
    
    def __init__(self, style_manager: IStyleManager, chart_generator: IChartGenerator, 
                 publication_formatter: IPublicationFormatter):
        self._style_manager = style_manager
        self._chart_generator = chart_generator
        self._publication_formatter = publication_formatter
    
    def construir_encabezado(self, docente: DocenteInfo, config: ConfiguracionReporte) -> List[Any]:
        """Construye el encabezado del documento."""
        elementos = []
        
        # Título principal con fecha
        titulo = f"Certificación de Publicaciones<br/><font size=10>{config.fecha}</font>"
        estilo_titulo = self._style_manager.obtener_estilo('MainTitle')
        elementos.append(Paragraph(titulo, estilo_titulo))
        
        # Información del docente
        autor_info = f"<b>{docente.nombre}</b><br/>{docente.departamento}<br/>Escuela Politécnica Nacional"
        estilo_normal = self._style_manager.obtener_estilo('Normal')
        elementos.append(Paragraph(autor_info, estilo_normal))
        elementos.append(Spacer(1, 20))
        
        return elementos
    
    def construir_resumen(self, docente: DocenteInfo, config: ConfiguracionReporte, 
                         publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la sección de resumen."""
        elementos = []
        
        # Subtítulo "RESUMEN"
        estilo_subtitulo = self._style_manager.obtener_estilo('SubTitle')
        elementos.append(Paragraph("<b>RESUMEN</b>", estilo_subtitulo))
        
        # Texto del resumen
        articulo = "del profesor" if docente.genero.value == "M" else "de la profesora"
        total_publicaciones = publicaciones.total_publicaciones()
        publicaciones_text = "las publicaciones" if total_publicaciones > 1 else "la publicación"
        
        if config.memorando:
            texto = f"El presente informe se realiza en base a la solicitud del memorando {config.memorando}, con la finalidad de certificar {publicaciones_text} {articulo} {docente.nombre}."
        else:
            texto = f"El presente informe se realiza con la finalidad de certificar {publicaciones_text} {articulo} {docente.nombre}."
        
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        elementos.append(Paragraph(texto, estilo_justificado))
        elementos.append(Spacer(1, 15))
        
        return elementos
    
    def construir_informe_tecnico(self, docente: DocenteInfo, 
                                 publicaciones: ColeccionesPublicaciones,
                                 estadisticas: EstadisticasPublicaciones) -> List[Any]:
        """Construye la sección de informe técnico."""
        elementos = []
        
        # Subtítulo "INFORME TÉCNICO"
        estilo_subtitulo = self._style_manager.obtener_estilo('SubTitle')
        elementos.append(Paragraph("<b>INFORME TÉCNICO</b>", estilo_subtitulo))
        
        # Introducción
        elementos.extend(self._construir_introduccion_informe(publicaciones))
        
        # Subsecciones
        if publicaciones.scopus:
            elementos.extend(self._construir_seccion_scopus(docente, publicaciones, estadisticas))
        
        if publicaciones.wos:
            elementos.extend(self._construir_seccion_wos(docente, publicaciones))
        
        if publicaciones.regionales:
            elementos.extend(self._construir_seccion_regionales(docente, publicaciones))
        
        if publicaciones.memorias:
            elementos.extend(self._construir_seccion_memorias(docente, publicaciones))
        
        if publicaciones.libros:
            elementos.extend(self._construir_seccion_libros(docente, publicaciones))
        
        return elementos
    
    def _construir_introduccion_informe(self, publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la introducción del informe técnico."""
        texto = "El presente informe se realiza en base a la información recopilada por la Dirección de Investigación"
        
        if publicaciones.scopus:
            texto += ", de la base de datos científicos Scopus"
            if publicaciones.regionales:
                texto += " y bases de datos indexadas"
        elif publicaciones.regionales:
            texto += ", de bases de datos indexadas"
        
        texto += "."
        
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        return [Paragraph(texto, estilo_justificado), Spacer(1, 20)]
    
    def _construir_seccion_scopus(self, docente: DocenteInfo, 
                                 publicaciones: ColeccionesPublicaciones,
                                 estadisticas: EstadisticasPublicaciones) -> List[Any]:
        """Construye la sección de publicaciones Scopus."""
        elementos = []
        
        estilo_subtitulo = self._style_manager.obtener_estilo('SubTitle')
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        
        elementos.append(Paragraph("Publicaciones Scopus", estilo_subtitulo))
        
        # Información del docente y estadísticas
        num_scopus = len(publicaciones.scopus)
        distribucion = self._publication_formatter.obtener_distribucion_tipos(publicaciones.scopus)
        
        texto_intro = f"{docente.obtener_articulo()} {docente.nombre}, es {docente.cargo} de la Escuela Politécnica Nacional y miembro del {docente.departamento}."
        elementos.append(Paragraph(texto_intro, estilo_justificado))
        elementos.append(Spacer(1, 10))
        
        if num_scopus > 1:
            texto_stats = f"Ha participado en un total de {num_scopus} publicaciones Scopus como {docente.obtener_autor_coautor()} de las mismas, distribuidas en {distribucion}. Tal como se detalla a continuación:"
        else:
            texto_stats = f"Ha participado en un total de {num_scopus} publicación Scopus como {docente.obtener_autor_coautor()} de la misma, siendo {distribucion}. Tal como se detalla a continuación:"
        
        elementos.append(Paragraph(texto_stats, estilo_justificado))
        elementos.append(Spacer(1, 15))
        
        # Lista de publicaciones
        elementos.extend(self._publication_formatter.formatear_lista_publicaciones(publicaciones.scopus, "Scopus"))
        
        # Gráfico solo para Scopus si hay datos suficientes
        if len(publicaciones.scopus) > 1 and estadisticas.tiene_suficientes_datos_para_grafico():
            elementos.extend(self._construir_grafico_tendencias(estadisticas, docente.nombre))
        
        # Áreas temáticas solo dentro de Scopus
        if estadisticas.areas_tematicas:
            elementos.append(Paragraph(
                f"<b>Áreas Temáticas de publicaciones Scopus del {docente.nombre}</b>",
                estilo_subtitulo
            ))
            elementos.extend(self._construir_areas_tematicas(docente, estadisticas))
        
        return elementos
    
    def _construir_grafico_tendencias(self, estadisticas: EstadisticasPublicaciones, docente_nombre: str) -> List[Any]:
        """Construye el gráfico de tendencias."""
        elementos = []
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        
        # Texto introductorio
        elementos.append(Paragraph(
            f"Adicionalmente, en la Figura 1 se muestra la tendencia por año de las publicaciones en Scopus del {docente_nombre}:",
            estilo_justificado
        ))
        elementos.append(Spacer(1, 15))
        
        # Generar gráfico
        chart_bytes = self._chart_generator.generar_grafico_tendencias(
            estadisticas.documentos_por_anio, docente_nombre)
        
        # Crear imagen
        img_buffer = io.BytesIO(chart_bytes)
        img = Image(img_buffer, width=15*cm, height=7.5*cm)
        elementos.append(img)
        elementos.append(Spacer(1, 10))
        
        # Caption centrado
        estilo_caption = self._style_manager.obtener_estilo('CaptionCenter')
        elementos.append(Paragraph(
            "<b>Figura 1.</b> Publicaciones Scopus por Año - Fuente web de Scopus.",
            estilo_caption
        ))
        elementos.append(Spacer(1, 20))
        
        return elementos
    
    def _construir_areas_tematicas(self, docente: DocenteInfo, estadisticas: EstadisticasPublicaciones) -> List[Any]:
        """Construye la sección de áreas temáticas."""
        elementos = []
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        estilo_publicacion = self._style_manager.obtener_estilo('Publication')
        
        num_areas = len(estadisticas.areas_tematicas)
        
        if num_areas > 1:
            texto = f"{docente.obtener_articulo()} {docente.nombre}, ha publicado en {num_areas} áreas temáticas, las cuales se detallan a continuación:"
        else:
            texto = f"{docente.obtener_articulo()} {docente.nombre}, ha publicado en {num_areas} área temática, la cual se detalla a continuación:"
        
        elementos.append(Paragraph(texto, estilo_justificado))
        elementos.append(Spacer(1, 10))
        
        # Lista de áreas temáticas
        for i, area in enumerate(estadisticas.areas_tematicas, 1):
            elementos.append(Paragraph(f"{i}. {area}", estilo_publicacion))
        
        elementos.append(Spacer(1, 15))
        return elementos
    
    def _construir_seccion_wos(self, docente: DocenteInfo, publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la sección de publicaciones Web of Science."""
        elementos = []
        estilo_subtitulo = self._style_manager.obtener_estilo('SubTitle')
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        
        elementos.append(Paragraph("Publicaciones Web of Science", estilo_subtitulo))
        
        num_wos = len(publicaciones.wos)
        distribucion = self._publication_formatter.obtener_distribucion_tipos(publicaciones.wos)
        
        if num_wos > 1:
            texto = f"Ha participado en un total de {num_wos} publicaciones indexadas en la Web of Science Core Collection como {docente.obtener_autor_coautor()} de las mismas, distribuidas en {distribucion}. Tal como se detalla a continuación:"
        else:
            texto = f"Ha participado en un total de {num_wos} publicación indexada en la Web of Science Core Collection como {docente.obtener_autor_coautor()} de la misma, siendo {distribucion}. Tal como se detalla a continuación:"
        
        elementos.append(Paragraph(texto, estilo_justificado))
        elementos.append(Spacer(1, 15))
        
        # Lista de publicaciones
        elementos.extend(self._publication_formatter.formatear_lista_publicaciones(publicaciones.wos, "Web of Science"))
        
        return elementos
    
    def _construir_seccion_regionales(self, docente: DocenteInfo, publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la sección de otras indexaciones."""
        elementos = []
        estilo_subtitulo = self._style_manager.obtener_estilo('SubTitle')
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        
        elementos.append(Paragraph("Otras Indexaciones", estilo_subtitulo))
        
        num_regionales = len(publicaciones.regionales)
        
        if num_regionales > 1:
            texto = f"{docente.obtener_articulo()} {docente.nombre}, cuenta con {num_regionales} indexaciones, como se detallan a continuación:"
        else:
            texto = f"{docente.obtener_articulo()} {docente.nombre}, cuenta con {num_regionales} artículo indexado, como se detalla a continuación:"
        
        elementos.append(Paragraph(texto, estilo_justificado))
        elementos.append(Spacer(1, 15))
        
        # Lista de publicaciones
        elementos.extend(self._publication_formatter.formatear_lista_publicaciones(publicaciones.regionales, "Regional"))
        
        return elementos
    
    def _construir_seccion_memorias(self, docente: DocenteInfo, publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la sección de memorias de eventos científicos."""
        elementos = []
        estilo_subtitulo = self._style_manager.obtener_estilo('SubTitle')
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        
        elementos.append(Paragraph("Memorias de Eventos Científicos", estilo_subtitulo))
        
        num_memorias = len(publicaciones.memorias)
        
        if num_memorias > 1:
            texto = f"{docente.obtener_articulo()} {docente.nombre}, cuenta con {num_memorias} publicaciones en memorias de eventos científicos, como se detallan a continuación:"
        else:
            texto = f"{docente.obtener_articulo()} {docente.nombre}, cuenta con {num_memorias} publicación en memorias de eventos científicos, como se detalla a continuación:"
        
        elementos.append(Paragraph(texto, estilo_justificado))
        elementos.append(Spacer(1, 15))
        
        # Lista de publicaciones
        elementos.extend(self._publication_formatter.formatear_lista_publicaciones(publicaciones.memorias, "Memorias"))
        
        return elementos
    
    def _construir_seccion_libros(self, docente: DocenteInfo, publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la sección de libros y capítulos de libros."""
        elementos = []
        estilo_subtitulo = self._style_manager.obtener_estilo('SubTitle')
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        
        elementos.append(Paragraph("Libros y Capítulos de Libros", estilo_subtitulo))
        
        num_libros = len(publicaciones.libros)
        
        if num_libros > 1:
            texto = f"{docente.obtener_articulo()} {docente.nombre}, cuenta con {num_libros} publicaciones en Libros y Capítulos de Libros, como se detallan a continuación:"
        else:
            texto = f"{docente.obtener_articulo()} {docente.nombre}, cuenta con {num_libros} publicación en Libros y Capítulos de Libros, como se detalla a continuación:"
        
        elementos.append(Paragraph(texto, estilo_justificado))
        elementos.append(Spacer(1, 15))
        
        # Lista de publicaciones
        elementos.extend(self._publication_formatter.formatear_lista_publicaciones(publicaciones.libros, "Libros"))
        
        return elementos
    
    def construir_conclusion(self, docente: DocenteInfo, config: ConfiguracionReporte,
                           publicaciones: ColeccionesPublicaciones) -> List[Any]:
        """Construye la sección de conclusión."""
        elementos = []
        estilo_subtitulo = self._style_manager.obtener_estilo('SubTitle')
        estilo_justificado = self._style_manager.obtener_estilo('Justified')
        
        elementos.append(Paragraph("Conclusión", estilo_subtitulo))
        
        articulo = "el" if docente.genero.value == "M" else "la"
        total_pubs = publicaciones.total_publicaciones()
        
        if config.firmante == TipoFirmante.DIRECTORA_INVESTIGACION:
            entidad = "la Dirección de Investigación"
        else:
            entidad = "el Vicerrectorado de Investigación, Innovación y Vinculación"
        
        texto_conclusion = f"Por los antecedentes expuestos, {entidad} de la Institución, certifica que {articulo} {docente.nombre}, cuenta con un total de {total_pubs} "
        
        if total_pubs > 1:
            texto_conclusion += "publicaciones."
        else:
            texto_conclusion += "publicación."
        
        elementos.append(Paragraph(texto_conclusion, estilo_justificado))
        elementos.append(Spacer(1, 15))
        
        texto_uso = f"{articulo.capitalize()} {docente.nombre} puede hacer uso del presente certificado para lo que considere necesario."
        elementos.append(Paragraph(texto_uso, estilo_justificado))
        
        return elementos
    
    def construir_firmas(self, config: ConfiguracionReporte) -> List[Any]:
        """Construye la sección de firmas."""
        elementos = []
        
        # Espaciado antes de las firmas
        elementos.append(Spacer(1, 40))
        
        # Información del firmante
        if config.firmante == TipoFirmante.DIRECTORA_INVESTIGACION:
            nombre_firmante = "Dra. María Monserrate Intriago Pazmiño"
            cargo_firmante = "DIRECTORA DE INVESTIGACIÓN DE LA ESCUELA POLITÉCNICA NACIONAL"
        else:
            nombre_firmante = "Dr. Marco Oswaldo Santórum Gaibor"
            cargo_firmante = "VICERRECTOR DE INVESTIGACIÓN, INNOVACIÓN Y VINCULACIÓN DE LA ESCUELA POLITÉCNICA NACIONAL"
        
        estilo_firma = self._style_manager.obtener_estilo('Firma')
        elementos.append(Paragraph(f"<b>{nombre_firmante}</b>", estilo_firma))
        elementos.append(Paragraph(f"<b>{cargo_firmante}</b>", estilo_firma))
        elementos.append(Spacer(1, 10))
        
        # Tabla de elaboración
        estilo_tabla = self._style_manager.obtener_estilo('TablaElaboracion')
        datos_tabla = [
            [Paragraph("Elaborado por:", estilo_tabla), Paragraph("M. Vásquez", estilo_tabla)]
        ]
        tabla = Table(datos_tabla, colWidths=[3*cm, 3*cm])
        tabla.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        elementos.append(tabla)
        return elementos
