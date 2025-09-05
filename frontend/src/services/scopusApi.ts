import axios from 'axios';
import type { 
  PublicacionesResponse, 
  DocumentosPorAnioResponse, 
  AreasTematicasResponse 
} from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 segundos timeout
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
      throw new Error('Error al obtener áreas temáticas.');
    }
  }
};

export default scopusApi;
