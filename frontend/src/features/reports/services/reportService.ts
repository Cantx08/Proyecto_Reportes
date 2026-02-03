import { axiosInstance } from "@/lib/axios";
import { ReportRequest, ElaboradorOption } from "@/features/reports/types";

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
     * Obtener opciones de elaboradores disponibles
     */
    getElaboradores: async (): Promise<ElaboradorOption[]> => {
        const response = await axiosInstance.get('/certificates/elaboradores');
        return response.data;
    },
};
