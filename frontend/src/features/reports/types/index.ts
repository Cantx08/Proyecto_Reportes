/**
 * Tipos para el módulo de certificados
 */

export interface ReportRequest {
    author_ids: string[];
    docente_nombre: string;
    docente_genero: string;
    departamento: string;
    cargo: string;
    memorando?: string;
    firmante?: number | string;
    firmante_nombre?: string;
    fecha?: string;
    elaborador?: string;
    is_draft?: boolean;

    /** Áreas temáticas del autor (obtenidas por el frontend desde Scopus Author Retrieval). */
    subject_areas?: string[];
}

/**
 * Opción de elaborador disponible
 */
export interface ElaboradorOption {
    value: string;
    label: string;
}

/**
 * Opciones de elaborador disponibles (constantes del cliente)
 */
export const ELABORADOR_OPTIONS: ElaboradorOption[] = [
    { value: 'M. Vásquez', label: 'M. Vásquez' },
    { value: 'C. Calderón', label: 'C. Calderón' },
    { value: 'C. Rivadeneira', label: 'C. Rivadeneira' },
];


// ============================================================================
// Tipos para metadatos de reportes guardados
// ============================================================================

/**
 * Snapshot de una publicación almacenada en metadatos.
 */
export interface PublicationSnapshot {
    scopus_id: string;
    eid?: string;
    doi?: string | null;
    title: string;
    year: number;
    publication_date?: string;
    source_title?: string;
    document_type?: string;
    affiliation_name?: string;
    affiliation_id?: string | null;
    source_id?: string | null;
    subject_areas?: string[];
    categories_with_quartiles?: string[];
    sjr_year_used?: number | null;
}

/**
 * DTO para guardar metadatos de un reporte.
 */
export interface SaveReportMetadataRequest {
    author_name: string;
    author_gender: string;
    department: string;
    position: string;
    author_ids: string[];
    publications: PublicationSnapshot[];
    subject_areas: string[];
    documents_by_year: Record<string, number>;
    memorandum?: string;
    signatory?: number | string;
    signatory_name?: string;
    report_date?: string;
    elaborador?: string;
    label?: string;
}

/**
 * DTO para actualizar solo los campos editables de metadatos.
 */
export interface UpdateReportMetadataRequest {
    memorandum?: string;
    signatory?: number | string;
    signatory_name?: string;
    report_date?: string;
    elaborador?: string;
    label?: string;
}

/**
 * Respuesta con metadatos de un reporte guardado.
 */
export interface ReportMetadataResponse {
    id: string;
    author_name: string;
    author_gender: string;
    department: string;
    position: string;
    author_ids: string[];
    publications: PublicationSnapshot[];
    subject_areas: string[];
    documents_by_year: Record<string, number>;
    memorandum?: string;
    signatory?: number | string;
    signatory_name?: string;
    report_date?: string;
    elaborador?: string;
    label: string;
    created_at: string;
    updated_at: string;
}
