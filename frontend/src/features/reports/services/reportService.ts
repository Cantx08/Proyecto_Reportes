import { axiosInstance } from "@/lib/axios";
import { ReportRequest, ProcessDraftMetadata, ElaboradorOption } from "@/features/reports/types";

/**
 * Servicio para generar certificados PDF de publicaciones académicas.
 */
export const reportService = {
    /**
     * Generar certificado de publicaciones
     * @param reportData Datos del certificado a generar
     */
    generateCertification: async (reportData: ReportRequest): Promise<Blob> => {
        const response = await axiosInstance.post('/certificates/generate', reportData, {
            responseType: 'blob',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        return response.data;
    },

    /**
     * Procesar borrador PDF existente y convertirlo en certificado final
     * @param file Archivo PDF del borrador
     * @param metadata Metadatos opcionales para el certificado
     */
    processDraft: async (
        file: File,
        metadata?: ProcessDraftMetadata
    ): Promise<Blob> => {
        const formData = new FormData();
        formData.append('file', file);

        // Añadir metadatos opcionales si existen
        if (metadata) {
            if (metadata.memorando) formData.append('memorando', metadata.memorando);
            if (metadata.firmante) formData.append('firmante', metadata.firmante.toString());
            if (metadata.firmante_nombre) formData.append('firmante_nombre', metadata.firmante_nombre);
            if (metadata.fecha) formData.append('fecha', metadata.fecha);
        }

        const response = await axiosInstance.post('/certificates/process-draft', formData, {
            responseType: 'blob',
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return response.data;
    },

    /**
     * Obtener opciones de elaboradores disponibles
     */
    getElaboradores: async (): Promise<ElaboradorOption[]> => {
        const response = await axiosInstance.get('/certificates/elaboradores');
        return response.data;
    },
};
