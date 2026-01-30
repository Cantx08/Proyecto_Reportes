import axios from 'axios';
import type { 
  PublicationsResponse,
  DocumentsByYearResponse,
  SubjectAreasResponse,


} from '@/types/api';

export interface ReportRequest {
  author_ids: string[];
  docente_nombre: string;
  docente_genero: string; // Cambiado de 'M' | 'F' a string para permitir texto libre
  departamento: string;
  cargo: string;
  memorando?: string;
  firmante?: number | string; // Cambiado para permitir texto libre
  firmante_nombre?: string; // Nuevo campo para nombre de firmante personalizado
  fecha?: string;
  es_borrador?: boolean; // Nuevo campo para indicar si es borrador o certificado final
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutos timeout para consultas grandes con múltiples autores
  headers: {
    'Content-Type': 'application/json',
  },
});

export const scopusApi = {
  /**
   * Obtener publicaciones por ID de Scopus
   */
  async getPublications(authorIds: string[]): Promise<PublicationsResponse> {
    try {
      const params = new URLSearchParams();
      authorIds.forEach(id => params.append('ids', id));
      
      const response = await api.get<PublicationsResponse>(`/scopus/publications?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener publicaciones:', error);
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          throw new Error('La consulta está tomando más tiempo del esperado. Intente con menos IDs o espere un momento.');
        }
        if (error.response?.status === 500) {
          throw new Error('Error interno del servidor. Intente nuevamente en unos minutos.');
        }
      }
      throw new Error('Error al conectar con el servidor. Verifique su conexión.');
    }
  },

  /**
   * Obtener documentos por año
   */
  async getDocumentsByYear(authorIds: string[]): Promise<DocumentsByYearResponse> {
    try {
      const params = new URLSearchParams();
      authorIds.forEach(id => params.append('ids', id));
      
      const response = await api.get<DocumentsByYearResponse>(`/scopus/docs_by_year?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener documentos por año:', error);
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          throw new Error('Procesando documentos por año... La consulta está tomando más tiempo del esperado.');
        }
        if (error.response?.status === 500) {
          throw new Error('Error interno del servidor al procesar documentos por año.');
        }
      }
      throw new Error('Error al obtener estadísticas por año.');
    }
  },

  /**
   * Obtener áreas temáticas
   */
  async getSubjectAreas(authorIds: string[]): Promise<SubjectAreasResponse> {
    try {
      const params = new URLSearchParams();
      authorIds.forEach(id => params.append('ids', id));
      
      const response = await api.get<SubjectAreasResponse>(`/scopus/subject_areas?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener áreas temáticas:', error);
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          throw new Error('Procesando áreas temáticas... La consulta está tomando más tiempo del esperado.');
        }
        if (error.response?.status === 500) {
          throw new Error('Error interno del servidor al procesar áreas temáticas.');
        }
      }
      throw new Error('Error al obtener áreas temáticas.');
    }
  },
  /**
   * Generar reporte de certificación
   */
  async generateCertification(reportData: ReportRequest): Promise<Blob> {
    try {
      const response = await api.post('/reports/inform', reportData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Error al generar reporte:', error);
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          throw new Error('La generación del reporte está tomando más tiempo del esperado.');
        }
        if (error.response?.status === 500) {
          throw new Error('Error interno del servidor al generar el reporte.');
        }
        if (error.response?.status === 422) {
          throw new Error('Datos inválidos para generar el reporte. Verifique la información.');
        }
      }
      throw new Error('Error al generar el reporte.');
    }
  },

  /**
   * Procesar borrador PDF existente y convertirlo en certificado final
   */
  async procesarBorrador(
    file: File,
    metadata?: {
      memorando?: string;
      firmante?: number;
      firmante_nombre?: string;
      fecha?: string;
    }
  ): Promise<Blob> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      // Añadir metadatos opcionales si existen
      if (metadata) {
        if (metadata.memorando) formData.append('memorando', metadata.memorando);
        if (metadata.firmante) formData.append('firmante', metadata.firmante.toString());
        if (metadata.firmante_nombre) formData.append('firmante_nombre', metadata.firmante_nombre);
        if (metadata.fecha) formData.append('fecha', metadata.fecha);
      }

      const response = await api.post('/reports/process-draft', formData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Error al procesar borrador:', error);
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          throw new Error('El procesamiento del borrador está tomando más tiempo del esperado.');
        }
        if (error.response?.status === 400) {
          throw new Error('El archivo no es un PDF válido o excede el tamaño máximo (10MB).');
        }
        if (error.response?.status === 500) {
          throw new Error('Error interno del servidor al procesar el borrador.');
        }
      }
      throw new Error('Error al procesar el borrador PDF.');
    }
  }
};

export default scopusApi;
