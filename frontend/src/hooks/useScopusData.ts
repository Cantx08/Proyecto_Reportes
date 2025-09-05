import { useState, useCallback } from 'react';
import type { AppState, ValidationResult } from '@/types/api';
import { scopusApi } from '@/services/scopusApi';

const initialState: AppState = {
  scopusIds: [''],
  isLoading: false,
  publicaciones: [],
  areasTematicas: [],
  documentosPorAnio: {},
  error: null,
};

export const useScopusData = () => {
  const [state, setState] = useState<AppState>(initialState);

  // Validar ID de Scopus (básico)
  const validateScopusId = useCallback((id: string): ValidationResult => {
    if (!id.trim()) {
      return { isValid: false, message: 'El ID no puede estar vacío.' };
    }
    
    // Validación básica: solo números y mínimo 8 dígitos
    const idPattern = /^[0-9]{8,}$/;
    if (!idPattern.test(id.trim())) {
      return { 
        isValid: false, 
        message: 'Debe tener al menos 8 dígitos numéricos.' 
      };
    }
    
    return { isValid: true };
  }, []);

  // Agregar nuevo campo de ID
  const addScopusId = useCallback(() => {
    setState(prev => ({
      ...prev,
      scopusIds: [...prev.scopusIds, '']
    }));
  }, []);

  // Remover campo de ID
  const removeScopusId = useCallback((index: number) => {
    setState(prev => ({
      ...prev,
      scopusIds: prev.scopusIds.filter((_, i) => i !== index)
    }));
  }, []);

  // Actualizar valor de ID específico
  const updateScopusId = useCallback((index: number, value: string) => {
    setState(prev => ({
      ...prev,
      scopusIds: prev.scopusIds.map((id, i) => i === index ? value : id)
    }));
  }, []);

  // Buscar datos de Scopus
  const searchScopusData = useCallback(async () => {
    // Validar IDs antes de enviar
    const validIds = state.scopusIds.filter(id => {
      const validation = validateScopusId(id);
      return validation.isValid;
    });

    if (validIds.length === 0) {
      setState(prev => ({
        ...prev,
        error: 'Debe ingresar al menos un ID válido de Scopus.'
      }));
      return;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Ejecutar todas las consultas en paralelo
      const [publicacionesResult, documentosResult, areasResult] = await Promise.all([
        scopusApi.getPublicaciones(validIds),
        scopusApi.getDocumentosPorAnio(validIds),
        scopusApi.getAreasTematicas(validIds)
      ]);

      // Combinar todas las publicaciones
      const todasPublicaciones = publicacionesResult.publicaciones
        .flatMap(autor => autor.lista_publicaciones);

      setState(prev => ({
        ...prev,
        publicaciones: todasPublicaciones,
        areasTematicas: areasResult.areas_tematicas,
        documentosPorAnio: documentosResult.documentos_por_anio,
        isLoading: false
      }));

    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Error desconocido.',
        isLoading: false
      }));
    }
  }, [state.scopusIds, validateScopusId]);

  // Limpiar resultados
  const clearResults = useCallback(() => {
    setState(initialState);
  }, []);

  return {
    ...state,
    validateScopusId,
    addScopusId,
    removeScopusId,
    updateScopusId,
    searchScopusData,
    clearResults,
  };
};
