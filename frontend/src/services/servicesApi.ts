import axios from 'axios';
import type {
  // Autores
  Author,
  AuthorCreateRequest,
  AuthorUpdateRequest,
  AuthorResponse,
  AuthorsResponse,
  // Departamentos
  NewDepartment,
  DepartmentCreateRequest,
  DepartmentUpdateRequest,
  DepartmentResponse,
  // Posiciones
  Position,
  PositionCreateRequest,
  PositionUpdateRequest,
  PositionResponse,
  PositionsResponse,
  // Cuentas Scopus
  ScopusAccount,
  ScopusAccountCreateRequest,
  ScopusAccountUpdateRequest,
  ScopusAccountResponse,
  ScopusAccountsResponse,
  LinkAuthorScopusRequest
} from '@/types/api';

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
// SERVICIOS PARA AUTORES
// ===============================

// Tipo de respuesta del backend para autores
interface BackendAuthorResponse {
  success: boolean;
  data: AuthorResponse;
  message: string;
}

interface BackendAuthorsResponse {
  success: boolean;
  data: AuthorResponse[];
  message: string;
  total: number;
}

export const authorsApi = {
  /**
   * Obtener todos los autores
   */
  async getAll(): Promise<AuthorsResponse> {
    const response = await api.get<BackendAuthorsResponse>('/authors');
    // Transformar la respuesta del backend al formato esperado por el frontend
    return {
      authors: response.data.data || []
    };
  },

  /**
   * Obtener un autor por ID
   */
  async getById(authorId: string): Promise<AuthorResponse> {
    const response = await api.get<BackendAuthorResponse>(`/authors/${authorId}`);
    return response.data.data;
  },

  /**
   * Crear un nuevo autor
   */
  async create(authorData: AuthorCreateRequest): Promise<AuthorResponse> {
    const response = await api.post<BackendAuthorResponse>('/authors', authorData);
    return response.data.data;
  },

  /**
   * Actualizar un autor existente
   */
  async update(authorId: string, authorData: AuthorUpdateRequest): Promise<AuthorResponse> {
    const response = await api.put<BackendAuthorResponse>(`/authors/${authorId}`, authorData);
    return response.data.data;
  },

  /**
   * Eliminar un autor
   */
  async delete(authorId: string): Promise<{ message: string }> {
    const response = await api.delete<BackendAuthorResponse>(`/authors/${authorId}`);
    return { message: response.data.message };
  },
};

// ===============================
// SERVICIOS PARA DEPARTAMENTOS
// ===============================

// Tipo de respuesta del backend para departamentos
interface BackendDepartmentResponse {
  success: boolean;
  data: DepartmentResponse;
  message: string;
}

interface BackendDepartmentsResponse {
  success: boolean;
  data: DepartmentResponse[];
  message: string;
  total: number;
}

export const newDepartmentsApi = {
  /**
   * Obtener todos los departamentos
   */
  async getAll(): Promise<DepartmentResponse[]> {
    const response = await api.get<BackendDepartmentsResponse>('/departments');
    return response.data.data || [];
  },

  /**
   * Obtener un departamento por ID
   */
  async getById(depId: string): Promise<DepartmentResponse> {
    const response = await api.get<BackendDepartmentResponse>(`/departments/${depId}`);
    return response.data.data;
  },

  /**
   * Obtener departamentos por facultad
   */
  async getByFaculty(facName: string): Promise<DepartmentResponse[]> {
    const response = await api.get<DepartmentResponse[]>(`/departments/faculty/${facName}`);
    // Este endpoint puede devolver directamente el array o estructura anidada
    return Array.isArray(response.data) ? response.data : [];
  },

  /**
   * Crear un nuevo departamento
   */
  async create(departmentData: DepartmentCreateRequest): Promise<DepartmentResponse> {
    const response = await api.post<BackendDepartmentResponse>('/departments', departmentData);
    return response.data.data;
  },

  /**
   * Actualizar un departamento existente
   */
  async update(depId: string, departmentData: DepartmentUpdateRequest): Promise<DepartmentResponse> {
    const response = await api.put<BackendDepartmentResponse>(`/departments/${depId}`, departmentData);
    return response.data.data;
  },

  /**
   * Eliminar un departamento
   */
  async delete(depId: string): Promise<{ message: string }> {
    const response = await api.delete<BackendDepartmentResponse>(`/departments/${depId}`);
    return { message: response.data.message };
  },
};

