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
    { value: 'S. Sánchez', label: 'S. Sánchez' },
    { value: 'J. Sayago', label: 'J. Sayago' },
];

export interface ProcessDraftMetadata {
    memorando?: string;
    firmante?: number;
    firmante_nombre?: string;
    fecha?: string;
}
