import {axiosInstance} from "@/lib/axios";
import {JobPositionCreateRequest, JobPositionResponse, JobPositionUpdateRequest} from "@/features/job-positions/types";

export const jobPositionService = {
    /**
     * Obtener todas las posiciones
     */
    getAll: async (): Promise<JobPositionResponse[]> => {
        const {data} = await axiosInstance.get('/job-positions');
        return Array.isArray(data) ? data : data.data || [];
    },

    /**
     * Obtener una posición por ID
     */
    getById: async (posId: string): Promise<JobPositionResponse> => {
        const {data} = await axiosInstance.get(`/job-positions/${posId}`);
        return data.data || data;
    },

    /**
     * Crear una nueva posición
     */
    create: async (payload: JobPositionCreateRequest): Promise<JobPositionResponse> => {
        const {data} = await axiosInstance.post('/job-positions', payload);
        return data.data || data;
    },

    /**
     * Actualizar una posición existente
     */
    update: async (posId: string, payload: JobPositionUpdateRequest): Promise<JobPositionResponse> => {
        const {data} = await axiosInstance.put(`/job-positions/${posId}`, payload);
        return data.data || data;
    },

    /**
     * Eliminar una posición
     */
    delete: async (posId: string): Promise<void> => {
        await axiosInstance.delete(`/job-positions/${posId}`);
    },
};