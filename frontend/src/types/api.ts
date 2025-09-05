// Tipos para las respuestas de la API del backend

export interface Publicacion {
  titulo: string;
  anio: string;
  fuente: string;
  tipo_documento: string;
  filiacion: string;
  doi: string;
  categorias: string;
}

export interface Autor {
  id_autor: string;
  lista_publicaciones: Publicacion[];
  error?: string;
}

export interface PublicacionesResponse {
  publicaciones: Autor[];
}

export interface DocumentosPorAnioResponse {
  author_ids: string[];
  documentos_por_anio: Record<string, number>;
}

export interface AreasTematicasResponse {
  author_ids: string[];
  areas_tematicas: string[];
}

// Tipos para el estado del componente principal
export interface AppState {
  scopusIds: string[];
  isLoading: boolean;
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
