import {Autor} from "@/features/authors/types";

// ------------------- CUENTAS SCOPUS -------------------
export interface ScopusAccount {
id?: number;
scopus_id: string;
author_id: string;
is_active?: boolean;
}

export interface ScopusAccountCreateRequest {
scopus_id: string;
author_id: string;
is_active?: boolean;
}

export interface ScopusAccountUpdateRequest {
author_id?: string;
is_active?: boolean;
}

export interface ScopusAccountResponse {
id?: number;
scopus_id: string;
author_id: string;
is_active?: boolean;
}

export interface ScopusAccountsResponse {
success: boolean;
data: ScopusAccountResponse[];
message: string;
total: number;
}

export interface LinkAuthorScopusRequest {
author_id: string;
scopus_id: string;
}

// ------------------- PUBLICACIONES -------------------
export interface Publication {
    title: string;
    year: string;
    source: string;
    document_type: string;
    affiliation: string;
    doi: string;
    categories: string | CategoryDetail[]; 
}

export interface PublicationsResponse {
    publications: Autor[];
}

export interface DocumentsByYearResponse {
    author_ids: string[];
    documents_by_year: Record<string, number>;
}

export interface SubjectAreasResponse {
    author_ids: string[];
    subject_areas: string[];
}

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