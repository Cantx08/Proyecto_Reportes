'use client';

import React, { useEffect } from 'react';
import { ScopusIdInput } from '@/components/ScopusIdInput';
import { PublicacionesList } from '@/components/PublicacionesList';
import { AreasTematicas } from '@/components/AreasTematicas';
import { DocumentosPorAnio } from '@/components/DocumentosPorAnio';
import { ErrorNotification } from '@/components/ErrorNotification';
import GeneradorReporte from '@/components/GeneradorReporte';
import { useScopusData } from '@/hooks/useScopusData';

export default function HomePage() {
  const {
    scopusIds,
    isLoading,
    loadingProgress,
    publicaciones,
    areasTematicas,
    documentosPorAnio,
    error,
    validateScopusId,
    addScopusId,
    removeScopusId,
    updateScopusId,
    searchScopusData,
    clearResults,
  } = useScopusData();

  // Limpiar error después de 5 segundos
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        clearResults();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearResults]);

  const dismissError = () => {
    clearResults();
  };

  const handleReportError = (error: string) => {
    // Usar el mismo sistema de error que ya existe
    clearResults();
    setTimeout(() => {
      // Simular un error para mostrarlo en el sistema existente
      window.dispatchEvent(new CustomEvent('scopus-error', { detail: error }));
    }, 100);
  };

  const hasResults = publicaciones.length > 0 || areasTematicas.length > 0;
  const validScopusIds = scopusIds.filter(item => item.trim() !== '').map(item => item.trim());

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">
              Análisis de Publicaciones Scopus
            </h1>
            <p className="mt-2 text-lg text-gray-600">
              Ingresa los IDs de Scopus para analizar publicaciones, áreas temáticas y estadísticas
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Input Section */}
        <ScopusIdInput
          scopusIds={scopusIds}
          onAddId={addScopusId}
          onRemoveId={removeScopusId}
          onUpdateId={updateScopusId}
          onSearch={searchScopusData}
          onClear={clearResults}
          isLoading={isLoading}
          validateScopusId={validateScopusId}
        />

        {/* Results Section */}
        {hasResults && (
          <div className="space-y-6">
            {/* Grid Layout for Results */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Publicaciones - Ocupa 2 columnas */}
              <div className="lg:col-span-2">
                <PublicacionesList publicaciones={publicaciones} />
              </div>

              {/* Sidebar - Áreas Temáticas */}
              <div className="space-y-6">
                <AreasTematicas areas={areasTematicas} />
              </div>
            </div>

            {/* Gráfico de Documentos por Año - Ancho completo */}
            <div className="w-full">
              <DocumentosPorAnio documentosPorAnio={documentosPorAnio} />
            </div>

            {/* Generador de Reportes */}
            {validScopusIds.length > 0 && (
              <div className="w-full">
                <GeneradorReporte 
                  authorIds={validScopusIds}
                  onError={handleReportError}
                />
              </div>
            )}
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="inline-flex items-center flex-col">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 mb-4" style={{ borderColor: 'rgba(0, 158, 206, 1)' }}></div>
              <span className="text-lg text-gray-600 mb-2">
                Procesando datos de Scopus...
              </span>
              {loadingProgress && (
                <span className="text-sm text-gray-500">
                  {loadingProgress}
                </span>
              )}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!hasResults && !isLoading && (
          <div className="text-center py-12">
            <div className="max-w-md mx-auto">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                Sin resultados
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Ingresa uno o más IDs de Scopus para comenzar el análisis
              </p>
            </div>
          </div>
        )}
      </main>

      {/* Error Notification */}
      <ErrorNotification error={error} onDismiss={dismissError} />
    </div>
  );
}
