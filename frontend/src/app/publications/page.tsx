'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  FileText, 
  Search, 
  Users,
  Microscope,
  ArrowRight
} from 'lucide-react';
import { ScopusIdInput } from '@/features/scopus-accounts/components/ScopusIdInput';
import { AuthorSelect } from '@/features/authors/components/AuthorSelect';
import { ErrorNotification } from '@/components/ErrorNotification';
import { useScopusData } from '@/features/scopus-accounts/hooks/useScopusData';
import { useAuthors } from '@/features/authors/hooks/useAuthors';
import { usePublicationsContext } from '@/contexts/PublicationsContext';

import { AuthorResponse } from "@/features/authors/types";

export default function PublicationsPage() {
  const router = useRouter();
  const {
    scopusIds,
    isLoading,
    loadingProgress,
    publications,
    subjectAreas,
    documentsByYear,
    error,
    validateScopusId,
    addScopusId,
    removeScopusId,
    updateScopusId,
    searchScopusData,
    clearResults,
  } = useScopusData();

  const { authors } = useAuthors();
  const { setPublicationsData } = usePublicationsContext();

  const [searchMode, setSearchMode] = useState<'scopus' | 'database'>('scopus');
  const [selectedAuthorIds, setSelectedAuthorIds] = useState<string[]>([]);

  const handleAuthorSelect = (authorId: string) => {
    // Solo permite seleccionar un autor a la vez (certificaciones individuales)
    setSelectedAuthorIds([authorId]);
  };

  // Obtener el primer autor seleccionado de la base de datos
  const getSelectedAuthor = (): AuthorResponse | undefined => {
    if (searchMode === 'database' && selectedAuthorIds.length > 0) {
      const firstSelectedId = selectedAuthorIds[0];
      return authors.find(author => author.author_id === firstSelectedId);
    }
    return undefined;
  };

  const handleSearch = async () => {
    // Combinar Scopus IDs y Author IDs
    const validScopusIds = scopusIds.filter(id => id.trim() !== '');
    const allIds = [...validScopusIds, ...selectedAuthorIds];

    if (allIds.length === 0) {
      return;
    }

    await searchScopusData(allIds);
  };

  // Efecto para redirigir cuando hay resultados
  useEffect(() => {
    if (publications.length > 0 && !isLoading) {
      // Guardar datos en el contexto
      const validScopusIds = scopusIds.filter(id => id.trim() !== '');
      setPublicationsData({
        publications,
        subjectAreas,
        documentsByYear,
        authorIds: [...validScopusIds, ...selectedAuthorIds],
        selectedAuthor: getSelectedAuthor(),
      });

      // Redirigir a la página de certificados
      router.push('/reports');
    }
  }, [publications, isLoading]);

  const dismissError = () => {
    clearResults();
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
              <FileText className="h-6 w-6 mr-3 text-primary-500" />
              Búsqueda de Publicaciones
            </h1>
            <p className="text-neutral-600 mt-1">
              Busque publicaciones y genere certificados académicos
            </p>
          </div>
        </div>
      </div>

      {/* Search Section */}
      <div className="space-y-8">
        {/* Search Mode Selector */}
        <div className="bg-white rounded-lg border border-neutral-200 p-6">
          <h3 className="text-sm font-medium text-neutral-700 mb-3">
            Buscar por:
          </h3>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => setSearchMode('scopus')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center ${
                searchMode === 'scopus'
                  ? 'bg-primary-500 text-white hover:bg-primary-600'
                  : 'bg-neutral-100 text-neutral-700 hover:bg-neutral-200'
              }`}
            >
              <Microscope className="h-4 w-4 mr-2" />
              Scopus IDs
            </button>
            <button
              onClick={() => setSearchMode('database')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center ${
                searchMode === 'database'
                  ? 'bg-primary-500 text-white hover:bg-primary-600'
                  : 'bg-neutral-100 text-neutral-700 hover:bg-neutral-200'
              }`}
            >
              <Users className="h-4 w-4 mr-2" />
              Autor
            </button>
          </div>
        </div>

        {/* Search Input Section */}
        <div className="bg-white rounded-lg border border-neutral-200 p-6">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-neutral-900 mb-2">
              Búsqueda de Publicaciones
            </h2>
            <p className="text-neutral-600">
              {searchMode === 'scopus' && 'Buscar publicaciones por Scopus IDs.'}
              {searchMode === 'database' && 'Buscar publicaciones por autor registrado.'}
            </p>
          </div>

          <div className="w-full">
            {/* Scopus IDs Input */}
            {searchMode === 'scopus' && (
              <div>
                <ScopusIdInput
                  scopusIds={scopusIds}
                  onAddId={addScopusId}
                  onRemoveId={removeScopusId}
                  onUpdateId={updateScopusId}
                  onSearch={handleSearch}
                  onClear={clearResults}
                  isLoading={isLoading}
                  validateScopusId={validateScopusId}
                />
              </div>
            )}

            {/* Author Selector */}
            {searchMode === 'database' && (
              <div>
                <AuthorSelect
                  onAuthorSelect={handleAuthorSelect}
                  selectedAuthors={selectedAuthorIds}
                />
              </div>
            )}
          </div>

          {/* Info box */}
          <div className="mt-6 p-4 bg-info-50 border border-info-200 rounded-lg">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <ArrowRight className="h-5 w-5 text-info-500" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-info-800">
                  ¿Qué sucederá?
                </h3>
                <p className="mt-1 text-sm text-info-700">
                  Al buscar publicaciones, será redirigido automáticamente a la pantalla de certificados 
                  donde podrá ver los resultados y generar el documento oficial.
                </p>
              </div>
            </div>
          </div>

          {/* Search Button */}
          <button
            onClick={handleSearch}
            disabled={isLoading || (scopusIds.filter(id => id.trim()).length === 0 && selectedAuthorIds.length === 0)}
            className="w-full mt-6 py-3 px-4 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:bg-neutral-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center text-sm font-medium"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Buscando...
              </>
            ) : (
              <>
                <Search className="h-4 w-4 mr-2" />
                Buscar y Generar Certificado
              </>
            )}
          </button>

          {/* Loading State */}
          {isLoading && (
            <div className="mt-8 text-center py-8">
              <div className="inline-flex items-center flex-col">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
                <span className="text-lg text-neutral-600 mb-2">
                  Procesando datos de Scopus...
                </span>
                {loadingProgress && (
                  <span className="text-sm text-neutral-500">
                    {loadingProgress}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Error Notification */}
      <ErrorNotification error={error} onDismiss={dismissError} />
    </div>
  );
}
