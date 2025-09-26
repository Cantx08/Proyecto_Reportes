'use client';

import { useState, useEffect } from 'react';
import { scopusApi } from '@/services/scopusApi';
import type { Department } from '@/types/api';

interface UseDepartmentsReturn {
  departments: Department[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useDepartments = (): UseDepartmentsReturn => {
  const [departments, setDepartments] = useState<Department[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDepartments = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await scopusApi.getDepartments();
      
      if (response.success) {
        setDepartments(response.data);
      } else {
        setError(response.message || 'Error al obtener departamentos');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido al obtener departamentos';
      setError(errorMessage);
      console.error('Error fetching departments:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDepartments();
  }, []);

  return {
    departments,
    isLoading,
    error,
    refetch: fetchDepartments,
  };
};