'use client';

import { useState, useEffect } from 'react';
import { scopusApi } from '@/services/scopusApi';
import type { Cargo } from '@/types/api';

interface UseCargosReturn {
  cargos: Cargo[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useCargos = (): UseCargosReturn => {
  const [cargos, setCargos] = useState<Cargo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCargos = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await scopusApi.getCargos();
      
      if (response.success) {
        setCargos(response.data);
      } else {
        setError(response.message || 'Error al obtener cargos');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido al obtener cargos';
      setError(errorMessage);
      console.error('Error fetching cargos:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCargos();
  }, []);

  return {
    cargos,
    isLoading,
    error,
    refetch: fetchCargos,
  };
};