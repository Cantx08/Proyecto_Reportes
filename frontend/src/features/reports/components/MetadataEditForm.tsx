'use client';

import React, { useState } from 'react';
import { Save, FileDown, Loader2 } from 'lucide-react';
import { ReportMetadataResponse, UpdateReportMetadataRequest } from '@/src/features/reports/types';
import { formatDateToSpanish, parseDateFromSpanish } from '@/src/utils/helpers';
import FirmanteSelect from './SignatorySelect';
import ElaboradorSelect from './ElaboradorSelect';

interface MetadataEditFormProps {
  report: ReportMetadataResponse;
  onSave: (data: UpdateReportMetadataRequest) => Promise<void>;
  onRegenerate: () => void;
  isRegenerating: boolean;
}

const MetadataEditForm: React.FC<MetadataEditFormProps> = ({
  report,
  onSave,
  onRegenerate,
  isRegenerating,
}) => {
  const [isSaving, setIsSaving] = useState(false);
  const [formData, setFormData] = useState<UpdateReportMetadataRequest>({
    memorandum: report.memorandum || '',
    signatory: report.signatory || 1,
    signatory_name: report.signatory_name || '',
    // Convertir la fecha española a ISO para el input type="date"
    report_date: report.report_date ? parseDateFromSpanish(report.report_date) || report.report_date : '',
    elaborador: report.elaborador || 'M. Vásquez',
    label: report.label || '',
  });

  const handleChange = (field: keyof UpdateReportMetadataRequest, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Convertir la fecha de ISO a formato español antes de enviar al backend
      const dataToSave: UpdateReportMetadataRequest = {
        ...formData,
        report_date: formData.report_date
          ? formatDateToSpanish(formData.report_date)
          : formData.report_date,
      };
      await onSave(dataToSave);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Etiqueta */}
      <div>
        <label className="block text-xs font-medium text-neutral-600 mb-1">
          Etiqueta descriptiva
        </label>
        <input
          type="text"
          className="w-full p-2 text-sm border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          placeholder="Ej: Certificado Dr. Pérez - Febrero 2026"
          value={formData.label}
          onChange={(e) => handleChange('label', e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Memorando */}
        <div>
          <label className="block text-xs font-medium text-neutral-600 mb-1">
            Memorando
          </label>
          <input
            type="text"
            className="w-full p-2 text-sm border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            placeholder="EPN-DOCDCTA-2025-0055-M"
            value={formData.memorandum}
            onChange={(e) => handleChange('memorandum', e.target.value)}
          />
        </div>

        {/* Fecha */}
        <div>
          <label className="block text-xs font-medium text-neutral-600 mb-1">
            Fecha del informe
          </label>
          <input
            type="date"
            className="w-full p-2 text-sm border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            value={formData.report_date}
            onChange={(e) => handleChange('report_date', e.target.value)}
          />
          {formData.report_date && (
            <p className="mt-1 text-xs text-neutral-500">
              {formatDateToSpanish(formData.report_date)}
            </p>
          )}
        </div>

        {/* Firmante */}
        <div>
          <label className="block text-xs font-medium text-neutral-600 mb-1">
            Firmante
          </label>
          <FirmanteSelect
            positionValue={formData.signatory || 1}
            nameValue={formData.signatory_name || ''}
            onPositionChange={(value) => handleChange('signatory', value)}
            onNameChange={(value) => handleChange('signatory_name', value)}
            placeholder="Seleccione firmante"
          />
        </div>

        {/* Elaborador */}
        <div>
          <label className="block text-xs font-medium text-neutral-600 mb-1">
            Elaborado por
          </label>
          <ElaboradorSelect
            value={formData.elaborador || ''}
            onChange={(value) => handleChange('elaborador', value)}
            placeholder="Seleccione elaborador"
          />
        </div>
      </div>

      {/* Botones */}
      <div className="flex items-center justify-end space-x-3 pt-2">
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="flex items-center px-4 py-2 text-sm bg-primary-500 text-white rounded-md hover:bg-primary-600 transition-colors disabled:opacity-50"
        >
          {isSaving ? (
            <Loader2 className="h-4 w-4 animate-spin mr-1.5" />
          ) : (
            <Save className="h-4 w-4 mr-1.5" />
          )}
          Guardar cambios
        </button>
        <button
          onClick={onRegenerate}
          disabled={isRegenerating}
          className="flex items-center px-4 py-2 text-sm bg-amber-500 text-white rounded-md hover:bg-amber-600 transition-colors disabled:opacity-50"
        >
          {isRegenerating ? (
            <Loader2 className="h-4 w-4 animate-spin mr-1.5" />
          ) : (
            <FileDown className="h-4 w-4 mr-1.5" />
          )}
          Regenerar Borrador
        </button>
      </div>
    </div>
  );
};

export default MetadataEditForm;
