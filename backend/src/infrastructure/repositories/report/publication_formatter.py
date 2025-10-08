from typing import List, Any
from reportlab.platypus import Paragraph, Spacer
from ....domain.entities.publication import Publication
from ....domain.repositories.report_repository import IPublicationFormatter, IStyleManager


class ReportLabPublicationFormatter(IPublicationFormatter):
    """Implementación de formateador de publicaciones usando ReportLab."""
    
    def __init__(self, style_manager: IStyleManager):
        self._style_manager = style_manager
    
    def format_publication_list(self, publications: List[Publication], tipo: str) -> List[Any]:
        """Formatea una lista de publicaciones."""
        elements = []
        
        for i, pub in enumerate(publications, 1):
            pub_text = self._generate_publications_list(pub, i, tipo)
            
            publication_style = self._style_manager.fetch_style('Publication')
            elements.append(Paragraph(pub_text, publication_style))
        
        elements.append(Spacer(1, 15))
        return elements
    
    def _generate_publications_list(self, pub: Publication, num: int, db_name: str) -> str:
        """Construye el texto formateado de una publicación."""
        pub_text = f"{num}. ({pub.year}) \"{pub.title}\". {pub.source}."
        
        # Agregar información de categorías e indexación
        if pub.categories:
            journal_categories = self._format_categories(pub.categories)
            format_type = "SCOPUS" if db_name == "Scopus" else db_name
            pub_text += f" <b>Indexada en {format_type} - {journal_categories}</b>."
        else:
            format_type = "SCOPUS" if db_name == "Scopus" else db_name
            pub_text += f" <b>Indexada en {format_type}</b>."
        
        # Agregar DOI si existe
        if pub.doi:
            pub_text += f" DOI: {pub.doi}"
        
        # Agregar indicación de filiación si no es EPN
        if pub.affiliation and "escuela politécnica nacional" not in pub.affiliation.lower():
            pub_text += " <u>(Sin Filiación)</u>"
        
        return pub_text
    
    @staticmethod
    def _format_categories(categories: Any) -> str:
        """Formatea las categorías de una publicación."""
        if isinstance(categories, str):
            return categories
        elif isinstance(categories, list) and len(categories) > 0:
            if len(categories[0]) > 1:
                return "; ".join(categories)
            else:
                return "".join(categories)
        else:
            return str(categories)
    
    def get_document_type(self, publications: List[Publication]) -> str:
        """Obtiene la distribución de tipos de documentos."""
        count_types = {}
        for pub in publications:
            source_type = pub.document_type or "Artículo"
            count_types[source_type] = count_types.get(source_type, 0) + 1
        
        distributions = []
        for source_type, count in count_types.items():
            if count > 1:
                distributions.append(f"{count} {source_type}s")
            else:
                distributions.append(f"{count} {source_type}")
        
        if len(distributions) > 1:
            return " y ".join([", ".join(distributions[:-1]), distributions[-1]])
        elif distributions:
            return distributions[0]
        else:
            return "Sin especificar"
