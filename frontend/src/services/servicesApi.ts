import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 segundos timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido, redirigir al login
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// ===============================
// SERVICIOS UTILITARIOS
// ===============================

export const apiUtils = {
  /**
   * Manejo de errores común para todas las APIs
   */
  handleError(error: unknown): string {
    if (axios.isAxiosError(error)) {
      if (error.response?.data?.detail) {
        return error.response.data.detail;
      }
      if (error.response?.status === 404) {
        return 'Recurso no encontrado';
      }
      if (error.response?.status === 500) {
        return 'Error interno del servidor';
      }
      if (error.code === 'ECONNABORTED') {
        return 'La operación tardó demasiado tiempo';
      }
    }
    return 'Error desconocido';
  },
};