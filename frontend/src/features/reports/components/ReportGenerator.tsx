'use client';

import React, { useState, useEffect } from 'react';
import { ReportRequest } from '@/features/reports/types';
import { reportService } from '@/features/reports/services/reportService';
import { formatDateToSpanish } from '@/utils/helpers';
import DepartmentSelect from '../../departments/components/DepartmentSelect';
import JobPositionSelect from '../../job-positions/components/JobPositionSelect';
import GenderSelect from './GenderSelect';
import FirmanteSelect from './SignatorySelect';
import ElaboradorSelect from './ElaboradorSelect';

import {AuthorResponse} from "@/features/authors/types";

interface ReportGeneratorProps {
  authorIds: string[];
  selectedAuthor?: AuthorResponse;
  onError: (error: string) => void;
}

const ReportGenerator: React.FC<ReportGeneratorProps> = ({ authorIds, selectedAuthor, onError }) => {
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
    elaborador: 'M. Vásquez',
  });

  // Pre-llenar los campos cuando hay un autor seleccionado
  useEffect(() => {
    if (selectedAuthor) {
      const fullName = `${selectedAuthor.title} ${selectedAuthor.first_name} ${selectedAuthor.last_name}`.trim();
      setFormData(prev => ({
        ...prev,
        docente_nombre: fullName,
        docente_genero: selectedAuthor.gender || 'M',
        // Los IDs de departamento y cargo se resuelven en los selectores
        departamento: selectedAuthor.department_id || '',
        cargo: selectedAuthor.job_position_id || '',
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
        elaborador: formData.elaborador || 'M. Vásquez',
      };

      const blob = await reportService.generateCertification(reportRequest);
      
      // Crear URL para descargar el PDF
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `certificado_${formData.docente_nombre.replace(/\s+/g, '_')}.pdf`;
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
                Datos autocompletados
              </h3>
              <p className="mt-1 text-sm text-info-700">
                Los campos se han completado con la información del autor seleccionado: <strong>{selectedAuthor.title} {selectedAuthor.first_name} {selectedAuthor.last_name}</strong>.
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
          <JobPositionSelect
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
            positionValue={formData.firmante || 1}
            nameValue={formData.firmante_nombre || ''}
            onPositionChange={(value) => handleInputChange('firmante', value)}
            onNameChange={(value) => handleInputChange('firmante_nombre', value)}
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

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Elaborado por
          </label>
          <ElaboradorSelect
            value={formData.elaborador || ''}
            onChange={(value) => handleInputChange('elaborador', value)}
            placeholder="Seleccione o escriba el elaborador"
          />
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleGenerateReport}
          disabled={isGenerating}
          className="w-full sm:w-auto bg-primary-600 hover:bg-primary-700 disabled:bg-neutral-400 disabled:cursor-not-allowed text-white font-medium py-3 px-8 rounded-md transition-colors duration-200 shadow-sm"
        >
          {isGenerating ? 'Generando...' : '📄 Generar Certificado'}
        </button>
      </div>
    </div>
  );
};

export default ReportGenerator;
