import { useState, useCallback } from 'react';
import type { AppState, ValidationResult } from '@/types/api';
import { scopusApi } from '@/services/scopusApi';

const initialState: AppState = {
  scopusIds: [''],
  isLoading: false,
  loadingProgress: null,
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
    
    // Verificar si contiene caracteres no numéricos
    const hasNonNumericChars = /[^0-9]/.test(id.trim());
    if (hasNonNumericChars) {
      return { 
        isValid: false, 
        message: 'Solo se permiten dígitos. No se permiten letras, símbolos o espacios.' 
      };
    }
    
    // Validación de longitud: mínimo 8 dígitos
    if (id.trim().length < 8) {
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

    setState(prev => ({ ...prev, isLoading: true, error: null, loadingProgress: 'Iniciando consulta...' }));

    try {
      // Para consultas grandes, ejecutar secuencialmente para evitar timeouts
      console.log('Iniciando consulta con', validIds.length, 'IDs...');
      
      setState(prev => ({ ...prev, loadingProgress: 'Obteniendo publicaciones...' }));
      const publicacionesResult = await scopusApi.getPublicaciones(validIds);
      console.log('Publicaciones obtenidas:', publicacionesResult.publications.length);
      
      setState(prev => ({ ...prev, loadingProgress: 'Procesando documentos por año...' }));
      const documentosResult = await scopusApi.getDocumentosPorAnio(validIds);
      console.log('Documentos por año procesados');
      
      setState(prev => ({ ...prev, loadingProgress: 'Procesando áreas temáticas...' }));
      const areasResult = await scopusApi.getAreasTematicas(validIds);
      console.log('Áreas temáticas procesadas');

      // Combinar todas las publicaciones
      const todasPublicaciones = publicacionesResult.publications
        .flatMap(autor => autor.publications_list || []);

      setState(prev => ({
        ...prev,
        publicaciones: todasPublicaciones,
        areasTematicas: areasResult.subject_areas,
        documentosPorAnio: documentosResult.documents_by_year,
        isLoading: false,
        loadingProgress: null
      }));

    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Error desconocido.',
        isLoading: false,
        loadingProgress: null
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
