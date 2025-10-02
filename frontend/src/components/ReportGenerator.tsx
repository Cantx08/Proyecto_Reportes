'use client';

import React, { useState } from 'react';
import { scopusApi, ReportRequest } from '@/services/scopusApi';
import { formatDateToSpanish } from '@/utils/helpers';
import DepartmentSelect from './DepartmentSelect';
import CargoSelect from './PositionSelect';
import GenderSelect from './GenderSelect';
import FirmanteSelect from './SignatorySelect';

interface GeneradorReporteProps {
  authorIds: string[];
  onError: (error: string) => void;
}

const GeneradorReporte: React.FC<GeneradorReporteProps> = ({ authorIds, onError }) => {
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
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4 text-gray-800">
        Generar Reporte de Certificación
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Nombre del Docente *
          </label>
          <input
            type="text"
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="PhD. Juan Pérez"
            value={formData.docente_nombre}
            onChange={(e) => handleInputChange('docente_nombre', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Género
          </label>
          <GenderSelect
            value={formData.docente_genero || ''}
            onChange={(value) => handleInputChange('docente_genero', value)}
            placeholder="Escriba o seleccione un género"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Departamento *
          </label>
          <DepartmentSelect
            value={formData.departamento || ''}
            onChange={(value) => handleInputChange('departamento', value)}
            placeholder="Seleccione un departamento"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Cargo *
          </label>
          <CargoSelect
            value={formData.cargo || ''}
            onChange={(value) => handleInputChange('cargo', value)}
            placeholder="Seleccione un cargo"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Memorando (Opcional)
          </label>
          <input
            type="text"
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="EPN-DOCDCTA-2025-0055-M"
            value={formData.memorando}
            onChange={(e) => handleInputChange('memorando', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
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
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Fecha (Opcional)
          </label>
          <input
            type="date"
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            value={formData.fecha}
            onChange={(e) => handleInputChange('fecha', e.target.value)}
          />
          {formData.fecha && (
            <p className="mt-2 text-sm text-gray-600">
              <span className="font-medium">Fecha de reporte:</span>{' '}
              <span className="text-blue-600">{formatDateToSpanish(formData.fecha)}</span>
            </p>
          )}
        </div>
      </div>

      {/* Toggle para borrador vs certificado final */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg border">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-lg font-medium text-gray-800 mb-1">
              Tipo de Documento
            </h4>
            <p className="text-sm text-gray-600">
              {formData.es_borrador 
                ? 'Borrador' 
                : 'Certificado final'}
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <span className={`text-sm font-medium ${formData.es_borrador ? 'text-blue-600' : 'text-gray-500'}`}>
              Borrador
            </span>
            <button
              type="button"
              onClick={() => handleInputChange('es_borrador', !formData.es_borrador)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                formData.es_borrador ? 'bg-gray-300' : 'bg-blue-600'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  formData.es_borrador ? 'translate-x-1' : 'translate-x-6'
                }`}
              />
            </button>
            <span className={`text-sm font-medium ${!formData.es_borrador ? 'text-blue-600' : 'text-gray-500'}`}>
              Final
            </span>
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleGenerateReport}
          disabled={isGenerating}
          className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-3 px-8 rounded-md transition-colors duration-200"
        >
          {isGenerating ? 'Generando...' : `📄 Generar ${formData.es_borrador ? 'Borrador' : 'Certificado Final'}`}
        </button>
      </div>

      <div className="mt-4 text-sm text-gray-600">
        <p><strong>IDs de Autor:</strong> {authorIds.join(', ')}</p>
        <p className="mt-1">* Campos requeridos</p>
      </div>
    </div>
  );
};

export default GeneradorReporte;
