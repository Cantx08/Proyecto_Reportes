import { useState, useEffect, useCallback } from 'react';
import { authorsApi, apiUtils } from '@/services/servicesApi';
import {
  Author,
  AuthorCreateRequest,
  AuthorResponse,
  AuthorsResponse,
  AuthorUpdateRequest
} from "@/features/authors/types";

export interface UseAuthorsState {
  authors: AuthorResponse[];
  loading: boolean;
  error: string | null;
  creating: boolean;
  updating: boolean;
  deleting: boolean;
}

export interface UseAuthorsActions {
  fetchAuthors: () => Promise<void>;
  getAuthor: (authorId: string) => Promise<AuthorResponse | null>;
  createAuthor: (authorData: AuthorCreateRequest) => Promise<AuthorResponse | null>;
  updateAuthor: (authorId: string, authorData: AuthorUpdateRequest) => Promise<AuthorResponse | null>;
  deleteAuthor: (authorId: string) => Promise<boolean>;
  clearError: () => void;
}

export function useAuthors(): UseAuthorsState & UseAuthorsActions {
  const [state, setState] = useState<UseAuthorsState>({
    authors: [],
    loading: false,
    error: null,
    creating: false,
    updating: false,
    deleting: false,
  });

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const fetchAuthors = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const response = await authorsApi.getAll();
      setState(prev => ({
        ...prev,
        authors: response?.authors || [],
        loading: false,
      }));
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage,
        authors: [], // Asegurar que authors sea un array vacío en caso de error
      }));
    }
  }, []);

  const getAuthor = useCallback(async (authorId: string): Promise<AuthorResponse | null> => {
    try {
      const author = await authorsApi.getById(authorId);
      return author;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return null;
    }
  }, []);

  const createAuthor = useCallback(async (authorData: AuthorCreateRequest): Promise<AuthorResponse | null> => {
    setState(prev => ({ ...prev, creating: true, error: null }));
    try {
      const newAuthor = await authorsApi.create(authorData);
      setState(prev => ({
        ...prev,
        authors: [...(prev.authors || []), newAuthor],
        creating: false,
      }));
      return newAuthor;
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

  const updateAuthor = useCallback(async (authorId: string, authorData: AuthorUpdateRequest): Promise<AuthorResponse | null> => {
    setState(prev => ({ ...prev, updating: true, error: null }));
    try {
      const updatedAuthor = await authorsApi.update(authorId, authorData);
      setState(prev => ({
        ...prev,
        authors: (prev.authors || []).map(author => 
          author.author_id === authorId ? updatedAuthor : author
        ),
        updating: false,
      }));
      return updatedAuthor;
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

  const deleteAuthor = useCallback(async (authorId: string): Promise<boolean> => {
    setState(prev => ({ ...prev, deleting: true, error: null }));
    try {
      await authorsApi.delete(authorId);
      setState(prev => ({
        ...prev,
        authors: (prev.authors || []).filter(author => author.author_id !== authorId),
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

  // Cargar autores al montar el componente
  useEffect(() => {
    fetchAuthors();
  }, [fetchAuthors]);

  return {
    ...state,
    fetchAuthors,
    getAuthor,
    createAuthor,
    updateAuthor,
    deleteAuthor,
    clearError,
  };
}