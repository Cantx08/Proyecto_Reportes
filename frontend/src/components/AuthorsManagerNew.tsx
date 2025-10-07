'use client';

import React, { useState } from 'react';
import { useAuthors } from '@/hooks/useAuthors';
import { Author } from '@/types/api';
import AuthorForm from './AuthorForm';
import { Plus, Edit, Trash2, Users } from 'lucide-react';

const AuthorsManagerNew: React.FC = () => {
  const { 
    authors, 
    loading, 
    error, 
    createAuthor, 
    updateAuthor, 
    deleteAuthor,
    clearError,
    creating,
    updating 
  } = useAuthors();

  const [showForm, setShowForm] = useState(false);
  const [editingAuthor, setEditingAuthor] = useState<Author | null>(null);

  const handleCreate = () => {
    setEditingAuthor(null);
    setShowForm(true);
  };

  const handleEdit = (author: Author) => {
    setEditingAuthor(author);
    setShowForm(true);
  };

  const handleDelete = async (authorId: string) => {
    if (window.confirm('¿Está seguro de eliminar este autor?')) {
      await deleteAuthor(authorId);
    }
  };

  const handleSave = async (authorData: Omit<Author, 'author_id'> | Author) => {
    try {
      if ('author_id' in authorData) {
        await updateAuthor(authorData.author_id, authorData);
      } else {
        // Generate a temporary ID for new authors
        const createData = {
          ...authorData,
          author_id: `temp-${Date.now()}`
        };
        await createAuthor(createData);
      }
      setShowForm(false);
      setEditingAuthor(null);
    } catch (error) {
      console.error('Error saving author:', error);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingAuthor(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
              <div className="mt-4">
                <button
                  type="button"
                  className="bg-red-50 text-red-800 rounded-md p-2 inline-flex items-center text-sm font-medium hover:bg-red-100"
                  onClick={clearError}
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Users className="h-6 w-6 text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Autores ({authors.length})
          </h2>
        </div>
        <button
          onClick={handleCreate}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>Nuevo Autor</span>
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            {editingAuthor ? 'Editar Autor' : 'Crear Nuevo Autor'}
          </h3>
          <AuthorForm
            author={editingAuthor}
            onSave={handleSave}
            onCancel={handleCancel}
            isLoading={creating || updating}
          />
        </div>
      )}

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {authors.map((author) => (
            <li key={author.author_id} className="px-6 py-4 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">
                      {author.title} {author.name} {author.surname}
                    </h3>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(author)}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(author.author_id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  <div className="mt-2 text-sm text-gray-600">
                    <p><strong>Género:</strong> {author.gender === 'M' ? 'Masculino' : 'Femenino'}</p>
                    <p><strong>Cargo:</strong> {author.position}</p>
                    <p><strong>Departamento:</strong> {author.department}</p>
                    {author.birth_date && (
                      <p><strong>Fecha de nacimiento:</strong> {author.birth_date}</p>
                    )}
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
        
        {authors.length === 0 && (
          <div className="text-center py-12">
            <Users className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No hay autores</h3>
            <p className="mt-1 text-sm text-gray-500">
              Comienza creando un nuevo autor.
            </p>
            <div className="mt-6">
              <button
                onClick={handleCreate}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                <Plus className="h-4 w-4 mr-2" />
                Nuevo Autor
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthorsManagerNew;