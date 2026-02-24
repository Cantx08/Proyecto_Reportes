'use client';

import React from 'react';

interface ScopusIdInputProps {
  scopusIds: string[];
  onAddId: () => void;
  onRemoveId: (index: number) => void;
  onUpdateId: (index: number, value: string) => void;
  onSearch: () => void;
  onClear: () => void;
  isLoading: boolean;
  validateScopusId: (id: string) => { isValid: boolean; message?: string };
}

export const ScopusIdInput: React.FC<ScopusIdInputProps> = ({
  scopusIds,
  onAddId,
  onRemoveId,
  onUpdateId,
  onSearch,
  onClear,
  isLoading,
  validateScopusId,
}) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        IDs de Scopus
      </h2>
      
      <div className="space-y-3">
        {scopusIds.map((id, index) => {
          const validation = validateScopusId(id);
          const showError = id.length > 0 && !validation.isValid;
          
          return (
            <div key={index} className="flex items-start space-x-2">
              <div className="flex-1">
                <input
                  type="text"
                  value={id}
                  onChange={(e) => {
                    const value = e.target.value;
                    // Permitir el valor tal como se ingresa para mostrar el error
                    onUpdateId(index, value);
                  }}
                  placeholder={`ID de Scopus ${index + 1}`}
                  className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 ${
                    showError ? 'border-red-300 focus:ring-red-500' : 'border-gray-300 focus:ring-[rgba(0,158,206,1)]'
                  }`}
                  disabled={isLoading}
                  maxLength={20}
                />
                {showError && (
                  <p className="text-red-500 text-sm mt-1">
                    {validation.message}
                  </p>
                )}
              </div>
              
              {scopusIds.length > 1 && (
                <button
                  onClick={() => onRemoveId(index)}
                  disabled={isLoading}
                  className="px-3 py-2 text-red-600 border border-red-300 rounded-md hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  ✕
                </button>
              )}
            </div>
          );
        })}
      </div>

      <div className="flex flex-wrap gap-3 mt-4">
        <button
          onClick={onAddId}
          disabled={isLoading}
          className="px-4 py-2 border rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          style={{
            color: 'rgba(4, 42, 83, 1)',
            borderColor: 'rgba(4, 42, 83, 0.3)'
          }}
        >
          + Agregar ID
        </button>
        
        <button
          onClick={onSearch}
          disabled={isLoading}
          className="px-6 py-2 text-white rounded-md hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          style={{
            backgroundColor: 'rgba(4, 42, 83, 1)'
          }}
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Buscando...
            </>
          ) : (
            'Buscar'
          )}
        </button>
        
        <button
          onClick={onClear}
          disabled={isLoading}
          className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Limpiar
        </button>
      </div>
    </div>
  );
};
