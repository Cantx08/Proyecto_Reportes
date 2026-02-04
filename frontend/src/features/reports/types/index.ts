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
    { value: 'C. Calderón', label: 'C. Calderón' },
    { value: 'C. Rivadeneira', label: 'C. Rivadeneira' },
];
