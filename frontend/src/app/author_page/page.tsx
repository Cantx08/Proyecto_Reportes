'use client';

import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Plus, 
  Edit, 
  Eye, 
  Filter,
  Download,
  Upload,
  Users,
  Mail,
  Building,
  BookOpen
} from 'lucide-react';

interface Author {
  id: string;
  nombre: string;
  email: string;
  scopusId: string;
  departamento: string;
  cargo: string;
  publicaciones: number;
  ultimaActualizacion: string;
  estado: 'activo' | 'inactivo';
}

const mockAuthors: Author[] = [
  {
    id: '1',
    nombre: 'Dr. Juan Carlos Pérez',
    email: 'juan.perez@epn.edu.ec',
    scopusId: '12345678900',
    departamento: 'Ingeniería Civil',
    cargo: 'Profesor Principal',
    publicaciones: 45,
    ultimaActualizacion: '2025-01-15',
    estado: 'activo'
  },
  {
    id: '2',
    nombre: 'Dra. María García López',
    email: 'maria.garcia@epn.edu.ec',
    scopusId: '98765432100',
    departamento: 'Ingeniería Química',
    cargo: 'Profesora Titular',
    publicaciones: 67,
    ultimaActualizacion: '2025-01-10',
    estado: 'activo'
  },
  {
    id: '3',
    nombre: 'Dr. Carlos Rodríguez',
    email: 'carlos.rodriguez@epn.edu.ec',
    scopusId: '55544433322',
    departamento: 'Ingeniería Eléctrica',
    cargo: 'Profesor Agregado',
    publicaciones: 23,
    ultimaActualizacion: '2024-12-20',
    estado: 'activo'
  }
];

export default function AutoresPage() {
  const [authors, setAuthors] = useState<Author[]>(mockAuthors);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [selectedCargo, setSelectedCargo] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  const filteredAuthors = authors.filter(author => {
    const matchesSearch = author.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         author.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         author.scopusId.includes(searchTerm);
    const matchesDepartment = !selectedDepartment || author.departamento === selectedDepartment;
    const matchesCargo = !selectedCargo || author.cargo === selectedCargo;
    
    return matchesSearch && matchesDepartment && matchesCargo;
  });

  const departments = Array.from(new Set(authors.map(author => author.departamento)));
  const cargos = Array.from(new Set(authors.map(author => author.cargo)));

  const stats = {
    total: authors.length,
    activos: authors.filter(a => a.estado === 'activo').length,
    totalPublicaciones: authors.reduce((sum, a) => sum + a.publicaciones, 0),
    promedioPublicaciones: Math.round(authors.reduce((sum, a) => sum + a.publicaciones, 0) / authors.length)
  };

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
            <button className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 flex items-center">
              <Upload className="h-4 w-4 mr-2" />
              Importar
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 flex items-center">
              <Download className="h-4 w-4 mr-2" />
              Exportar
            </button>
            <button className="px-4 py-2 text-white rounded-lg text-sm font-medium hover:opacity-90 flex items-center" style={{ backgroundColor: '#1f2937' }}>
              <Plus className="h-4 w-4 mr-2" />
              Nuevo Autor
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
            <div className="text-sm text-gray-600">Total Autores</div>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-green-600">{stats.activos}</div>
            <div className="text-sm text-gray-600">Autores Activos</div>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold" style={{ color: '#042a53' }}>{stats.totalPublicaciones}</div>
            <div className="text-sm text-gray-600">Total Publicaciones</div>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="text-2xl font-bold text-purple-600">{stats.promedioPublicaciones}</div>
            <div className="text-sm text-gray-600">Promedio por Autor</div>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search Bar */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar por nombre, email o Scopus ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:border-transparent"
                style={{ '--tw-ring-color': '#042a53' } as React.CSSProperties}
              />
            </div>
            
            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`px-4 py-2 border rounded-lg text-sm font-medium flex items-center ${
                showFilters ? 'text-white border-gray-300' : 'text-gray-700 border-gray-300 hover:bg-gray-50'
              }`}
              style={showFilters ? { backgroundColor: '#042a53' } : {}}
            >
              <Filter className="h-4 w-4 mr-2" />
              Filtros
            </button>
          </div>

          {/* Filters */}
          {showFilters && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Departamento
                  </label>
                  <select
                    value={selectedDepartment}
                    onChange={(e) => setSelectedDepartment(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Todos los departamentos</option>
                    {departments.map(dept => (
                      <option key={dept} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Cargo
                  </label>
                  <select
                    value={selectedCargo}
                    onChange={(e) => setSelectedCargo(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Todos los cargos</option>
                    {cargos.map(cargo => (
                      <option key={cargo} value={cargo}>{cargo}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          )}
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
                  Publicaciones
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredAuthors.map((author) => (
                <tr key={author.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full flex items-center justify-center" style={{ backgroundColor: '#042a5320' }}>
                          <span className="text-sm font-medium" style={{ color: '#042a53' }}>
                            {author.nombre.split(' ').map(n => n[0]).join('').slice(0, 2)}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{author.nombre}</div>
                        <div className="text-sm text-gray-500 flex items-center">
                          <Mail className="h-3 w-3 mr-1" />
                          {author.email}
                        </div>
                        <div className="text-xs text-gray-400">Scopus: {author.scopusId}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center text-sm text-gray-900">
                      <Building className="h-4 w-4 mr-2 text-gray-400" />
                      {author.departamento}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {author.cargo}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center text-sm text-gray-900">
                      <BookOpen className="h-4 w-4 mr-2 text-gray-400" />
                      {author.publicaciones}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      author.estado === 'activo' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {author.estado}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <button className="hover:opacity-75" style={{ color: '#042a53' }}>
                        <Eye className="h-4 w-4" />
                      </button>
                      <button className="text-green-600 hover:text-green-900">
                        <Edit className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredAuthors.length === 0 && (
          <div className="text-center py-12">
            <Users className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No se encontraron autores</h3>
            <p className="mt-1 text-sm text-gray-500">
              Intenta ajustar los filtros de búsqueda o agregar nuevos autores.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}