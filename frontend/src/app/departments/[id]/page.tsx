'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useDepartments } from '@/features/departments/hooks/useDepartments';
import { FacultySelect } from '@/components/FacultySelect';
import { Building, ArrowLeft, Save, Loader2 } from 'lucide-react';
import Link from 'next/link';
import {DepartmentUpdateRequest} from "@/features/departments/types";

export default function EditDepartmentPage() {
  const router = useRouter();
  const params = useParams();
  const depId = params.id as string;
  
  const { getDepartment, updateDepartment, updating } = useDepartments();

  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    depCode: '',
    depName: '',
    facultyName: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    const loadDepartment = async () => {
      try {
        const department = await getDepartment(depId);
        if (department) {
          setFormData({
            depCode: department.depCode || department.depId,
            depName: department.depName,
            facultyName: department.facultyName
          });
        }
      } catch (error) {
        console.error('Error loading department:', error);
      } finally {
        setLoading(false);
      }
    };

    if (depId) {
      loadDepartment();
    }
  }, [depId, getDepartment]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.depCode.trim()) {
      newErrors.depCode = 'El código del departamento es requerido';
    }

    if (!formData.depName.trim()) {
      newErrors.depName = 'El nombre del departamento es requerido';
    }

    if (!formData.facultyName.trim()) {
      newErrors.facultyName = 'La facultad es requerida';
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
      facultyName: value
    }));
    
    if (errors.facultyName) {
      setErrors(prev => ({
        ...prev,
        facultyName: ''
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    try {
      const updateData: DepartmentUpdateRequest = {
        depCode: formData.depCode,
        depName: formData.depName,
        facultyName: formData.facultyName
      };
      
      const result = await updateDepartment(depId, updateData);
      
      if (result) {
        router.push('/departments-and-positions');
      }
    } catch (error) {
      console.error('Error updating department:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-primary-600" />
          <p className="text-neutral-600">Cargando departamento...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">

      <div className="mb-6 mt-6">
        <Link 
          href="/departments-and-positions"
          className="inline-flex items-center text-sm text-neutral-600 hover:text-primary-600 transition-colors"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver a Departamentos y Cargos
        </Link>
      </div>

      <div className="bg-white rounded-lg border border-neutral-200 shadow-sm">
        <div className="p-6 border-b border-neutral-200">
          <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
            <Building className="h-6 w-6 mr-3 text-primary-600" />
            Editar Departamento
          </h1>
          <p className="text-neutral-600 mt-1">
            Modifica la información del departamento
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div>
            <label htmlFor="depCode" className="block text-sm font-medium text-neutral-700 mb-1">
              Código del Departamento <span className="text-error-500">*</span>
            </label>
            <input
              type="text"
              id="depCode"
              name="depCode"
              value={formData.depCode}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors ${
                errors.depCode ? 'border-error-500' : 'border-neutral-300'
              }`}
              placeholder="Ejemplo: DCCO, DFIS, DICA"
            />
            {errors.depCode && (
              <p className="mt-1 text-sm text-error-600">{errors.depCode}</p>
            )}
            <p className="mt-1 text-sm text-neutral-500">
              Código único del departamento (siglas)
            </p>
          </div>

          <div>
            <label htmlFor="depName" className="block text-sm font-medium text-neutral-700 mb-1">
              Nombre del Departamento <span className="text-error-500">*</span>
            </label>
            <input
              type="text"
              id="depName"
              name="depName"
              value={formData.depName}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors ${
                errors.depName ? 'border-error-500' : 'border-neutral-300'
              }`}
              placeholder="Ejemplo: Departamento de Ciencias de la Computación"
            />
            {errors.depName && (
              <p className="mt-1 text-sm text-error-600">{errors.depName}</p>
            )}
          </div>

          <div>
            <label htmlFor="facultyName" className="block text-sm font-medium text-neutral-700 mb-1">
              Facultad <span className="text-error-500">*</span>
            </label>
            <FacultySelect
              value={formData.facultyName}
              onChange={handleFacultyChange}
              error={errors.facultyName}
              required
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4 border-t border-neutral-200">
            <Link href="/departments-and-positions" className="px-4 py-2 text-sm font-medium text-neutral-700 bg-white border border-neutral-300 rounded-lg hover:bg-neutral-50 transition-colors">
              Cancelar
            </Link>
            <button
              type="submit"
              disabled={updating}
              className="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-colors"
            >
              {updating ? (
                <>
                  <span className="mr-2">Actualizando...</span>
                  <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Actualizar Departamento
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
