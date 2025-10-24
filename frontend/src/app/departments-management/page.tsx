'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useNewDepartments } from '@/hooks/useNewDepartments';
import { usePositions } from '@/hooks/useNewPositions';
import { DepartmentResponse, PositionResponse } from '@/types/api';
import { ErrorNotification } from '@/components/ErrorNotification';
import { Plus, Edit, Trash2, Search, Building, Loader2, Filter, Briefcase } from 'lucide-react';

interface Faculty {
  key: string;
  value: string;
}

type ViewMode = 'departments' | 'positions';

const DepartmentsManagementPage: React.FC = () => {
  const [viewMode, setViewMode] = useState<ViewMode>('departments');
  
  // Departments hooks
  const { 
    departments, 
    loading: loadingDepartments, 
    error: errorDepartments, 
    deleteDepartment, 
    fetchDepartments 
  } = useNewDepartments();

  // Positions hooks
  const { 
    positions, 
    loading: loadingPositions, 
    error: errorPositions, 
    deletePosition, 
    fetchPositions 
  } = usePositions();

  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [selectedFaculty, setSelectedFaculty] = useState<string>('all');

  useEffect(() => {
    // Cargar facultades
    const loadFaculties = async () => {
      try {
        const response = await fetch('http://localhost:8000/faculties');
        const data = await response.json();
        if (data.success) {
          setFaculties(data.data);
        }
      } catch (error) {
        console.error('Error loading faculties:', error);
      }
    };
    loadFaculties();
  }, []);

  // Reset search when changing view
  useEffect(() => {
    setSearchTerm('');
    setDeleteConfirm(null);
    setSelectedFaculty('all');
  }, [viewMode]);

  const filteredDepartments = departments.filter((department: DepartmentResponse) => {
    const matchesSearch = 
      department.dep_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (department.dep_code && department.dep_code.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesFaculty = selectedFaculty === 'all' || department.fac_name === selectedFaculty;
    
    return matchesSearch && matchesFaculty;
  });

  const filteredPositions = positions.filter((position: PositionResponse) => 
    position.pos_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (position.pos_id && position.pos_id.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleDeleteDepartment = async (departmentId: string) => {
    try {
      await deleteDepartment(departmentId);
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Error deleting department:', error);
    }
  };

  const handleDeletePosition = async (positionId: string) => {
    try {
      await deletePosition(positionId);
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Error deleting position:', error);
    }
  };

  const loading = viewMode === 'departments' ? loadingDepartments : loadingPositions;
  const error = viewMode === 'departments' ? errorDepartments : errorPositions;

  if (loading && (viewMode === 'departments' ? departments.length === 0 : positions.length === 0)) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">
            {viewMode === 'departments' ? 'Cargando departamentos...' : 'Cargando cargos...'}
          </p>
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
              {viewMode === 'departments' ? (
                <>
                  <Building className="h-6 w-6 mr-3 text-[#1f2937]" />
                  Gestión de Departamentos
                </>
              ) : (
                <>
                  <Briefcase className="h-6 w-6 mr-3 text-[#1f2937]" />
                  Gestión de Cargos
                </>
              )}
            </h1>
            <p className="text-gray-600 mt-1">
              {viewMode === 'departments' 
                ? 'Administra los departamentos y facultades de la institución.'
                : 'Administra los cargos y posiciones de la institución.'}
            </p>
          </div>
          <div className="flex space-x-3">
            {viewMode === 'departments' ? (
              <Link href="/departments/departments-new" className="px-4 py-2 bg-[#1f2937] text-white rounded-lg text-sm font-medium hover:bg-[#1f2937]/80 flex items-center">
                <Plus className="h-4 w-4 mr-2" />
                Nuevo Departamento
              </Link>
            ) : (
              <Link href="/positions/positions-new" className="px-4 py-2 bg-[#1f2937] text-white rounded-lg text-sm font-medium hover:bg-[#1f2937]/80 flex items-center">
                <Plus className="h-4 w-4 mr-2" />
                Nuevo Cargo
              </Link>
            )}
          </div>
        </div>

        {/* View Mode Tabs */}
        <div className="flex space-x-2 mb-6 border-b border-gray-200">
          <button
            onClick={() => setViewMode('departments')}
            className={`px-6 py-3 text-sm font-medium transition-colors relative ${
              viewMode === 'departments'
                ? 'text-[#1f2937] border-b-2 border-[#1f2937]'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <div className="flex items-center">
              <Building className="h-4 w-4 mr-2" />
              Departamentos
            </div>
          </button>
          <button
            onClick={() => setViewMode('positions')}
            className={`px-6 py-3 text-sm font-medium transition-colors relative ${
              viewMode === 'positions'
                ? 'text-[#1f2937] border-b-2 border-[#1f2937]'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <div className="flex items-center">
              <Briefcase className="h-4 w-4 mr-2" />
              Cargos
            </div>
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <ErrorNotification
            error={error}
            onDismiss={() => viewMode === 'departments' ? fetchDepartments() : fetchPositions()}
          />
        )}

        {/* Search Bar and Filter */}
        <div className="bg-white rounded-lg border border-gray-200 p-4 mb-6">
          <div className="flex items-center space-x-3">
            {/* Search Bar */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder={viewMode === 'departments' 
                  ? "Buscar por código o nombre de departamento..."
                  : "Buscar por código o nombre de cargo..."}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            {/* Faculty Filter - Only for departments */}
            {viewMode === 'departments' && (
              <div className="flex items-center space-x-2 min-w-[300px]">
                <Filter className="h-5 w-5 text-gray-400" />
                <select
                  value={selectedFaculty}
                  onChange={(e) => setSelectedFaculty(e.target.value)}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="all">Todas las Facultades</option>
                  {faculties.map((faculty) => (
                    <option key={faculty.key} value={faculty.value}>
                      {faculty.value}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>
        </div>

        {/* Stats Card */}
        <div className="px-4 mb-6">
          <div className="text-sm text-gray-600">
            {viewMode === 'departments' ? (
              <>
                {filteredDepartments.length} { }
                {selectedFaculty === 'all' ? 'departamentos encontrados' : 'departamento/s encontrado/s'}
              </>
            ) : (
              <>
                {filteredPositions.length} cargo/s encontrado/s
              </>
            )}
          </div>
        </div>
      </div>

      {/* Content - Departments or Positions Table */}
      {viewMode === 'departments' ? (
        <DepartmentsTable 
          filteredDepartments={filteredDepartments}
          searchTerm={searchTerm}
          selectedFaculty={selectedFaculty}
          setDeleteConfirm={setDeleteConfirm}
        />
      ) : (
        <PositionsTable 
          filteredPositions={filteredPositions}
          searchTerm={searchTerm}
          setDeleteConfirm={setDeleteConfirm}
        />
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Confirmar eliminación
            </h3>
            <p className="text-sm text-gray-500 mb-6">
              ¿Estás seguro de que deseas eliminar este {viewMode === 'departments' ? 'departamento' : 'cargo'}? Esta acción no se puede deshacer.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setDeleteConfirm(null)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                onClick={() => viewMode === 'departments' ? handleDeleteDepartment(deleteConfirm) : handleDeletePosition(deleteConfirm)}
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

// Departments Table Component
const DepartmentsTable: React.FC<{
  filteredDepartments: DepartmentResponse[];
  searchTerm: string;
  selectedFaculty: string;
  setDeleteConfirm: (id: string) => void;
}> = ({ filteredDepartments, searchTerm, selectedFaculty, setDeleteConfirm }) => {
  return (
    <div className="bg-white rounded-lg border border-gray-200">
      {filteredDepartments.length === 0 ? (
        <div className="text-center py-12">
          <Building className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            No se encontraron departamentos
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm || selectedFaculty !== 'all' 
              ? 'Intenta con otros términos de búsqueda o filtros' 
              : 'Comienza creando un nuevo departamento'}
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Código
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
              {filteredDepartments.map((department: DepartmentResponse) => (
                <tr key={department.dep_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {department.dep_code || department.dep_id}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {department.dep_name}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <Link href={`/departments/${department.dep_id}`} className="text-blue-600 hover:text-blue-900 p-1" title="Editar">
                        <Edit className="h-4 w-4 text-green-600" />
                      </Link>
                      <button
                        onClick={() => setDeleteConfirm(department.dep_id)}
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
  );
};

// Positions Table Component
const PositionsTable: React.FC<{
  filteredPositions: PositionResponse[];
  searchTerm: string;
  setDeleteConfirm: (id: string) => void;
}> = ({ filteredPositions, searchTerm, setDeleteConfirm }) => {
  return (
    <div className="bg-white rounded-lg border border-gray-200">
      {filteredPositions.length === 0 ? (
        <div className="text-center py-12">
          <Briefcase className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            No se encontraron cargos
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm 
              ? 'Intenta con otros términos de búsqueda' 
              : 'Comienza creando un nuevo cargo'}
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Código
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
              {filteredPositions.map((position: PositionResponse) => (
                <tr key={position.pos_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {position.pos_id}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {position.pos_name}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <Link href={`/positions/${position.pos_id}`} className="text-blue-600 hover:text-blue-900 p-1" title="Editar">
                        <Edit className="h-4 w-4 text-green-600" />
                      </Link>
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
  );
};

export default DepartmentsManagementPage;