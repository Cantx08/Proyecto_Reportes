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
        <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
        <span className="ml-2 text-sm text-gray-600">Cargando cuentas Scopus...</span>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <label className="block text-sm font-medium text-gray-700">
          Cuentas Scopus
        </label>
        {!readOnly && !isAddingNew && (
          <button
            type="button"
            onClick={() => setIsAddingNew(true)}
            disabled={loading}
            className="flex items-center gap-1 px-3 py-1 text-sm text-[#042a53] hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors disabled:opacity-50"
          >
            <Plus size={16} />
            Agregar Cuenta
          </button>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Formulario para agregar nueva cuenta */}
      {isAddingNew && !readOnly && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
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
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
              autoFocus
            />
            <button
              type="button"
              onClick={handleAddAccount}
              disabled={!newScopusId.trim() || loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
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
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors disabled:opacity-50"
            >
              Cancelar
            </button>
          </div>
          <p className="mt-2 text-xs text-gray-500">
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
                  ? 'border-gray-200 bg-white'
                  : 'border-gray-200 bg-gray-50 opacity-60'
              }`}
            >
              <div className="flex items-center gap-3 flex-1">
                {/* ID de Scopus */}
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm font-medium text-gray-900">
                      {account.scopus_id}
                    </span>
                    {!account.is_active && (
                      <span className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full">
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
                    className={`p-1.5 rounded-md transition-colors ${
                      account.is_active
                        ? 'text-green-600 hover:bg-green-50'
                        : 'text-gray-400 hover:bg-gray-100'
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
                    className="p-1.5 text-red-600 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
        <div className="text-center py-8 bg-gray-50 border border-dashed border-gray-300 rounded-lg">
          <p className="text-sm text-gray-500">
            No hay cuentas Scopus asociadas
          </p>
          {!readOnly && !isAddingNew && (
            <button
              type="button"
              onClick={() => setIsAddingNew(true)}
              className="mt-2 text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              Agregar la primera cuenta
            </button>
          )}
        </div>
      )}

      {/* Información adicional */}
      {accounts.length > 0 && (
        <div className="flex items-start gap-2 p-3 bg-[#042a53]/5 border border-[#042a53]/20 rounded-lg">
          <div className="text-blue-600 mt-0.5">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="text-xs text-[#042a53]">
            <strong>Nota:</strong> Los IDs de Scopus se utilizarán para obtener las publicaciones del autor.
            Las cuentas inactivas no se considerarán en las consultas.
          </div>
        </div>
      )}
    </div>
  );
}
