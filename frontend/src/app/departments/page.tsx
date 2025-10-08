'use client';

import React, { useState } from 'react';
import { 
  Building2, 
  Plus, 
  Edit, 
  Users,
  Search,
  Filter,
  MoreVertical,
  Eye,
  Trash2
} from 'lucide-react';

interface Department {
  id: string;
  nombre: string;
  codigo: string;
  descripcion: string;
  totalAutores: number;
  totalPublicaciones: number;
  director: string;
  email: string;
  telefono: string;
  ubicacion: string;
  fechaCreacion: string;
  estado: 'activo' | 'inactivo';
}

interface Cargo {
  id: string;
  nombre: string;
  descripcion: string;
  nivel: number;
  departamento: string;
  totalPersonas: number;
}

const mockDepartments: Department[] = [
  {
    id: '1',
    nombre: 'Ingeniería Civil y Ambiental',
    codigo: 'DICA',
    descripcion: 'Departamento encargado de la formación en ingeniería civil y ambiental',
    totalAutores: 45,
    totalPublicaciones: 234,
    director: 'Dr. Juan Carlos Pérez',
    email: 'dica@epn.edu.ec',
    telefono: '+593-2-2976300 ext. 2801',
    ubicacion: 'Edificio de Ingeniería Civil, 2do piso',
    fechaCreacion: '1970-01-15',
    estado: 'activo'
  },
  {
    id: '2',
    nombre: 'Ingeniería Química y Agroindustria',
    codigo: 'DIQA',
    descripcion: 'Departamento de ingeniería química y procesos agroindustriales',
    totalAutores: 38,
    totalPublicaciones: 189,
    director: 'Dra. María García López',
    email: 'diqa@epn.edu.ec',
    telefono: '+593-2-2976300 ext. 2901',
    ubicacion: 'Edificio de Química, 3er piso',
    fechaCreacion: '1975-03-20',
    estado: 'activo'
  },
  {
    id: '3',
    nombre: 'Ingeniería Eléctrica y Electrónica',
    codigo: 'DIEE',
    descripcion: 'Departamento de ingeniería eléctrica y sistemas electrónicos',
    totalAutores: 52,
    totalPublicaciones: 312,
    director: 'Dr. Carlos Rodríguez',
    email: 'diee@epn.edu.ec',
    telefono: '+593-2-2976300 ext. 2701',
    ubicacion: 'Edificio de Eléctrica, 1er piso',
    fechaCreacion: '1968-09-10',
    estado: 'activo'
  }
];

const mockCargos: Cargo[] = [
  { id: '1', nombre: 'Profesor Principal', descripcion: 'Máximo nivel académico docente', nivel: 5, departamento: 'Todos', totalPersonas: 45 },
  { id: '2', nombre: 'Profesor Titular', descripcion: 'Profesor con dedicación exclusiva', nivel: 4, departamento: 'Todos', totalPersonas: 78 },
  { id: '3', nombre: 'Profesor Agregado', descripcion: 'Profesor nivel intermedio', nivel: 3, departamento: 'Todos', totalPersonas: 92 },
  { id: '4', nombre: 'Profesor Auxiliar', descripcion: 'Profesor nivel inicial', nivel: 2, departamento: 'Todos', totalPersonas: 34 },
  { id: '5', nombre: 'Director de Departamento', descripcion: 'Responsable administrativo del departamento', nivel: 6, departamento: 'Específico', totalPersonas: 12 }
];

