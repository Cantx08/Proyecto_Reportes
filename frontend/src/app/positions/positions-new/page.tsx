'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { usePositions } from '@/hooks/useNewPositions';
import { PositionCreateRequest } from '@/types/api';
import { ErrorNotification } from '@/components/ErrorNotification';
import { Briefcase, Save, ArrowLeft } from 'lucide-react';

const NewPositionPage: React.FC = () => {
  const router = useRouter();
  const { createPosition, creating, error } = usePositions();

  const [formData, setFormData] = useState<PositionCreateRequest>({
    pos_id: '',
    pos_name: '',
  });

  const [validationErrors, setValidationErrors] = useState<{
    pos_id?: string;
    pos_name?: string;
  }>({});

  const validateForm = (): boolean => {
    const errors: typeof validationErrors = {};

    if (!formData.pos_id.trim()) {
      errors.pos_id = 'El código del cargo es requerido';
    }

    if (!formData.pos_name.trim()) {
      errors.pos_name = 'El nombre del cargo es requerido';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const result = await createPosition({
      pos_id: formData.pos_id.trim(),
      pos_name: formData.pos_name.trim(),
    });

    if (result) {
      router.push('/departments-and-positions');
    }
  };

  const handleChange = (field: keyof PositionCreateRequest, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Limpiar error de validación del campo cuando el usuario empieza a escribir
    if (validationErrors[field]) {
      setValidationErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <Link href="/departments-and-positions" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-4">
          <ArrowLeft className="h-4 w-4 mr-1" />
          Volver a Gestión de Cargos
        </Link>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center">
          <Briefcase className="h-6 w-6 mr-3 text-blue-600" />
          Nuevo Cargo
        </h1>
        <p className="text-gray-600 mt-1">
          Crea un nuevo cargo en el sistema
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <ErrorNotification
          error={error}
          onDismiss={() => {}}
        />
      )}

      {/* Form */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Código del Cargo */}
          <div>
            <label htmlFor="pos_id" className="block text-sm font-medium text-gray-700 mb-2">
              Código del Cargo <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="pos_id"
              value={formData.pos_id}
              onChange={(e) => handleChange('pos_id', e.target.value)}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                validationErrors.pos_id ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Ej: PROF_PRINCIPAL"
            />
            {validationErrors.pos_id && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.pos_id}</p>
            )}
            <p className="mt-1 text-sm text-gray-500">
              Este código se usará como identificador único del cargo
            </p>
          </div>

          {/* Nombre del Cargo */}
          <div>
            <label htmlFor="pos_name" className="block text-sm font-medium text-gray-700 mb-2">
              Nombre del Cargo <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="pos_name"
              value={formData.pos_name}
              onChange={(e) => handleChange('pos_name', e.target.value)}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                validationErrors.pos_name ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Ej: Profesor Principal"
            />
            {validationErrors.pos_name && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.pos_name}</p>
            )}
          </div>

          {/* Buttons */}
          <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <Link href="/departments-and-positions" className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </Link>
            <button
              type="submit"
              disabled={creating}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {creating ? (
                <>
                  <span className="mr-2">Creando...</span>
                  <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Crear Cargo
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewPositionPage;
