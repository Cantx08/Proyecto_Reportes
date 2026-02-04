'use client';

import React, {useState, useEffect} from 'react';
import {Plus, Trash2, Loader2} from 'lucide-react';

import {scopusAccountsService} from "@/src/features/scopus-accounts/services/scopusAccountService";

export interface ScopusAccountUiItem {
    account_id?: string;
    scopus_id: string;
}

interface ScopusAccountsManagerProps {
    author_id?: string;
    initialAccounts?: ScopusAccountUiItem[];
    onChange: (accounts: ScopusAccountUiItem[]) => void;
    readOnly?: boolean;
}

export default function ScopusAccountsManager({
                                                  author_id,
                                                  initialAccounts = [],
                                                  onChange,
                                                  readOnly = false,
                                              }: ScopusAccountsManagerProps) {
    const [accounts, setAccounts] = useState<ScopusAccountUiItem[]>(initialAccounts);
    const [newScopusId, setNewScopusId] = useState('');
    const [isAddingNew, setIsAddingNew] = useState(false);
    const [loading, setLoading] = useState(false);
    const [loadingAccounts, setLoadingAccounts] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // 1. Cargar cuentas existentes
    useEffect(() => {
        const loadAccounts = async () => {
            if (author_id) {
                setLoadingAccounts(true);
                try {
                    const accountsData = await scopusAccountsService.getByAuthor(author_id);

                    const mappedAccounts: ScopusAccountUiItem[] = accountsData.map((account) => ({
                        account_id: account.account_id,
                        scopus_id: account.scopus_id,
                    }));

                    setAccounts(mappedAccounts);
                    onChange(mappedAccounts);
                } catch (err) {
                    console.error('Error loading Scopus accounts:', err);
                    setError('Error al cargar las cuentas Scopus');
                } finally {
                    setLoadingAccounts(false);
                }
            }
        };

        loadAccounts();
    }, [author_id, onChange]);

    useEffect(() => {
        if (!author_id) {
            setAccounts(initialAccounts);
        }
    }, [initialAccounts, author_id]);

    const handleAddAccount = async () => {
        const trimmedId = newScopusId.trim();
        if (!trimmedId) return;

        setError(null);

        if (accounts.some(acc => acc.scopus_id === trimmedId)) {
            setError('Esta cuenta Scopus ya está agregada');
            return;
        }

        // Caso A: Tenemos author_id (UUID), guardamos en Backend
        if (author_id) {
            setLoading(true);
            try {
                await scopusAccountsService.create({
                    scopus_id: trimmedId,
                    author_id: author_id, // Enviamos el UUID directamente
                });

                // Recargamos para obtener el UUID de la nueva cuenta creada
                const accountsData = await scopusAccountsService.getByAuthor(author_id);
                const mappedAccounts = accountsData.map((acc) => ({
                    account_id: acc.account_id,
                    scopus_id: acc.scopus_id,
                }));

                setAccounts(mappedAccounts);
                onChange(mappedAccounts);
                setNewScopusId('');
                setIsAddingNew(false);
            } catch (err) {
                console.error('Error creating Scopus account:', err);
                setError('Error al agregar la cuenta Scopus en el servidor');
            } finally {
                setLoading(false);
            }
        } else {
            // Caso B: Creación local (sin author_id aún)
            const newAccount: ScopusAccountUiItem = {
                scopus_id: trimmedId,
            };

            const updatedAccounts = [...accounts, newAccount];
            setAccounts(updatedAccounts);
            onChange(updatedAccounts);
            setNewScopusId('');
            setIsAddingNew(false);
        }
    };

    const handleRemoveAccount = async (index: number) => {
        const accountToRemove = accounts[index];

        // Caso A: Borrar de BD (requiere account_id UUID y author_id UUID)
        if (accountToRemove.account_id && author_id) {
            setLoading(true);
            try {
                await scopusAccountsService.delete(accountToRemove.account_id);

                const accountsData = await scopusAccountsService.getByAuthor(author_id);
                const mappedAccounts = accountsData.map((acc) => ({
                    account_id: acc.account_id,
                    scopus_id: acc.scopus_id,
                }));

                setAccounts(mappedAccounts);
                onChange(mappedAccounts);
            } catch (err) {
                console.error('Error deleting Scopus account:', err);
                setError('Error al eliminar la cuenta Scopus');
            } finally {
                setLoading(false);
            }
        } else {
            // Caso B: Borrar local
            const updatedAccounts = accounts.filter((_, i) => i !== index);
            setAccounts(updatedAccounts);
            onChange(updatedAccounts);
        }
    };

    if (loadingAccounts) {
        return (
            <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-primary-500"/>
                <span className="ml-2 text-sm text-neutral-600">Cargando cuentas Scopus...</span>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-end">
                {!readOnly && !isAddingNew && (
                    <button
                        type="button"
                        onClick={() => setIsAddingNew(true)}
                        disabled={loading}
                        className="flex items-center gap-1 px-3 py-1.5 text-sm text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition-colors disabled:opacity-50 font-medium"
                    >
                        <Plus size={16}/>
                        Agregar Cuenta
                    </button>
                )}
            </div>

            {error && (
                <div className="bg-error-50 border border-error-200 rounded-lg p-3">
                    <div className="flex items-center">
                        <svg className="h-5 w-5 text-error-400 mr-2" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd"
                                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                  clipRule="evenodd"/>
                        </svg>
                        <p className="text-sm text-error-700">{error}</p>
                    </div>
                </div>
            )}

            {isAddingNew && !readOnly && (
                <div className="bg-neutral-50 border border-neutral-200 rounded-lg p-4">
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                        Scopus ID
                    </label>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={newScopusId}
                            onChange={(e) => setNewScopusId(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    e.preventDefault();
                                    handleAddAccount();
                                }
                            }}
                            placeholder="Ej: 57211234567"
                            disabled={loading}
                            className="flex-1 px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50 transition-colors"
                            autoFocus
                        />
                        <button
                            type="button"
                            onClick={handleAddAccount}
                            disabled={!newScopusId.trim() || loading}
                            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-neutral-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2 shadow-sm"
                        >
                            {loading && <Loader2 size={16} className="animate-spin"/>}
                            Agregar
                        </button>
                        <button
                            type="button"
                            onClick={() => {
                                setIsAddingNew(false);
                                setNewScopusId('');
                                setError(null);
                            }}
                            disabled={loading}
                            className="px-4 py-2 bg-neutral-200 text-neutral-700 rounded-lg hover:bg-neutral-300 transition-colors disabled:opacity-50"
                        >
                            Cancelar
                        </button>
                    </div>
                    <p className="mt-2 text-xs text-neutral-500">
                        Ingresa el ID numérico de Scopus del autor.
                    </p>
                </div>
            )}

            {accounts.length > 0 ? (
                <div className="space-y-2">
                    {accounts.map((account, index) => (
                        <div
                            key={account.account_id || `temp-${index}`}
                            className="flex items-center justify-between p-4 border border-neutral-200 bg-white rounded-lg hover:border-neutral-300 transition-all"
                        >
                            <div className="flex items-center gap-3 flex-1">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2">
                    <span className="font-mono text-sm font-medium text-neutral-900">
                      {account.scopus_id}
                    </span>
                                    </div>
                                </div>
                            </div>

                            {!readOnly && (
                                <button
                                    type="button"
                                    onClick={() => !loading && handleRemoveAccount(index)}
                                    disabled={loading}
                                    className="p-1.5 text-error-600 hover:bg-error-50 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                    title="Eliminar cuenta"
                                >
                                    {loading ? <Loader2 size={18} className="animate-spin"/> : <Trash2 size={18}/>}
                                </button>
                            )}
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center py-8 bg-neutral-50 border-2 border-dashed border-neutral-300 rounded-lg">
                    <p className="text-sm text-neutral-500">
                        No hay cuentas Scopus asociadas
                    </p>
                    {!readOnly && !isAddingNew && (
                        <button
                            type="button"
                            onClick={() => setIsAddingNew(true)}
                            className="mt-2 text-sm text-primary-600 hover:text-primary-700 font-medium"
                        >
                            Agregar cuenta
                        </button>
                    )}
                </div>
            )}

            {accounts.length > 0 && (
                <div className="flex items-start gap-2 p-3 bg-info-50 border border-info-200 rounded-lg">
                    <div className="text-info-600 mt-0.5">
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd"
                                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                  clipRule="evenodd"/>
                        </svg>
                    </div>
                    <div className="text-xs text-info-700">
                        <strong className="font-semibold">Nota:</strong> Los IDs de Scopus se utilizarán para obtener
                        las publicaciones del autor.
                    </div>
                </div>
            )}
        </div>
    );
}