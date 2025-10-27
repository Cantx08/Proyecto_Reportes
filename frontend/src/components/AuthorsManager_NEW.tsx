'use client';

import React, { useState } from 'react';
import { useAuthors } from '@/hooks/useAuthors';
import { useScopusAccounts } from '@/hooks/useScopusAccounts';
import type { AuthorCreateRequest, AuthorUpdateRequest } from '@/types/api';
import { 
  Users, 
  Plus, 
  Edit, 
  Trash2, 
  Search, 
  UserPlus,
  Mail,
  Building,
  Briefcase,
  Calendar
} from 'lucide-react';

export default function AuthorsManager() {
  const {
    authors,
    loading,
    error,
    creating,
    updating,
    deleting,
    createAuthor,
    updateAuthor,
    deleteAuthor,
    clearError
  } = useAuthors();

  const {
    accounts: scopusAccounts,
    linkAuthorScopus
  } = useScopusAccounts();

  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingAuthor, setEditingAuthor] = useState<string | null>(null);
  const [formData, setFormData] = useState<AuthorCreateRequest>({
    author_id: '',
    name: '',
    surname: '',
    title: '',
    birth_date: '',
    gender: 'M',
    position: '',
    department: ''
  });

  // Filtrar autores por término de búsqueda
  const filteredAuthors = authors.filter(author =>
    author.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    author.surname.toLowerCase().includes(searchTerm.toLowerCase()) ||
    author.author_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (editingAuthor) {
      // Actualizar autor existente
      const updateData: AuthorUpdateRequest = { ...formData };
      delete (updateData as any).author_id; // No se puede actualizar el ID
      
      const success = await updateAuthor(editingAuthor, updateData);
      if (success) {
        setEditingAuthor(null);
        resetForm();
      }
    } else {
      // Crear nuevo autor
      const success = await createAuthor(formData);
      if (success) {
        setShowCreateForm(false);
        resetForm();
      }
    }
  };

  const handleEdit = (author: any) => {
    setFormData({
      author_id: author.author_id,
      name: author.name,
      surname: author.surname,
      title: author.title,
      birth_date: author.birth_date || '',
      gender: author.gender,
      position: author.position,
      department: author.department
    });
    setEditingAuthor(author.author_id);
    setShowCreateForm(true);
  };

  const handleDelete = async (authorId: string) => {
    if (confirm('¿Está seguro de que desea eliminar este autor?')) {
      await deleteAuthor(authorId);
    }
  };

  const resetForm = () => {
    setFormData({
      author_id: '',
      name: '',
      surname: '',
      title: '',
      birth_date: '',
      gender: 'M',
      position: '',
      department: ''
    });
    setShowCreateForm(false);
    setEditingAuthor(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
        <span className="ml-2 text-neutral-600">Cargando autores...</span>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-neutral-200 mb-6">
        <div className="px-6 py-4 flex items-center justify-between">
          <div className="flex items-center">
            <Users className="h-6 w-6 text-primary-500 mr-3" />
            <h1 className="text-2xl font-bold text-neutral-900">Gestión de Autores</h1>
          </div>
          <button
            onClick={() => setShowCreateForm(true)}
            className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg flex items-center transition-colors"
          >
            <Plus className="h-4 w-4 mr-2" />
            Nuevo Autor
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-error-50 border border-error-200 rounded-lg p-4 mb-6">
          <div className="flex items-center justify-between">
            <p className="text-error-800">{error}</p>
            <button 
              onClick={clearError}
              className="text-error-600 hover:text-error-800 transition-colors"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="bg-white rounded-lg shadow-sm border border-neutral-200 mb-6">
        <div className="p-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
            <input
              type="text"
              placeholder="Buscar autores por nombre, apellido o ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className={`w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                searchTerm ? 'border-primary-400 bg-primary-50' : 'border-neutral-300'
              }`}
            />
          </div>
        </div>
      </div>

      {/* Create/Edit Form */}
      {showCreateForm && (
        <div className="bg-white rounded-lg shadow-sm border border-neutral-200 mb-6">
          <div className="px-6 py-4 border-b border-neutral-200">
            <h2 className="text-lg font-semibold text-neutral-900">
              {editingAuthor ? 'Editar Autor' : 'Crear Nuevo Autor'}
            </h2>
          </div>
          <form onSubmit={handleSubmit} className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  ID del Autor *
                </label>
                <input
                  type="text"
                  required
                  disabled={!!editingAuthor}
                  value={formData.author_id}
                  onChange={(e) => setFormData({...formData, author_id: e.target.value})}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-neutral-100 disabled:text-neutral-500 transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Nombre *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Apellido *
                </label>
                <input
                  type="text"
                  required
                  value={formData.surname}
                  onChange={(e) => setFormData({...formData, surname: e.target.value})}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Título *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Fecha de Nacimiento
                </label>
                <input
                  type="date"
                  value={formData.birth_date}
                  onChange={(e) => setFormData({...formData, birth_date: e.target.value})}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Género *
                </label>
                <select
                  required
                  value={formData.gender}
                  onChange={(e) => setFormData({...formData, gender: e.target.value})}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                >
                  <option value="M">Masculino</option>
                  <option value="F">Femenino</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Posición *
                </label>
                <input
                  type="text"
                  required
                  value={formData.position}
                  onChange={(e) => setFormData({...formData, position: e.target.value})}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Departamento *
                </label>
                <input
                  type="text"
                  required
                  value={formData.department}
                  onChange={(e) => setFormData({...formData, department: e.target.value})}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-4 mt-6">
              <button
                type="button"
                onClick={resetForm}
                className="px-4 py-2 border border-neutral-300 rounded-lg text-neutral-700 hover:bg-neutral-50 transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={creating || updating}
                className="bg-success-600 hover:bg-success-700 text-white px-4 py-2 rounded-lg disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors"
              >
                {creating || updating ? 'Guardando...' : (editingAuthor ? 'Actualizar' : 'Crear')}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Authors List */}
      <div className="bg-white rounded-lg shadow-sm border border-neutral-200">
        <div className="px-6 py-4 border-b border-neutral-200">
          <h2 className="text-lg font-semibold text-neutral-900">
            Autores ({filteredAuthors.length})
          </h2>
        </div>
        
        <div className="divide-y divide-neutral-200">
          {filteredAuthors.map((author) => (
            <div key={author.author_id} className="p-6 hover:bg-primary-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center mb-2">
                    <h3 className="text-lg font-medium text-neutral-900">
                      {author.title} {author.name} {author.surname}
                    </h3>
                    <span className="ml-3 px-2 py-1 bg-primary-100 text-primary-800 text-sm rounded font-medium">
                      ID: {author.author_id}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm text-neutral-600">
                    <div className="flex items-center">
                      <Building className="h-4 w-4 mr-2 text-neutral-400" />
                      {author.department}
                    </div>
                    <div className="flex items-center">
                      <Briefcase className="h-4 w-4 mr-2 text-neutral-400" />
                      {author.position}
                    </div>
                    <div className="flex items-center">
                      <UserPlus className="h-4 w-4 mr-2 text-neutral-400" />
                      {author.gender === 'M' ? 'Masculino' : 'Femenino'}
                    </div>
                    {author.birth_date && (
                      <div className="flex items-center">
                        <Calendar className="h-4 w-4 mr-2 text-neutral-400" />
                        {new Date(author.birth_date).toLocaleDateString()}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  <button
                    onClick={() => handleEdit(author)}
                    className="p-2 text-success-600 hover:bg-success-50 rounded transition-colors"
                    title="Editar autor"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(author.author_id)}
                    disabled={deleting}
                    className="p-2 text-error-600 hover:bg-error-50 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    title="Eliminar autor"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
          
          {filteredAuthors.length === 0 && (
            <div className="p-8 text-center text-neutral-500">
              {searchTerm ? 'No se encontraron autores que coincidan con la búsqueda.' : 'No hay autores registrados.'}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
