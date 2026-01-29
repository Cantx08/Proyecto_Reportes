import {axiosInstance} from "@/lib/axios";
import {DepartmentCreateRequest, DepartmentResponse, DepartmentUpdateRequest} from "@/features/departments/types";

export const departmentService = {
    /**
     * Obtener todos los departamentos
     */
    getAll: async (): Promise<DepartmentResponse[]> => {
        const {data} = await axiosInstance.get('/departments');
        return Array.isArray(data) ? data : data.data || [];
    },

    /**
     * Obtener un departamento por ID
     */
    getById: async (depId: string): Promise<DepartmentResponse> => {
        const {data} = await axiosInstance.get(`/departments/${depId}`);
        return data.data || data;
    },

    /**
     * Obtener departamentos por facultad
     */
    getByFaculty: async (facultyName: string): Promise<DepartmentResponse[]> => {
        const {data} = await axiosInstance.get(`/departments/faculty/${facultyName}`);
        return Array.isArray(data) ? data : data.data || [];
    },

    /**
     * Crear un nuevo departamento
     */
    create: async (payload: DepartmentCreateRequest): Promise<DepartmentResponse> => {
        const {data} = await axiosInstance.post('/departments', payload);
        return data.data || data;
    },

    /**
     * Actualizar un departamento existente
     */
    update: async (depId: string, payload: DepartmentUpdateRequest): Promise<DepartmentResponse> => {
        const {data} = await axiosInstance.put(`/departments/${depId}`, payload);
        return data.data || data;
    },

    /**
     * Eliminar un departamento
     */
    delete: async (depId: string): Promise<void> => {
        await axiosInstance.delete(`/departments/${depId}`);
    },
};