'use client';

import React, { useState } from 'react';
import { usePositions } from '@/hooks/useNewPositions';
import { PositionResponse, PositionCreateRequest, PositionUpdateRequest } from '@/types/api';
import { ErrorNotification } from '@/components/ErrorNotification';
import { Plus, Edit, Trash2, Search, Briefcase } from 'lucide-react';

const PositionsManagementPage: React.FC = () => {
  const { 
    positions, 
    loading, 
    error, 
    createPosition, 
    updatePosition, 
    deletePosition, 
    fetchPositions 
  } = usePositions();

  const [showForm, setShowForm] = useState(false);
  const [editingPosition, setEditingPosition] = useState<PositionResponse | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    pos_id: '',
    pos_name: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const filteredPositions = positions.filter((position: PositionResponse) => 
    position.pos_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.pos_name.trim()) {
      newErrors.pos_name = 'El nombre del cargo es requerido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const resetForm = () => {
    setFormData({
      pos_id: '',
      pos_name: ''
    });
    setErrors({});
    setEditingPosition(null);
  };

  const handleCreate = async () => {
    if (!validateForm()) return;
    
    try {
      const pos_id = `pos_${Date.now()}`;
      const createData: PositionCreateRequest = {
        pos_id,
        pos_name: formData.pos_name
      };
      
      await createPosition(createData);
      setShowForm(false);
      resetForm();
    } catch (error) {
      console.error('Error creating position:', error);
    }
  };

  const handleUpdate = async () => {
    if (!editingPosition || !validateForm()) return;
    
    try {
      const updateData: PositionUpdateRequest = {
        pos_name: formData.pos_name
      };
      
      await updatePosition(editingPosition.pos_id, updateData);
      setEditingPosition(null);
      setShowForm(false);
      resetForm();
    } catch (error) {
      console.error('Error updating position:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingPosition) {
      handleUpdate();
    } else {
      handleCreate();
    }
  };

  const handleEdit = (position: PositionResponse) => {
    setEditingPosition(position);
    setFormData({
      pos_id: position.pos_id,
      pos_name: position.pos_name
    });
    setShowForm(true);
  };

  const handleDelete = async (positionId: string) => {
    try {
      await deletePosition(positionId);
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Error deleting position:', error);
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    resetForm();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
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

  if (loading && positions.length === 0) {
    return (
      <div className="flex justify-center items-center min-h-96">
        <div className="text-lg text-gray-600">Cargando cargos...</div>
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
              <Briefcase className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Gestión de Cargos/Posiciones
                </h1>
                <p className="text-gray-600">
                  Administra los cargos y posiciones disponibles
                </p>
              </div>
            </div>
            <button
              onClick={() => setShowForm(true)}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Plus className="h-5 w-5 mr-2" />
              Nuevo Cargo
            </button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="p-6 border-b border-gray-200">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar por nombre o descripción..."
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
              onDismiss={() => fetchPositions()}
            />
          )}

          {showForm && (
            <div className="mb-8 p-6 bg-gray-50 rounded-lg border">
              <h2 className="text-xl font-semibold mb-4">
                {editingPosition ? 'Editar Cargo' : 'Nuevo Cargo'}
              </h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="pos_name" className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre del Cargo *
                  </label>
                  <input
                    type="text"
                    id="pos_name"
                    name="pos_name"
                    value={formData.pos_name}
                    onChange={handleChange}
                    className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 ${
                      errors.pos_name ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="Ejemplo: Profesor Titular, Director, etc."
                  />
                  {errors.pos_name && <p className="mt-1 text-sm text-red-600">{errors.pos_name}</p>}
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
                    {editingPosition ? 'Actualizar' : 'Crear'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Positions Table */}
          {filteredPositions.length === 0 ? (
            <div className="text-center py-12">
              <Briefcase className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                No se encontraron cargos
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                {searchTerm ? 'Intenta con otros términos de búsqueda' : 'Comienza creando un nuevo cargo'}
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
                      Nombre
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredPositions.map((position: PositionResponse) => (
                    <tr key={position.pos_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {position.pos_id}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {position.pos_name}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEdit(position)}
                            className="text-blue-600 hover:text-blue-900 p-1"
                            title="Editar"
                          >
                            <Edit className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => setDeleteConfirm(position.pos_id)}
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
              ¿Estás seguro de que deseas eliminar este cargo? Esta acción no se puede deshacer.
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

export default PositionsManagementPage;