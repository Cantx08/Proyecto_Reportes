/**
 * Tipos para el módulo de reportes
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
    es_borrador?: boolean;
}

export interface ProcessDraftMetadata {
    memorando?: string;
    firmante?: number;
    firmante_nombre?: string;
    fecha?: string;
}
