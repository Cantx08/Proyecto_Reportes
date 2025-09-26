import axios from 'axios';
import type { 
  PublicacionesResponse, 
  DocumentosPorAnioResponse, 
  AreasTematicasResponse,
  DepartmentsResponse,
  CargosResponse 
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
  timeout: 120000, // 2 minutos timeout para consultas grandes
  headers: {
    'Content-Type': 'application/json',
  },
});

export const scopusApi = {
  /**
   * Obtener publicaciones por IDs de Scopus
   */
  async getPublicaciones(authorIds: string[]): Promise<PublicacionesResponse> {
    try {
      const params = new URLSearchParams();
      authorIds.forEach(id => params.append('ids', id));
      
      const response = await api.get<PublicacionesResponse>(`/scopus/publications?${params.toString()}`);
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
  async getDocumentosPorAnio(authorIds: string[]): Promise<DocumentosPorAnioResponse> {
    try {
      const params = new URLSearchParams();
      authorIds.forEach(id => params.append('ids', id));
      
      const response = await api.get<DocumentosPorAnioResponse>(`/scopus/docs_by_year?${params.toString()}`);
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
  async getAreasTematicas(authorIds: string[]): Promise<AreasTematicasResponse> {
    try {
      const params = new URLSearchParams();
      authorIds.forEach(id => params.append('ids', id));
      
      const response = await api.get<AreasTematicasResponse>(`/scopus/subject_areas?${params.toString()}`);
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
   * Obtener lista de departamentos
   */
  async getDepartments(): Promise<DepartmentsResponse> {
    try {
      const response = await api.get<DepartmentsResponse>('/departments');
      return response.data;
    } catch (error) {
      console.error('Error al obtener departamentos:', error);
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 500) {
          throw new Error('Error interno del servidor al obtener departamentos.');
        }
      }
      throw new Error('Error al conectar con el servidor para obtener departamentos.');
    }
  },

  /**
   * Obtener lista de cargos
   */
  async getCargos(): Promise<CargosResponse> {
    try {
      const response = await api.get<CargosResponse>('/cargos');
      return response.data;
    } catch (error) {
      console.error('Error al obtener cargos:', error);
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 500) {
          throw new Error('Error interno del servidor al obtener cargos.');
        }
      }
      throw new Error('Error al conectar con el servidor para obtener cargos.');
    }
  },

  /**
   * Generar reporte de certificación
   */
  async generarReporte(reportData: ReportRequest): Promise<Blob> {
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
  }
};

export default scopusApi;
