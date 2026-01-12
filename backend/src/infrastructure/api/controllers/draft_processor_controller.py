"""
Controlador para procesar borradores PDF.
"""
from typing import Optional
from fastapi import UploadFile, HTTPException, Form
from fastapi.responses import Response
from ....application.services.draft_processor_service import DraftProcessorService
from ....application.dto.report_dto import ProcessDraftRequestDTO


class DraftProcessorController:
    """Controlador para manejar el procesamiento de borradores PDF."""    
    def __init__(self, draft_processor_service: DraftProcessorService):
        """
        Inicializa el controlador.
        
        Args:
            draft_processor_service: Servicio de procesamiento de borradores
        """
        self.draft_processor_service = draft_processor_service

    async def process_draft(
        self,
        file: UploadFile,
        memorando: Optional[str] = Form(None),
        firmante: Optional[int] = Form(None),
        firmante_nombre: Optional[str] = Form(None),
        fecha: Optional[str] = Form(None)
    ) -> Response:
        """
        Procesa un borrador PDF y lo convierte en certificado final.
        
        Args:
            file: Archivo PDF borrador
            memorando: Número de memorando (opcional)
            firmante: Tipo de firmante (opcional)
            firmante_nombre: Nombre del firmante (opcional)
            fecha: Fecha del certificado (opcional)
        
        Returns:
            Response: PDF final con plantilla aplicada
            
        Raises:
            HTTPException: Si hay errores de validación o procesamiento
        """
        # Validar tipo de archivo
        if not file.content_type or 'pdf' not in file.content_type.lower():
            raise HTTPException(
                status_code=400,
                detail="El archivo debe ser un PDF"
            )

        # Leer contenido del archivo
        try:
            draft_pdf_bytes = await file.read()
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Error al leer el archivo: {str(e)}"
                                ) from e

        # Validar tamaño máximo (10MB)
        max_size = 10 * 1024 * 1024  # 10 MB
        if len(draft_pdf_bytes) > max_size:
            raise HTTPException(status_code=400,
                                detail="El archivo excede el tamaño máximo permitido (10MB)"
                                )

        # Crear DTO con metadatos (para extensión futura)
        metadata = ProcessDraftRequestDTO(
            memorando=memorando,
            firmante=firmante,
            firmante_nombre=firmante_nombre,
            fecha=fecha
        )

        # Procesar el borrador
        try:
            final_pdf_bytes = await self.draft_processor_service.process_draft(
                draft_pdf_bytes,
                metadata
            )
        except ValueError as e:
            raise HTTPException(status_code=400,
                                detail=str(e)
                                ) from e
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Error al procesar el borrador: {str(e)}"
                                ) from e

        # Retornar PDF final
        return Response(content=final_pdf_bytes,
                        media_type="application/pdf",
                        headers={
                            "Content-Disposition": "attachment; filename=certificado_final.pdf"
                        }
        )
