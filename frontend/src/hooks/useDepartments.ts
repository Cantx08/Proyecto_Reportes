import { useState, useEffect, useCallback } from 'react';
import { newDepartmentsApi, apiUtils } from '@/services/servicesApi';
import type { 
  DepartmentResponse, 
  DepartmentCreateRequest, 
  DepartmentUpdateRequest 
} from '@/types/api';

export interface UseDepartmentsState {
  departments: DepartmentResponse[];
  loading: boolean;
  error: string | null;
  creating: boolean;
  updating: boolean;
  deleting: boolean;
}

export interface UseDepartmentsActions {
  fetchDepartments: () => Promise<void>;
  getDepartment: (depId: string) => Promise<DepartmentResponse | null>;
  getDepartmentsByFaculty: (facName: string) => Promise<DepartmentResponse[]>;
  createDepartment: (departmentData: DepartmentCreateRequest) => Promise<DepartmentResponse | null>;
  updateDepartment: (depId: string, departmentData: DepartmentUpdateRequest) => Promise<DepartmentResponse | null>;
  deleteDepartment: (depId: string) => Promise<boolean>;
  clearError: () => void;
}

export function useDepartments(): UseDepartmentsState & UseDepartmentsActions {
  const [state, setState] = useState<UseDepartmentsState>({
    departments: [],
    loading: false,
    error: null,
    creating: false,
    updating: false,
    deleting: false,
  });

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const fetchDepartments = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const departments = await newDepartmentsApi.getAll();
      setState(prev => ({
        ...prev,
        departments: departments || [],
        loading: false,
      }));
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage,
        departments: [], // Asegurar que departments sea un array vacío en caso de error
      }));
    }
  }, []);

  const getDepartment = useCallback(async (depId: string): Promise<DepartmentResponse | null> => {
    try {
      const department = await newDepartmentsApi.getById(depId);
      return department;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return null;
    }
  }, []);

  const getDepartmentsByFaculty = useCallback(async (facName: string): Promise<DepartmentResponse[]> => {
    try {
      const departments = await newDepartmentsApi.getByFaculty(facName);
      return departments;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return [];
    }
  }, []);

  const createDepartment = useCallback(async (departmentData: DepartmentCreateRequest): Promise<DepartmentResponse | null> => {
    setState(prev => ({ ...prev, creating: true, error: null }));
    try {
      const newDepartment = await newDepartmentsApi.create(departmentData);
      setState(prev => ({
        ...prev,
        departments: [...(prev.departments || []), newDepartment],
        creating: false,
      }));
      return newDepartment;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        creating: false,
        error: errorMessage,
      }));
      return null;
    }
  }, []);

  const updateDepartment = useCallback(async (depId: string, departmentData: DepartmentUpdateRequest): Promise<DepartmentResponse | null> => {
    setState(prev => ({ ...prev, updating: true, error: null }));
    try {
      const updatedDepartment = await newDepartmentsApi.update(depId, departmentData);
      setState(prev => ({
        ...prev,
        departments: (prev.departments || []).map(dept => 
          dept.dep_id === depId ? updatedDepartment : dept
        ),
        updating: false,
      }));
      return updatedDepartment;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        updating: false,
        error: errorMessage,
      }));
      return null;
    }
  }, []);

  const deleteDepartment = useCallback(async (depId: string): Promise<boolean> => {
    setState(prev => ({ ...prev, deleting: true, error: null }));
    try {
      await newDepartmentsApi.delete(depId);
      setState(prev => ({
        ...prev,
        departments: (prev.departments || []).filter(dept => dept.dep_id !== depId),
        deleting: false,
      }));
      return true;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        deleting: false,
        error: errorMessage,
      }));
      return false;
    }
  }, []);

  // Cargar departamentos al montar el componente
  useEffect(() => {
    fetchDepartments();
  }, [fetchDepartments]);

  return {
    ...state,
    fetchDepartments,
    getDepartment,
    getDepartmentsByFaculty,
    createDepartment,
    updateDepartment,
    deleteDepartment,
    clearError,
  };
}