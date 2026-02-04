import {useCallback, useState} from 'react';
import {apiUtils} from '@/src/services/servicesApi';
import {ScopusAccountCreateRequest, ScopusAccountResponse} from "@/src/features/scopus-accounts/types";
import {scopusAccountsService} from "@/src/features/scopus-accounts/services/scopusAccountService";

export interface UseScopusAccountsState {
    accounts: ScopusAccountResponse[];
    scopusIds: string[];
    loading: boolean;
    error: string | null;
    creating: boolean;
    deleting: boolean;
}

export interface UseScopusAccountsActions {
    getAccountsByAuthor: (authorId: string) => Promise<ScopusAccountResponse[]>;
    getAccount: (scopusId: string) => Promise<ScopusAccountResponse | null>;
    createAccount: (accountData: ScopusAccountCreateRequest) => Promise<ScopusAccountResponse | null>;
    deleteAccount: (scopusId: string) => Promise<boolean>;
    clearError: () => void;
}

export function useScopusAccounts(): UseScopusAccountsState & UseScopusAccountsActions {
    const [state, setState] = useState<UseScopusAccountsState>({
        accounts: [],
        scopusIds: [],
        loading: false,
        error: null,
        creating: false,
        deleting: false,
    });

    const clearError = useCallback(() => {
        setState(prev => ({...prev, error: null}));
    }, []);

    const getAccountsByAuthor = useCallback(async (authorId: string): Promise<ScopusAccountResponse[]> => {
        try {
            return await scopusAccountsService.getByAuthor(authorId);
        } catch (error) {
            const errorMessage = apiUtils.handleError(error);
            setState(prev => ({...prev, error: errorMessage}));
            return [];
        }
    }, []);

    const getAccount = useCallback(async (scopusId: string): Promise<ScopusAccountResponse | null> => {
        try {
            return await scopusAccountsService.getById(scopusId);
        } catch (error) {
            const errorMessage = apiUtils.handleError(error);
            setState(prev => ({...prev, error: errorMessage}));
            return null;
        }
    }, []);

    const createAccount = useCallback(async (accountData: ScopusAccountCreateRequest): Promise<ScopusAccountResponse | null> => {
        setState(prev => ({...prev, creating: true, error: null}));
        try {
            const newAccount = await scopusAccountsService.create(accountData);
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

    const deleteAccount = useCallback(async (scopusId: string): Promise<boolean> => {
        setState(prev => ({...prev, deleting: true, error: null}));
        try {
            await scopusAccountsService.delete(scopusId);
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

    return {
        ...state,
        getAccount,
        getAccountsByAuthor,
        createAccount,
        deleteAccount,
        clearError,
    };
}