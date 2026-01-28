'use client';

import React, { useEffect, useState } from 'react';
import { 
  FileText, 
  Search, 
  Filter,
  BarChart3,
  FileEdit,
  Users,
  Microscope
} from 'lucide-react';
import { ScopusIdInput } from '@/components/ScopusIdInput';
import { AuthorSelector } from '@/components/AuthorSelector';
import { PublicationsList } from '@/components/PublicationsList';
import { SubjectAreas } from '@/components/SubjectAreas';
import { DocumentsByYear } from '@/components/DocumentsByYearChart';
import { ErrorNotification } from '@/components/ErrorNotification';
import ReportGenerator from '@/components/ReportGenerator';
import { useScopusData } from '@/hooks/useScopusData';
import { useAuthors } from '@/hooks/useAuthors';

import {AuthorResponse} from "@/features/authors/types";

export default function PublicationsPage() {
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

  const [viewMode, setViewMode] = useState<'search' | 'results'>('search');
  const [searchMode, setSearchMode] = useState<'scopus' | 'database'>('scopus');
  const [selectedAuthorIds, setSelectedAuthorIds] = useState<string[]>([]);

  // Auto-cambiar a vista de resultados cuando hay datos
  useEffect(() => {
    if (publications.length > 0 || subjectAreas.length > 0) {
      setViewMode('results');
    } else {
      setViewMode('search');
    }
  }, [publications, subjectAreas]);

  const handleAuthorSelect = (authorId: string) => {
    // Solo permite seleccionar un autor a la vez (certificaciones individuales)
    setSelectedAuthorIds([authorId]);
  };

  const handleSearch = async () => {
    // Combinar Scopus IDs y Author IDs
    const validScopusIds = scopusIds.filter(id => id.trim() !== '');
    const allIds = [...validScopusIds, ...selectedAuthorIds];

    if (allIds.length === 0) {
      // Usar el error del estado
      return;
    }

    await searchScopusData(allIds);
  };

  const dismissError = () => {
    clearResults();
  };

  const handleReportError = (error: string) => {
    clearResults();
    setTimeout(() => {
      window.dispatchEvent(new CustomEvent('scopus-error', { detail: error }));
    }, 100);
  };

  // Obtener el primer autor seleccionado de la base de datos para prellenar el formulario
  const getSelectedAuthor = (): AuthorResponse | undefined => {
    if (searchMode === 'database' && selectedAuthorIds.length > 0) {
      const firstSelectedId = selectedAuthorIds[0];
      return authors.find(author => author.author_id === firstSelectedId);
    }
    return undefined;
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
              <FileText className="h-6 w-6 mr-3 text-primary-500" />
              Gestión de Publicaciones
            </h1>
            <p className="text-neutral-600 mt-1">
              Búsqueda y visualización de publicaciones indexadas en Scopus
            </p>
          </div>
          <div className="flex space-x-3">
            <button 
              onClick={() => setViewMode('search')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                viewMode === 'search' 
                  ? 'bg-primary-500 text-white hover:bg-primary-600' 
                  : 'border border-neutral-300 text-neutral-700 hover:bg-neutral-50'
              }`}
            >
              <Search className="h-4 w-4 mr-2 inline" />
              Búsqueda
            </button>
            <button 
              onClick={() => setViewMode('results')}
              disabled={publications.length === 0}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                viewMode === 'results' 
                  ? 'bg-primary-500 text-white hover:bg-primary-600' 
                  : publications.length > 0 
                    ? 'border border-neutral-300 text-neutral-700 hover:bg-neutral-50' 
                    : 'border border-neutral-200 text-neutral-400 cursor-not-allowed'
              }`}
            >
              <BarChart3 className="h-4 w-4 mr-2 inline" />
              Resultados
            </button>
          </div>
        </div>
      </div>

      {/* Content based on view mode */}
      {viewMode === 'search' ? (
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

          {/* Search Section */}
          <div className="bg-white rounded-lg border border-neutral-200 p-6">
            <div className="mb-6">
              <h2 className="text-lg font-semibold text-neutral-900 mb-2">
                Búsqueda de Publicaciones
              </h2>
              <p className="text-neutral-600">
                {searchMode === 'scopus' && 'Buscar publicaciones por Scopus IDs.'}
                {searchMode === 'database' && 'Buscar publicaciones por autor.'}
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
                  <AuthorSelector
                    onAuthorSelect={handleAuthorSelect}
                    selectedAuthors={selectedAuthorIds}
                  />
                </div>
              )}
            </div>

            {/* Selection Summary - Solo mostrar para Scopus IDs */}
            {searchMode === 'scopus' && scopusIds.filter(id => id.trim()).length > 0 && (
              <div className="mt-6 p-4 bg-neutral-50 rounded-lg border border-neutral-200">
                <h3 className="font-medium text-neutral-900 mb-3 flex items-center">
                  <Filter className="h-4 w-4 mr-2" />
                  Selección Actual
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <p className="text-sm text-neutral-600">Scopus IDs</p>
                    <p className="text-2xl font-bold text-primary-500">
                      {scopusIds.filter(id => id.trim()).length}
                    </p>
                  </div>
                </div>
              </div>
            )}

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
                  Buscar Publicaciones
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
      ) : (
        <div className="space-y-6">
          {/* Quick Search Bar in Results Mode */}
          <div className="bg-white p-4 rounded-lg border border-neutral-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-neutral-700">
                Realizar nueva búsqueda
              </h3>
              <button
                onClick={() => setViewMode('search')}
                className="text-sm text-primary-500 hover:text-primary-600 flex items-center"
              >
                <Search className="h-4 w-4 mr-1" />
                Búsqueda avanzada
              </button>
            </div>
            <button
              onClick={handleSearch}
              disabled={isLoading}
              className="w-full py-2 px-4 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:bg-neutral-300 transition-colors text-sm font-medium"
            >
              {isLoading ? 'Buscando...' : 'Actualizar Resultados'}
            </button>
          </div>

          {/* Results Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Publicaciones - Ocupa 2 columnas */}
            <div className="lg:col-span-2">
              <PublicationsList publications={publications} />
            </div>

            {/* Sidebar - Áreas Temáticas */}
            <div className="space-y-6">
              <SubjectAreas areas={subjectAreas} />
            </div>
          </div>

          {/* Gráfico de Documentos por Año - Ancho completo */}
          {Object.keys(documentsByYear).length > 0 && (
            <div className="w-full">
              <DocumentsByYear documentsByYear={documentsByYear} />
            </div>
          )}

          {/* Generador de Borrador - Solo cuando hay resultados */}
          {(scopusIds.filter(id => id.trim() !== '').length > 0 || selectedAuthorIds.length > 0) && publications.length > 0 && (
            <div className="w-full">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center mb-4">
                  <FileEdit className="h-6 w-6 text-orange-600 mr-3" />
                  <div>
                    <h3 className="text-lg font-semibold text-neutral-900">
                      Generar Borrador
                    </h3>
                  </div>
                </div>
                <ReportGenerator
                  authorIds={[...scopusIds.filter(id => id.trim() !== ''), ...selectedAuthorIds]}
                  selectedAuthor={getSelectedAuthor()}
                  onError={handleReportError}
                />
              </div>
            </div>
          )}

          {/* Empty State */}
          {publications.length === 0 && !isLoading && (
            <div className="text-center py-12 bg-white rounded-lg border border-neutral-200">
              <FileText className="mx-auto h-12 w-12 text-neutral-400" />
              <h3 className="mt-2 text-sm font-medium text-neutral-900">
                No se encontraron publicaciones
              </h3>
              <p className="mt-1 text-sm text-neutral-500">
                Ingresa IDs de Scopus o selecciona autores para comenzar el análisis
              </p>
              <button
                onClick={() => setViewMode('search')}
                className="mt-4 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 text-sm"
              >
                Volver a la búsqueda
              </button>
            </div>
          )}
        </div>
      )}

      {/* Error Notification */}
      <ErrorNotification error={error} onDismiss={dismissError} />
    </div>
  );
}
