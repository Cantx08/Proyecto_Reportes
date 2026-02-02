'use client';

import React, { useState, useEffect } from 'react';
import DepartmentSelectNew from '../../departments/components/DepartmentSelect';
import PositionSelectNew from '../../job-positions/components/JobPositionSelect';
import { Save, X } from 'lucide-react';
import {AuthorResponse} from "@/features/authors/types";

interface AuthorFormProps {
  author?: AuthorResponse | null;
  onSave: (author: {
    first_name: string;
    last_name: string;
    institutional_email: string;
    title: string;
    gender: string;
    job_position_id: string;
    department_id: string;
    author_id: string
  } | {
    first_name: string;
    last_name: string;
    institutional_email: string;
    title: string;
    gender: string;
    job_position_id: string;
    department_id: string
  }) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

const AuthorForm: React.FC<AuthorFormProps> = ({
  author,
  onSave,
  onCancel,
  isLoading = false
}) => {

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    title: '',
    institutional_email: '',
    gender: 'M',
    job_position_id: '',
    department_id: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  // Actualizar formData cuando cambie el autor (para modo edición)
  useEffect(() => {
    if (author) {
      setFormData({
        first_name: author.first_name || '',
        last_name: author.last_name || '',
        title: author.title || '',
        institutional_email: author.institutional_email || '',
        gender: author.gender || 'M',
        job_position_id: author.job_position_id || '',
        department_id: author.department_id || ''
      });
    } else {
      // Reset form para nuevo autor
      setFormData({
        first_name: '',
        last_name: '',
        title: '',
        institutional_email: '',
        gender: 'M',
        job_position_id: '',
        department_id: ''
      });
    }
    setErrors({});
  }, [author]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.first_name.trim()) {
      newErrors.first_name = 'El nombre es requerido';
    } else if (formData.first_name.trim().length < 2) {
      newErrors.first_name = 'El nombre debe tener al menos 2 caracteres';
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = 'El apellido es requerido';
    } else if (formData.last_name.trim().length < 2) {
      newErrors.last_name = 'El apellido debe tener al menos 2 caracteres';
    }

    // Validar email institucional (opcional pero si se proporciona debe ser válido)
    if (formData.institutional_email && formData.institutional_email.trim()) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.institutional_email.trim())) {
        newErrors.institutional_email = 'El correo institucional no es válido';
      }
    }

    if (!formData.job_position_id.trim()) {
      newErrors.job_position_id = 'El cargo es requerido';
    }

    if (!formData.department_id.trim()) {
      newErrors.department_id = 'El departamento es requerido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const authorData = author
      ? { ...formData, author_id: author.author_id }
      : formData;

    onSave(authorData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-1">
            Nombre *
          </label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
              errors.first_name ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Ingrese el nombre"
          />
          {errors.first_name && <p className="mt-1 text-sm text-red-600">{errors.first_name}</p>}
        </div>

        <div>
          <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-1">
            Apellido *
          </label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
              errors.last_name ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Ingrese el apellido"
          />
          {errors.last_name && <p className="mt-1 text-sm text-red-600">{errors.last_name}</p>}
        </div>

        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Título
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
            placeholder="PhD., MsC., Ing., etc."
          />
        </div>

        <div>
          <label htmlFor="institutional_email" className="block text-sm font-medium text-gray-700 mb-1">
            Correo Institucional
          </label>
          <input
            type="email"
            id="institutional_email"
            name="institutional_email"
            value={formData.institutional_email}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
              errors.institutional_email ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="user@example.edu.ec"
          />
          {errors.institutional_email && <p className="mt-1 text-sm text-red-600">{errors.institutional_email}</p>}
        </div>

        <div>
          <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-1">
            Género
          </label>
          <select
            id="gender"
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="M">Masculino</option>
            <option value="F">Femenino</option>
          </select>
        </div>

        <div>
          <label htmlFor="position" className="block text-sm font-medium text-gray-700 mb-1">
            Cargo *
          </label>
          <PositionSelectNew
            value={formData.job_position_id}
            onChange={(value) => setFormData(prev => ({ ...prev, position: value }))}
            error={errors.position}
            placeholder="Seleccione un cargo"
          />
          {errors.position && <p className="mt-1 text-sm text-red-600">{errors.position}</p>}
        </div>

        <div className="md:col-span-2">
          <label htmlFor="department" className="block text-sm font-medium text-gray-700 mb-1">
            Departamento *
          </label>
          <DepartmentSelectNew
            value={formData.department_id}
            onChange={(value) => setFormData(prev => ({ ...prev, department: value }))}
            error={errors.department}
            placeholder="Seleccione un departamento"
          />
          {errors.department && <p className="mt-1 text-sm text-red-600">{errors.department}</p>}
        </div>
      </div>

      <div className="flex justify-end space-x-3 pt-6 border-t border-gray-200">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          disabled={isLoading}
        >
          <X className="w-4 h-4 mr-2 inline" />
          Cancelar
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          disabled={isLoading}
        >
          <Save className="w-4 h-4 mr-2 inline" />
          {isLoading ? 'Guardando...' : (author ? 'Actualizar' : 'Crear')}
        </button>
      </div>
    </form>
  );
};

export default AuthorForm;