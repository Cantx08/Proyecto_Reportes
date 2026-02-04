import { useState, useCallback } from 'react';
import type { AppState, ValidationResult } from '@/src/types/api';
import { publicationService } from "@/src/features/publications/services/publicationService";
import { Publication } from "@/src/features/publications/types";

const initialState: AppState = {
  scopusIds: [''],
  isLoading: false,
  loadingProgress: null,
  publications: [],
  subjectAreas: [],
  documentsByYear: {},
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

  /**
   * Extrae áreas temáticas únicas de las publicaciones
   */
  const extractSubjectAreas = (publications: Publication[]): string[] => {
    const areasSet = new Set<string>();
    publications.forEach(pub => {
      pub.subject_areas?.forEach(area => areasSet.add(area));
    });
    return Array.from(areasSet).sort();
  };

  /**
   * Calcula documentos por año de las publicaciones
   */
  const calculateDocumentsByYear = (publications: Publication[]): Record<string, number> => {
    const byYear: Record<string, number> = {};
    publications.forEach(pub => {
      const year = String(pub.year);
      byYear[year] = (byYear[year] || 0) + 1;
    });
    return byYear;
  };

  // Buscar datos de Scopus
  const searchScopusData = useCallback(async (mixedIds?: string[]) => {
    // Si se pasan IDS mixtos, usarlos. Si no, usar los del estado
    const idsToSearch = mixedIds || state.scopusIds;
    
    // Separar IDs: UUIDs (author_id) vs numéricos (Scopus ID)
    const authorIds: string[] = [];
    const scopusIds: string[] = [];
    
    idsToSearch.forEach(id => {
      const trimmedId = id.trim();
      if (!trimmedId) return;
      
      // UUID format check (para author_id del sistema)
      if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(trimmedId)) {
        authorIds.push(trimmedId);
      }
      // Scopus ID (numérico)
      else if (/^\d{8,}$/.test(trimmedId)) {
        scopusIds.push(trimmedId);
      }
    });

    if (authorIds.length === 0 && scopusIds.length === 0) {
      setState(prev => ({
        ...prev,
        error: 'Debe ingresar al menos un ID válido de Scopus o seleccionar un autor.'
      }));
      return;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null, loadingProgress: 'Iniciando consulta...' }));

    try {
      let allPublications: Publication[] = [];

      // Procesar Author IDS (usando el nuevo endpoint)
      for (const authorId of authorIds) {
        setState(prev => ({ 
          ...prev, 
          loadingProgress: `Obteniendo publicaciones del autor (esto puede tardar varios minutos)...` 
        }));
        try {
          const response = await publicationService.getByAuthor(authorId);
          allPublications = [...allPublications, ...response.publications];
        } catch (error) {
          console.error(`Error al obtener publicaciones del autor ${authorId}:`, error);
          // Propagar el error con un mensaje más claro
          const errorMessage = error instanceof Error 
            ? error.message 
            : 'Error al obtener publicaciones del autor';
          setState(prev => ({
            ...prev,
            error: errorMessage,
            isLoading: false,
            loadingProgress: null
          }));
          return; // Detener la ejecución si hay error
        }
      }

      // Procesar Scopus IDS directamente
      for (const scopusId of scopusIds) {
        setState(prev => ({ 
          ...prev, 
          loadingProgress: `Obteniendo publicaciones de Scopus ID ${scopusId}...` 
        }));
        try {
          const publications = await publicationService.getByScopusId(scopusId);
          allPublications = [...allPublications, ...publications];
        } catch (error) {
          console.error(`Error al obtener publicaciones de Scopus ID ${scopusId}:`, error);
          // Continuar con el siguiente ID en caso de error
        }
      }

      // Eliminar duplicados por scopus_id
      const uniquePublications = allPublications.reduce((acc, pub) => {
        if (!acc.find(p => p.scopus_id === pub.scopus_id)) {
          acc.push(pub);
        }
        return acc;
      }, [] as Publication[]);

      // Extraer datos derivados
      const subjectAreas = extractSubjectAreas(uniquePublications);
      const documentsByYear = calculateDocumentsByYear(uniquePublications);

      setState(prev => ({
        ...prev,
        publications: uniquePublications,
        subjectAreas,
        documentsByYear,
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
  }, [state.scopusIds]);

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
