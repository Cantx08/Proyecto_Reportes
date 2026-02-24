import { axiosInstance } from "@/src/lib/axios";
import {
    ReportRequest,
    ElaboradorOption,
    SaveReportMetadataRequest,
    UpdateReportMetadataRequest,
    ReportMetadataResponse,
} from "@/src/features/reports/types";
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
     * Generar certificado final de publicaciones (con plantilla institucional)
     * @param reportData Datos del certificado a generar
     */
    generateCertification: async (reportData: ReportRequest): Promise<Blob> => {
        try {
            const response = await reportAxiosInstance.post('/certificates/generate', {
                ...reportData,
                is_draft: false,
            }, {
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
     * Generar borrador de publicaciones (sin plantilla institucional)
     * @param reportData Datos del borrador a generar
     */
    generateDraft: async (reportData: ReportRequest): Promise<Blob> => {
        try {
            const response = await reportAxiosInstance.post('/certificates/generate', {
                ...reportData,
                is_draft: true,
            }, {
                responseType: 'blob',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.code === 'ECONNABORTED') {
                    throw new Error('La generación del borrador está tardando más de lo esperado. Por favor, intente nuevamente.');
                }
                if (error.response?.status === 500) {
                    throw new Error('Error al generar el borrador. Verifique los datos ingresados e intente nuevamente.');
                }
            }
            throw error;
        }
    },

    /**
     * Procesar un borrador PDF y aplicarle la plantilla institucional
     * @param file Archivo PDF borrador
     */
    processDraft: async (file: File): Promise<Blob> => {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await reportAxiosInstance.post('/certificates/process-draft', formData, {
                responseType: 'blob',
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.response?.status === 400) {
                    // Intentar leer el mensaje de error del blob
                    try {
                        const errorBlob = error.response.data;
                        const errorText = await errorBlob.text();
                        const errorJson = JSON.parse(errorText);
                        throw new Error(errorJson.detail || 'Archivo PDF inválido.');
                    } catch {
                        throw new Error('El archivo proporcionado no es un PDF válido o está corrupto.');
                    }
                }
                if (error.response?.status === 500) {
                    throw new Error('Error al procesar el borrador. Intente nuevamente.');
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

    // =========================================================================
    // Métodos para metadatos de reportes
    // =========================================================================

    /**
     * Guardar metadatos de un reporte (publicaciones + datos del formulario)
     */
    saveMetadata: async (data: SaveReportMetadataRequest): Promise<ReportMetadataResponse> => {
        const response = await axiosInstance.post('/certificates/metadata', data);
        return response.data;
    },

    /**
     * Listar todos los reportes guardados
     */
    listMetadata: async (): Promise<ReportMetadataResponse[]> => {
        const response = await axiosInstance.get('/certificates/metadata');
        return response.data;
    },

    /**
     * Obtener metadatos de un reporte por ID
     */
    getMetadata: async (id: string): Promise<ReportMetadataResponse> => {
        const response = await axiosInstance.get(`/certificates/metadata/${id}`);
        return response.data;
    },

    /**
     * Actualizar solo los campos editables de un reporte guardado
     */
    updateMetadata: async (id: string, data: UpdateReportMetadataRequest): Promise<ReportMetadataResponse> => {
        const response = await axiosInstance.put(`/certificates/metadata/${id}`, data);
        return response.data;
    },

    /**
     * Eliminar un reporte guardado
     */
    deleteMetadata: async (id: string): Promise<void> => {
        await axiosInstance.delete(`/certificates/metadata/${id}`);
    },

    /**
     * Regenerar borrador PDF desde metadatos guardados (sin volver a buscar publicaciones)
     */
    regenerateFromMetadata: async (id: string): Promise<Blob> => {
        try {
            const response = await reportAxiosInstance.post(
                `/certificates/metadata/${id}/generate`,
                {},
                {
                    responseType: 'blob',
                }
            );
            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.code === 'ECONNABORTED') {
                    throw new Error('La regeneración del borrador está tardando más de lo esperado.');
                }
                if (error.response?.status === 404) {
                    throw new Error('No se encontraron los metadatos guardados.');
                }
                if (error.response?.status === 500) {
                    throw new Error('Error al regenerar el borrador.');
                }
            }
            throw error;
        }
    },
};
