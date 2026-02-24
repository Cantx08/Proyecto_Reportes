import {
    AuthorCreateRequest,
    AuthorResponse,
    AuthorUpdateRequest,
    ImportAuthorsResponse
} from "@/src/features/authors/types";
import {axiosInstance} from "@/src/lib/axios";

export const authorService = {
    /**
     * Obtener todos los autores
     */
    getAll: async (): Promise<AuthorResponse[]> => {
        const {data} = await axiosInstance.get('/authors');
        return Array.isArray(data) ? data : data.data || [];
    },

    /**
     * Obtener un autor por ID
     */
    getById: async (author_id: string): Promise<AuthorResponse> => {
        const {data} = await axiosInstance.get(`/authors/${author_id}`);
        return data.data || data;
    },

    /**
     * Obtener autores por departamento
     */
    getByDepartment: async (dep_code: string): Promise<AuthorResponse[]> => {
        const {data} = await axiosInstance.get(`/authors/departments/${dep_code}`);
        return Array.isArray(data) ? data : data.data || [];
    },

    /**
     * Crear un nuevo autor
     */
    create: async (payload: AuthorCreateRequest): Promise<AuthorResponse> => {
        const {data} = await axiosInstance.post('/authors', payload);
        return data.data || data;
    },

    /**
     * Actualizar un autor existente
     */
    update: async (author_id: string, payload: AuthorUpdateRequest): Promise<AuthorResponse> => {
        const {data} = await axiosInstance.put(`/authors/${author_id}`, payload);
        return data.data || data;
    },

    /**
     * Eliminar un autor
     */
    delete: async (author_id: string): Promise<void> => {
        await axiosInstance.delete(`/authors/${author_id}`);
    },

    /**
     * Importar autores desde un CSV
     */
    importAuthors: async (file: File): Promise<ImportAuthorsResponse> => {
        const formData = new FormData();
        formData.append('file', file);

        const { data } = await axiosInstance.post('/authors/import', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return data;
    },
};