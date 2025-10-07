import { useState, useEffect, useCallback } from 'react';
import { positionsApi, apiUtils } from '@/services/newApi';
import type { 
  PositionResponse, 
  PositionsResponse,
  PositionCreateRequest, 
  PositionUpdateRequest 
} from '@/types/api';

export interface UsePositionsState {
  positions: PositionResponse[];
  loading: boolean;
  error: string | null;
  creating: boolean;
  updating: boolean;
  deleting: boolean;
}

export interface UsePositionsActions {
  fetchPositions: () => Promise<void>;
  getPosition: (posId: string) => Promise<PositionResponse | null>;
  createPosition: (positionData: PositionCreateRequest) => Promise<PositionResponse | null>;
  updatePosition: (posId: string, positionData: PositionUpdateRequest) => Promise<PositionResponse | null>;
  deletePosition: (posId: string) => Promise<boolean>;
  clearError: () => void;
}

export function usePositions(): UsePositionsState & UsePositionsActions {
  const [state, setState] = useState<UsePositionsState>({
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
      const response = await positionsApi.getAll();
      setState(prev => ({
        ...prev,
        positions: response.positions,
        loading: false,
      }));
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage,
      }));
    }
  }, []);

  const getPosition = useCallback(async (posId: string): Promise<PositionResponse | null> => {
    try {
      const position = await positionsApi.getById(posId);
      return position;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return null;
    }
  }, []);

  const createPosition = useCallback(async (positionData: PositionCreateRequest): Promise<PositionResponse | null> => {
    setState(prev => ({ ...prev, creating: true, error: null }));
    try {
      const newPosition = await positionsApi.create(positionData);
      setState(prev => ({
        ...prev,
        positions: [...prev.positions, newPosition],
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

  const updatePosition = useCallback(async (posId: string, positionData: PositionUpdateRequest): Promise<PositionResponse | null> => {
    setState(prev => ({ ...prev, updating: true, error: null }));
    try {
      const updatedPosition = await positionsApi.update(posId, positionData);
      setState(prev => ({
        ...prev,
        positions: prev.positions.map(pos => 
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
      await positionsApi.delete(posId);
      setState(prev => ({
        ...prev,
        positions: prev.positions.filter(pos => pos.pos_id !== posId),
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