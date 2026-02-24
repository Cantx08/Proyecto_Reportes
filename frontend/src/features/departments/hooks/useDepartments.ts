import {useCallback, useState} from 'react';
import {apiUtils} from '@/src/services/servicesApi';
import {DepartmentCreateRequest, DepartmentResponse, DepartmentUpdateRequest} from "@/src/features/departments/types";
import {departmentService} from "@/src/features/departments/services/departmentService";

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
  getDepartment: (dep_id: string) => Promise<DepartmentResponse | null>;
  getDepartmentsByFaculty: (faculty_name: string) => Promise<DepartmentResponse[]>;
  createDepartment: (departmentData: DepartmentCreateRequest) => Promise<DepartmentResponse | null>;
  updateDepartment: (dep_id: string, departmentData: DepartmentUpdateRequest) => Promise<DepartmentResponse | null>;
  deleteDepartment: (dep_id: string) => Promise<boolean>;
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
      const departments = await departmentService.getAll();
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
        departments: [],
      }));
    }
  }, []);

  const getDepartment = useCallback(async (dep_id: string): Promise<DepartmentResponse | null> => {
    try {
      return await departmentService.getById(dep_id);
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return null;
    }
  }, []);

  const getDepartmentsByFaculty = useCallback(async (faculty_name: string): Promise<DepartmentResponse[]> => {
    try {
      return await departmentService.getByFaculty(faculty_name);
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return [];
    }
  }, []);

  const createDepartment = useCallback(async (departmentData: DepartmentCreateRequest): Promise<DepartmentResponse | null> => {
    setState(prev => ({ ...prev, creating: true, error: null }));
    try {
      const newDepartment = await departmentService.create(departmentData);
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

  const updateDepartment = useCallback(async (dep_id: string, departmentData: DepartmentUpdateRequest): Promise<DepartmentResponse | null> => {
    setState(prev => ({ ...prev, updating: true, error: null }));
    try {
      const updatedDepartment = await departmentService.update(dep_id, departmentData);
      setState(prev => ({
        ...prev,
        departments: (prev.departments || []).map(dept => 
          dept.dep_id === dep_id ? updatedDepartment : dept
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

  const deleteDepartment = useCallback(async (dep_id: string): Promise<boolean> => {
    setState(prev => ({ ...prev, deleting: true, error: null }));
    try {
      await departmentService.delete(dep_id);
      setState(prev => ({
        ...prev,
        departments: (prev.departments || []).filter(dept => dept.dep_id !== dep_id),
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