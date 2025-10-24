'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuthors } from '@/hooks/useAuthors';
import { 
  Plus, 
  Edit, 
  Trash2,
  Users,
  Loader2
} from 'lucide-react';

export default function AutoresPage() {
  const { authors, loading, error, fetchAuthors, deleteAuthor } = useAuthors();
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  useEffect(() => {
    fetchAuthors();
  }, [fetchAuthors]);

  // Manejar eliminación de autor
  const handleDelete = async (authorId: string) => {
    const success = await deleteAuthor(authorId);
    if (success) {
      setDeleteConfirm(null);
      fetchAuthors(); // Recargar la lista
    }
  };

  // Filtrar autores según el término de búsqueda
  const filteredAuthors = authors.filter(author => 
    author.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    author.surname.toLowerCase().includes(searchTerm.toLowerCase()) ||
    author.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
    author.position.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const stats = {
    total: authors.length,
    masculine: authors.filter(a => a.gender === 'M').length,
    feminine: authors.filter(a => a.gender === 'F').length,
    departments: new Set(authors.map(a => a.department)).size
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4" style={{ color: '#042a53' }} />
          <p className="text-gray-600">Cargando autores...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header Section */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <Users className="h-6 w-6 mr-3" style={{ color: '#042a53' }} />
              Gestión de Autores
            </h1>
            <p className="text-gray-600 mt-1">
              Administra la información de autores y sus cuentas Scopus asociadas.
            </p>
          </div>
          <div className="flex space-x-3">
            <Link href="/authors/authors-new">
              <button className="px-4 py-2 text-white rounded-lg text-sm font-medium hover:opacity-90 flex items-center" style={{ backgroundColor: '#1f2937' }}>
                <Plus className="h-4 w-4 mr-2" />
                Nuevo Autor
              </button>
            </Link>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error al cargar autores</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
            <div className="text-sm text-gray-600">Total Autores</div>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-blue-600">{stats.masculine}</div>
            <div className="text-sm text-gray-600">Masculino</div>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-pink-600">{stats.feminine}</div>
            <div className="text-sm text-gray-600">Femenino</div>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold" style={{ color: '#042a53' }}>{stats.departments}</div>
            <div className="text-sm text-gray-600">Departamentos</div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="mb-4">
          <input
            type="text"
            placeholder="Buscar por nombre, apellido, departamento o cargo..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {/* Authors Table */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Autor
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Departamento
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Cargo
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
                    <div className="text-sm font-medium text-gray-900">
                      {author.title} {author.name} {author.surname}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {author.department}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {author.position}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <Link href={`/authors/${author.author_id}`}>
                        <button className="text-green-600 hover:text-green-900" title="Editar">
                          <Edit className="h-4 w-4" />
                        </button>
                      </Link>
                      <button 
                        onClick={() => setDeleteConfirm(author.author_id)}
                        className="text-red-600 hover:text-red-900" 
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

        {filteredAuthors.length === 0 && !loading && (
          <div className="text-center py-12">
            <Users className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              {searchTerm ? 'No se encontraron autores' : 'No hay autores registrados'}
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {searchTerm 
                ? 'Intenta con otros términos de búsqueda' 
                : 'Comienza agregando nuevos autores.'
              }
            </p>
            {!searchTerm && (
              <div className="mt-6">
                <Link href="/authors/authors-new">
                  <button className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white hover:opacity-90" style={{ backgroundColor: '#042a53' }}>
                    <Plus className="h-4 w-4 mr-2" />
                    Agregar Primer Autor
                  </button>
                </Link>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Modal de Confirmación de Eliminación */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Confirmar Eliminación
            </h3>
            <p className="text-gray-600 mb-6">
              ¿Estás seguro de que deseas eliminar este autor? Esta acción no se puede deshacer.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setDeleteConfirm(null)}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                onClick={() => handleDelete(deleteConfirm)}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}