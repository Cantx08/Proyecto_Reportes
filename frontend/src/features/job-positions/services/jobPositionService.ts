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
    getById: async (pos_id: string): Promise<JobPositionResponse> => {
        const {data} = await axiosInstance.get(`/job-positions/${pos_id}`);
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
    update: async (pos_id: string, payload: JobPositionUpdateRequest): Promise<JobPositionResponse> => {
        const {data} = await axiosInstance.put(`/job-positions/${pos_id}`, payload);
        return data.data || data;
    },

    /**
     * Eliminar una posición
     */
    delete: async (pos_id: string): Promise<void> => {
        await axiosInstance.delete(`/job-positions/${pos_id}`);
    },
};