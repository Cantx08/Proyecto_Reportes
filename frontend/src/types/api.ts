import {Publication} from "@/src/features/publications/types";


// Tipos para el estado del componente principal
export interface AppState {
    scopusIds: string[];
    isLoading: boolean;
    loadingProgress: string | null; // Para mostrar el progreso actual
    publications: Publication[];
    subjectAreas: string[];
    documentsByYear: Record<string, number>;
    error: string | null;
}

// Tipo para validación de IDs
export interface ValidationResult {
    isValid: boolean;
    message?: string;
}


// ---------- DETALLE DE CATEGORÍAS ----------
export interface CategoryDetail {
    name: string;
    quartile: string;
    percentile: number;
    rank: number;
    total: number;
}