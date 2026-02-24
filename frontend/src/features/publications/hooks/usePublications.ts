import { useCallback, useState } from 'react';
import { apiUtils } from '@/src/services/servicesApi';
import { 
    AuthorPublicationsResponse, 
    Publication,
    PublicationsStatsResponse,
    PublicationFilters
} from '@/src/features/publications/types';
import { publicationService } from '@/src/features/publications/services/publicationService';

export interface UsePublicationsState {
    publications: Publication[];
    authorId: string | null;
    scopusIds: string[];
    totalPublications: number;
    stats: PublicationsStatsResponse | null;
    loading: boolean;
    refreshing: boolean;
    error: string | null;
}

export interface UsePublicationsActions {
    fetchByAuthor: (authorId: string, refresh?: boolean) => Promise<void>;
    fetchByScopusId: (scopusId: string) => Promise<Publication[]>;
    fetchStats: (authorId: string) => Promise<void>;
    refreshPublications: () => Promise<void>;
    filterPublications: (filters: PublicationFilters) => Publication[];
    clearError: () => void;
    clearData: () => void;
}

export function usePublications(): UsePublicationsState & UsePublicationsActions {
    const [state, setState] = useState<UsePublicationsState>({
        publications: [],
        authorId: null,
        scopusIds: [],
        totalPublications: 0,
        stats: null,
        loading: false,
        refreshing: false,
        error: null,
    });

    const clearError = useCallback(() => {
        setState(prev => ({ ...prev, error: null }));
    }, []);

    const clearData = useCallback(() => {
        setState({
            publications: [],
            authorId: null,
            scopusIds: [],
            totalPublications: 0,
            stats: null,
            loading: false,
            refreshing: false,
            error: null,
        });
    }, []);

    const fetchByAuthor = useCallback(async (
        authorId: string, 
        refresh: boolean = false
    ): Promise<void> => {
        setState(prev => ({ 
            ...prev, 
            loading: !refresh,
            refreshing: refresh,
            error: null 
        }));

        try {
            const response: AuthorPublicationsResponse = await publicationService.getByAuthor(
                authorId, 
                refresh
            );

            setState(prev => ({
                ...prev,
                publications: response.publications,
                authorId: response.author_id,
                scopusIds: response.scopus_ids,
                totalPublications: response.total_publications,
                loading: false,
                refreshing: false,
            }));
        } catch (error) {
            const errorMessage = apiUtils.handleError(error);
            setState(prev => ({
                ...prev,
                loading: false,
                refreshing: false,
                error: errorMessage,
            }));
        }
    }, []);

    const fetchByScopusId = useCallback(async (scopusId: string): Promise<Publication[]> => {
        setState(prev => ({ ...prev, loading: true, error: null }));

        try {
            const publications = await publicationService.getByScopusId(scopusId);
            setState(prev => ({
                ...prev,
                publications,
                totalPublications: publications.length,
                loading: false,
            }));
            return publications;
        } catch (error) {
            const errorMessage = apiUtils.handleError(error);
            setState(prev => ({
                ...prev,
                loading: false,
                error: errorMessage,
            }));
            return [];
        }
    }, []);

    const fetchStats = useCallback(async (authorId: string): Promise<void> => {
        try {
            const stats = await publicationService.getStatsByAuthor(authorId);
            setState(prev => ({ ...prev, stats }));
        } catch (error) {
            const errorMessage = apiUtils.handleError(error);
            setState(prev => ({ ...prev, error: errorMessage }));
        }
    }, []);

    const refreshPublications = useCallback(async (): Promise<void> => {
        if (!state.authorId) {
            setState(prev => ({ 
                ...prev, 
                error: 'No hay un autor seleccionado para actualizar' 
            }));
            return;
        }

        await fetchByAuthor(state.authorId, true);
    }, [state.authorId, fetchByAuthor]);

    const filterPublications = useCallback((filters: PublicationFilters): Publication[] => {
        return state.publications.filter(pub => {
            // Filtro por año desde
            if (filters.yearFrom && pub.year < filters.yearFrom) {
                return false;
            }

            // Filtro por año hasta
            if (filters.yearTo && pub.year > filters.yearTo) {
                return false;
            }

            // Filtro por tipo de documento
            if (filters.documentType && pub.document_type !== filters.documentType) {
                return false;
            }

            // Filtro por búsqueda de texto
            if (filters.searchQuery) {
                const query = filters.searchQuery.toLowerCase();
                const matchesTitle = pub.title.toLowerCase().includes(query);
                const matchesSource = pub.source_title.toLowerCase().includes(query);
                const matchesDoi = pub.doi?.toLowerCase().includes(query) || false;
                
                if (!matchesTitle && !matchesSource && !matchesDoi) {
                    return false;
                }
            }

            return true;
        });
    }, [state.publications]);

    return {
        ...state,
        fetchByAuthor,
        fetchByScopusId,
        fetchStats,
        refreshPublications,
        filterPublications,
        clearError,
        clearData,
    };
}
