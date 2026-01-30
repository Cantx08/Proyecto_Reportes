'use client';

import React, { useState } from 'react';
import { useAuthors } from '@/features/authors/hooks/useAuthors';
import AuthorForm from './AuthorForm';
import { Plus, Edit, Trash2, Users, X } from 'lucide-react';
import {Author} from "@/features/authors/types";

const AuthorsManager: React.FC = () => {
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
      if ('author_id' in authorData && authorData.author_id) {
        // Modo edición
        await updateAuthor(authorData.author_id, authorData);
      } else {
        // Modo creación - NO enviar author_id, la BD lo generará automáticamente
        const { author_id, ...createData } = authorData as any;
        await createAuthor(createData);
      }
      setShowForm(false);
      setEditingAuthor(null);
    } catch (error) {
      console.error('Error saving author:', error);
      // El error ya se maneja en el hook, no necesitamos hacer nada más aquí
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
          <div className="flex justify-between items-start">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
            <button
              type="button"
              className="ml-auto text-red-400 hover:text-red-600"
              onClick={clearError}
            >
              <X className="h-5 w-5" />
            </button>
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
                  <div className="mt-2 text-sm text-gray-600 space-y-1">
                    <p><strong>DNI:</strong> {author.dni}</p>
                    <p><strong>Género:</strong> {author.gender === 'M' ? 'Masculino' : 'Femenino'}</p>
                    <p><strong>Cargo:</strong> {author.position}</p>
                    <p><strong>Departamento:</strong> {author.department}</p>
                    {author.birth_date && (
                      <p><strong>Fecha de nacimiento:</strong> {new Date(author.birth_date).toLocaleDateString('es-ES')}</p>
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
            <div className="mt-6">
              <button
                onClick={handleCreate}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-[#1f2937] hover:bg-[#1f2937]/80"
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

export default AuthorsManager;