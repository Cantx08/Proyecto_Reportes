'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter, useParams } from 'next/navigation';
import { usePositions } from '@/hooks/useNewPositions';
import { PositionUpdateRequest, PositionResponse } from '@/types/api';
import { ErrorNotification } from '@/components/ErrorNotification';
import { Briefcase, Save, ArrowLeft, Loader2 } from 'lucide-react';

const EditPositionPage: React.FC = () => {
  const router = useRouter();
  const params = useParams();
  const posId = params?.id as string;
  
  const { getPosition, updatePosition, updating, error } = usePositions();

  const [loading, setLoading] = useState(true);
  const [position, setPosition] = useState<PositionResponse | null>(null);
  const [formData, setFormData] = useState<PositionUpdateRequest>({
    pos_name: '',
  });

  const [validationErrors, setValidationErrors] = useState<{
    pos_name?: string;
  }>({});

  useEffect(() => {
    const loadPosition = async () => {
      if (!posId) return;
      
      setLoading(true);
      const positionData = await getPosition(posId);
      
      if (positionData) {
        setPosition(positionData);
        setFormData({
          pos_name: positionData.pos_name,
        });
      }
      setLoading(false);
    };

    loadPosition();
  }, [posId, getPosition]);

  const validateForm = (): boolean => {
    const errors: typeof validationErrors = {};

    if (!formData.pos_name?.trim()) {
      errors.pos_name = 'El nombre del cargo es requerido';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm() || !posId) {
      return;
    }

    const result = await updatePosition(posId, {
      pos_name: formData.pos_name?.trim(),
    });

    if (result) {
      router.push('/departments-and-positions');
    }
  };

  const handleChange = (field: keyof PositionUpdateRequest, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Limpiar error de validación del campo cuando el usuario empieza a escribir
    if (validationErrors[field]) {
      setValidationErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Cargando cargo...</p>
        </div>
      </div>
    );
  }

  if (!position) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">No se pudo cargar el cargo</p>
          <Link href="/departments-and-positions" className="text-red-600 hover:text-red-800 text-sm mt-2 inline-block">
            Volver a Gestión de Cargos
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <Link href="/departments-and-positions" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-4">
          <ArrowLeft className="h-4 w-4 mr-1" />
          Volver a Gestión de Cargos
        </Link>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center">
          <Briefcase className="h-6 w-6 mr-3 text-[#042a53]" />
          Editar Cargo
        </h1>
        <p className="text-gray-600 mt-1">
          Modifica la información del cargo
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
          {/* Código del Cargo (disabled) */}
          <div>
            <label htmlFor="pos_id" className="block text-sm font-medium text-gray-700 mb-2">
              Código del Cargo
            </label>
            <input
              type="text"
              id="pos_id"
              value={position.pos_id}
              disabled
              className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500 cursor-not-allowed"
            />
            <p className="mt-1 text-sm text-gray-500">
              El código del cargo no puede ser modificado
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
              disabled={updating}
              className="px-4 py-2 text-sm font-medium text-white bg-[#042a53] rounded-lg hover:bg-[#042a53]/80 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {updating ? (
                <>
                  <span className="mr-2">Actualizando...</span>
                  <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Actualizar Cargo
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditPositionPage;