// ===============================
// SERVICIOS PARA POSICIONES
// ===============================

// Tipo de respuesta del backend para posiciones
interface BackendPositionResponse {
  success: boolean;
  data: PositionResponse;
  message: string;
}

interface BackendPositionsResponse {
  success: boolean;
  data: PositionResponse[];
  message: string;
  total: number;
}

export const positionsApi = {
  /**
   * Obtener todas las posiciones
   */
  async getAll(): Promise<PositionsResponse> {
    const response = await api.get<BackendPositionsResponse>('/positions');
    return {
      positions: response.data.data || []
    };
  },

  /**
   * Obtener una posición por ID
   */
  async getById(posId: string): Promise<PositionResponse> {
    const response = await api.get<BackendPositionResponse>(`/positions/${posId}`);
    return response.data.data;
  },

  /**
   * Crear una nueva posición
   */
  async create(positionData: PositionCreateRequest): Promise<PositionResponse> {
    const response = await api.post<BackendPositionResponse>('/positions', positionData);
    return response.data.data;
  },

  /**
   * Actualizar una posición existente
   */
  async update(posId: string, positionData: PositionUpdateRequest): Promise<PositionResponse> {
    const response = await api.put<BackendPositionResponse>(`/positions/${posId}`, positionData);
    return response.data.data;
  },

  /**
   * Eliminar una posición
   */
  async delete(posId: string): Promise<{ message: string }> {
    const response = await api.delete<BackendPositionResponse>(`/positions/${posId}`);
    return { message: response.data.message };
  },
};

// ===============================
// SERVICIOS PARA CUENTAS SCOPUS
// ===============================

export const scopusAccountsApi = {
  /**
   * Obtener todas las cuentas Scopus
   */
  async getAll(): Promise<ScopusAccountResponse[]> {
    const response = await api.get<ScopusAccountsResponse>('/scopus-accounts');
    return response.data.data; // Retornar directamente el array de cuentas
  },

  /**
   * Obtener una cuenta Scopus por ID
   */
  async getById(scopusId: string): Promise<ScopusAccountResponse> {
    const response = await api.get<{ success: boolean; data: ScopusAccountResponse; message: string }>(`/scopus-accounts/${scopusId}`);
    return response.data.data; // Acceder a la propiedad 'data' de la respuesta estructurada
  },

  /**
   * Obtener cuentas Scopus por autor
   */
  async getByAuthor(authorId: string): Promise<ScopusAccountResponse[]> {
    const response = await api.get<ScopusAccountsResponse>(`/scopus-accounts/by-author/${authorId}`);
    return response.data.data; // Acceder a la propiedad 'data' de la respuesta estructurada
  },

  /**
   * Crear una nueva cuenta Scopus
   */
  async create(accountData: ScopusAccountCreateRequest): Promise<ScopusAccountResponse> {
    const response = await api.post<{ success: boolean; data: ScopusAccountResponse; message: string }>('/scopus-accounts', accountData);
    return response.data.data; // Acceder a la propiedad 'data' de la respuesta estructurada
  },

  /**
   * Actualizar una cuenta Scopus existente
   */
  async update(scopusId: string, accountData: ScopusAccountUpdateRequest): Promise<ScopusAccountResponse> {
    const response = await api.put<{ success: boolean; data: ScopusAccountResponse; message: string }>(`/scopus-accounts/${scopusId}`, accountData);
    return response.data.data; // Acceder a la propiedad 'data' de la respuesta estructurada
  },

  /**
   * Eliminar una cuenta Scopus
   */
  async delete(scopusId: string): Promise<{ message: string }> {
    const response = await api.delete(`/scopus-accounts/${scopusId}`);
    return response.data;
  },

  /**
   * Vincular un autor con una cuenta Scopus
   */
  async linkAuthor(linkData: LinkAuthorScopusRequest): Promise<ScopusAccountResponse> {
    const response = await api.post<{ success: boolean; data: ScopusAccountResponse; message: string }>('/scopus-accounts/link', linkData);
    return response.data.data; // Acceder a la propiedad 'data' de la respuesta estructurada
  },

  /**
   * Obtener todos los IDs de Scopus disponibles
   */
  async getAllScopusIds(): Promise<string[]> {
    const response = await api.get<string[]>('/scopus-accounts/author-ids');
    return response.data;
  },
};

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