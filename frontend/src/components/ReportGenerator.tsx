'use client';

import React, { useState, useEffect } from 'react';
import { scopusApi, ReportRequest } from '@/services/scopusApi';
import { formatDateToSpanish } from '@/utils/helpers';
import DepartmentSelect from './DepartmentSelect';
import PositionSelect from './PositionSelect';
import GenderSelect from './GenderSelect';
import FirmanteSelect from './SignatorySelect';
import type { AuthorResponse } from '@/types/api';

interface ReportGeneratorProps {
  authorIds: string[];
  selectedAuthor?: AuthorResponse;
  onError: (error: string) => void;
}

const ReportGenerator: React.FC<ReportGeneratorProps> = ({ authorIds, selectedAuthor, onError }) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [formData, setFormData] = useState<Partial<ReportRequest>>({
    author_name: '',
    author_gender: 'M',
    department: '',
    position: '',
    memorandum: '',
    signatory: 1,
    authority_name: '',
    cert_date: '',
    is_draft: true,
  });

  // Pre-llenar los campos cuando hay un autor seleccionado
  useEffect(() => {
    if (selectedAuthor) {
      const fullName = `${selectedAuthor.title} ${selectedAuthor.name} ${selectedAuthor.surname}`.trim();
      setFormData(prev => ({
        ...prev,
        author_name: fullName,
        author_gender: selectedAuthor.gender || 'M',
        department: selectedAuthor.department || '',
        position: selectedAuthor.position || '',
      }));
    }
  }, [selectedAuthor]);

  const handleInputChange = (field: keyof ReportRequest, value: string | number | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleGenerateReport = async () => {
    // Validar campos requeridos
    if (!formData.author_name || !formData.department || !formData.position) {
      onError('Por favor complete todos los campos requeridos');
      return;
    }

    if (authorIds.length === 0) {
      onError('Debe ingresar al menos un ID de autor');
      return;
    }

    setIsGenerating(true);
    
    try {
      const reportRequest: ReportRequest = {
        author_ids: authorIds,
        author_name: formData.author_name!,
        author_gender: formData.author_gender!,
        department: formData.department!,
        position: formData.position!,
        memorandum: formData.memorandum || undefined,
        signatory: formData.signatory || 1,
        authority_name: formData.authority_name || undefined,
        cert_date: formData.cert_date ? formatDateToSpanish(formData.cert_date) : undefined,
        is_draft: formData.is_draft ?? true,
      };

      const blob = await scopusApi.generateCertification(reportRequest);
      
      // Crear URL para descargar el PDF
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const tipoDoc = formData.is_draft ? 'borrador' : 'certificado_final';
      link.download = `${tipoDoc}_${formData.author_name.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Error al generar el reporte');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="bg-white p-6">
      {/* Mensaje informativo si los datos fueron pre-llenados */}
      {selectedAuthor && (
        <div className="mb-6 p-4 bg-info-50 border border-info-200 rounded-lg">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-info-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-info-800">
                Datos pre-llenados automáticamente
              </h3>
              <p className="mt-1 text-sm text-info-700">
                Los campos se han completado con la información del autor seleccionado: <strong>{selectedAuthor.title} {selectedAuthor.name} {selectedAuthor.surname}</strong>. 
                Puedes modificarlos según sea necesario.
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Nombre del Docente *
          </label>
          <input
            type="text"
            className="w-full p-3 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
            placeholder="PhD. Juan Pérez"
            value={formData.author_name}
            onChange={(e) => handleInputChange('author_name', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Género
          </label>
          <GenderSelect
            value={formData.author_gender || ''}
            onChange={(value) => handleInputChange('author_gender', value)}
            placeholder="Escriba o seleccione un género"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Departamento *
          </label>
          <DepartmentSelect
            value={formData.department || ''}
            onChange={(value) => handleInputChange('department', value)}
            placeholder="Seleccione un departamento"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Cargo *
          </label>
          <PositionSelect
            value={formData.position || ''}
            onChange={(value) => handleInputChange('position', value)}
            placeholder="Seleccione un cargo"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Memorando (Opcional)
          </label>
          <input
            type="text"
            className="w-full p-3 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
            placeholder="EPN-DOCDCTA-2025-0055-M"
            value={formData.memorandum}
            onChange={(e) => handleInputChange('memorandum', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Firmante
          </label>
          <FirmanteSelect
            positionValue={formData.signatory || 1}
            nameValue={formData.authority_name || ''}
            onPositionChange={(value) => handleInputChange('signatory', value)}
            onNameChange={(value) => handleInputChange('authority_name', value)}
            placeholder="Escriba o seleccione un firmante"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Fecha (Opcional)
          </label>
          <input
            type="date"
            className="w-full p-3 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
            value={formData.cert_date}
            onChange={(e) => handleInputChange('cert_date', e.target.value)}
          />
          {formData.cert_date && (
            <p className="mt-2 text-sm text-neutral-600">
              <span className="font-medium">Fecha de reporte:</span>{' '}
              <span className="text-primary-600 font-medium">{formatDateToSpanish(formData.cert_date)}</span>
            </p>
          )}
        </div>
      </div>

      {/* Toggle para borrador vs certificado final */}
      <div className="mb-6 p-4 bg-neutral-50 rounded-lg border border-neutral-200">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-lg font-medium text-neutral-800 mb-1">
              Tipo de Documento
            </h4>
            <p className="text-sm text-neutral-600">
              {formData.is_draft
                ? 'Borrador' 
                : 'Certificado final'}
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <span className={`text-sm font-medium ${formData.is_draft ? 'text-primary-600' : 'text-neutral-500'}`}>
              Borrador
            </span>
            <button
              type="button"
              onClick={() => handleInputChange('is_draft', !formData.is_draft)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
                formData.is_draft ? 'bg-neutral-300' : 'bg-primary-600'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  formData.is_draft ? 'translate-x-1' : 'translate-x-6'
                }`}
              />
            </button>
            <span className={`text-sm font-medium ${!formData.is_draft ? 'text-primary-600' : 'text-neutral-500'}`}>
              Final
            </span>
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleGenerateReport}
          disabled={isGenerating}
          className="w-full sm:w-auto bg-primary-600 hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed text-white font-medium py-3 px-8 rounded-md transition-colors duration-200 shadow-sm"
        >
          {isGenerating ? 'Generando...' : `📄 Generar ${formData.is_draft ? 'Borrador' : 'Certificado Final'}`}
        </button>
      </div>

      <div className="mt-4 text-sm text-neutral-600">
        <p><strong>IDs de Autor:</strong> {authorIds.join(', ')}</p>
        <p className="mt-1">* Campos requeridos</p>
      </div>
    </div>
  );
};

export default ReportGenerator;
