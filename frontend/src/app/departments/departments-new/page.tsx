'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useNewDepartments } from '@/hooks/useNewDepartments';
import { DepartmentCreateRequest } from '@/types/api';
import { FacultySelect } from '@/components/FacultySelect';
import { Building, ArrowLeft, Save } from 'lucide-react';
import Link from 'next/link';

export default function NewDepartmentPage() {
  const router = useRouter();
  const { createDepartment, creating } = useNewDepartments();

  const [formData, setFormData] = useState({
    dep_code: '',
    dep_name: '',
    fac_name: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.dep_code.trim()) {
      newErrors.dep_code = 'El código del departamento es requerido';
    }

    if (!formData.dep_name.trim()) {
      newErrors.dep_name = 'El nombre del departamento es requerido';
    }

    if (!formData.fac_name.trim()) {
      newErrors.fac_name = 'La facultad es requerida';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleFacultyChange = (value: string) => {
    setFormData(prev => ({
      ...prev,
      fac_name: value
    }));
    
    if (errors.fac_name) {
      setErrors(prev => ({
        ...prev,
        fac_name: ''
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    try {
      const createData: DepartmentCreateRequest = {
        dep_id: formData.dep_code,
        dep_code: formData.dep_code,
        dep_name: formData.dep_name,
        fac_name: formData.fac_name
      };
      
      const result = await createDepartment(createData);
      
      if (result) {
        router.push('/departments-and-positions');
      }
    } catch (error) {
      console.error('Error creating department:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <Link 
          href="/departments-and-positions"
          className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver a Departamentos
        </Link>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <Building className="h-6 w-6 mr-3 text-blue-600" />
            Nuevo Departamento
          </h1>
          <p className="text-gray-600 mt-1">
            Completa la información del departamento
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div>
            <label htmlFor="dep_code" className="block text-sm font-medium text-gray-700 mb-1">
              Código del Departamento <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="dep_code"
              name="dep_code"
              value={formData.dep_code}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.dep_code ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Ejemplo: DCCO, DFIS, DICA"
            />
            {errors.dep_code && (
              <p className="mt-1 text-sm text-red-600">{errors.dep_code}</p>
            )}
            <p className="mt-1 text-sm text-gray-500">
              Código único del departamento (siglas)
            </p>
          </div>

          <div>
            <label htmlFor="dep_name" className="block text-sm font-medium text-gray-700 mb-1">
              Nombre del Departamento <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="dep_name"
              name="dep_name"
              value={formData.dep_name}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.dep_name ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Ejemplo: Departamento de Ciencias de la Computación"
            />
            {errors.dep_name && (
              <p className="mt-1 text-sm text-red-600">{errors.dep_name}</p>
            )}
          </div>

          <div>
            <label htmlFor="fac_name" className="block text-sm font-medium text-gray-700 mb-1">
              Facultad <span className="text-red-500">*</span>
            </label>
            <FacultySelect
              value={formData.fac_name}
              onChange={handleFacultyChange}
              error={errors.fac_name}
              required
            />
          </div>

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
                  <span className="mr-2">Guardando...</span>
                  <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Guardar Departamento
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
