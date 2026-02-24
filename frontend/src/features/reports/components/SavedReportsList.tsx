'use client';

import React, { useState, useEffect, useCallback } from 'react';
import {
  Database,
  Calendar,
  User,
  Trash2,
  Edit3,
  FileDown,
  ChevronDown,
  ChevronUp,
  Loader2,
  AlertCircle,
} from 'lucide-react';
import { ReportMetadataResponse, UpdateReportMetadataRequest } from '@/src/features/reports/types';
import { reportService } from '@/src/features/reports/services/reportService';
import MetadataEditForm from '@/src/features/reports/components/MetadataEditForm';

interface SavedReportsListProps {
  onError: (error: string) => void;
}

const SavedReportsList: React.FC<SavedReportsListProps> = ({ onError }) => {
  const [reports, setReports] = useState<ReportMetadataResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [regeneratingId, setRegeneratingId] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchReports = useCallback(async () => {
    try {
      setLoading(true);
      const data = await reportService.listMetadata();
      setReports(data);
    } catch {
      onError('Error al cargar los reportes guardados.');
    } finally {
      setLoading(false);
    }
  }, [onError]);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  const handleToggleExpand = (id: string) => {
    setExpandedId(prev => (prev === id ? null : id));
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('¿Está seguro de eliminar estos metadatos? Esta acción no se puede deshacer.')) return;
    try {
      setDeletingId(id);
      await reportService.deleteMetadata(id);
      setReports(prev => prev.filter(r => r.id !== id));
      if (expandedId === id) setExpandedId(null);
    } catch {
      onError('Error al eliminar los metadatos.');
    } finally {
      setDeletingId(null);
    }
  };

  const handleUpdate = async (id: string, data: UpdateReportMetadataRequest) => {
    try {
      const updated = await reportService.updateMetadata(id, data);
      setReports(prev => prev.map(r => (r.id === id ? updated : r)));
    } catch {
      onError('Error al actualizar los metadatos.');
    }
  };

  const handleRegenerate = async (id: string, authorName: string) => {
    try {
      setRegeneratingId(id);
      const blob = await reportService.regenerateFromMetadata(id);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `borrador_${authorName.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Error al regenerar el borrador.');
    } finally {
      setRegeneratingId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-6 w-6 animate-spin text-primary-500 mr-2" />
        <span className="text-neutral-600">Cargando reportes guardados...</span>
      </div>
    );
  }

  if (reports.length === 0) {
    return (
      <div className="text-center py-10">
        <Database className="h-10 w-10 text-neutral-300 mx-auto mb-3" />
        <p className="text-neutral-500 text-sm">
          No hay reportes guardados aún.
        </p>
        <p className="text-neutral-400 text-xs mt-1">
          Genere un borrador desde el módulo de publicaciones y se guardará automáticamente.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {reports.map(report => {
        const isExpanded = expandedId === report.id;
        const isRegenerating = regeneratingId === report.id;
        const isDeleting = deletingId === report.id;

        return (
          <div
            key={report.id}
            className="border border-neutral-200 rounded-lg bg-white overflow-hidden"
          >
            {/* Header */}
            <div
              className="flex items-center justify-between px-4 py-3 cursor-pointer hover:bg-neutral-50 transition-colors"
              onClick={() => handleToggleExpand(report.id)}
            >
              <div className="flex items-center min-w-0 flex-1">
                <Database className="h-4 w-4 text-primary-400 shrink-0 mr-3" />
                <div className="min-w-0">
                  <p className="text-sm font-medium text-neutral-900 truncate">
                    {report.label || report.author_name}
                  </p>
                  <div className="flex items-center text-xs text-neutral-500 mt-0.5 space-x-3">
                    <span className="flex items-center">
                      <User className="h-3 w-3 mr-1" />
                      {report.author_name}
                    </span>
                    <span className="flex items-center">
                      <Calendar className="h-3 w-3 mr-1" />
                      {new Date(report.updated_at).toLocaleDateString('es-EC')}
                    </span>
                    <span>{report.publications.length} publicaciones</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-2 ml-3">
                {/* Regenerar */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleRegenerate(report.id, report.author_name);
                  }}
                  disabled={isRegenerating}
                  className="p-1.5 text-amber-600 hover:bg-amber-50 rounded-md transition-colors disabled:opacity-50"
                  title="Regenerar borrador"
                >
                  {isRegenerating ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <FileDown className="h-4 w-4" />
                  )}
                </button>

                {/* Eliminar */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(report.id);
                  }}
                  disabled={isDeleting}
                  className="p-1.5 text-red-500 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50"
                  title="Eliminar"
                >
                  {isDeleting ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                </button>

                {/* Expand/Collapse */}
                {isExpanded ? (
                  <ChevronUp className="h-4 w-4 text-neutral-400" />
                ) : (
                  <ChevronDown className="h-4 w-4 text-neutral-400" />
                )}
              </div>
            </div>

            {/* Expanded Content */}
            {isExpanded && (
              <div className="border-t border-neutral-100 px-4 py-4">
                {/* Info no editable */}
                <div className="mb-4 p-3 bg-neutral-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <AlertCircle className="h-4 w-4 text-neutral-400 mr-2" />
                    <span className="text-xs font-medium text-neutral-600 uppercase tracking-wider">
                      Datos oficiales (no editables)
                    </span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                    <div>
                      <span className="text-neutral-500">Docente:</span>
                      <p className="font-medium text-neutral-800">{report.author_name}</p>
                    </div>
                    <div>
                      <span className="text-neutral-500">Departamento:</span>
                      <p className="font-medium text-neutral-800">{report.department}</p>
                    </div>
                    <div>
                      <span className="text-neutral-500">Cargo:</span>
                      <p className="font-medium text-neutral-800">{report.position}</p>
                    </div>
                    <div>
                      <span className="text-neutral-500">Publicaciones:</span>
                      <p className="font-medium text-neutral-800">{report.publications.length}</p>
                    </div>
                    <div>
                      <span className="text-neutral-500">Áreas temáticas:</span>
                      <p className="font-medium text-neutral-800">{report.subject_areas.length}</p>
                    </div>
                  </div>
                </div>

                {/* Formulario editable */}
                <div className="flex items-center mb-3">
                  <Edit3 className="h-4 w-4 text-primary-500 mr-2" />
                  <span className="text-xs font-medium text-neutral-600 uppercase tracking-wider">
                    Metadatos editables
                  </span>
                </div>
                <MetadataEditForm
                  report={report}
                  onSave={(data: UpdateReportMetadataRequest) => handleUpdate(report.id, data)}
                  onRegenerate={() => handleRegenerate(report.id, report.author_name)}
                  isRegenerating={isRegenerating}
                />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default SavedReportsList;
