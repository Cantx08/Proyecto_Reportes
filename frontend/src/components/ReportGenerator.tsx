'use client';

import React, { useState, useEffect } from 'react';
import { scopusApi, ReportRequest } from '@/services/scopusApi';
import { formatDateToSpanish } from '@/utils/helpers';
import DepartmentSelect from './DepartmentSelectNew';
import PositionSelect from './PositionSelectNew';
import GenderSelect from './GenderSelect';
import FirmanteSelect from './SignatorySelect';
import type { AuthorResponse } from '@/types/api';

interface GeneradorReporteProps {
  authorIds: string[];
  selectedAuthor?: AuthorResponse;
  onError: (error: string) => void;
}

const GeneradorReporte: React.FC<GeneradorReporteProps> = ({ authorIds, selectedAuthor, onError }) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [formData, setFormData] = useState<Partial<ReportRequest>>({
    docente_nombre: '',
    docente_genero: 'M',
    departamento: '',
    cargo: '',
    memorando: '',
    firmante: 1,
    firmante_nombre: '',
    fecha: '',
    es_borrador: true,
  });

  // Pre-llenar los campos cuando hay un autor seleccionado
  useEffect(() => {
    if (selectedAuthor) {
      const fullName = `${selectedAuthor.title} ${selectedAuthor.name} ${selectedAuthor.surname}`.trim();
      setFormData(prev => ({
        ...prev,
        docente_nombre: fullName,
        docente_genero: selectedAuthor.gender || 'M',
        departamento: selectedAuthor.department || '',
        cargo: selectedAuthor.position || '',
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
    if (!formData.docente_nombre || !formData.departamento || !formData.cargo) {
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
        docente_nombre: formData.docente_nombre!,
        docente_genero: formData.docente_genero!,
        departamento: formData.departamento!,
        cargo: formData.cargo!,
        memorando: formData.memorando || undefined,
        firmante: formData.firmante || 1,
        firmante_nombre: formData.firmante_nombre || undefined,
        fecha: formData.fecha ? formatDateToSpanish(formData.fecha) : undefined,
        es_borrador: formData.es_borrador ?? true,
      };

      const blob = await scopusApi.generarReporte(reportRequest);
      
      // Crear URL para descargar el PDF
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const tipoDoc = formData.es_borrador ? 'borrador' : 'certificado_final';
      link.download = `${tipoDoc}_${formData.docente_nombre.replace(/\s+/g, '_')}.pdf`;
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
    <div className="bg-white p-6 rounded-lg shadow-lg border border-neutral-200">
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
            value={formData.docente_nombre}
            onChange={(e) => handleInputChange('docente_nombre', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Género
          </label>
          <GenderSelect
            value={formData.docente_genero || ''}
            onChange={(value) => handleInputChange('docente_genero', value)}
            placeholder="Escriba o seleccione un género"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Departamento *
          </label>
          <DepartmentSelect
            value={formData.departamento || ''}
            onChange={(value) => handleInputChange('departamento', value)}
            placeholder="Seleccione un departamento"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Cargo *
          </label>
          <PositionSelect
            value={formData.cargo || ''}
            onChange={(value) => handleInputChange('cargo', value)}
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
            value={formData.memorando}
            onChange={(e) => handleInputChange('memorando', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Firmante
          </label>
          <FirmanteSelect
            cargoValue={formData.firmante || 1}
            nombreValue={formData.firmante_nombre || ''}
            onCargoChange={(value) => handleInputChange('firmante', value)}
            onNombreChange={(value) => handleInputChange('firmante_nombre', value)}
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
            value={formData.fecha}
            onChange={(e) => handleInputChange('fecha', e.target.value)}
          />
          {formData.fecha && (
            <p className="mt-2 text-sm text-neutral-600">
              <span className="font-medium">Fecha de reporte:</span>{' '}
              <span className="text-primary-600 font-medium">{formatDateToSpanish(formData.fecha)}</span>
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
              {formData.es_borrador 
                ? 'Borrador' 
                : 'Certificado final'}
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <span className={`text-sm font-medium ${formData.es_borrador ? 'text-primary-600' : 'text-neutral-500'}`}>
              Borrador
            </span>
            <button
              type="button"
              onClick={() => handleInputChange('es_borrador', !formData.es_borrador)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
                formData.es_borrador ? 'bg-neutral-300' : 'bg-primary-600'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  formData.es_borrador ? 'translate-x-1' : 'translate-x-6'
                }`}
              />
            </button>
            <span className={`text-sm font-medium ${!formData.es_borrador ? 'text-primary-600' : 'text-neutral-500'}`}>
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
          {isGenerating ? 'Generando...' : `📄 Generar ${formData.es_borrador ? 'Borrador' : 'Certificado Final'}`}
        </button>
      </div>

      <div className="mt-4 text-sm text-neutral-600">
        <p><strong>IDs de Autor:</strong> {authorIds.join(', ')}</p>
        <p className="mt-1">* Campos requeridos</p>
      </div>
    </div>
  );
};

export default GeneradorReporte;
