'use client';

import React, { useState, useEffect } from 'react';
import { Author, Department, Position } from '@/types/api';
import DepartmentSelectNew from './DepartmentSelect';
import PositionSelectNew from './PositionSelect';
import type { DepartmentResponse, PositionResponse } from '@/types/api';
import { Save, X } from 'lucide-react';

interface AuthorFormProps {
  author?: Author | null;
  onSave: (author: Omit<Author, 'author_id'> | Author) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

const AuthorForm: React.FC<AuthorFormProps> = ({
  author,
  onSave,
  onCancel,
  isLoading = false
}) => {
  // Los datos se obtienen directamente de los componentes selectores

  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    dni: '',
    title: '',
    institutional_email: '',
    gender: 'M',
    position: '',
    department: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  // Actualizar formData cuando cambie el autor (para modo edición)
  useEffect(() => {
    if (author) {
      setFormData({
        name: author.name || '',
        surname: author.surname || '',
        dni: author.dni || '',
        title: author.title || '',
        institutional_email: author.institutional_email || '',
        gender: author.gender || 'M',
        position: author.position || '',
        department: author.department || ''
      });
    } else {
      // Reset form para nuevo autor
      setFormData({
        name: '',
        surname: '',
        dni: '',
        title: '',
        institutional_email: '',
        gender: 'M',
        position: '',
        department: ''
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

    if (!formData.name.trim()) {
      newErrors.name = 'El nombre es requerido';
    } else if (formData.name.trim().length < 2) {
      newErrors.name = 'El nombre debe tener al menos 2 caracteres';
    }

    if (!formData.surname.trim()) {
      newErrors.surname = 'El apellido es requerido';
    } else if (formData.surname.trim().length < 2) {
      newErrors.surname = 'El apellido debe tener al menos 2 caracteres';
    }

    if (!formData.dni.trim()) {
      newErrors.dni = 'El DNI/Cédula es requerido';
    } else if (formData.dni.trim().length < 5) {
      newErrors.dni = 'El DNI/Cédula debe tener al menos 5 caracteres';
    }

    // Validar email institucional (opcional pero si se proporciona debe ser válido)
    if (formData.institutional_email && formData.institutional_email.trim()) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.institutional_email.trim())) {
        newErrors.institutional_email = 'El correo institucional no es válido';
      }
    }

    if (!formData.position.trim()) {
      newErrors.position = 'El cargo es requerido';
    }

    if (!formData.department.trim()) {
      newErrors.department = 'El departamento es requerido';
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
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Nombre *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
              errors.name ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Ingrese el nombre"
          />
          {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
        </div>

        <div>
          <label htmlFor="surname" className="block text-sm font-medium text-gray-700 mb-1">
            Apellido *
          </label>
          <input
            type="text"
            id="surname"
            name="surname"
            value={formData.surname}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
              errors.surname ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Ingrese el apellido"
          />
          {errors.surname && <p className="mt-1 text-sm text-red-600">{errors.surname}</p>}
        </div>

        <div>
          <label htmlFor="dni" className="block text-sm font-medium text-gray-700 mb-1">
            DNI/Cédula *
          </label>
          <input
            type="text"
            id="dni"
            name="dni"
            value={formData.dni}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
              errors.dni ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Ingrese el DNI o cédula"
          />
          {errors.dni && <p className="mt-1 text-sm text-red-600">{errors.dni}</p>}
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
            placeholder="Dr., Mg., Ing., etc."
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
            placeholder="correo@epn.edu.ec"
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
            value={formData.position}
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
            value={formData.department}
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