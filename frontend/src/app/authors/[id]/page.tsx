'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuthors } from '@/hooks/useAuthors';
import { useNewDepartments } from '@/hooks/useNewDepartments';
import { usePositions } from '@/hooks/useNewPositions';
import { ArrowLeft, Save, Loader2, User } from 'lucide-react';
import Link from 'next/link';
import ScopusAccountsManager from '@/components/ScopusAccountsManager';

export default function EditarAutorPage() {
  const router = useRouter();
  const params = useParams();
  const authorId = params?.id as string;

  const { getAuthor, updateAuthor, updating, error } = useAuthors();
  const { departments, loading: loadingDepartments } = useNewDepartments();
  const { positions, loading: loadingPositions } = usePositions();

  const [loading, setLoading] = useState(true);
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

  // Cargar datos del autor
  useEffect(() => {
    const loadAuthor = async () => {
      if (!authorId) {
        router.push('/authors');
        return;
      }

      setLoading(true);
      const author = await getAuthor(authorId);
      
      if (author) {
        setFormData({
          name: author.name || '',
          surname: author.surname || '',
          dni: author.dni || '',
          title: author.title || '',
          birth_date: author.birth_date ? author.birth_date.split('T')[0] : '',
          gender: author.gender || 'M',
          position: author.position || '',
          department: author.department || ''
        });
      } else {
        setSubmitError('No se pudo cargar el autor');
      }
      
      setLoading(false);
    };

    loadAuthor();
  }, [authorId, getAuthor, router]);

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

    const updatedAuthor = await updateAuthor(authorId, formData);

    if (updatedAuthor) {
      setSubmitSuccess(true);
      setTimeout(() => {
        router.push('/authors');
      }, 1500);
    } else {
      setSubmitError(error || 'Error al actualizar el autor');
    }
  };

  if (loading || loadingDepartments || loadingPositions) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-primary-500" />
          <p className="text-neutral-600">Cargando datos del autor...</p>
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
            <User className="h-12 w-12 mr-3 text-neutral-900" />
            <div>
              <h1 className="text-2xl font-bold text-neutral-900">Editar Autor</h1>
              <p className="text-neutral-600 mt-1">Actualiza la información del autor</p>
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
              <h3 className="text-sm font-medium text-error-800">Error al actualizar</h3>
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
              <p className="mt-2 text-sm text-success-700">El autor se actualizó correctamente. Redirigiendo...</p>
            </div>
          </div>
        </div>
      )}

      {/* Form */}
      <div className="bg-white rounded-lg border border-neutral-200 shadow-sm">
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Información Personal Section */}
          <div className="space-y-6">
            <div className="flex items-center pb-3 border-b border-neutral-200">
              <div className="flex-shrink-0 w-10 h-10 flex items-center justify-center">
                <User className="h-8 w-8 text-primary-600" />
              </div>
              <div className="ml-3">
                <h3 className="text-xl font-semibold text-primary-600">Información Personal</h3>
              </div>
            </div>

            {/* Cédula y Título */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="dni" className="block text-sm font-medium text-neutral-700 mb-2">
                  Cédula de Identidad <span className="text-error-500">*</span>
                </label>
                <input
                  type="text"
                  id="dni"
                  name="dni"
                  value={formData.dni}
                  onChange={handleInputChange}
                  placeholder="1234567890"
                  maxLength={10}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                    validationErrors.dni 
                      ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50' 
                      : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
                  }`}
                />
                {validationErrors.dni && (
                  <p className="mt-1 text-sm text-error-600 flex items-center">
                    <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    {validationErrors.dni}
                  </p>
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
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                />
              </div>
            </div>

            {/* Nombres y Apellidos */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                  placeholder="Juan Carlos"
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                    validationErrors.name 
                      ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50' 
                      : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
                  }`}
                />
                {validationErrors.name && (
                  <p className="mt-1 text-sm text-error-600 flex items-center">
                    <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    {validationErrors.name}
                  </p>
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
                  placeholder="Pérez García"
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                    validationErrors.surname 
                      ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50' 
                      : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
                  }`}
                />
                {validationErrors.surname && (
                  <p className="mt-1 text-sm text-error-600 flex items-center">
                    <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    {validationErrors.surname}
                  </p>
                )}
              </div>
            </div>

            {/* Fecha de Nacimiento y Género */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
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
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                >
                  <option value="M">Masculino</option>
                  <option value="F">Femenino</option>
                </select>
              </div>
            </div>
          </div>

          {/* Información Académica Section */}
          <div className="space-y-6 pt-6">
            <div className="flex items-center pb-3 border-b border-neutral-200">
              <div className="flex-shrink-0 w-10 h-10 flex items-center justify-center">
                <svg className="h-8 w-8 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-xl font-semibold text-secondary-600">Información Académica</h3>
              </div>
            </div>

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
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                  validationErrors.department 
                    ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50' 
                    : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
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
                <p className="mt-1 text-sm text-error-600 flex items-center">
                  <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {validationErrors.department}
                </p>
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
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                  validationErrors.position 
                    ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50' 
                    : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
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
                <p className="mt-1 text-sm text-error-600 flex items-center">
                  <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {validationErrors.position}
                </p>
              )}
            </div>
          </div>

          {/* Identificadores de Investigación Section */}
          <div className="space-y-6 pt-6">
            <div className="flex items-center pb-3 border-b border-neutral-200">
              <div className="flex-shrink-0 w-10 h-10 flex items-center justify-center">
                <svg className="h-8 w-8 text-info-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-xl font-semibold text-info-600">Cuentas Scopus</h3>
              </div>
            </div>
            
            {/* Cuentas Scopus */}
            <ScopusAccountsManager
              authorId={authorId ? parseInt(authorId) : undefined}
              initialAccounts={scopusAccounts}
              onChange={setScopusAccounts}
            />
          </div>

          {/* Buttons */}
          <div className="flex justify-end space-x-3 pt-6">
            <Link href="/authors">
              <button
                type="button"
                className="px-6 py-2.5 border border-neutral-300 rounded-lg text-neutral-700 hover:bg-neutral-50 transition-colors font-medium"
              >
                Cancelar
              </button>
            </Link>
            <button
              type="submit"
              disabled={updating}
              className="px-6 py-2.5 bg-primary-500 hover:bg-primary-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-colors shadow-sm font-medium"
            >
              {updating ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Actualizando...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Actualizar Autor
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
