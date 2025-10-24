'use client';

import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Loader2, XCircle } from 'lucide-react';
import { scopusAccountsApi } from '@/services/newApi';
import type { ScopusAccountResponse } from '@/types/api';

interface ScopusAccountData {
  id?: number;
  scopus_id: string;
  is_active: boolean;
}

interface ScopusAccountsManagerProps {
  authorId?: number;
  initialAccounts?: ScopusAccountData[];
  onChange: (accounts: ScopusAccountData[]) => void;
  readOnly?: boolean;
}

export default function ScopusAccountsManager({
  authorId,
  initialAccounts = [],
  onChange,
  readOnly = false,
}: ScopusAccountsManagerProps) {
  const [accounts, setAccounts] = useState<ScopusAccountData[]>(initialAccounts);
  const [newScopusId, setNewScopusId] = useState('');
  const [isAddingNew, setIsAddingNew] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loadingAccounts, setLoadingAccounts] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Cargar cuentas existentes cuando tenemos authorId
  useEffect(() => {
    const loadAccounts = async () => {
      if (authorId) {
        setLoadingAccounts(true);
        try {
          const accountsData = await scopusAccountsApi.getByAuthor(authorId.toString());
          const mappedAccounts = accountsData.map((acc: ScopusAccountResponse) => ({
            id: acc.id,
            scopus_id: acc.scopus_id,
            is_active: acc.is_active !== false,
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
  }, [authorId]);

  useEffect(() => {
    if (!authorId) {
      setAccounts(initialAccounts);
    }
  }, [initialAccounts, authorId]);

  const handleAddAccount = async () => {
    if (!newScopusId.trim()) return;

    setError(null);

    // Validar que no exista ya
    if (accounts.some(acc => acc.scopus_id === newScopusId.trim())) {
      setError('Esta cuenta Scopus ya está agregada');
      return;
    }

    const newAccount: ScopusAccountData = {
      scopus_id: newScopusId.trim(),
      is_active: true,
    };

    // Si tenemos authorId, guardar en el backend inmediatamente
    if (authorId) {
      setLoading(true);
      try {
        await scopusAccountsApi.create({
          scopus_id: newAccount.scopus_id,
          author_id: authorId.toString(),
          is_active: newAccount.is_active,
        });

        // Recargar las cuentas del autor
        const accountsData = await scopusAccountsApi.getByAuthor(authorId.toString());
        const mappedAccounts = accountsData.map((acc: ScopusAccountResponse) => ({
          id: acc.id,
          scopus_id: acc.scopus_id,
          is_active: acc.is_active !== false,
        }));
        setAccounts(mappedAccounts);
        onChange(mappedAccounts);
      } catch (err) {
        console.error('Error creating Scopus account:', err);
        setError('Error al agregar la cuenta Scopus');
      } finally {
        setLoading(false);
      }
    } else {
      // Si no hay authorId, solo actualizar el estado local
      const updatedAccounts = [...accounts, newAccount];
      setAccounts(updatedAccounts);
      onChange(updatedAccounts);
    }

    setNewScopusId('');
    setIsAddingNew(false);
  };

  const handleRemoveAccount = async (index: number) => {
    const accountToRemove = accounts[index];

    // Si tiene ID, eliminarlo del backend
    if (accountToRemove.id && authorId) {
      setLoading(true);
      try {
        await scopusAccountsApi.delete(accountToRemove.scopus_id);
        
        // Recargar las cuentas
        const accountsData = await scopusAccountsApi.getByAuthor(authorId.toString());
        const mappedAccounts = accountsData.map((acc: ScopusAccountResponse) => ({
          id: acc.id,
          scopus_id: acc.scopus_id,
          is_active: acc.is_active !== false,
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
      // Si no tiene ID, solo eliminar del estado local
      const updatedAccounts = accounts.filter((_, i) => i !== index);
      setAccounts(updatedAccounts);
      onChange(updatedAccounts);
    }
  };

  const handleToggleActive = async (index: number) => {
    const updatedAccounts = accounts.map((acc, i) =>
      i === index ? { ...acc, is_active: !acc.is_active } : acc
    );

    // Si tenemos authorId y la cuenta tiene ID, actualizar en el backend
    if (authorId && updatedAccounts[index].id) {
      setLoading(true);
      try {
        await scopusAccountsApi.update(updatedAccounts[index].scopus_id, {
          is_active: updatedAccounts[index].is_active,
        });
      } catch (err) {
        console.error('Error toggling account status:', err);
        setError('Error al cambiar el estado de la cuenta');
      } finally {
        setLoading(false);
      }
    }

    setAccounts(updatedAccounts);
    onChange(updatedAccounts);
  };

  if (loadingAccounts) {
    return (
      <div className="flex items-center justify-center py-8">
        <Loader2 className="h-6 w-6 animate-spin text-primary-500" />
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
            <Plus size={16} />
            Agregar Cuenta
          </button>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-error-50 border border-error-200 rounded-lg p-3">
          <div className="flex items-center">
            <svg className="h-5 w-5 text-error-400 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <p className="text-sm text-error-700">{error}</p>
          </div>
        </div>
      )}

      {/* Formulario para agregar nueva cuenta */}
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
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddAccount())}
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
              {loading && <Loader2 size={16} className="animate-spin" />}
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
            Ingresa el ID numérico de Scopus del autor
          </p>
        </div>
      )}

      {/* Lista de cuentas existentes */}
      {accounts.length > 0 ? (
        <div className="space-y-2">
          {accounts.map((account, index) => (
            <div
              key={account.id || `new-${index}`}
              className={`flex items-center justify-between p-4 border rounded-lg transition-all ${
                account.is_active
                  ? 'border-neutral-200 bg-white hover:border-neutral-300'
                  : 'border-neutral-200 bg-neutral-50 opacity-60'
              }`}
            >
              <div className="flex items-center gap-3 flex-1">
                {/* ID de Scopus */}
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm font-medium text-neutral-900">
                      {account.scopus_id}
                    </span>
                    {!account.is_active && (
                      <span className="text-xs px-2 py-0.5 bg-neutral-100 text-neutral-600 rounded-full font-medium">
                        Inactiva
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Controles */}
              {!readOnly && (
                <div className="flex items-center gap-2">
                  {/* Toggle activo/inactivo */}
                  <button
                    type="button"
                    onClick={() => !loading && handleToggleActive(index)}
                    disabled={loading}
                    className={`p-1.5 rounded-lg transition-colors ${
                      account.is_active
                        ? 'text-success-600 hover:bg-success-50'
                        : 'text-neutral-400 hover:bg-neutral-100'
                    } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    title={account.is_active ? 'Desactivar cuenta' : 'Activar cuenta'}
                  >
                    {account.is_active ? (
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <XCircle size={20} />
                    )}
                  </button>

                  {/* Botón eliminar */}
                  <button
                    type="button"
                    onClick={() => !loading && handleRemoveAccount(index)}
                    disabled={loading}
                    className="p-1.5 text-error-600 hover:bg-error-50 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Eliminar cuenta"
                  >
                    {loading ? <Loader2 size={18} className="animate-spin" /> : <Trash2 size={18} />}
                  </button>
                </div>
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

      {/* Información adicional */}
      {accounts.length > 0 && (
        <div className="flex items-start gap-2 p-3 bg-info-50 border border-info-200 rounded-lg">
          <div className="text-info-600 mt-0.5">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="text-xs text-info-700">
            <strong className="font-semibold">Nota:</strong> Los IDs de Scopus se utilizarán para obtener las publicaciones del autor.
            Las cuentas inactivas no se considerarán en las consultas.
          </div>
        </div>
      )}
    </div>
  );
}
