"""
Formateador de publicaciones para reportes.
"""
from typing import List, Any
from reportlab.platypus import Paragraph, Spacer

from ..domain.entities import Publicacion
from ..domain.interfaces import IPublicationFormatter, IStyleManager


class ReportLabPublicationFormatter(IPublicationFormatter):
    """Implementación de formateador de publicaciones usando ReportLab."""
    
    def __init__(self, style_manager: IStyleManager):
        self._style_manager = style_manager
    
    def formatear_lista_publicaciones(self, publicaciones: List[Publicacion], tipo: str) -> List[Any]:
        """Formatea una lista de publicaciones."""
        elementos = []
        
        for i, pub in enumerate(publicaciones, 1):
            texto_pub = self._construir_texto_publicacion(pub, i, tipo)
            
            estilo_publicacion = self._style_manager.obtener_estilo('Publication')
            elementos.append(Paragraph(texto_pub, estilo_publicacion))
        
        elementos.append(Spacer(1, 15))
        return elementos
    
    def _construir_texto_publicacion(self, pub: Publicacion, numero: int, tipo: str) -> str:
        """Construye el texto formateado de una publicación."""
        texto_pub = f"{numero}. ({pub.anio}) \"{pub.titulo}\". {pub.fuente}."
        
        # Agregar información de categorías e indexación
        if pub.categorias:
            categorias_str = self._formatear_categorias(pub.categorias)
            tipo_formato = "SCOPUS" if tipo == "Scopus" else tipo
            texto_pub += f" <b>Indexada en {tipo_formato} - {categorias_str}</b>."
        else:
            tipo_formato = "SCOPUS" if tipo == "Scopus" else tipo
            texto_pub += f" <b>Indexada en {tipo_formato}</b>."
        
        # Agregar DOI si existe
        if pub.doi:
            texto_pub += f" DOI: {pub.doi}"
        
        # Agregar indicación de filiación si no es EPN
        if pub.filiacion and "escuela politécnica nacional" not in pub.filiacion.lower():
            texto_pub += " <u>(Sin Filiación)</u>"
        
        return texto_pub
    
    def _formatear_categorias(self, categorias: Any) -> str:
        """Formatea las categorías de una publicación."""
        if isinstance(categorias, str):
            return categorias
        elif isinstance(categorias, list) and len(categorias) > 0:
            if len(categorias[0]) > 1:
                return "; ".join(categorias)
            else:
                return "".join(categorias)
        else:
            return str(categorias)
    
    def obtener_distribucion_tipos(self, publicaciones: List[Publicacion]) -> str:
        """Obtiene la distribución de tipos de documentos."""
        tipos_count = {}
        for pub in publicaciones:
            tipo = pub.tipo_documento or "Artículo"
            tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
        
        distribuciones = []
        for tipo, count in tipos_count.items():
            if count > 1:
                distribuciones.append(f"{count} {tipo}s")
            else:
                distribuciones.append(f"{count} {tipo}")
        
        if len(distribuciones) > 1:
            return " y ".join([", ".join(distribuciones[:-1]), distribuciones[-1]])
        elif distribuciones:
            return distribuciones[0]
        else:
            return "Sin especificar"
