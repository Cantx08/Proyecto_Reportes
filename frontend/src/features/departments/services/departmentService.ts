import {axiosInstance} from "@/src/lib/axios";
import {DepartmentCreateRequest, DepartmentResponse, DepartmentUpdateRequest} from "@/src/features/departments/types";

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
    getById: async (dep_id: string): Promise<DepartmentResponse> => {
        const {data} = await axiosInstance.get(`/departments/${dep_id}`);
        return data.data || data;
    },

    /**
     * Obtener departamentos por facultad
     */
    getByFaculty: async (faculty_name: string): Promise<DepartmentResponse[]> => {
        const {data} = await axiosInstance.get(`/departments/faculty/${faculty_name}`);
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
    update: async (dep_id: string, payload: DepartmentUpdateRequest): Promise<DepartmentResponse> => {
        const {data} = await axiosInstance.put(`/departments/${dep_id}`, payload);
        return data.data || data;
    },

    /**
     * Eliminar un departamento
     */
    delete: async (dep_id: string): Promise<void> => {
        await axiosInstance.delete(`/departments/${dep_id}`);
    },
};