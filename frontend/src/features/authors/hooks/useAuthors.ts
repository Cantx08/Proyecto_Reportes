import {useCallback, useEffect, useState} from 'react';
import {apiUtils} from '@/services/servicesApi';
import {AuthorCreateRequest, AuthorResponse, AuthorUpdateRequest} from "@/features/authors/types";
import {authorService} from "@/features/authors/services/authorService";

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
  getAuthorsByDepartment: (depId: string) => Promise<AuthorResponse[]>;
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
      const authors = await authorService.getAll();
      setState(prev => ({
        ...prev,
        authors: authors || [],
        loading: false,
      }));
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage,
        authors: [],
      }));
    }
  }, []);

  const getAuthor = useCallback(async (authorId: string): Promise<AuthorResponse | null> => {
    try {
      return await authorService.getById(authorId);
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return null;
    }
  }, []);

  const getAuthorsByDepartment = useCallback(async (depId: string): Promise<AuthorResponse[]> => {
    try {
      return await authorService.getByDepartment(depId);
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return [];
    }
  }, []);

  const createAuthor = useCallback(async (authorData: AuthorCreateRequest): Promise<AuthorResponse | null> => {
    setState(prev => ({ ...prev, creating: true, error: null }));
    try {
      const newAuthor = await authorService.create(authorData);
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
      const updatedAuthor = await authorService.update(authorId, authorData);
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
      await authorService.delete(authorId);
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
    getAuthorsByDepartment,
    createAuthor,
    updateAuthor,
    deleteAuthor,
    clearError,
  };
}