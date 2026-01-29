import {useCallback, useEffect, useState} from 'react';
import {apiUtils} from '@/services/servicesApi';
import {JobPositionCreateRequest, JobPositionResponse, JobPositionUpdateRequest} from "@/features/job-positions/types";
import {jobPositionService} from "@/features/job-positions/services/jobPositionService";

export interface UseJobPositionsState {
  positions: JobPositionResponse[];
  loading: boolean;
  error: string | null;
  creating: boolean;
  updating: boolean;
  deleting: boolean;
}

export interface UseJobPositionsActions {
  fetchPositions: () => Promise<void>;
  getPosition: (posId: string) => Promise<JobPositionResponse | null>;
  createPosition: (positionData: JobPositionCreateRequest) => Promise<JobPositionResponse | null>;
  updatePosition: (posId: string, positionData: JobPositionUpdateRequest) => Promise<JobPositionResponse | null>;
  deletePosition: (posId: string) => Promise<boolean>;
  clearError: () => void;
}

export function useJobPositions(): UseJobPositionsState & UseJobPositionsActions {
  const [state, setState] = useState<UseJobPositionsState>({
    positions: [],
    loading: false,
    error: null,
    creating: false,
    updating: false,
    deleting: false,
  });

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const fetchPositions = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const jobPositions = await jobPositionService.getAll();
      setState(prev => ({
        ...prev,
        positions: jobPositions || [],
        loading: false,
      }));
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage,
        positions: [],
      }));
    }
  }, []);

  const getPosition = useCallback(async (posId: string): Promise<JobPositionResponse | null> => {
    try {
      return await jobPositionService.getById(posId);
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return null;
    }
  }, []);

  const createPosition = useCallback(async (positionData: JobPositionCreateRequest): Promise<JobPositionResponse | null> => {
    setState(prev => ({ ...prev, creating: true, error: null }));
    try {
      const newPosition = await jobPositionService.create(positionData);
      setState(prev => ({
        ...prev,
        positions: [...(prev.positions || []), newPosition],
        creating: false,
      }));
      return newPosition;
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

  const updatePosition = useCallback(async (posId: string, positionData: JobPositionUpdateRequest): Promise<JobPositionResponse | null> => {
    setState(prev => ({ ...prev, updating: true, error: null }));
    try {
      const updatedPosition = await jobPositionService.update(posId, positionData);
      setState(prev => ({
        ...prev,
        positions: (prev.positions || []).map(pos => 
          pos.pos_id === posId ? updatedPosition : pos
        ),
        updating: false,
      }));
      return updatedPosition;
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

  const deletePosition = useCallback(async (posId: string): Promise<boolean> => {
    setState(prev => ({ ...prev, deleting: true, error: null }));
    try {
      await jobPositionService.delete(posId);
      setState(prev => ({
        ...prev,
        positions: (prev.positions || []).filter(pos => pos.pos_id !== posId),
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

  // Cargar posiciones al montar el componente
  useEffect(() => {
    fetchPositions();
  }, [fetchPositions]);

  return {
    ...state,
    fetchPositions,
    getPosition,
    createPosition,
    updatePosition,
    deletePosition,
    clearError,
  };
}