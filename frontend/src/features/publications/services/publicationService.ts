import {
    AuthorPublicationsResponse,
    Publication,
    PublicationsStatsResponse
} from "@/features/publications/types";
import { axiosInstance } from "@/lib/axios";

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
        const params = refresh ? { refresh: true } : {};
        const { data } = await axiosInstance.get(
            `/publications/author/${authorId}`,
            { params }
        );
        return data;
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