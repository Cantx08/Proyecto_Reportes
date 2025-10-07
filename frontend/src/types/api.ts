// Tipos para las respuestas de la API del backend

export interface Publicacion {
  title: string;           // Cambio: titulo -> title
  year: string;           // Cambio: anio -> year  
  source: string;         // Cambio: fuente -> source
  document_type: string;  // Cambio: tipo_documento -> document_type
  affiliation: string;    // Cambio: filiacion -> affiliation
  doi: string;
  categories: string;     // Cambio: categorias -> categories
}

export interface Autor {
  author_id: string;             // Cambio: id_autor -> author_id
  publications_list: Publicacion[]; // Cambio: lista_publicaciones -> publications_list
  error?: string;
}

export interface PublicacionesResponse {
  publications: Autor[];        // Cambio: publicaciones -> publications
}

export interface DocumentosPorAnioResponse {
  author_ids: string[];
  documents_by_year: Record<string, number>;  // Cambio: documentos_por_anio -> documents_by_year
}

export interface AreasTematicasResponse {
  author_ids: string[];
  subject_areas: string[];                    // Cambio: areas_tematicas -> subject_areas
}

// ===========================
// TIPOS LEGACY (mantener para compatibilidad)
// ===========================
export interface Department {
  sigla: string;
  nombre: string;
  facultad: string;
}

export interface DepartmentsResponse {
  success: boolean;
  data: Department[];
  message: string;
}

export interface Cargo {
  cargo: string;
  tiempo: string;
}

export interface CargosResponse {
  success: boolean;
  data: Cargo[];
  message: string;
}

// ===========================
// NUEVOS TIPOS REFACTORIZADOS
// ===========================

// Autor
export interface Author {
  author_id: string;
  name: string;
  surname: string;
  title: string;
  birth_date?: string;
  gender: string;
  position: string;
  department: string;
}

export interface AuthorCreateRequest {
  author_id: string;
  name: string;
  surname: string;
  title: string;
  birth_date?: string;
  gender: string;
  position: string;
  department: string;
}

export interface AuthorUpdateRequest {
  name?: string;
  surname?: string;
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
  title: string;
  birth_date?: string;
  gender: string;
  position: string;
  department: string;
}

export interface AuthorsResponse {
  authors: AuthorResponse[];
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

// Posición/Cargo (nuevo)
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

// Cuenta Scopus
export interface ScopusAccount {
  scopus_id: string;
  scopus_user: string;
  author_id: string;
}

export interface ScopusAccountCreateRequest {
  scopus_id: string;
  scopus_user: string;
  author_id: string;
}

export interface ScopusAccountUpdateRequest {
  scopus_user?: string;
  author_id?: string;
}

export interface ScopusAccountResponse {
  scopus_id: string;
  scopus_user: string;
  author_id: string;
}

export interface ScopusAccountsResponse {
  scopus_accounts: ScopusAccountResponse[];
}

export interface LinkAuthorScopusRequest {
  author_id: string;
  scopus_id: string;
  scopus_user?: string;
}

// Tipos para el estado del componente principal
export interface AppState {
  scopusIds: string[];
  isLoading: boolean;
  loadingProgress: string | null; // Para mostrar el progreso actual
  publicaciones: Publicacion[];
  areasTematicas: string[];
  documentosPorAnio: Record<string, number>;
  error: string | null;
}

// Tipo para validación de IDs
export interface ValidationResult {
  isValid: boolean;
  message?: string;
}
