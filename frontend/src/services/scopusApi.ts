import axios from 'axios';

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


