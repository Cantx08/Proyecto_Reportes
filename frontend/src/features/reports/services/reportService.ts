import { axiosInstance } from "@/src/lib/axios";
import { ReportRequest, ElaboradorOption } from "@/src/features/reports/types";
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Instancia específica para generación de reportes con timeout extendido
// La generación de PDF puede tardar debido a:
// - Obtención de publicaciones de múltiples cuentas Scopus
// - Generación de gráficos con matplotlib
// - Renderizado del PDF con ReportLab
const reportAxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 180000, // 3 minutos para generación de certificados
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Servicio para generar certificados PDF de publicaciones académicas.
 */
export const reportService = {
    /**
     * Generar certificado de publicaciones
     * @param reportData Datos del certificado a generar
     */
    generateCertification: async (reportData: ReportRequest): Promise<Blob> => {
        try {
            const response = await reportAxiosInstance.post('/certificates/generate', reportData, {
                responseType: 'blob',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.code === 'ECONNABORTED') {
                    throw new Error('La generación del certificado está tardando más de lo esperado. Esto puede ocurrir con autores que tienen muchas publicaciones o múltiples cuentas Scopus. Por favor, intente nuevamente.');
                }
                if (error.response?.status === 404) {
                    throw new Error('No se encontraron los datos necesarios para generar el certificado.');
                }
                if (error.response?.status === 500) {
                    throw new Error('Error al generar el certificado. Verifique los datos ingresados e intente nuevamente.');
                }
            }
            throw error;
        }
    },

    /**
     * Obtener opciones de elaboradores disponibles
     */
    getElaboradores: async (): Promise<ElaboradorOption[]> => {
        const response = await axiosInstance.get('/certificates/elaboradores');
        return response.data;
    },
};
