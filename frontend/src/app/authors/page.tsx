'use client';

import React, {useState, useEffect} from 'react';
import Link from 'next/link';
import {useAuthors} from '@/hooks/useAuthors';
import {
    Plus,
    Edit,
    Trash2,
    Users,
    Loader2,
    Search,
    Filter,
    X,
    ChevronLeft,
    ChevronRight,
    Download,
    Upload
} from 'lucide-react';

interface Faculty {
    key: string;
    value: string;
}

interface Department {
    dep_id: string;
    dep_name: string;
    fac_name: string;
}

export default function AuthorsPage() {
    const {authors, loading, error, fetchAuthors, deleteAuthor} = useAuthors();
    const [searchTerm, setSearchTerm] = useState('');
    const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
    const [faculties, setFaculties] = useState<Faculty[]>([]);
    const [departments, setDepartments] = useState<Department[]>([]);
    const [selectedFaculty, setSelectedFaculty] = useState<string>('all');
    const [selectedDepartment, setSelectedDepartment] = useState<string>('all');
    const [currentPage, setCurrentPage] = useState(1);
    const [hoveredRow, setHoveredRow] = useState<string | null>(null);
    const [exporting, setExporting] = useState(false);
    const [importing, setImporting] = useState(false);
    const [importResult, setImportResult] = useState<{ success: boolean; message: string } | null>(null);
    const itemsPerPage = 10;


    useEffect(() => {
        fetchAuthors();

        // Cargar facultades
        const loadFaculties = async () => {
            try {
                const response = await fetch('http://localhost:8000/departments/faculties');
                const data = await response.json();
                if (Array.isArray(data)) {
                    setFaculties(data);
                } else if (data.data && Array.isArray(data.data)) {
                    // Por si acaso tu backend usa un wrapper de respuesta
                    setFaculties(data.data);
                }

            } catch (error) {
                console.error('Error loading faculties:', error);
            }
        };

        // Cargar departamentos
        const loadDepartments = async () => {
            try {
                const response = await fetch('http://localhost:8000/departments');
                const data = await response.json();
                if (data.success) {
                    setDepartments(data.data);
                }
            } catch (error) {
                console.error('Error loading departments:', error);
            }
        };

        loadFaculties();
        loadDepartments();
    }, [fetchAuthors]);

    // Manejar eliminación de autor
    const handleDelete = async (authorId: string) => {
        const success = await deleteAuthor(authorId);
        if (success) {
            setDeleteConfirm(null);
            await fetchAuthors(); // Recargar la lista
        }
    };

    // Filtrar departamentos por facultad seleccionada
    const filteredDepartmentsByFaculty = selectedFaculty === 'all'
        ? departments
        : departments.filter(dept => dept.fac_name === selectedFaculty);

    // Filtrar autores según los filtros aplicados
    const filteredAuthors = authors.filter(author => {
        const matchesSearch =
            author.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            author.surname.toLowerCase().includes(searchTerm.toLowerCase()) ||
            author.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
            author.position.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesFaculty = selectedFaculty === 'all' ||
            departments.find(d => d.dep_name === author.department)?.fac_name === selectedFaculty;

        const matchesDepartment = selectedDepartment === 'all' ||
            author.department === selectedDepartment;

        return matchesSearch && matchesFaculty && matchesDepartment;
    });

    // Reset department filter when faculty changes
    useEffect(() => {
        setSelectedDepartment('all');
    }, [selectedFaculty]);

    // Reset department filter when faculty changes
    useEffect(() => {
        setSelectedDepartment('all');
    }, [selectedFaculty]);

    // Función para limpiar todos los filtros
    const clearFilters = () => {
        setSearchTerm('');
        setSelectedFaculty('all');
        setSelectedDepartment('all');
        setCurrentPage(1);
    };

    // Verificar si hay filtros activos
    const hasActiveFilters = searchTerm !== '' || selectedFaculty !== 'all' || selectedDepartment !== 'all';

    // Función para exportar autores a CSV
    const handleExportAuthors = async () => {

        setExporting(true);
        try {
            const token = localStorage.getItem('auth_token');
            const response = await fetch('http://localhost:8000/authors/export', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Error al exportar autores');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'autores_export.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Error exporting authors:', error);
            alert('Error al exportar autores. Por favor intente de nuevo.');
        } finally {
            setExporting(false);
        }
    };

    // Función para importar autores desde CSV
    const handleImportAuthors = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        // Validar que sea un archivo CSV
        if (!file.name.endsWith('.csv')) {
            setImportResult({success: false, message: 'El archivo debe ser un CSV'});
            return;
        }

        setImporting(true);
        setImportResult(null);

        try {
            const token = localStorage.getItem('auth_token');
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://localhost:8000/authors/import', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || 'Error al importar autores');
            }

            setImportResult({
                success: true,
                message: result.message || `Importación completada. Creados: ${result.data?.created || 0}, Actualizados: ${result.data?.updated || 0}`
            });

            // Recargar la lista de autores
            await fetchAuthors();

        } catch (error) {
            console.error('Error importing authors:', error);
            setImportResult({
                success: false,
                message: error instanceof Error ? error.message : 'Error al importar autores'
            });
        } finally {
            setImporting(false);
            // Limpiar el input para permitir subir el mismo archivo de nuevo
            event.target.value = '';
        }
    };

    // Paginación
    const totalPages = Math.ceil(filteredAuthors.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedAuthors = filteredAuthors.slice(startIndex, endIndex);

    // Reset page when filters change
    useEffect(() => {
        setCurrentPage(1);
    }, [searchTerm, selectedFaculty, selectedDepartment]);

    if (loading) {
        return (
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
                                <Users className="h-6 w-6 mr-3 text-primary-500"/>
                                Gestión de Autores
                            </h1>
                            <p className="text-neutral-600 mt-1">
                                Administra la información de autores y sus cuentas Scopus asociadas.
                            </p>
                        </div>
                    </div>
                </div>

                {/* Skeleton Loading */}
                <div className="bg-white rounded-lg border border-neutral-200 overflow-hidden shadow-sm">
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-neutral-200">
                            <thead className="bg-neutral-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Autor</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Departamento</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Cargo</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Acciones</th>
                            </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-neutral-200">
                            {[...Array(5)].map((_, i) => (
                                <tr key={i}>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="h-4 bg-neutral-200 rounded animate-pulse w-48"></div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="h-4 bg-neutral-200 rounded animate-pulse w-40"></div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="h-4 bg-neutral-200 rounded animate-pulse w-32"></div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="flex space-x-2">
                                            <div className="h-4 w-4 bg-neutral-200 rounded animate-pulse"></div>
                                            <div className="h-4 w-4 bg-neutral-200 rounded animate-pulse"></div>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
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
                        <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
                            <Users className="h-6 w-6 mr-3 text-primary-500"/>
                            Gestión de Autores
                        </h1>
                        <p className="text-neutral-600 mt-1">
                            Administra la información de autores y sus cuentas Scopus asociadas.
                        </p>
                    </div>
                    <div className="flex space-x-3">
                        <input
                            type="file"
                            id="import-csv"
                            accept=".csv"
                            onChange={handleImportAuthors}
                            className="hidden"
                        />
                        <label
                            htmlFor="import-csv"
                            className={`px-4 py-2 bg-info-500 hover:bg-info-600 text-white rounded-lg text-sm font-medium transition-colors flex items-center shadow-sm cursor-pointer ${importing ? 'opacity-50 cursor-not-allowed' : ''}`}
                            title="Importar autores desde CSV"
                        >
                            {importing ? (
                                <>
                                    <Loader2 className="h-4 w-4 mr-2 animate-spin"/>
                                    Importando...
                                </>
                            ) : (
                                <>
                                    <Upload className="h-4 w-4 mr-2"/>
                                    Importar CSV
                                </>
                            )}
                        </label>
                        <button
                            onClick={handleExportAuthors}
                            disabled={exporting}
                            className="px-4 py-2 bg-secondary-500 hover:bg-secondary-600 text-white rounded-lg text-sm font-medium transition-colors flex items-center shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            title="Exportar autores a CSV"
                        >
                            {exporting ? (
                                <>
                                    <Loader2 className="h-4 w-4 mr-2 animate-spin"/>
                                    Exportando...
                                </>
                            ) : (
                                <>
                                    <Download className="h-4 w-4 mr-2"/>
                                    Exportar CSV
                                </>
                            )}
                        </button>
                        <Link href="/authors/authors-new">
                            <button
                                className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg text-sm font-medium transition-colors flex items-center shadow-sm">
                                <Plus className="h-4 w-4 mr-2"/>
                                Nuevo Autor
                            </button>
                        </Link>
                    </div>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="bg-error-50 border border-error-200 rounded-lg p-4 mb-6">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <svg className="h-5 w-5 text-error-400" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd"
                                          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                          clipRule="evenodd"/>
                                </svg>
                            </div>
                            <div className="ml-3">
                                <h3 className="text-sm font-medium text-error-800">Error al cargar autores</h3>
                                <div className="mt-2 text-sm text-error-700">
                                    <p>{error}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Import Result Message */}
                {importResult && (
                    <div className={`border rounded-lg p-4 mb-6 ${
                        importResult.success
                            ? 'bg-success-50 border-success-200'
                            : 'bg-error-50 border-error-200'
                    }`}>
                        <div className="flex justify-between items-start">
                            <div className="flex">
                                <div className="flex-shrink-0">
                                    {importResult.success ? (
                                        <svg className="h-5 w-5 text-success-400" viewBox="0 0 20 20"
                                             fill="currentColor">
                                            <path fillRule="evenodd"
                                                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                                  clipRule="evenodd"/>
                                        </svg>
                                    ) : (
                                        <svg className="h-5 w-5 text-error-400" viewBox="0 0 20 20" fill="currentColor">
                                            <path fillRule="evenodd"
                                                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                                  clipRule="evenodd"/>
                                        </svg>
                                    )}
                                </div>
                                <div className="ml-3">
                                    <h3 className={`text-sm font-medium ${importResult.success ? 'text-success-800' : 'text-error-800'}`}>
                                        {importResult.success ? 'Importación exitosa' : 'Error en la importación'}
                                    </h3>
                                    <div
                                        className={`mt-2 text-sm ${importResult.success ? 'text-success-700' : 'text-error-700'}`}>
                                        <p>{importResult.message}</p>
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={() => setImportResult(null)}
                                className={`p-1 rounded-full hover:bg-opacity-20 ${
                                    importResult.success ? 'hover:bg-success-600' : 'hover:bg-error-600'
                                }`}
                            >
                                <X className={`h-4 w-4 ${importResult.success ? 'text-success-500' : 'text-error-500'}`}/>
                            </button>
                        </div>
                    </div>
                )}

                {/* Search Bar and Filters */}
                <div className="bg-white rounded-lg border border-neutral-200 p-4 mb-4 shadow-sm">
                    <div className="flex items-center gap-3">
                        {/* Search Bar */}
                        <div className="relative flex-1">
                            <Search
                                className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-neutral-400"/>
                            <input
                                type="text"
                                placeholder="Buscar por nombre, apellido, departamento o cargo..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className={`w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all ${
                                    searchTerm ? 'border-primary-400 bg-primary-50' : 'border-neutral-300'
                                }`}
                            />
                        </div>

                        {/* Filter Icon Separator */}
                        <div className="flex items-center px-2">
                            <div className="h-8 w-px bg-neutral-300 mr-3"></div>
                            <Filter className="h-5 w-5 text-neutral-400"/>
                        </div>

                        {/* Faculty Filter */}
                        <select
                            value={selectedFaculty}
                            onChange={(e) => setSelectedFaculty(e.target.value)}
                            className={`w-64 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all ${
                                selectedFaculty !== 'all' ? 'border-secondary-400 bg-secondary-50' : 'border-neutral-300'
                            }`}
                        >
                            <option value="all">Todas las Facultades</option>
                            {faculties.map((faculty) => (
                                <option key={faculty.key} value={faculty.key}>
                                    {faculty.value}
                                </option>
                            ))}
                        </select>

                        {/* Department Filter */}
                        <select
                            value={selectedDepartment}
                            onChange={(e) => setSelectedDepartment(e.target.value)}
                            className={`w-64 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all ${
                                selectedDepartment !== 'all' ? 'border-info-400 bg-info-50' : 'border-neutral-300'
                            }`}
                            disabled={selectedFaculty !== 'all' && filteredDepartmentsByFaculty.length === 0}
                        >
                            <option value="all">Todos los Departamentos</option>
                            {filteredDepartmentsByFaculty.map((department) => (
                                <option key={department.dep_id} value={department.dep_name}>
                                    {department.dep_name}
                                </option>
                            ))}
                        </select>

                        {/* Clear Filters Button */}
                        {hasActiveFilters && (
                            <button
                                onClick={clearFilters}
                                className="px-4 py-2 bg-neutral-100 hover:bg-neutral-200 text-neutral-700 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
                                title="Limpiar todos los filtros"
                            >
                                <X className="h-4 w-4"/>
                                Limpiar
                            </button>
                        )}
                    </div>
                </div>

                {/* Results Counter with Active Filters Badges */}
                <div className="flex items-center justify-between px-4 mb-6">
                    <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-neutral-700">
              {filteredAuthors.length} autor/es encontrado/s
            </span>

                        {/* Active Filters Badges */}
                        <div className="flex items-center gap-2">
                            {searchTerm && (
                                <span
                                    className="inline-flex items-center gap-1 px-3 py-1 bg-primary-100 text-primary-800 text-xs font-medium rounded-full">
                  Búsqueda: "{searchTerm.length > 20 ? searchTerm.substring(0, 20) + '...' : searchTerm}"
                  <button onClick={() => setSearchTerm('')} className="hover:bg-primary-200 rounded-full p-0.5">
                    <X className="h-3 w-3"/>
                  </button>
                </span>
                            )}
                            {selectedFaculty !== 'all' && (
                                <span
                                    className="inline-flex items-center gap-1 px-3 py-1 bg-secondary-100 text-secondary-800 text-xs font-medium rounded-full">
                  Facultad
                  <button onClick={() => setSelectedFaculty('all')}
                          className="hover:bg-secondary-200 rounded-full p-0.5">
                    <X className="h-3 w-3"/>
                  </button>
                </span>
                            )}
                            {selectedDepartment !== 'all' && (
                                <span
                                    className="inline-flex items-center gap-1 px-3 py-1 bg-info-100 text-info-800 text-xs font-medium rounded-full">
                  Departamento
                  <button onClick={() => setSelectedDepartment('all')} className="hover:bg-info-200 rounded-full p-0.5">
                    <X className="h-3 w-3"/>
                  </button>
                </span>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Authors Table */}
            <div className="bg-white rounded-lg border border-neutral-200 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-neutral-200">
                        <thead className="bg-neutral-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Autor
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Departamento
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Cargo
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Acciones
                            </th>
                        </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-neutral-200">
                        {paginatedAuthors.map((author) => (
                            <tr
                                key={author.author_id}
                                className="hover:bg-primary-50 transition-colors"
                                onMouseEnter={() => setHoveredRow(author.author_id)}
                                onMouseLeave={() => setHoveredRow(null)}
                            >
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm font-medium text-neutral-900">
                                        {author.title} {author.name} {author.surname}
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-700">
                                    {author.department}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-700">
                                    {author.position}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <div className={`flex space-x-3 transition-opacity duration-200 ${
                                        hoveredRow === author.author_id ? 'opacity-100' : 'opacity-0'
                                    }`}>
                                        <Link href={`/authors/${author.author_id}`}>
                                            <button
                                                className="p-2 text-success-600 hover:text-success-900 hover:bg-success-50 rounded-lg transition-colors"
                                                title="Editar autor"
                                            >
                                                <Edit className="h-4 w-4"/>
                                            </button>
                                        </Link>
                                        <button
                                            onClick={() => setDeleteConfirm(author.author_id)}
                                            className="p-2 text-error-600 hover:text-error-900 hover:bg-error-50 rounded-lg transition-colors"
                                            title="Eliminar autor"
                                        >
                                            <Trash2 className="h-4 w-4"/>
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
                        <Users className="mx-auto h-12 w-12 text-neutral-400"/>
                        <h3 className="mt-2 text-sm font-medium text-neutral-900">
                            {searchTerm || hasActiveFilters ? 'No se encontraron autores' : 'No hay autores registrados'}
                        </h3>
                        <p className="mt-1 text-sm text-neutral-500">
                            {searchTerm || hasActiveFilters
                                ? 'Intenta ajustando los filtros de búsqueda'
                                : 'Comienza agregando nuevos autores.'
                            }
                        </p>
                    </div>
                )}

                {/* Pagination */}
                {filteredAuthors.length > 0 && totalPages > 1 && (
                    <div className="bg-neutral-50 px-6 py-4 border-t border-neutral-200">
                        <div className="flex items-center justify-between">
                            <div className="text-sm text-neutral-700">
                                Mostrando <span className="font-medium text-primary-600">{startIndex + 1}</span> a{' '}
                                <span
                                    className="font-medium text-primary-600">{Math.min(endIndex, filteredAuthors.length)}</span> de{' '}
                                <span
                                    className="font-medium text-primary-600">{filteredAuthors.length}</span> resultados
                            </div>
                            <div className="flex items-center space-x-2">
                                <button
                                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                    disabled={currentPage === 1}
                                    className="p-2 rounded-lg border border-neutral-300 bg-white hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                    title="Página anterior"
                                >
                                    <ChevronLeft className="h-4 w-4 text-neutral-600"/>
                                </button>

                                <div className="flex items-center space-x-1">
                                    {[...Array(totalPages)].map((_, idx) => {
                                        const pageNumber = idx + 1;
                                        // Show first page, last page, current page, and pages around current
                                        if (
                                            pageNumber === 1 ||
                                            pageNumber === totalPages ||
                                            (pageNumber >= currentPage - 1 && pageNumber <= currentPage + 1)
                                        ) {
                                            return (
                                                <button
                                                    key={pageNumber}
                                                    onClick={() => setCurrentPage(pageNumber)}
                                                    className={`min-w-[36px] px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                                                        currentPage === pageNumber
                                                            ? 'bg-primary-600 text-white shadow-sm'
                                                            : 'bg-white border border-neutral-300 text-neutral-700 hover:bg-neutral-50'
                                                    }`}
                                                >
                                                    {pageNumber}
                                                </button>
                                            );
                                        } else if (
                                            pageNumber === currentPage - 2 ||
                                            pageNumber === currentPage + 2
                                        ) {
                                            return <span key={pageNumber} className="px-2 text-neutral-400">...</span>;
                                        }
                                        return null;
                                    })}
                                </div>

                                <button
                                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                                    disabled={currentPage === totalPages}
                                    className="p-2 rounded-lg border border-neutral-300 bg-white hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                    title="Página siguiente"
                                >
                                    <ChevronRight className="h-4 w-4 text-neutral-600"/>
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Modal de Confirmación de Eliminación */}
            {deleteConfirm && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4 shadow-xl">
                        <h3 className="text-lg font-semibold text-neutral-900 mb-4">
                            Confirmar Eliminación
                        </h3>
                        <p className="text-neutral-600 mb-6">
                            ¿Estás seguro de que deseas eliminar este autor? Esta acción no se puede deshacer.
                        </p>
                        <div className="flex justify-end space-x-3">
                            <button
                                onClick={() => setDeleteConfirm(null)}
                                className="px-4 py-2 border border-neutral-300 rounded-lg text-neutral-700 hover:bg-neutral-50 transition-colors"
                            >
                                Cancelar
                            </button>
                            <button
                                onClick={() => handleDelete(deleteConfirm)}
                                className="px-4 py-2 bg-error-600 text-white rounded-lg hover:bg-error-700 transition-colors"
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