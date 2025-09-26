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
