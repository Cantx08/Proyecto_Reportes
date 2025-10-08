'use client';

import React, { useState, useEffect } from 'react';
import { useAuthors } from '@/hooks/useAuthors';
import { Author, AuthorResponse, AuthorCreateRequest, AuthorUpdateRequest } from '@/types/api';
import AuthorForm from '@/components/AuthorForm';
import { ErrorNotification } from '@/components/ErrorNotification';
import { Plus, Edit, Trash2, Search, Users } from 'lucide-react';

const AuthorsManagementPage: React.FC = () => {
  const { 
    authors, 
    loading, 
    error, 
    createAuthor, 
    updateAuthor, 
    deleteAuthor, 
    fetchAuthors 
  } = useAuthors();

  const [showForm, setShowForm] = useState(false);
  const [editingAuthor, setEditingAuthor] = useState<AuthorResponse | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  // Cargar autores al montar el componente
  useEffect(() => {
    fetchAuthors();
  }, [fetchAuthors]);

  const filteredAuthors = (authors || []).filter(author => 
    author.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    author.surname.toLowerCase().includes(searchTerm.toLowerCase()) ||
    author.dni.toLowerCase().includes(searchTerm.toLowerCase()) ||
    author.department.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleCreate = async (authorData: Omit<Author, 'author_id'>) => {
    try {
      // Generar un ID único basado en timestamp
      const author_id = `author_${Date.now()}`;
      const createData: AuthorCreateRequest = {
        author_id,
        name: authorData.name,
        surname: authorData.surname,
        dni: authorData.dni,
        title: authorData.title,
        birth_date: authorData.birth_date,
        gender: authorData.gender,
        position: authorData.position,
        department: authorData.department
      };
      
      await createAuthor(createData);
      setShowForm(false);
      // Recargar la lista de autores
      await fetchAuthors();
    } catch (error) {
      console.error('Error creating author:', error);
    }
  };

  const handleUpdate = async (authorData: Author) => {
    if (!editingAuthor) return;
    
    try {
      const updateData: AuthorUpdateRequest = {
        name: authorData.name,
        surname: authorData.surname,
        dni: authorData.dni,
        title: authorData.title,
        birth_date: authorData.birth_date,
        gender: authorData.gender,
        position: authorData.position,
        department: authorData.department
      };
      
      await updateAuthor(editingAuthor.author_id, updateData);
      setEditingAuthor(null);
      setShowForm(false);
      // Recargar la lista de autores
      await fetchAuthors();
    } catch (error) {
      console.error('Error updating author:', error);
    }
  };

  const handleSave = (authorData: Omit<Author, 'author_id'> | Author) => {
    if ('author_id' in authorData) {
      handleUpdate(authorData);
    } else {
      handleCreate(authorData);
    }
  };

  const handleEdit = (author: AuthorResponse) => {
    console.log('Editing author:', author); // Para debug
    setEditingAuthor(author);
    setShowForm(true);
  };

  const handleDelete = async (authorId: string) => {
    try {
      await deleteAuthor(authorId);
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Error deleting author:', error);
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingAuthor(null);
  };

  if (loading && (!authors || authors.length === 0)) {
    return (
      <div className="flex justify-center items-center min-h-96">
        <div className="text-lg text-gray-600">Cargando autores...</div>
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
              <Users className="h-8 w-8 text-[#042a53]" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Autores
                </h1>
                <p className="text-gray-600">
                  Administra la información de los autores académicos
                </p>
              </div>
            </div>
            <button
              onClick={() => setShowForm(true)}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 bg-[#1f2937] text-white rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Plus className="h-5 w-5 mr-2" />
              Agregar
            </button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="p-6 border-b border-gray-200">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar por nombre, apellido, DNI o departamento..."
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
              onDismiss={() => fetchAuthors()}
            />
          )}

          {showForm && (
            <div className="mb-8 p-6 bg-gray-50 rounded-lg border">
              <h2 className="text-xl font-semibold mb-4">
                {editingAuthor ? 'Editar Autor' : 'Nuevo Autor'}
              </h2>
              <AuthorForm
                author={editingAuthor as Author}
                onSave={handleSave}
                onCancel={handleCancelForm}
                isLoading={loading}
              />
            </div>
          )}

          {/* Authors Table */}
          {!filteredAuthors || filteredAuthors.length === 0 ? (
            <div className="text-center py-12">
              <Users className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                No se encontraron autores
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                {searchTerm ? 'Intenta con otros términos de búsqueda' : 'Comienza creando un nuevo autor'}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Autor
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      DNI
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Cargo
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Departamento
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredAuthors.map((author) => (
                    <tr key={author.author_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {author.title} {author.name} {author.surname}
                          </div>
                          <div className="text-sm text-gray-500">
                            {author.gender} • {author.birth_date}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{author.dni}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{author.position}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{author.department}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEdit(author)}
                            className="text-blue-600 hover:text-blue-900 p-1"
                            title="Editar"
                          >
                            <Edit className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => setDeleteConfirm(author.author_id)}
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
              ¿Estás seguro de que deseas eliminar este autor? Esta acción no se puede deshacer.
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

export default AuthorsManagementPage;