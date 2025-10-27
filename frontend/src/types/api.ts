
// ------------------- AUTORES -------------------
export interface Autor {
    author_id: string;
    publications_list: Publication[];
    error?: string;
}

// Autor
export interface Author {
    author_id: string;
    name: string;
    surname: string;
    dni: string;
    title: string;
    birth_date?: string;
    gender: string;
    position: string;
    department: string;
}

export interface AuthorCreateRequest {
    author_id?: string;
    name: string;
    surname: string;
    dni: string;
    title: string;
    birth_date?: string;
    gender: string;
    position: string;
    department: string;
}

export interface AuthorUpdateRequest {
    name?: string;
    surname?: string;
    dni?: string;
    title?: string;
    birth_date?: string;
    gender?: string;
    position?: string;
    department?: string;
}

export interface AuthorResponse {
    author_id: string;
    name: string;
    surname: string;
    dni: string;
    title: string;
    birth_date?: string;
    gender: string;
    position: string;
    department: string;
}

export interface AuthorsResponse {
    authors: AuthorResponse[];
}



// ------------------- DEPARTAMENTOS -------------------
export interface Department {
dep_code: string;
dep_name: string;
fac_name: string;
}

export interface DepartmentsResponse {
success: boolean;
data: Department[];
message: string;
}

// Departamento (nuevo)
export interface NewDepartment {
dep_id: string;
dep_code: string;
dep_name: string;
fac_name: string;
}

export interface DepartmentCreateRequest {
dep_id: string;
dep_code: string;
dep_name: string;
fac_name: string;
}

export interface DepartmentUpdateRequest {
dep_code?: string;
dep_name?: string;
fac_name?: string;
}

export interface DepartmentResponse {
dep_id: string;
dep_code: string;
dep_name: string;
fac_name: string;
}

// ------------------- CARGOS -------------------
export interface Position {
pos_id: string;
pos_name: string;
}

export interface PositionCreateRequest {
pos_id: string;
pos_name: string;
}

export interface PositionUpdateRequest {
pos_name?: string;
}

export interface PositionResponse {
pos_id: string;
pos_name: string;
}

export interface PositionsResponse {
positions: PositionResponse[];
}

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
    categories: string;
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
