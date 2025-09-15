'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useWorkflow, useWorkflowActions } from '@/components/workflow/WorkflowProvider';

export default function SearchStep() {
  const [searchType, setSearchType] = useState<'scopus' | 'name'>('scopus');
  const [searchQuery, setSearchQuery] = useState('');
  const [scopusId, setScopusId] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  
  const { state } = useWorkflow();
  const { setSearchResults, setAuthor, setLoading, setError } = useWorkflowActions();
  const router = useRouter();

  const validateScopusId = (id: string) => {
    // Scopus ID debe ser numérico y tener entre 10-11 dígitos
    return /^\d{10,11}$/.test(id);
  };

  const handleScopusSearch = async () => {
    if (!validateScopusId(scopusId)) {
      setError('El ID de Scopus debe tener 10-11 dígitos numéricos');
      return;
    }

    setIsSearching(true);
    setError(null);

    try {
      // Buscar en base de datos local primero
      const response = await fetch(`/api/v1/authors/search?scopus_id=${scopusId}`);
      const data = await response.json();

      if (data.authors && data.authors.length > 0) {
        // Autor encontrado en BD local
        setAuthor(data.authors[0]);
        router.push('/step-2-author');
      } else {
        // Buscar en Scopus
        const scopusResponse = await fetch('/api/v1/publications/search-scopus', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ author_scopus_ids: [scopusId] }),
        });

        if (scopusResponse.ok) {
          // Datos encontrados en Scopus, crear nuevo autor
          router.push(`/step-2-author/create?scopus_id=${scopusId}`);
        } else {
          setError('No se encontraron datos para este ID de Scopus');
        }
      }
    } catch (error) {
      setError('Error al realizar la búsqueda. Verifique su conexión.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleNameSearch = async () => {
    if (!searchQuery.trim()) {
      setError('Por favor ingrese un nombre para buscar');
      return;
    }

    setIsSearching(true);
    setError(null);

    try {
      const response = await fetch(`/api/v1/authors/search?query=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();

      if (data.authors && data.authors.length > 0) {
        setSearchResults(data.authors);
      } else {
        setError('No se encontraron autores con ese nombre');
      }
    } catch (error) {
      setError('Error al realizar la búsqueda. Verifique su conexión.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleSelectAuthor = (author: any) => {
    setAuthor(author);
    router.push('/step-2-author');
  };

  const handleCreateNewAuthor = () => {
    router.push('/step-2-author/create');
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Búsqueda de Autor
        </h2>
        <p className="text-lg text-gray-600">
          Comience buscando por ID de Scopus o nombre del autor en la base de datos
        </p>
      </div>

      {/* Selector de tipo de búsqueda */}
      <div className="mb-6">
        <div className="flex space-x-4 justify-center">
          <button
            type="button"
            onClick={() => setSearchType('scopus')}
            className={`px-4 py-2 rounded-md font-medium ${
              searchType === 'scopus'
                ? 'bg-blue-100 text-blue-700 border-2 border-blue-300'
                : 'bg-white text-gray-700 border-2 border-gray-300 hover:bg-gray-50'
            }`}
          >
            Buscar por ID Scopus
          </button>
          <button
            type="button"
            onClick={() => setSearchType('name')}
            className={`px-4 py-2 rounded-md font-medium ${
              searchType === 'name'
                ? 'bg-blue-100 text-blue-700 border-2 border-blue-300'
                : 'bg-white text-gray-700 border-2 border-gray-300 hover:bg-gray-50'
            }`}
          >
            Buscar por Nombre
          </button>
        </div>
      </div>

      {/* Formulario de búsqueda por Scopus ID */}
      {searchType === 'scopus' && (
        <div className="bg-blue-50 p-6 rounded-lg">
          <label htmlFor="scopus-id" className="block text-sm font-medium text-gray-700 mb-2">
            ID de Scopus
          </label>
          <div className="flex space-x-3">
            <input
              type="text"
              id="scopus-id"
              value={scopusId}
              onChange={(e) => setScopusId(e.target.value)}
              placeholder="Ej: 12345678900"
              className={`flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                scopusId && !validateScopusId(scopusId) 
                  ? 'border-red-300 bg-red-50' 
                  : 'border-gray-300'
              }`}
            />
            <button
              type="button"
              onClick={handleScopusSearch}
              disabled={isSearching || !scopusId || !validateScopusId(scopusId)}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {isSearching ? 'Buscando...' : 'Buscar'}
            </button>
          </div>
          {scopusId && !validateScopusId(scopusId) && (
            <p className="mt-2 text-sm text-red-600">
              El ID de Scopus debe contener 10-11 dígitos numéricos
            </p>
          )}
        </div>
      )}

      {/* Formulario de búsqueda por nombre */}
      {searchType === 'name' && (
        <div className="bg-green-50 p-6 rounded-lg">
          <label htmlFor="author-name" className="block text-sm font-medium text-gray-700 mb-2">
            Nombre del Autor
          </label>
          <div className="flex space-x-3">
            <input
              type="text"
              id="author-name"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Ej: Juan Pérez"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <button
              type="button"
              onClick={handleNameSearch}
              disabled={isSearching || !searchQuery.trim()}
              className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {isSearching ? 'Buscando...' : 'Buscar'}
            </button>
          </div>
        </div>
      )}

      {/* Mostrar errores */}
      {state.error && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">{state.error}</div>
            </div>
          </div>
        </div>
      )}

      {/* Resultados de búsqueda por nombre */}
      {state.searchResults.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Resultados de Búsqueda</h3>
          <div className="space-y-3">
            {state.searchResults.map((author) => (
              <div
                key={author.id}
                className="border border-gray-300 rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
                onClick={() => handleSelectAuthor(author)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-medium text-gray-900">
                      {author.title} {author.first_name} {author.last_name}
                    </h4>
                    <p className="text-sm text-gray-600">{author.email}</p>
                    <p className="text-sm text-gray-500">{author.position}</p>
                  </div>
                  <button className="text-blue-600 hover:text-blue-800 font-medium">
                    Seleccionar
                  </button>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-4 text-center">
            <button
              type="button"
              onClick={handleCreateNewAuthor}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              ¿No encuentra el autor? Crear nuevo autor
            </button>
          </div>
        </div>
      )}
    </div>
  );
}