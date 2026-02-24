import {
    AuthorPublicationsResponse,
    AuthorScopusStatusResponse,
    AuthorSubjectAreasResponse,
    Publication,
    PublicationsStatsResponse,
} from "@/src/features/publications/types";
import { axiosInstance } from "@/src/lib/axios";
import {
    fetchAuthorSubjectAreas,
    fetchPublicationsByScopusId,
} from "@/src/services/scopusApi";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Instancia específica para publicaciones con timeout extendido
const publicationAxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 180000, // 3 minutos: el frontend puede tardar en paginar Scopus
    headers: {
        "Content-Type": "application/json",
    },
});

// ---------------------------------------------------------------------------
// Helper – clave de entorno para la API de Scopus
// ---------------------------------------------------------------------------

function getScopusApiKey(): string {
    const key = process.env.NEXT_PUBLIC_SCOPUS_API_KEY ?? "";
    if (!key) {
        console.warn(
            "[publicationService] NEXT_PUBLIC_SCOPUS_API_KEY no está configurada. " +
            "Las llamadas a Scopus fallarán."
        );
    }
    return key;
}

/**
 * Servicio para gestionar publicaciones científicas.
 *
 * Flujo de obtención de publicaciones (refactoring IP institucional):
 *  1. GET /publications/author/{id}/scopus-ids  → cuentas + estado de caché
 *  2. Para cuentas sin caché válida: el frontend llama a Scopus directamente
 *     (IP institucional) y envía los datos crudos al backend.
 *  3. POST /publications/process-account  → backend transforma + SJR + caché
 *  4. GET /publications/author/{id}/from-cache → resultado final consolidado
 */
export const publicationService = {
    /**
     * Obtener publicaciones de un autor.
     * El frontend llama a Scopus directamente cuando la caché está expirada.
     */
    getByAuthor: async (
        authorId: string,
        refresh: boolean = false,
    ): Promise<AuthorPublicationsResponse> => {
        try {
            const apiKey = getScopusApiKey();

            // 1. Obtener cuentas Scopus + estado de caché
            const { data: statusData } =
                await publicationAxiosInstance.get<AuthorScopusStatusResponse>(
                    `/publications/author/${authorId}/scopus-ids`,
                );

            const accounts = statusData.scopus_accounts;

            // 2. Para cada cuenta sin caché válida (o si se fuerza refresco),
            //    obtener datos de Scopus directamente y enviarlos al backend.
            for (const account of accounts) {
                if (!refresh && account.cache_valid) {
                    // Datos ya están en caché, no se llama a Scopus
                    continue;
                }

                const rawEntries = await fetchPublicationsByScopusId(
                    account.scopus_id,
                    apiKey,
                );

                await publicationAxiosInstance.post("/publications/process-account", {
                    account_id: account.account_id,
                    scopus_author_id: account.scopus_id,
                    raw_publications: rawEntries,
                });
            }

            // 3. Obtener el resultado final consolidado desde caché
            const { data } =
                await publicationAxiosInstance.get<AuthorPublicationsResponse>(
                    `/publications/author/${authorId}/from-cache`,
                );

            return data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.code === "ECONNABORTED") {
                    throw new Error(
                        "La consulta está tardando más de lo esperado. " +
                        "El autor puede tener muchas publicaciones o múltiples cuentas Scopus. " +
                        "Por favor, intente nuevamente.",
                    );
                }
                if (error.response?.status === 404) {
                    throw new Error("El autor no tiene cuentas Scopus asociadas.");
                }
                if (error.response?.status === 500) {
                    throw new Error(
                        "Error al obtener publicaciones desde Scopus. Por favor, intente nuevamente.",
                    );
                }
            }
            throw error;
        }
    },

    /**
     * Obtener publicaciones directamente por Scopus ID.
     * Útil para verificar publicaciones antes de vincular una cuenta.
     *
     * El frontend llama a Scopus directamente (IP institucional) y envía
     * los datos crudos al backend para transformar + enriquecer con SJR,
     * sin almacenar en caché.
     */
    getByScopusId: async (scopusId: string): Promise<Publication[]> => {
        const apiKey = getScopusApiKey();

        // 1. Obtener publicaciones crudas directamente desde Scopus
        const rawEntries = await fetchPublicationsByScopusId(scopusId, apiKey);

        if (rawEntries.length === 0) return [];

        // 2. Enviar al backend para transformar + enriquecer (sin caché)
        const { data } = await publicationAxiosInstance.post<Publication[]>(
            "/publications/process-preview",
            {
                scopus_author_id: scopusId,
                raw_publications: rawEntries,
            },
        );

        return Array.isArray(data) ? data : [];
    },

    /**
     * Obtener estadísticas de publicaciones de un autor.
     */
    getStatsByAuthor: async (
        authorId: string,
    ): Promise<PublicationsStatsResponse> => {
        const { data } = await axiosInstance.get(
            `/publications/author/${authorId}/stats`,
        );
        return data;
    },

    /**
     * Forzar actualización de publicaciones de un autor desde Scopus.
     */
    refreshAuthorPublications: async (
        authorId: string,
    ): Promise<AuthorPublicationsResponse> => {
        return publicationService.getByAuthor(authorId, true);
    },

    /**
     * Obtener áreas temáticas de un autor.
     * El frontend llama a Scopus Author Retrieval directamente (IP institucional).
     */
    getSubjectAreasByAuthor: async (
        authorId: string,
    ): Promise<AuthorSubjectAreasResponse> => {
        try {
            const apiKey = getScopusApiKey();

            // 1. Obtener lista de scopus_ids desde la BD (sin llamar a Scopus)
            const { data: statusData } =
                await publicationAxiosInstance.get<AuthorScopusStatusResponse>(
                    `/publications/author/${authorId}/scopus-ids`,
                );

            const scopusIds = statusData.scopus_accounts.map((a) => a.scopus_id);

            // 2. Llamar a Author Retrieval directamente por cada cuenta
            const results = await Promise.all(
                scopusIds.map((id) => fetchAuthorSubjectAreas(id, apiKey)),
            );

            // 3. Fusionar y deduplicar
            const merged = [...new Set(results.flat())].sort();

            return {
                author_id: authorId,
                scopus_ids: scopusIds,
                subject_areas: merged,
            };
        } catch (error) {
            if (axios.isAxiosError(error) && error.response?.status === 404) {
                throw new Error("El autor no tiene cuentas Scopus asociadas.");
            }
            throw error;
        }
    },
};
