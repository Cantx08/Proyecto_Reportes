import {ScopusAccountCreateRequest, ScopusAccountResponse} from "@/src/features/scopus-accounts/types";
import {axiosInstance} from "@/src/lib/axios";

export const scopusAccountsService = {
    /**
     * Obtener cuentas Scopus por autor
     */
    getByAuthor: async (author_id: string): Promise<ScopusAccountResponse[]> => {
        const {data} = await axiosInstance.get(`/scopus-accounts/author/${author_id}`);
        return Array.isArray(data) ? data : data.data || [];
    },

    /**
     * Obtener una cuenta Scopus por su Scopus ID
     */
    getById: async (scopus_id: string): Promise<ScopusAccountResponse> => {
        const {data} = await axiosInstance.get(`/scopus-accounts/${scopus_id}`);
        return data.data || data;
    },

    /**
     * Crear una nueva cuenta Scopus
     */
    create: async (payload: ScopusAccountCreateRequest): Promise<ScopusAccountResponse> => {
        const {data} = await axiosInstance.post('/scopus-accounts', payload);
        return data.data || data;
    },

    /**
     * Eliminar una cuenta Scopus
     */
    delete: async (account_id: string): Promise<void> => {
        await axiosInstance.delete(`/scopus-accounts/${account_id}`);
    },
};