'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { 
  ClipboardCheck, 
  ArrowLeft,
  FileText,
  Search
} from 'lucide-react';

import { usePublicationsContext } from '@/src/contexts/PublicationsContext';
import { PublicationsList } from '@/src/features/publications/components/PublicationsList';
import { SubjectAreas } from '@/src/features/publications/components/SubjectAreas';
import { DocumentsByYear } from '@/src/features/publications/components/DocumentsByYearChart';
import ReportGenerator from '@/src/features/reports/components/ReportGenerator';
import PdfDropZone from '@/src/features/reports/components/PdfDropZone';
import SavedReportsList from '@/src/features/reports/components/SavedReportsList';
import { ErrorNotification } from '@/src/components/ErrorNotification';

export default function CertificatePage() {
  const router = useRouter();
  const { data, hasData, clearPublicationsData } = usePublicationsContext();
  const [error, setError] = React.useState<string | null>(null);

  const handleBackToSearch = () => {
    clearPublicationsData();
    router.push('/publications');
  };

  const handleGoToPublications = () => {
    router.push('/publications');
  };

  const handleReportError = (errorMsg: string) => {
    setError(errorMsg);
  };

  const dismissError = () => {
    setError(null);
  };

  // Sin publicaciones - mostrar opciones: ir a buscar o subir borrador
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

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Opción 1: Generar nuevo borrador */}
          <div className="bg-white rounded-lg border border-neutral-200 p-8">
            <div className="text-center">
              <div className="mx-auto h-14 w-14 bg-primary-50 rounded-full flex items-center justify-center mb-4">
                <Search className="h-7 w-7 text-primary-500" />
              </div>
              <h2 className="text-lg font-semibold text-neutral-900 mb-2">
                Generar nuevo borrador
              </h2>
              <p className="text-sm text-neutral-600 mb-6 max-w-sm mx-auto">
                Busque las publicaciones de un autor en el módulo de publicaciones para generar un borrador de certificado.
              </p>
              <button
                onClick={handleGoToPublications}
                className="px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors flex items-center mx-auto font-medium"
              >
                <Search className="h-4 w-4 mr-2" />
                Ir a Buscar Publicaciones
              </button>
            </div>
          </div>

          {/* Opción 2: Generar certificado final desde borrador */}
          <div className="bg-white rounded-lg border border-neutral-200 p-8">
            <div className="text-center mb-6">
              <div className="mx-auto h-14 w-14 bg-success-50 rounded-full flex items-center justify-center mb-4">
                <FileText className="h-7 w-7 text-success-500" />
              </div>
              <h2 className="text-lg font-semibold text-neutral-900 mb-2">
                Generar certificado final
              </h2>
              <p className="text-sm text-neutral-600 max-w-sm mx-auto">
                Si ya tiene un borrador PDF, súbalo aquí para aplicarle la plantilla institucional y obtener el certificado final.
              </p>
            </div>
            <PdfDropZone onError={handleReportError} />
          </div>
        </div>

        {/* Sección de reportes guardados */}
        <div className="mt-8">
          <div className="bg-white rounded-lg border border-neutral-200 p-6">
            <div className="flex items-center mb-4">
              <ClipboardCheck className="h-5 w-5 text-primary-500 mr-2" />
              <h2 className="text-lg font-semibold text-neutral-900">
                Reportes guardados
              </h2>
            </div>
            <p className="text-sm text-neutral-500 mb-4">
              Modifique datos como memorando, fecha, firmante o elaborador y regenere el borrador sin repetir la búsqueda de publicaciones.
            </p>
            <SavedReportsList onError={handleReportError} />
          </div>
        </div>

        {/* Error Notification */}
        <ErrorNotification error={error} onDismiss={dismissError} />
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
              Revise las publicaciones y genere el borrador del certificado
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

        {/* Formulario de Generación de Borrador */}
        <div className="bg-white rounded-lg border border-neutral-200 p-6">
          <div className="flex items-center mb-6">
            <ClipboardCheck className="h-6 w-6 text-primary-600 mr-3" />
            <div>
              <h2 className="text-lg font-semibold text-neutral-900">
                Datos del Certificado
              </h2>
              <p className="text-sm text-neutral-500 mt-0.5">
                Complete los datos y genere el borrador. Luego podrá aplicar la plantilla institucional desde el módulo de certificados.
              </p>
            </div>
          </div>
          <ReportGenerator
            authorIds={data.authorIds}
            selectedAuthor={data.selectedAuthor}
            publications={data.publications}
            subjectAreas={data.subjectAreas}
            documentsByYear={data.documentsByYear}
            onError={handleReportError}
          />
        </div>
      </div>

      {/* Error Notification */}
      <ErrorNotification error={error} onDismiss={dismissError} />
    </div>
  );
}
