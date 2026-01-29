'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useDepartments } from '@/features/departments/hooks/useDepartments';
import { useJobPositions } from '@/features/job-positions/hooks/useJobPositions';
import { ErrorNotification } from '@/components/ErrorNotification';
import { Plus, Edit, Trash2, Search, Building, Loader2, Filter, Briefcase, X, ChevronLeft, ChevronRight } from 'lucide-react';
import {DepartmentResponse} from "@/features/departments/types";
import {JobPositionResponse} from "@/features/job-positions/types";

interface Faculty {
  key: string;
  value: string;
}

type ViewMode = 'departments' | 'positions';

const DepartmentsAndPositionsPage: React.FC = () => {
  const [viewMode, setViewMode] = useState<ViewMode>('departments');
  
  // Departments hooks
  const { 
    departments, 
    loading: loadingDepartments, 
    error: errorDepartments, 
    deleteDepartment, 
    fetchDepartments 
  } = useDepartments();

  // Positions hooks
  const { 
    positions, 
    loading: loadingPositions, 
    error: errorPositions, 
    deletePosition, 
    fetchPositions 
  } = useJobPositions();

  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [selectedFaculty, setSelectedFaculty] = useState<string>('all');

  // Pagination states
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(5);

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
    setCurrentPage(1); // Reset to first page when changing view
  }, [viewMode]);

  // Reset page when search or filter changes
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, selectedFaculty]);

  const filteredDepartments = departments.filter((department: DepartmentResponse) => {
    const matchesSearch = 
      department.dep_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (department.dep_code && department.dep_code.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesFaculty = selectedFaculty === 'all' || department.faculty_name === selectedFaculty;
    
    return matchesSearch && matchesFaculty;
  });

  const filteredPositions = positions.filter((position: JobPositionResponse) =>
    position.pos_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (position.pos_id && position.pos_id?.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  // Check if filters are active
  const hasActiveFilters = searchTerm !== '' || selectedFaculty !== 'all';

  // Clear all filters
  const clearFilters = () => {
    setSearchTerm('');
    setSelectedFaculty('all');
    setCurrentPage(1);
  };

  // Pagination logic
  const currentData = viewMode === 'departments' ? filteredDepartments : filteredPositions;
  const totalPages = Math.ceil(currentData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedData = currentData.slice(startIndex, endIndex);

  const goToPage = (page: number) => {
    setCurrentPage(Math.max(1, Math.min(page, totalPages)));
  };

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
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-primary-500" />
          <p className="text-neutral-600">
            {viewMode === 'departments' ? 'Cargando departamentos...' : 'Cargando cargos...'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header Section */}
      <div className="mb-8 mt-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
              {viewMode === 'departments' ? (
                <>
                  <Building className="h-7 w-7 mr-3 text-primary-600" />
                  Gestión de Departamentos
                </>
              ) : (
                <>
                  <Briefcase className="h-7 w-7 mr-3 text-primary-600" />
                  Gestión de Cargos
                </>
              )}
            </h1>
            <p className="text-neutral-600 mt-1">
              {viewMode === 'departments' 
                ? 'Administra los departamentos y facultades de la institución.'
                : 'Administra los cargos y posiciones de la institución.'}
            </p>
          </div>
          <div className="flex space-x-3">
            {viewMode === 'departments' ? (
              <Link href="/departments/new" className="px-5 py-2.5 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 flex items-center shadow-sm hover:shadow transition-all">
                <Plus className="h-4 w-4 mr-2" />
                Nuevo Departamento
              </Link>
            ) : (
              <Link href="/positions/new" className="px-5 py-2.5 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 flex items-center shadow-sm hover:shadow transition-all">
                <Plus className="h-4 w-4 mr-2" />
                Nuevo Cargo
              </Link>
            )}
          </div>
        </div>

        {/* View Mode Tabs */}
        <div className="flex space-x-2 mb-6 border-b border-neutral-200">
          <button
            onClick={() => setViewMode('departments')}
            className={`px-6 py-3 text-sm font-medium transition-all relative ${
              viewMode === 'departments'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-neutral-500 hover:text-neutral-700 hover:bg-neutral-50 rounded-t-lg'
            }`}
          >
            <div className="flex items-center">
              <Building className="h-4 w-4 mr-2" />
              Departamentos
            </div>
          </button>
          <button
            onClick={() => setViewMode('positions')}
            className={`px-6 py-3 text-sm font-medium transition-all relative ${
              viewMode === 'positions'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-neutral-500 hover:text-neutral-700 hover:bg-neutral-50 rounded-t-lg'
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
        <div className="bg-white rounded-lg border border-neutral-200 shadow-sm p-4 mb-6">
          <div className="flex flex-col md:flex-row md:items-center space-y-3 md:space-y-0 md:space-x-3">
            {/* Search Bar */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-neutral-400" />
              <input
                type="text"
                placeholder={viewMode === 'departments' 
                  ? "Buscar por código o nombre de departamento..."
                  : "Buscar por código o nombre de cargo..."}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              />
            </div>
            
            {/* Faculty Filter - Only for departments */}
            {viewMode === 'departments' && (
              <div className="flex items-center space-x-2 md:min-w-[300px]">
                <Filter className="h-5 w-5 text-neutral-400" />
                <select
                  value={selectedFaculty}
                  onChange={(e) => setSelectedFaculty(e.target.value)}
                  className="flex-1 px-4 py-2.5 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white transition-colors"
                >
                  <option value="all">Todas las Facultades</option>
                  {faculties.map((faculty) => (
                    <option key={faculty.key} value={faculty.key}>
                      {faculty.value}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Clear Filters Button - Only show when filters are active */}
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="px-4 py-2.5 bg-neutral-100 hover:bg-neutral-200 text-neutral-700 rounded-lg text-sm font-medium flex items-center transition-colors whitespace-nowrap"
              >
                <X className="h-4 w-4 mr-2" />
                Limpiar filtros
              </button>
            )}
          </div>

          {/* Active Filters Badge */}
          {hasActiveFilters && (
            <div className="mt-3 flex flex-wrap gap-2">
              {searchTerm && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-700 border border-primary-200">
                  Búsqueda: "{searchTerm}"
                  <button
                    onClick={() => setSearchTerm('')}
                    className="ml-2 hover:text-primary-900"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
              {viewMode === 'departments' && selectedFaculty !== 'all' && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-secondary-100 text-secondary-700 border border-secondary-200">
                  Facultad: {faculties.find(f => f.key === selectedFaculty)?.value || selectedFaculty}
                  <button
                    onClick={() => setSelectedFaculty('all')}
                    className="ml-2 hover:text-secondary-900"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
            </div>
          )}
        </div>

        {/* Stats Card with Result Count */}
        <div className="px-4 mb-6 flex items-center justify-between flex-wrap gap-3">
          <div className="inline-flex items-center px-4 py-2 bg-info-50 border border-info-200 rounded-lg">
            <div className="text-sm font-medium text-info-700">
              {viewMode === 'departments' ? (
                <>
                  Mostrando {startIndex + 1}-{Math.min(endIndex, filteredDepartments.length)} de {filteredDepartments.length} departamento/s
                  {hasActiveFilters && ' (filtrados)'}
                </>
              ) : (
                <>
                  Mostrando {startIndex + 1}-{Math.min(endIndex, filteredPositions.length)} de {filteredPositions.length} cargo/s
                  {hasActiveFilters && ' (filtrados)'}
                </>
              )}
            </div>
          </div>

          {/* Items per page selector */}
          <div className="flex items-center space-x-2">
            <span className="text-sm text-neutral-600">Por página:</span>
            <select
              value={itemsPerPage}
              onChange={(e) => {
                setItemsPerPage(Number(e.target.value));
                setCurrentPage(1);
              }}
              className="px-3 py-1.5 border border-neutral-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
            >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={25}>25</option>
            </select>
          </div>
        </div>
      </div>

      {/* Content - Departments or Positions Table */}
      {viewMode === 'departments' ? (
        <DepartmentsTable 
          filteredDepartments={paginatedData as DepartmentResponse[]}
          searchTerm={searchTerm}
          selectedFaculty={selectedFaculty}
          setDeleteConfirm={setDeleteConfirm}
        />
      ) : (
        <PositionsTable 
          filteredPositions={paginatedData as JobPositionResponse[]}
          searchTerm={searchTerm}
          setDeleteConfirm={setDeleteConfirm}
        />
      )}

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="mt-6 flex items-center justify-between bg-white rounded-lg border border-neutral-200 shadow-sm px-6 py-4">
          <div className="text-sm text-neutral-600">
            Página {currentPage} de {totalPages}
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => goToPage(currentPage - 1)}
              disabled={currentPage === 1}
              className="p-2 rounded-lg border border-neutral-300 hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              title="Página anterior"
            >
              <ChevronLeft className="h-5 w-5 text-neutral-600" />
            </button>

            {/* Page numbers */}
            <div className="flex space-x-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                let pageNum;
                if (totalPages <= 5) {
                  pageNum = i + 1;
                } else if (currentPage <= 3) {
                  pageNum = i + 1;
                } else if (currentPage >= totalPages - 2) {
                  pageNum = totalPages - 4 + i;
                } else {
                  pageNum = currentPage - 2 + i;
                }

                return (
                  <button
                    key={i}
                    onClick={() => goToPage(pageNum)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                      currentPage === pageNum
                        ? 'bg-primary-600 text-white'
                        : 'text-neutral-600 hover:bg-neutral-100'
                    }`}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>

            <button
              onClick={() => goToPage(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="p-2 rounded-lg border border-neutral-300 hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              title="Página siguiente"
            >
              <ChevronRight className="h-5 w-5 text-neutral-600" />
            </button>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-white rounded-lg max-w-md w-full p-6 shadow-xl">
            <div className="flex items-center mb-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-error-100 flex items-center justify-center mr-3">
                <Trash2 className="h-5 w-5 text-error-600" />
              </div>
              <h3 className="text-lg font-semibold text-neutral-900">
                Confirmar eliminación
              </h3>
            </div>
            <p className="text-sm text-neutral-600 mb-6 ml-13">
              ¿Estás seguro de que deseas eliminar este {viewMode === 'departments' ? 'departamento' : 'cargo'}? Esta acción no se puede deshacer.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setDeleteConfirm(null)}
                className="px-5 py-2.5 text-sm font-medium text-neutral-700 bg-white border-2 border-neutral-300 rounded-lg hover:bg-neutral-50 hover:border-neutral-400 transition-all"
              >
                Cancelar
              </button>
              <button
                onClick={() => viewMode === 'departments' ? handleDeleteDepartment(deleteConfirm) : handleDeletePosition(deleteConfirm)}
                className="px-5 py-2.5 text-sm font-medium text-white bg-error-600 rounded-lg hover:bg-error-700 shadow-sm hover:shadow transition-all"
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
    <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
      {filteredDepartments.length === 0 ? (
        <div className="text-center py-16">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-neutral-100 mb-4">
            <Building className="h-8 w-8 text-neutral-400" />
          </div>
          <h3 className="text-base font-semibold text-neutral-900 mb-2">
            No se encontraron departamentos
          </h3>
          <p className="text-sm text-neutral-500">
            {searchTerm || selectedFaculty !== 'all' 
              ? 'Intenta con otros términos de búsqueda o filtros' 
              : 'Comienza creando un nuevo departamento'}
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-neutral-200">
            <thead className="bg-neutral-50">
              <tr>
                <th className="px-6 py-3.5 text-left text-xs font-semibold text-neutral-700 uppercase tracking-wider">
                  Código
                </th>
                <th className="px-6 py-3.5 text-left text-xs font-semibold text-neutral-700 uppercase tracking-wider">
                  Departamento
                </th>
                <th className="px-6 py-3.5 text-left text-xs font-semibold text-neutral-700 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-neutral-200">
              {filteredDepartments.map((department: DepartmentResponse) => (
                <tr key={department.dep_id} className="hover:bg-neutral-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-neutral-900">
                      {department.dep_code || department.dep_id}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-neutral-900">
                      {department.dep_name}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <Link 
                        href={`/departments/${department.dep_id}`}
                        className="p-2 text-info-600 hover:bg-info-50 rounded-lg transition-colors" 
                        title="Editar"
                      >
                        <Edit className="h-4 w-4" />
                      </Link>
                      <button
                        onClick={() => setDeleteConfirm(department.dep_id)}
                        className="p-2 text-error-600 hover:bg-error-50 rounded-lg transition-colors"
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
  filteredPositions: JobPositionResponse[];
  searchTerm: string;
  setDeleteConfirm: (id: string) => void;
}> = ({ filteredPositions, searchTerm, setDeleteConfirm }) => {
  return (
    <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
      {filteredPositions.length === 0 ? (
        <div className="text-center py-16">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-neutral-100 mb-4">
            <Briefcase className="h-8 w-8 text-neutral-400" />
          </div>
          <h3 className="text-base font-semibold text-neutral-900 mb-2">
            No se encontraron cargos
          </h3>
          <p className="text-sm text-neutral-500">
            {searchTerm 
              ? 'Intenta con otros términos de búsqueda' 
              : 'Comienza creando un nuevo cargo'}
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-neutral-200">
            <thead className="bg-neutral-50">
              <tr>
                <th className="px-6 py-3.5 text-left text-xs font-semibold text-neutral-700 uppercase tracking-wider">
                  Código
                </th>
                <th className="px-6 py-3.5 text-left text-xs font-semibold text-neutral-700 uppercase tracking-wider">
                  Cargo
                </th>
                <th className="px-6 py-3.5 text-left text-xs font-semibold text-neutral-700 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-neutral-200">
              {filteredPositions.map((position: JobPositionResponse) => (
                <tr key={position.pos_id} className="hover:bg-neutral-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-neutral-900">
                      {position.pos_id}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-neutral-900">
                      {position.pos_name}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <Link 
                        href={`/positions/${position.pos_id}`}
                        className="p-2 text-info-600 hover:bg-info-50 rounded-lg transition-colors" 
                        title="Editar"
                      >
                        <Edit className="h-4 w-4" />
                      </Link>
                      <button
                        onClick={() => setDeleteConfirm(position.pos_id)}
                        className="p-2 text-error-600 hover:bg-error-50 rounded-lg transition-colors"
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

export default DepartmentsAndPositionsPage;