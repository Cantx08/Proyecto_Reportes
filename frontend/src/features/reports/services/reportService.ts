import { axiosInstance } from "@/lib/axios";
import { ReportRequest, ProcessDraftMetadata } from "@/features/reports/types";

/**
 * Servicio para generar reportes y certificados PDF.
 */
export const reportService = {
    /**
     * Generar reporte de certificación
     * @param reportData Datos del reporte a generar
     */
    generateCertification: async (reportData: ReportRequest): Promise<Blob> => {
        const response = await axiosInstance.post('/reports/inform', reportData, {
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

        const response = await axiosInstance.post('/reports/process-draft', formData, {
            responseType: 'blob',
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return response.data;
    },
};
