import {
    AuthorPublicationsResponse,
    Publication,
    PublicationsStatsResponse
} from "@/src/features/publications/types";
import { axiosInstance } from "@/src/lib/axios";
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Instancia específica para publicaciones con timeout extendido
const publicationAxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 180000, // 3 minutos para consultas de publicaciones que pueden tardar
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Servicio para gestionar publicaciones científicas.
 * Consume el endpoint /publications del backend.
 */
export const publicationService = {
    /**
     * Obtener publicaciones de un autor por su ID del sistema
     * @param authorId UUID del autor en el sistema
     * @param refresh Si es true, fuerza actualización desde Scopus (ignora caché)
     */
    getByAuthor: async (
        authorId: string, 
        refresh: boolean = false
    ): Promise<AuthorPublicationsResponse> => {
        try {
            const params = refresh ? { refresh: true } : {};
            const { data } = await publicationAxiosInstance.get(
                `/publications/author/${authorId}`,
                { params }
            );
            return data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.code === 'ECONNABORTED') {
                    throw new Error('La consulta está tardando más de lo esperado. El autor puede tener muchas publicaciones o múltiples cuentas Scopus. Por favor, intente nuevamente.');
                }
                if (error.response?.status === 404) {
                    throw new Error('El autor no tiene cuentas Scopus asociadas.');
                }
                if (error.response?.status === 500) {
                    throw new Error('Error al obtener publicaciones desde Scopus. Por favor, intente nuevamente.');
                }
            }
            throw error;
        }
    },

    /**
     * Obtener publicaciones directamente por Scopus ID
     * Útil para verificar publicaciones antes de vincular una cuenta
     * @param scopusId ID de Scopus del autor
     */
    getByScopusId: async (scopusId: string): Promise<Publication[]> => {
        const { data } = await axiosInstance.get(
            `/publications/scopus/${scopusId}`
        );
        return Array.isArray(data) ? data : data.publications || [];
    },

    /**
     * Obtener estadísticas de publicaciones de un autor
     * @param authorId UUID del autor en el sistema
     */
    getStatsByAuthor: async (authorId: string): Promise<PublicationsStatsResponse> => {
        const { data } = await axiosInstance.get(
            `/publications/author/${authorId}/stats`
        );
        return data;
    },

    /**
     * Forzar actualización de publicaciones de un autor desde Scopus
     * @param authorId UUID del autor en el sistema
     */
    refreshAuthorPublications: async (
        authorId: string
    ): Promise<AuthorPublicationsResponse> => {
        return publicationService.getByAuthor(authorId, true);
    }
};