export default function DepartamentosPage() {
  const [activeTab, setActiveTab] = useState<'departamentos' | 'cargos'>('departamentos');
  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  const filteredDepartments = mockDepartments.filter(dept =>
    dept.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    dept.codigo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    dept.director.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredCargos = mockCargos.filter(cargo =>
    cargo.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cargo.descripcion.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const departmentStats = {
    total: mockDepartments.length,
    activos: mockDepartments.filter(d => d.estado === 'activo').length,
    totalAutores: mockDepartments.reduce((sum, d) => sum + d.totalAutores, 0),
    totalPublicaciones: mockDepartments.reduce((sum, d) => sum + d.totalPublicaciones, 0)
  };

  const cargoStats = {
    total: mockCargos.length,
    totalPersonas: mockCargos.reduce((sum, c) => sum + c.totalPersonas, 0),
    nivelPromedio: Math.round(mockCargos.reduce((sum, c) => sum + c.nivel, 0) / mockCargos.length)
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <Building2 className="h-6 w-6 mr-3" style={{ color: '#042a53' }} />
              Gestión de Departamentos y Cargos
            </h1>
            <p className="text-gray-600 mt-1">
              Administra la estructura organizacional de la institución
            </p>
          </div>
          <button className="px-4 py-2 text-white rounded-lg text-sm font-medium hover:opacity-90 flex items-center" style={{ backgroundColor: '#1f2937' }}>
            <Plus className="h-4 w-4 mr-2" />
            Nuevo {activeTab === 'departamentos' ? 'Departamento' : 'Cargo'}
          </button>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('departamentos')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'departamentos'
                  ? 'border-[#042a53] text-[#042a53]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Departamentos
            </button>
            <button
              onClick={() => setActiveTab('cargos')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'cargos'
                  ? 'border-[#042a53] text-[#042a53]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Cargos
            </button>
          </nav>
        </div>

        {/* Stats Cards */}
        {activeTab === 'departamentos' ? (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-gray-900">{departmentStats.total}</div>
              <div className="text-sm text-gray-600">Total Departamentos</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-green-600">{departmentStats.activos}</div>
              <div className="text-sm text-gray-600">Departamentos Activos</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold" style={{ color: '#042a53' }}>{departmentStats.totalAutores}</div>
              <div className="text-sm text-gray-600">Total Autores</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-purple-600">{departmentStats.totalPublicaciones}</div>
              <div className="text-sm text-gray-600">Total Publicaciones</div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-gray-900">{cargoStats.total}</div>
              <div className="text-sm text-gray-600">Total Cargos</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold" style={{ color: '#042a53' }}>{cargoStats.totalPersonas}</div>
              <div className="text-sm text-gray-600">Total Personas</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-green-600">{cargoStats.nivelPromedio}</div>
              <div className="text-sm text-gray-600">Nivel Promedio</div>
            </div>
          </div>
        )}

        {/* Search Bar */}
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder={`Buscar ${activeTab}...`}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`px-4 py-2 border rounded-lg text-sm font-medium flex items-center ${
                showFilters ? 'bg-blue-50 text-blue-700 border-blue-200' : 'text-gray-700 border-gray-300 hover:bg-gray-50'
              }`}
            >
              <Filter className="h-4 w-4 mr-2" />
              Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      {activeTab === 'departamentos' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredDepartments.map((department) => (
            <div key={department.id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <Building2 className="h-5 w-5 text-blue-600" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-lg font-semibold text-gray-900">{department.nombre}</h3>
                    <p className="text-sm text-gray-600">{department.codigo}</p>
                  </div>
                </div>
                <div className="relative">
                  <button className="p-1 text-gray-400 hover:text-gray-600">
                    <MoreVertical className="h-4 w-4" />
                  </button>
                </div>
              </div>

              <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                {department.descripcion}
              </p>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="text-center p-2 bg-gray-50 rounded">
                  <div className="text-lg font-semibold text-gray-900">{department.totalAutores}</div>
                  <div className="text-xs text-gray-600">Autores</div>
                </div>
                <div className="text-center p-2 bg-gray-50 rounded">
                  <div className="text-lg font-semibold text-gray-900">{department.totalPublicaciones}</div>
                  <div className="text-xs text-gray-600">Publicaciones</div>
                </div>
              </div>

              <div className="border-t pt-4">
                <div className="text-sm text-gray-600 mb-2">
                  <strong>Director:</strong> {department.director}
                </div>
                <div className="text-sm text-gray-600 mb-2">
                  <strong>Email:</strong> {department.email}
                </div>
                <div className="text-sm text-gray-600 mb-3">
                  <strong>Ubicación:</strong> {department.ubicacion}
                </div>
                
                <div className="flex items-center justify-between">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    department.estado === 'activo' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {department.estado}
                  </span>
                  <div className="flex space-x-2">
                    <button className="text-blue-600 hover:text-blue-900">
                      <Eye className="h-4 w-4" />
                    </button>
                    <button className="text-green-600 hover:text-green-900">
                      <Edit className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cargo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nivel
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ámbito
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Personas
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredCargos.map((cargo) => (
                  <tr key={cargo.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{cargo.nombre}</div>
                        <div className="text-sm text-gray-500">{cargo.descripcion}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className={`h-2 w-2 rounded-full mr-2 ${
                          cargo.nivel >= 5 ? 'bg-green-400' :
                          cargo.nivel >= 3 ? 'bg-yellow-400' : 'bg-red-400'
                        }`}></div>
                        <span className="text-sm text-gray-900">Nivel {cargo.nivel}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {cargo.departamento}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center text-sm text-gray-900">
                        <Users className="h-4 w-4 mr-2 text-gray-400" />
                        {cargo.totalPersonas}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button className="text-blue-600 hover:text-blue-900">
                          <Eye className="h-4 w-4" />
                        </button>
                        <button className="text-green-600 hover:text-green-900">
                          <Edit className="h-4 w-4" />
                        </button>
                        <button className="text-red-600 hover:text-red-900">
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}