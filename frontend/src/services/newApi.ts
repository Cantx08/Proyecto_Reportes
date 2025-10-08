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

// ===============================
// SERVICIOS PARA AUTORES
// ===============================

export const authorsApi = {
  /**
   * Obtener todos los autores
   */
  async getAll(): Promise<AuthorsResponse> {
    const response = await api.get<AuthorsResponse>('/authors');
    return response.data;
  },

  /**
   * Obtener un autor por ID
   */
  async getById(authorId: string): Promise<AuthorResponse> {
    const response = await api.get<AuthorResponse>(`/authors/${authorId}`);
    return response.data;
  },

  /**
   * Crear un nuevo autor
   */
  async create(authorData: AuthorCreateRequest): Promise<AuthorResponse> {
    const response = await api.post<AuthorResponse>('/authors', authorData);
    return response.data;
  },

  /**
   * Actualizar un autor existente
   */
  async update(authorId: string, authorData: AuthorUpdateRequest): Promise<AuthorResponse> {
    const response = await api.put<AuthorResponse>(`/authors/${authorId}`, authorData);
    return response.data;
  },

  /**
   * Eliminar un autor
   */
  async delete(authorId: string): Promise<{ message: string }> {
    const response = await api.delete(`/authors/${authorId}`);
    return response.data;
  },
};

// ===============================
// SERVICIOS PARA DEPARTAMENTOS NUEVOS
// ===============================

export const newDepartmentsApi = {
  /**
   * Obtener todos los departamentos
   */
  async getAll(): Promise<DepartmentResponse[]> {
    const response = await api.get<DepartmentResponse[]>('/new-departments');
    return response.data;
  },

  /**
   * Obtener un departamento por ID
   */
  async getById(depId: string): Promise<DepartmentResponse> {
    const response = await api.get<DepartmentResponse>(`/new-departments/${depId}`);
    return response.data;
  },

  /**
   * Obtener departamentos por facultad
   */
  async getByFaculty(facName: string): Promise<DepartmentResponse[]> {
    const response = await api.get<DepartmentResponse[]>(`/new-departments/faculty/${facName}`);
    return response.data;
  },

  /**
   * Crear un nuevo departamento
   */
  async create(departmentData: DepartmentCreateRequest): Promise<DepartmentResponse> {
    const response = await api.post<DepartmentResponse>('/new-departments', departmentData);
    return response.data;
  },

  /**
   * Actualizar un departamento existente
   */
  async update(depId: string, departmentData: DepartmentUpdateRequest): Promise<DepartmentResponse> {
    const response = await api.put<DepartmentResponse>(`/new-departments/${depId}`, departmentData);
    return response.data;
  },

  /**
   * Eliminar un departamento
   */
  async delete(depId: string): Promise<{ message: string }> {
    const response = await api.delete(`/new-departments/${depId}`);
    return response.data;
  },
};

// ===============================
// SERVICIOS PARA POSICIONES
// ===============================

export const positionsApi = {
  /**
   * Obtener todas las posiciones
   */
  async getAll(): Promise<PositionsResponse> {
    const response = await api.get<PositionsResponse>('/positions');
    return response.data;
  },

  /**
   * Obtener una posición por ID
   */
  async getById(posId: string): Promise<PositionResponse> {
    const response = await api.get<PositionResponse>(`/positions/${posId}`);
    return response.data;
  },

  /**
   * Crear una nueva posición
   */
  async create(positionData: PositionCreateRequest): Promise<PositionResponse> {
    const response = await api.post<PositionResponse>('/positions', positionData);
    return response.data;
  },

  /**
   * Actualizar una posición existente
   */
  async update(posId: string, positionData: PositionUpdateRequest): Promise<PositionResponse> {
    const response = await api.put<PositionResponse>(`/positions/${posId}`, positionData);
    return response.data;
  },

  /**
   * Eliminar una posición
   */
  async delete(posId: string): Promise<{ message: string }> {
    const response = await api.delete(`/positions/${posId}`);
    return response.data;
  },
};

// ===============================
// SERVICIOS PARA CUENTAS SCOPUS
// ===============================

export const scopusAccountsApi = {
  /**
   * Obtener todas las cuentas Scopus
   */
  async getAll(): Promise<ScopusAccountsResponse> {
    const response = await api.get<ScopusAccountsResponse>('/scopus-accounts');
    return response.data;
  },

  /**
   * Obtener una cuenta Scopus por ID
   */
  async getById(scopusId: string): Promise<ScopusAccountResponse> {
    const response = await api.get<ScopusAccountResponse>(`/scopus-accounts/${scopusId}`);
    return response.data;
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
    const response = await api.post<ScopusAccountResponse>('/scopus-accounts', accountData);
    return response.data;
  },

  /**
   * Actualizar una cuenta Scopus existente
   */
  async update(scopusId: string, accountData: ScopusAccountUpdateRequest): Promise<ScopusAccountResponse> {
    const response = await api.put<ScopusAccountResponse>(`/scopus-accounts/${scopusId}`, accountData);
    return response.data;
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
    const response = await api.post<ScopusAccountResponse>('/scopus-accounts/link', linkData);
    return response.data;
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