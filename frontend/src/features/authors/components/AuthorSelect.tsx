import React, { useState, useEffect } from 'react';
import { Search, User, Check, Loader2 } from 'lucide-react';
import { useAuthors } from '@/src/features/authors/hooks/useAuthors';

interface AuthorSelectorProps {
  onAuthorSelect: (authorId: string) => void;
  selectedAuthors: string[];
  className?: string;
}

export const AuthorSelect: React.FC<AuthorSelectorProps> = ({
  onAuthorSelect,
  selectedAuthors,
  className = ''
}) => {
  const { authors, loading, fetchAuthors, error } = useAuthors();
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchAuthors();
  }, [fetchAuthors]);

  const filteredAuthors = authors.filter(author => {
    const searchLower = searchTerm.toLowerCase();
    return (
      author.first_name.toLowerCase().includes(searchLower) ||
      author.last_name.toLowerCase().includes(searchLower) ||
      author.author_id.toLowerCase().includes(searchLower) ||
      author.department_id.toLowerCase().includes(searchLower)
    );
  });

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar por nombre, apellido, ID o departamento..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          />
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
          <span className="ml-2 text-gray-600">Cargando autores...</span>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Authors List */}
      {!loading && !error && (
        <>
          {/* Selected Author Info */}
          {selectedAuthors.length > 0 && (
            <div className="text-sm text-gray-600">
              Lista de autores
            </div>
          )}

          {/* List */}
          <div className="max-h-96 overflow-y-auto border border-gray-200 rounded-lg">
            {filteredAuthors.length === 0 ? (
              <div className="p-8 text-center text-gray-500">
                <User className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                <p>No se encontraron autores</p>
                {searchTerm && (
                  <p className="text-sm mt-1">
                    Intenta con otro término de búsqueda
                  </p>
                )}
              </div>
            ) : (
              filteredAuthors.map(author => {
                const isSelected = selectedAuthors.includes(author.author_id);
                const fullName = `${author.title ? `${author.title} ` : ''}${author.first_name} ${author.last_name}`;
                
                return (
                  <div
                    key={author.author_id}
                    onClick={() => onAuthorSelect(author.author_id)}
                    className={`px-4 py-2 cursor-pointer transition-colors border-b border-gray-100 last:border-b-0 flex items-center justify-between ${
                      isSelected 
                        ? 'bg-blue-50 hover:bg-blue-100' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <span className="text-gray-900">
                      {fullName}
                    </span>
                    {isSelected && (
                      <Check className="h-4 w-4 text-blue-600 flex-shrink-0 ml-2" />
                    )}
                  </div>
                );
              })
            )}
          </div>

          {/* Results Info */}
          {filteredAuthors.length > 0 && (
            <p className="text-xs text-gray-500">
              Mostrando {filteredAuthors.length} de {authors.length} autores
            </p>
          )}
        </>
      )}
    </div>
  );
};
