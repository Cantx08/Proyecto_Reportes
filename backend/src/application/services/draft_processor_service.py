"""
Servicio para procesar borradores PDF y convertirlos en certificados finales.
"""
import io
from typing import Optional
from pypdf import PdfReader
from src.application.dto.report_dto import ProcessDraftRequestDTO
from src.infrastructure.repositories.report.template_overlay_service import TemplateOverlayService


class DraftProcessorService:
    """
    Servicio que procesa borradores PDF existentes y les aplica la plantilla institucional.
    """
    
    def __init__(self, template_service: TemplateOverlayService):
        """
        Inicializa el servicio.
        
        Args:
            template_service: Servicio para aplicar plantilla sobre PDF
        """
        self.template_service = template_service
    
    async def process_draft(
        self,
        draft_pdf_bytes: bytes,
        metadata: Optional[ProcessDraftRequestDTO] = None
    ) -> bytes:
        """
        Procesa un borrador PDF y genera el certificado final con plantilla.
        
        Args:
            draft_pdf_bytes: Contenido del PDF borrador
            metadata: Metadatos opcionales (actualmente no utilizados, para extensión futura)
        
        Returns:
            bytes: PDF final con plantilla institucional aplicada
            
        Raises:
            ValueError: Si el PDF no es válido o está corrupto
        """
        # Validar que el PDF sea válido
        self._validate_pdf(draft_pdf_bytes)
        
        # Aplicar la plantilla institucional sobre el borrador
        final_pdf_bytes = self.template_service.overlay_content_on_template(draft_pdf_bytes)
        
        return final_pdf_bytes
    
    def _validate_pdf(self, pdf_bytes: bytes) -> None:
        """
        Valida que los bytes proporcionados sean un PDF válido.
        
        Args:
            pdf_bytes: Contenido del PDF a validar
            
        Raises:
            ValueError: Si el PDF no es válido o está corrupto
        """
        try:
            pdf_stream = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)
            
            # Verificar que tenga al menos una página
            if len(reader.pages) == 0:
                raise ValueError("El PDF no contiene páginas")
                
            # Intentar leer la primera página para verificar integridad
            _ = reader.pages[0]
            
        except Exception as e:
            raise ValueError(f"PDF inválido o corrupto: {str(e)}")
    
    def extract_metadata(self, pdf_bytes: bytes) -> dict:
        """
        Extrae metadatos del PDF (opcional, para extensión futura).
        
        Args:
            pdf_bytes: Contenido del PDF
            
        Returns:
            dict: Diccionario con metadatos del PDF
        """
        try:
            pdf_stream = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)
            
            metadata = {
                "num_pages": len(reader.pages),
                "metadata": reader.metadata if reader.metadata else {},
            }
            
            return metadata
            
        except Exception:
            return {"num_pages": 0, "metadata": {}}
