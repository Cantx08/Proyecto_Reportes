'use client';

import React, { useEffect, useState } from 'react';
import { 
  FileText, 
  Search, 
  Filter,
  Download,
  Eye,
  Calendar,
  BarChart3,
  Globe,
  TrendingUp,
  FileEdit,
  Plus
} from 'lucide-react';
import { ScopusIdInput } from '@/components/ScopusIdInput';
import { PublicacionesList } from '@/components/PublicationsList';
import { AreasTematicas } from '@/components/SubjectAreas';
import { DocumentosPorAnio } from '@/components/DocumentsByYearChart';
import { ErrorNotification } from '@/components/ErrorNotification';
import GeneradorReporte from '@/components/ReportGenerator';
import { useScopusData } from '@/hooks/useScopusData';

export default function PublicacionesPage() {
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

  const [viewMode, setViewMode] = useState<'search' | 'results'>('search');

  // Auto-cambiar a vista de resultados cuando hay datos
  useEffect(() => {
    if (publicaciones.length > 0 || areasTematicas.length > 0) {
      setViewMode('results');
    } else {
      setViewMode('search');
    }
  }, [publicaciones, areasTematicas]);

  const dismissError = () => {
    clearResults();
  };

  const handleReportError = (error: string) => {
    clearResults();
    setTimeout(() => {
      window.dispatchEvent(new CustomEvent('scopus-error', { detail: error }));
    }, 100);
  };

  const stats = {
    totalPublicaciones: publicaciones.length,
    totalAreas: areasTematicas.length,
    totalAnios: documentosPorAnio.length,
    autoresAnalizados: scopusIds.filter(id => id.trim() !== '').length
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <FileText className="h-6 w-6 mr-3" style={{ color: '#042a53' }} />
              Gestión de Publicaciones
            </h1>
            <p className="text-gray-600 mt-1">
              Búsqueda, análisis y visualización de publicaciones académicas
            </p>
          </div>
          <div className="flex space-x-3">
            <button 
              onClick={() => setViewMode('search')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                viewMode === 'search' 
                  ? 'text-white' 
                  : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
              style={viewMode === 'search' ? { backgroundColor: '#1f2937' } : {}}
            >
              <Search className="h-4 w-4 mr-2 inline" />
              Búsqueda
            </button>
            <button 
              onClick={() => setViewMode('results')}
              disabled={publicaciones.length === 0}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                viewMode === 'results' 
                  ? 'text-white' 
                  : publicaciones.length > 0 
                    ? 'border border-gray-300 text-gray-700 hover:bg-gray-50' 
                    : 'border border-gray-200 text-gray-400 cursor-not-allowed'
              }`}
              style={viewMode === 'results' ? { backgroundColor: '#1f2937' } : {}}
            >
              <BarChart3 className="h-4 w-4 mr-2 inline" />
              Análisis
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        {stats.totalPublicaciones > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="flex items-center">
                <FileText className="h-8 w-8" style={{ color: '#042a53' }} />
                <div className="ml-3">
                  <div className="text-2xl font-bold text-gray-900">{stats.totalPublicaciones}</div>
                  <div className="text-sm text-gray-600">Publicaciones</div>
                </div>
              </div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="flex items-center">
                <Globe className="h-8 w-8 text-green-600" />
                <div className="ml-3">
                  <div className="text-2xl font-bold text-gray-900">{stats.totalAreas}</div>
                  <div className="text-sm text-gray-600">Áreas Temáticas</div>
                </div>
              </div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="flex items-center">
                <Calendar className="h-8 w-8 text-purple-600" />
                <div className="ml-3">
                  <div className="text-2xl font-bold text-gray-900">{stats.totalAnios}</div>
                  <div className="text-sm text-gray-600">Años Analizados</div>
                </div>
              </div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="flex items-center">
                <TrendingUp className="h-8 w-8 text-orange-600" />
                <div className="ml-3">
                  <div className="text-2xl font-bold text-gray-900">{stats.autoresAnalizados}</div>
                  <div className="text-sm text-gray-600">Autores Analizados</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Content based on view mode */}
      {viewMode === 'search' ? (
        <div className="space-y-8">
          {/* Search Section */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="mb-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                Búsqueda de Publicaciones por Autor
              </h2>
              <p className="text-gray-600">
                Ingresa los IDs de Scopus de los autores para obtener sus publicaciones y análisis estadístico.
              </p>
            </div>
            
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

            {/* Loading State */}
            {isLoading && (
              <div className="mt-8 text-center py-8">
                <div className="inline-flex items-center flex-col">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
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
          </div>

          {/* Quick Access */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Acceso Rápido</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button className="text-left p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                <Eye className="h-6 w-6 mb-2" style={{ color: '#042a53' }} />
                <h4 className="font-medium text-gray-900">Búsquedas Recientes</h4>
                <p className="text-sm text-gray-600">Ver análisis anteriores</p>
              </button>
              <button className="text-left p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                <Download className="h-6 w-6 text-green-600 mb-2" />
                <h4 className="font-medium text-gray-900">Importar Lista</h4>
                <p className="text-sm text-gray-600">Cargar IDs desde archivo</p>
              </button>
              <button className="text-left p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                <Filter className="h-6 w-6 text-purple-600 mb-2" />
                <h4 className="font-medium text-gray-900">Filtros Avanzados</h4>
                <p className="text-sm text-gray-600">Configurar búsqueda específica</p>
              </button>
            </div>
          </div>

          {/* Guidelines */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Guía de Uso</h3>
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-sm font-semibold text-blue-600">
                  1
                </div>
                <div className="ml-3">
                  <h4 className="font-medium text-gray-900">Ingresar IDs de Scopus</h4>
                  <p className="text-sm text-gray-600">Añade uno o más IDs de autores para análisis. Ejemplo: 12345678900</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-sm font-semibold text-blue-600">
                  2
                </div>
                <div className="ml-3">
                  <h4 className="font-medium text-gray-900">Ejecutar Búsqueda</h4>
                  <p className="text-sm text-gray-600">Presiona 'Buscar Publicaciones' para obtener datos de Scopus</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-sm font-semibold text-blue-600">
                  3
                </div>
                <div className="ml-3">
                  <h4 className="font-medium text-gray-900">Analizar Resultados</h4>
                  <p className="text-sm text-gray-600">Revisa publicaciones, áreas temáticas y estadísticas por año</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Search Bar in Results Mode */}
          <div className="bg-white p-4 rounded-lg border border-gray-200">
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
          </div>

          {/* Results Grid */}
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
          {documentosPorAnio.length > 0 && (
            <div className="w-full">
              <DocumentosPorAnio documentosPorAnio={documentosPorAnio} />
            </div>
          )}

          {/* Generador de Borrador - Solo cuando hay resultados */}
          {scopusIds.filter(id => id.trim() !== '').length > 0 && publicaciones.length > 0 && (
            <div className="w-full">
              <div className="bg-gradient-to-r from-orange-50 to-yellow-50 rounded-lg p-6 border border-orange-200">
                <div className="flex items-center mb-4">
                  <FileEdit className="h-6 w-6 text-orange-600 mr-3" />
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Generar Borrador de Reporte
                    </h3>
                    <p className="text-sm text-gray-600">
                      Crea un borrador del reporte basado en las publicaciones encontradas
                    </p>
                  </div>
                </div>
                <GeneradorReporte 
                  authorIds={scopusIds.filter(id => id.trim() !== '')}
                  onError={handleReportError}
                />
              </div>
            </div>
          )}

          {/* Empty State */}
          {publicaciones.length === 0 && !isLoading && (
            <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
              <FileText className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                No se encontraron publicaciones
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Ingresa IDs de Scopus válidos para comenzar el análisis
              </p>
            </div>
          )}
        </div>
      )}

      {/* Error Notification */}
      <ErrorNotification error={error} onDismiss={dismissError} />
    </div>
  );
}