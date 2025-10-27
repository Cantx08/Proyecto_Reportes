import { useState, useEffect, useCallback } from 'react';
import { scopusAccountsApi, apiUtils } from '@/services/servicesApi';
import type { 
  ScopusAccountResponse, 
  ScopusAccountsResponse,
  ScopusAccountCreateRequest, 
  ScopusAccountUpdateRequest,
  LinkAuthorScopusRequest
} from '@/types/api';

export interface UseScopusAccountsState {
  accounts: ScopusAccountResponse[];
  scopusIds: string[];
  loading: boolean;
  error: string | null;
  creating: boolean;
  updating: boolean;
  deleting: boolean;
  linking: boolean;
}

export interface UseScopusAccountsActions {
  fetchAccounts: () => Promise<void>;
  fetchScopusIds: () => Promise<void>;
  getAccount: (scopusId: string) => Promise<ScopusAccountResponse | null>;
  getAccountsByAuthor: (authorId: string) => Promise<ScopusAccountResponse[]>;
  createAccount: (accountData: ScopusAccountCreateRequest) => Promise<ScopusAccountResponse | null>;
  updateAccount: (scopusId: string, accountData: ScopusAccountUpdateRequest) => Promise<ScopusAccountResponse | null>;
  deleteAccount: (scopusId: string) => Promise<boolean>;
  linkAuthorScopus: (linkData: LinkAuthorScopusRequest) => Promise<ScopusAccountResponse | null>;
  clearError: () => void;
}

export function useScopusAccounts(): UseScopusAccountsState & UseScopusAccountsActions {
  const [state, setState] = useState<UseScopusAccountsState>({
    accounts: [],
    scopusIds: [],
    loading: false,
    error: null,
    creating: false,
    updating: false,
    deleting: false,
    linking: false,
  });

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const fetchAccounts = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const response = await scopusAccountsApi.getAll();
      setState(prev => ({
        ...prev,
        accounts: response.scopus_accounts,
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

  const fetchScopusIds = useCallback(async () => {
    try {
      const scopusIds = await scopusAccountsApi.getAllScopusIds();
      setState(prev => ({
        ...prev,
        scopusIds,
      }));
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
    }
  }, []);

  const getAccount = useCallback(async (scopusId: string): Promise<ScopusAccountResponse | null> => {
    try {
      const account = await scopusAccountsApi.getById(scopusId);
      return account;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return null;
    }
  }, []);

  const getAccountsByAuthor = useCallback(async (authorId: string): Promise<ScopusAccountResponse[]> => {
    try {
      const accounts = await scopusAccountsApi.getByAuthor(authorId);
      return accounts;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({ ...prev, error: errorMessage }));
      return [];
    }
  }, []);

  const createAccount = useCallback(async (accountData: ScopusAccountCreateRequest): Promise<ScopusAccountResponse | null> => {
    setState(prev => ({ ...prev, creating: true, error: null }));
    try {
      const newAccount = await scopusAccountsApi.create(accountData);
      setState(prev => ({
        ...prev,
        accounts: [...prev.accounts, newAccount],
        creating: false,
      }));
      return newAccount;
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

  const updateAccount = useCallback(async (scopusId: string, accountData: ScopusAccountUpdateRequest): Promise<ScopusAccountResponse | null> => {
    setState(prev => ({ ...prev, updating: true, error: null }));
    try {
      const updatedAccount = await scopusAccountsApi.update(scopusId, accountData);
      setState(prev => ({
        ...prev,
        accounts: prev.accounts.map(account => 
          account.scopus_id === scopusId ? updatedAccount : account
        ),
        updating: false,
      }));
      return updatedAccount;
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

  const deleteAccount = useCallback(async (scopusId: string): Promise<boolean> => {
    setState(prev => ({ ...prev, deleting: true, error: null }));
    try {
      await scopusAccountsApi.delete(scopusId);
      setState(prev => ({
        ...prev,
        accounts: prev.accounts.filter(account => account.scopus_id !== scopusId),
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

  const linkAuthorScopus = useCallback(async (linkData: LinkAuthorScopusRequest): Promise<ScopusAccountResponse | null> => {
    setState(prev => ({ ...prev, linking: true, error: null }));
    try {
      const linkedAccount = await scopusAccountsApi.linkAuthor(linkData);
      // Actualizar la cuenta existente o agregar nueva
      setState(prev => {
        const existingIndex = prev.accounts.findIndex(account => account.scopus_id === linkedAccount.scopus_id);
        if (existingIndex >= 0) {
          // Actualizar existente
          const newAccounts = [...prev.accounts];
          newAccounts[existingIndex] = linkedAccount;
          return { ...prev, accounts: newAccounts, linking: false };
        } else {
          // Agregar nueva
          return { ...prev, accounts: [...prev.accounts, linkedAccount], linking: false };
        }
      });
      return linkedAccount;
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      setState(prev => ({
        ...prev,
        linking: false,
        error: errorMessage,
      }));
      return null;
    }
  }, []);

  // Cargar cuentas y IDs al montar el componente
  useEffect(() => {
    fetchAccounts();
    fetchScopusIds();
  }, [fetchAccounts, fetchScopusIds]);

  return {
    ...state,
    fetchAccounts,
    fetchScopusIds,
    getAccount,
    getAccountsByAuthor,
    createAccount,
    updateAccount,
    deleteAccount,
    linkAuthorScopus,
    clearError,
  };
}