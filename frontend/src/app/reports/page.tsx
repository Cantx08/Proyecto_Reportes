'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { 
  ClipboardCheck, 
  ArrowLeft,
  AlertCircle
} from 'lucide-react';

import { usePublicationsContext } from '@/src/contexts/PublicationsContext';
import { PublicationsList } from '@/src/features/publications/components/PublicationsList';
import { SubjectAreas } from '@/src/features/publications/components/SubjectAreas';
import { DocumentsByYear } from '@/src/features/publications/components/DocumentsByYearChart';
import ReportGenerator from '@/src/features/reports/components/ReportGenerator';
import { ErrorNotification } from '@/src/components/ErrorNotification';

export default function CertificatePage() {
  const router = useRouter();
  const { data, hasData, clearPublicationsData } = usePublicationsContext();
  const [error, setError] = React.useState<string | null>(null);

  // Log para debug
  React.useEffect(() => {
    console.log('[REPORTS PAGE] Context data:', data);
    console.log('[REPORTS PAGE] Selected Author:', data?.selectedAuthor);
  }, [data]);

  const handleBackToSearch = () => {
    clearPublicationsData();
    router.push('/publications');
  };

  const handleReportError = (errorMsg: string) => {
    setError(errorMsg);
  };

  const dismissError = () => {
    setError(null);
  };

  // Estado vacío - redirigir a búsqueda
  if (!hasData || !data) {
    return (
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
                <ClipboardCheck className="h-6 w-6 mr-3 text-primary-500" />
                Generación de Certificados
              </h1>
              <p className="text-neutral-600 mt-1">
                Genere certificados de publicaciones académicas
              </p>
            </div>
          </div>
        </div>

        {/* Empty State */}
        <div className="bg-white rounded-lg border border-neutral-200 p-12">
          <div className="text-center">
            <AlertCircle className="mx-auto h-16 w-16 text-warning-400 mb-4" />
            <h2 className="text-xl font-semibold text-neutral-900 mb-2">
              No hay publicaciones para certificar
            </h2>
            <p className="text-neutral-600 mb-6 max-w-md mx-auto">
              Primero debe buscar las publicaciones de un autor en la sección de publicaciones.
              Los resultados de la búsqueda se mostrarán aquí para generar el certificado.
            </p>
            <button
              onClick={handleBackToSearch}
              className="px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors flex items-center mx-auto"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Ir a Buscar Publicaciones
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
              <ClipboardCheck className="h-6 w-6 mr-3 text-primary-500" />
              Generación de Certificados
            </h1>
            <p className="text-neutral-600 mt-1">
              Revise las publicaciones y genere el certificado oficial
            </p>
          </div>
          <button
            onClick={handleBackToSearch}
            className="px-4 py-2 border border-neutral-300 rounded-lg text-sm font-medium text-neutral-700 hover:bg-neutral-50 flex items-center transition-colors"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Nueva Búsqueda
          </button>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="space-y-6">
        {/* Results Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Publicaciones - Ocupa 2 columnas */}
          <div className="lg:col-span-2">
            <PublicationsList publications={data.publications} />
          </div>

          {/* Sidebar - Áreas Temáticas */}
          <div className="space-y-6">
            <SubjectAreas areas={data.subjectAreas} />
          </div>
        </div>

        {/* Gráfico de Documentos por Año - Ancho completo */}
        {Object.keys(data.documentsByYear).length > 0 && (
          <div className="w-full">
            <DocumentsByYear documentsByYear={data.documentsByYear} />
          </div>
        )}

        {/* Formulario de Generación */}
        <div className="bg-white rounded-lg border border-neutral-200 p-6">
          <div className="flex items-center mb-6">
            <ClipboardCheck className="h-6 w-6 text-primary-600 mr-3" />
            <div>
              <h2 className="text-lg font-semibold text-neutral-900">
                Datos del Certificado
              </h2>
            </div>
          </div>
          <ReportGenerator
            authorIds={data.authorIds}
            selectedAuthor={data.selectedAuthor}
            onError={handleReportError}
          />
        </div>
      </div>

      {/* Error Notification */}
      <ErrorNotification error={error} onDismiss={dismissError} />
    </div>
  );
}
