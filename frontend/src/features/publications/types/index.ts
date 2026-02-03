/**
 * Tipos para el módulo de publicaciones
 * Alineados con el backend: PublicationResponseDTO, AuthorPublicationsResponseDTO
 */

/**
 * Representa una publicación científica obtenida de Scopus
 * enriquecida con datos SJR
 */
export interface Publication {
    scopus_id: string;
    eid: string;
    doi: string | null;
    title: string;
    year: number;
    publication_date: string;
    source_title: string;
    document_type: string;
    affiliation_name: string;
    affiliation_id: string | null;
    subject_areas: string[];
    categories_with_quartiles: string[];
    sjr_year_used: number | null;
}

/**
 * Respuesta del endpoint de publicaciones por autor
 */
export interface AuthorPublicationsResponse {
    author_id: string;
    scopus_ids: string[];
    total_publications: number;
    publications: Publication[];
}

/**
 * Estadísticas de documentos por año
 */
export interface DocumentsByYearItem {
    year: number;
    count: number;
}

/**
 * Respuesta del endpoint de estadísticas de publicaciones
 */
export interface PublicationsStatsResponse {
    author_id: string;
    total_publications: number;
    documents_by_year: DocumentsByYearItem[];
    documents_by_type: Record<string, number>;
}

/**
 * Opciones de filtrado para publicaciones
 */
export interface PublicationFilters {
    yearFrom?: number;
    yearTo?: number;
    documentType?: string;
    searchQuery?: string;
}