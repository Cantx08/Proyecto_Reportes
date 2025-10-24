'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthors } from '@/hooks/useAuthors';
import { useNewDepartments } from '@/hooks/useNewDepartments';
import { usePositions } from '@/hooks/useNewPositions';
import { ArrowLeft, Save, Loader2, UserPlus } from 'lucide-react';
import Link from 'next/link';
import ScopusAccountsManager from '@/components/ScopusAccountsManager';

export default function NuevoAutorPage() {
  const router = useRouter();
  const { createAuthor, creating, error } = useAuthors();
  const { departments, loading: loadingDepartments } = useNewDepartments();
  const { positions, loading: loadingPositions } = usePositions();

  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    dni: '',
    title: '',
    birth_date: '',
    gender: 'M',
    position: '',
    department: ''
  });

  const [scopusAccounts, setScopusAccounts] = useState<any[]>([]);

  const [validationErrors, setValidationErrors] = useState<{
    name?: string;
    surname?: string;
    dni?: string;
    position?: string;
    department?: string;
  }>({});

  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error de validación al editar
    if (validationErrors[name as keyof typeof validationErrors]) {
      setValidationErrors(prev => ({
        ...prev,
        [name]: undefined
      }));
    }
  };

  const validateForm = (): boolean => {
    const errors: typeof validationErrors = {};
    
    if (!formData.name.trim()) {
      errors.name = 'El nombre es obligatorio';
    }
    
    if (!formData.surname.trim()) {
      errors.surname = 'El apellido es obligatorio';
    }
    
    if (!formData.dni.trim()) {
      errors.dni = 'La cédula es obligatoria';
    }
    
    if (!formData.position.trim()) {
      errors.position = 'El cargo es obligatorio';
    }
    
    if (!formData.department.trim()) {
      errors.department = 'El departamento es obligatorio';
    }
    
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);
    setSubmitSuccess(false);

    if (!validateForm()) {
      return;
    }

    const newAuthor = await createAuthor(formData);

    if (newAuthor) {
      setSubmitSuccess(true);
      setTimeout(() => {
        router.push('/authors');
      }, 1500);
    } else {
      setSubmitError(error || 'Error al crear el autor');
    }
  };

  if (loadingDepartments || loadingPositions) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4" style={{ color: '#042a53' }} />
          <p className="text-gray-600">Cargando datos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">        
        <div className="flex items-center">
          <UserPlus className="h-8 w-8 mr-3" style={{ color: '#042a53' }} />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Agregar Autor</h1>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {submitError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <p className="mt-2 text-sm text-red-700">{submitError}</p>
            </div>
          </div>
        </div>
      )}

      {/* Success Message */}
      {submitSuccess && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">¡Éxito!</h3>
              <p className="mt-2 text-sm text-green-700">El autor se creó correctamente. Redirigiendo...</p>
            </div>
          </div>
        </div>
      )}

      {/* Form */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Título */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Título
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              placeholder="Ej: Dr., Mg., Ing."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Nombres y Apellidos */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                Nombres <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.name ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.name && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.name}</p>
              )}
            </div>

            <div>
              <label htmlFor="surname" className="block text-sm font-medium text-gray-700 mb-2">
                Apellidos <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="surname"
                name="surname"
                value={formData.surname}
                onChange={handleInputChange}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.surname ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.surname && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.surname}</p>
              )}
            </div>
          </div>

          {/* DNI */}
          <div>
            <label htmlFor="dni" className="block text-sm font-medium text-gray-700 mb-2">
              Cédula <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="dni"
              name="dni"
              value={formData.dni}
              onChange={handleInputChange}
              placeholder="Ej: 1234567890"
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                validationErrors.dni ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {validationErrors.dni && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.dni}</p>
            )}
          </div>

          {/* Fecha de Nacimiento y Género */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="birth_date" className="block text-sm font-medium text-gray-700 mb-2">
                Fecha de Nacimiento
              </label>
              <input
                type="date"
                id="birth_date"
                name="birth_date"
                value={formData.birth_date}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-2">
                Género <span className="text-red-500">*</span>
              </label>
              <select
                id="gender"
                name="gender"
                value={formData.gender}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
              </select>
            </div>
          </div>

          {/* Departamento */}
          <div>
            <label htmlFor="department" className="block text-sm font-medium text-gray-700 mb-2">
              Departamento <span className="text-red-500">*</span>
            </label>
            <select
              id="department"
              name="department"
              value={formData.department}
              onChange={handleInputChange}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                validationErrors.department ? 'border-red-500' : 'border-gray-300'
              }`}
            >
              <option value="">Seleccione un departamento</option>
              {departments.map((dept) => (
                <option key={dept.dep_id} value={dept.dep_name}>
                  {dept.dep_name} - {dept.fac_name}
                </option>
              ))}
            </select>
            {validationErrors.department && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.department}</p>
            )}
          </div>

          {/* Cargo */}
          <div>
            <label htmlFor="position" className="block text-sm font-medium text-gray-700 mb-2">
              Cargo <span className="text-red-500">*</span>
            </label>
            <select
              id="position"
              name="position"
              value={formData.position}
              onChange={handleInputChange}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                validationErrors.position ? 'border-red-500' : 'border-gray-300'
              }`}
            >
              <option value="">Seleccione un cargo</option>
              {positions.map((pos) => (
                <option key={pos.pos_id} value={pos.pos_name}>
                  {pos.pos_name}
                </option>
              ))}
            </select>
            {validationErrors.position && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.position}</p>
            )}
          </div>

          {/* Divisor */}
          <div className="border-t border-gray-200 pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Identificadores de Investigación
            </h3>
            
            {/* Cuentas Scopus */}
            <ScopusAccountsManager
              initialAccounts={scopusAccounts}
              onChange={setScopusAccounts}
            />
          </div>

          {/* Buttons */}
          <div className="flex justify-end space-x-4 pt-4">
            <Link href="/authors">
              <button
                type="button"
                className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
            </Link>
            <button
              type="submit"
              disabled={creating}
              className="px-6 py-2 text-white rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              style={{ backgroundColor: '#042a53' }}
            >
              {creating ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Creando...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Crear Autor
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}