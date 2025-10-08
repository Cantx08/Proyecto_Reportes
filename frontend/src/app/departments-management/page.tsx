'use client';

import React, { useState } from 'react';
import { useNewDepartments } from '@/hooks/useNewDepartments';
import { DepartmentResponse, DepartmentCreateRequest, DepartmentUpdateRequest } from '@/types/api';
import { ErrorNotification } from '@/components/ErrorNotification';
import { Plus, Edit, Trash2, Search, Building } from 'lucide-react';

const DepartmentsManagementPage: React.FC = () => {
  const { 
    departments, 
    loading, 
    error, 
    createDepartment, 
    updateDepartment, 
    deleteDepartment, 
    fetchDepartments 
  } = useNewDepartments();

  const [showForm, setShowForm] = useState(false);
  const [editingDepartment, setEditingDepartment] = useState<DepartmentResponse | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    dep_id: '',
    dep_name: '',
    fac_name: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const filteredDepartments = departments.filter((department: DepartmentResponse) => 
    department.dep_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    department.fac_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.dep_name.trim()) {
      newErrors.dep_name = 'El nombre del departamento es requerido';
    }

    if (!formData.fac_name.trim()) {
      newErrors.fac_name = 'El nombre de la facultad es requerido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const resetForm = () => {
    setFormData({
      dep_id: '',
      dep_name: '',
      fac_name: ''
    });
    setErrors({});
    setEditingDepartment(null);
  };

  const handleCreate = async () => {
    if (!validateForm()) return;
    
    try {
      const dep_id = `dep_${Date.now()}`;
      const createData: DepartmentCreateRequest = {
        dep_id,
        dep_code: dep_id, // Usando el mismo ID como código
        dep_name: formData.dep_name,
        fac_name: formData.fac_name
      };
      
      await createDepartment(createData);
      setShowForm(false);
      resetForm();
    } catch (error) {
      console.error('Error creating department:', error);
    }
  };

  const handleUpdate = async () => {
    if (!editingDepartment || !validateForm()) return;
    
    try {
      const updateData: DepartmentUpdateRequest = {
        dep_code: formData.dep_id, // Actualizando también el código
        dep_name: formData.dep_name,
        fac_name: formData.fac_name
      };
      
      await updateDepartment(editingDepartment.dep_id, updateData);
      setEditingDepartment(null);
      setShowForm(false);
      resetForm();
    } catch (error) {
      console.error('Error updating department:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingDepartment) {
      handleUpdate();
    } else {
      handleCreate();
    }
  };

  const handleEdit = (department: DepartmentResponse) => {
    setEditingDepartment(department);
    setFormData({
      dep_id: department.dep_id,
      dep_name: department.dep_name,
      fac_name: department.fac_name
    });
    setShowForm(true);
  };

  const handleDelete = async (departmentId: string) => {
    try {
      await deleteDepartment(departmentId);
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Error deleting department:', error);
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    resetForm();
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

  if (loading && departments.length === 0) {
    return (
      <div className="flex justify-center items-center min-h-96">
        <div className="text-lg text-gray-600">Cargando departamentos...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md">
        {/* Header */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Building className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Gestión de Departamentos
                </h1>
                <p className="text-gray-600">
                  Administra los departamentos y facultades
                </p>
              </div>
            </div>
            <button
              onClick={() => setShowForm(true)}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Plus className="h-5 w-5 mr-2" />
              Nuevo Departamento
            </button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="p-6 border-b border-gray-200">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar por departamento o facultad..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {error && (
            <ErrorNotification
              error={error}
              onDismiss={() => fetchDepartments()}
            />
          )}

          {showForm && (
            <div className="mb-8 p-6 bg-gray-50 rounded-lg border">
              <h2 className="text-xl font-semibold mb-4">
                {editingDepartment ? 'Editar Departamento' : 'Nuevo Departamento'}
              </h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="dep_name" className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre del Departamento *
                  </label>
                  <input
                    type="text"
                    id="dep_name"
                    name="dep_name"
                    value={formData.dep_name}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
                      errors.dep_name ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="Ejemplo: Ingeniería de Sistemas, Matemáticas, etc."
                  />
                  {errors.dep_name && <p className="mt-1 text-sm text-red-600">{errors.dep_name}</p>}
                </div>

                <div>
                  <label htmlFor="fac_name" className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre de la Facultad *
                  </label>
                  <input
                    type="text"
                    id="fac_name"
                    name="fac_name"
                    value={formData.fac_name}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
                      errors.fac_name ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="Ejemplo: Facultad de Ingeniería en Sistemas, etc."
                  />
                  {errors.fac_name && <p className="mt-1 text-sm text-red-600">{errors.fac_name}</p>}
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={handleCancelForm}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
                  >
                    {editingDepartment ? 'Actualizar' : 'Crear'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Departments Table */}
          {filteredDepartments.length === 0 ? (
            <div className="text-center py-12">
              <Building className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                No se encontraron departamentos
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                {searchTerm ? 'Intenta con otros términos de búsqueda' : 'Comienza creando un nuevo departamento'}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Departamento
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Facultad
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredDepartments.map((department: DepartmentResponse) => (
                    <tr key={department.dep_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {department.dep_id}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {department.dep_name}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {department.fac_name}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEdit(department)}
                            className="text-blue-600 hover:text-blue-900 p-1"
                            title="Editar"
                          >
                            <Edit className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => setDeleteConfirm(department.dep_id)}
                            className="text-red-600 hover:text-red-900 p-1"
                            title="Eliminar"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Confirmar eliminación
            </h3>
            <p className="text-sm text-gray-500 mb-6">
              ¿Estás seguro de que deseas eliminar este departamento? Esta acción no se puede deshacer.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setDeleteConfirm(null)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                onClick={() => handleDelete(deleteConfirm)}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DepartmentsManagementPage;