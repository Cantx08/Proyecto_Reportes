'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthors } from '@/hooks/useAuthors';
import { useDepartments } from '@/hooks/useDepartments';
import { usePositions } from '@/hooks/usePositions';
import { ArrowLeft, Save, Loader2, UserPlus, User, AlertCircle, GraduationCap, BookOpen } from 'lucide-react';
import Link from 'next/link';
import ScopusAccountsManager from '@/components/ScopusAccountsManager';

export default function NewAuthorPage() {
  const router = useRouter();
  const { createAuthor, creating, error } = useAuthors();
  const { departments, loading: loadingDepartments } = useDepartments();
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
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-primary-500" />
          <p className="text-neutral-600">Cargando datos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">        
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <UserPlus className="h-8 w-8 mr-3 text-primary-500" />
            <div>
              <h1 className="text-2xl font-bold text-neutral-900">Nuevo Autor</h1>
              <p className="text-neutral-600 mt-1">Registra un nuevo autor en el sistema</p>
            </div>
          </div>
          <Link href="/authors">
            <button className="flex items-center px-4 py-2 text-neutral-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Volver
            </button>
          </Link>
        </div>
      </div>

      {/* Error Message */}
      {submitError && (
        <div className="bg-error-50 border border-error-200 rounded-lg p-4 mb-6 animate-fade-in">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-error-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-error-800">Error al crear autor</h3>
              <p className="mt-2 text-sm text-error-700">{submitError}</p>
            </div>
          </div>
        </div>
      )}

      {/* Success Message */}
      {submitSuccess && (
        <div className="bg-success-50 border border-success-200 rounded-lg p-4 mb-6 animate-fade-in">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-success-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-success-800">¡Éxito!</h3>
              <p className="mt-2 text-sm text-success-700">El autor se creó correctamente. Redirigiendo...</p>
            </div>
          </div>
        </div>
      )}

      {/* Form */}
      <div className="bg-white shadow-md rounded-lg p-8">
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Personal Information Section */}
          <div>
            <div className="flex items-center mb-6">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary-100 mr-3">
                <User className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-neutral-900">Información Personal</h2>
                <p className="text-sm text-neutral-500">Datos básicos del autor</p>
              </div>
            </div>

            <div className="space-y-6">
              {/* Cédula y Título */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="dni" className="block text-sm font-medium text-neutral-700 mb-2">
                    Cédula <span className="text-error-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="dni"
                    name="dni"
                    value={formData.dni}
                    onChange={handleInputChange}
                    placeholder="Ej: 1234567890"
                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                      validationErrors.dni ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
                    }`}
                  />
                  {validationErrors.dni && (
                    <div className="flex items-center mt-2 text-error-600">
                      <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0" />
                      <p className="text-sm">{validationErrors.dni}</p>
                    </div>
                  )}
                </div>

                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-neutral-700 mb-2">
                    Título Académico
                  </label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    placeholder="Ej: Dr., Mg., Ing."
                    className="w-full px-4 py-2.5 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white hover:border-neutral-400 transition-colors"
                  />
                </div>
              </div>

              {/* Nombres y Apellidos */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-neutral-700 mb-2">
                    Nombres <span className="text-error-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="Ej: Juan Carlos"
                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                      validationErrors.name ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
                    }`}
                  />
                  {validationErrors.name && (
                    <div className="flex items-center mt-2 text-error-600">
                      <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0" />
                      <p className="text-sm">{validationErrors.name}</p>
                    </div>
                  )}
                </div>

                <div>
                  <label htmlFor="surname" className="block text-sm font-medium text-neutral-700 mb-2">
                    Apellidos <span className="text-error-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="surname"
                    name="surname"
                    value={formData.surname}
                    onChange={handleInputChange}
                    placeholder="Ej: Pérez González"
                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                      validationErrors.surname ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
                    }`}
                  />
                  {validationErrors.surname && (
                    <div className="flex items-center mt-2 text-error-600">
                      <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0" />
                      <p className="text-sm">{validationErrors.surname}</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Fecha de Nacimiento y Género */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="birth_date" className="block text-sm font-medium text-neutral-700 mb-2">
                    Fecha de Nacimiento
                  </label>
                  <input
                    type="date"
                    id="birth_date"
                    name="birth_date"
                    value={formData.birth_date}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2.5 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white hover:border-neutral-400 transition-colors"
                  />
                </div>

                <div>
                  <label htmlFor="gender" className="block text-sm font-medium text-neutral-700 mb-2">
                    Género <span className="text-error-500">*</span>
                  </label>
                  <select
                    id="gender"
                    name="gender"
                    value={formData.gender}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2.5 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white hover:border-neutral-400 transition-colors"
                  >
                    <option value="M">Masculino</option>
                    <option value="F">Femenino</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Academic Information Section */}
          <div className="border-t border-neutral-200 pt-8">
            <div className="flex items-center mb-6">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-info-100 mr-3">
                <GraduationCap className="h-5 w-5 text-info-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-neutral-900">Información Académica</h2>
                <p className="text-sm text-neutral-500">Departamento al que pertenece y cargo que ocupa.</p>
              </div>
            </div>

            <div className="space-y-6">
              {/* Departamento */}
              <div>
                <label htmlFor="department" className="block text-sm font-medium text-neutral-700 mb-2">
                  Departamento <span className="text-error-500">*</span>
                </label>
                <select
                  id="department"
                  name="department"
                  value={formData.department}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                    validationErrors.department ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
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
                  <div className="flex items-center mt-2 text-error-600">
                    <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0" />
                    <p className="text-sm">{validationErrors.department}</p>
                  </div>
                )}
              </div>

              {/* Cargo */}
              <div>
                <label htmlFor="position" className="block text-sm font-medium text-neutral-700 mb-2">
                  Cargo <span className="text-error-500">*</span>
                </label>
                <select
                  id="position"
                  name="position"
                  value={formData.position}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                    validationErrors.position ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
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
                  <div className="flex items-center mt-2 text-error-600">
                    <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0" />
                    <p className="text-sm">{validationErrors.position}</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Research IDs Section */}
          <div className="border-t border-neutral-200 pt-8">
            <div className="flex items-center mb-6">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-secondary-100 mr-3">
                <BookOpen className="h-5 w-5 text-secondary-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-neutral-900">Cuentas Scopus</h2>
                <p className="text-sm text-neutral-500">IDs de cuentas asociadas</p>
              </div>
            </div>
            
            {/* Cuentas Scopus */}
            <ScopusAccountsManager
              initialAccounts={scopusAccounts}
              onChange={setScopusAccounts}
            />
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end space-x-4 pt-6 border-t border-neutral-200">
            <Link href="/authors">
              <button
                type="button"
                className="px-6 py-2.5 border-2 border-neutral-300 rounded-lg text-neutral-700 font-medium hover:bg-neutral-50 hover:border-neutral-400 transition-all"
              >
                Cancelar
              </button>
            </Link>
            <button
              type="submit"
              disabled={creating}
              className="px-6 py-2.5 bg-success-600 text-white rounded-lg font-medium hover:bg-success-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center shadow-sm hover:shadow transition-all"
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