'use client';

import React, {useState, useEffect} from 'react';
import {useRouter, useParams} from 'next/navigation';
import {useAuthors} from '@/src/features/authors/hooks/useAuthors';
import {useDepartments} from '@/src/features/departments/hooks/useDepartments';
import {useJobPositions} from '@/src/features/job-positions/hooks/useJobPositions';
import ScopusAccountsManager, {ScopusAccountUiItem} from '@/src/features/scopus-accounts/components/ScopusAccountsManager';
import {ArrowLeft, Save, Loader2, User, GraduationCap, BookOpen} from 'lucide-react';
import Link from 'next/link';

export default function EditAuthorPage() {
    const router = useRouter();
    const params = useParams();
    const author_id = params?.id as string;

    const {getAuthor, updateAuthor, updating, error} = useAuthors();
    const {departments, loading: loadingDepartments, fetchDepartments} = useDepartments();
    const {positions, loading: loadingPositions, fetchPositions} = useJobPositions();

    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        title: '',
        gender: 'M',
        institutional_email: ' ',
        job_position_id: '',
        department_id: ''
    });

    const [scopusAccounts, setScopusAccounts] = useState<ScopusAccountUiItem[]>([]);

    const [validationErrors, setValidationErrors] = useState<{
        first_name?: string;
        last_name?: string;
        job_position_id?: string;
        department_id?: string;
    }>({});

    const [submitError, setSubmitError] = useState<string | null>(null);
    const [submitSuccess, setSubmitSuccess] = useState(false);

    // Cargar datos del autor
    useEffect(() => {
        // Cargar departamentos y posiciones
        fetchDepartments();
        fetchPositions();

        const loadAuthor = async () => {
            if (!author_id) {
                router.push('/authors');
                return;
            }

            setLoading(true);
            const author = await getAuthor(author_id);

            if (author) {
                setFormData({
                    first_name: author.first_name || '',
                    last_name: author.last_name || '',
                    title: author.title || '',
                    gender: author.gender || 'M',
                    institutional_email: author.institutional_email || ' ',
                    job_position_id: author.job_position_id || '',
                    department_id: author.department_id || ''
                });
            } else {
                setSubmitError('No se pudo cargar el autor');
            }

            setLoading(false);
        };

        loadAuthor();
    }, [author_id, getAuthor, router, fetchDepartments, fetchPositions]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const {name, value} = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        // Limpiar error de validación al editar
        if (validationErrors[name as keyof typeof validationErrors]) {
            setValidationErrors(prev => ({
                ...prev,
                [name]: undefined
            }));
        }
    };

    const validateForm = (): boolean => {
        const errors: typeof validationErrors = {};

        if (!formData.first_name.trim()) {
            errors.first_name = 'El nombre es obligatorio';
        }

        if (!formData.last_name.trim()) {
            errors.last_name = 'El apellido es obligatorio';
        }

        if (!formData.job_position_id.trim()) {
            errors.job_position_id = 'El cargo es obligatorio';
        }

        if (!formData.department_id.trim()) {
            errors.department_id = 'El departamento es obligatorio';
        }

        setValidationErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitError(null);
        setSubmitSuccess(false);

        if (!validateForm()) {
            return;
        }

        const updatedAuthor = await updateAuthor(author_id, formData);

        if (updatedAuthor) {
            setSubmitSuccess(true);
            setTimeout(() => {
                router.push('/authors');
            }, 1500);
        } else {
            setSubmitError(error || 'Error al actualizar el autor');
        }
    };

    if (loading || loadingDepartments || loadingPositions) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-center">
                    <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-primary-500"/>
                    <p className="text-neutral-600">Cargando datos del autor...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center justify-between">
                    <div className="flex items-center">
                        <User className="h-12 w-12 mr-3 text-neutral-900"/>
                        <div>
                            <h1 className="text-2xl font-bold text-neutral-900">Editar Autor</h1>
                        </div>
                    </div>
                    <Link href="/authors">
                        <button
                            className="flex items-center px-4 py-2 text-neutral-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors">
                            <ArrowLeft className="h-4 w-4 mr-2"/>
                            Volver
                        </button>
                    </Link>
                </div>
            </div>

            {/* Error Message */}
            {submitError && (
                <div className="bg-error-50 border border-error-200 rounded-lg p-4 mb-6 animate-fade-in">
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-error-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd"
                                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                      clipRule="evenodd"/>
                            </svg>
                        </div>
                        <div className="ml-3">
                            <h3 className="text-sm font-medium text-error-800">Error al actualizar</h3>
                            <p className="mt-2 text-sm text-error-700">{submitError}</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Success Message */}
            {submitSuccess && (
                <div className="bg-success-50 border border-success-200 rounded-lg p-4 mb-6 animate-fade-in">
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-success-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd"
                                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                      clipRule="evenodd"/>
                            </svg>
                        </div>
                        <div className="ml-3">
                            <h3 className="text-sm font-medium text-success-800">¡Éxito!</h3>
                            <p className="mt-2 text-sm text-success-700">El autor se actualizó correctamente.
                                Redirigiendo...</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Form */}
            <div className="bg-white shadow-md rounded-lg p-8">
                <form onSubmit={handleSubmit} className="space-y-8">
                    {/* Información Personal Section */}
                    <div>
                        <div className="flex items-center mb-6">
                            <div
                                className="flex items-center justify-center w-10 h-10 rounded-full bg-primary-100 mr-3">
                                <User className="h-5 w-5 text-primary-600"/>
                            </div>
                            <div>
                                <h2 className="text-lg font-semibold text-neutral-900">Información Personal</h2>
                            </div>
                        </div>

                        <div className="space-y-6">
                            {/* Nombres y Apellidos */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <label htmlFor="first_name"
                                           className="block text-sm font-medium text-neutral-700 mb-2">
                                        Nombres <span className="text-error-500">*</span>
                                    </label>
                                    <input
                                        type="text"
                                        id="first_name"
                                        name="first_name"
                                        value={formData.first_name}
                                        onChange={handleInputChange}
                                        placeholder="Juan Carlos"
                                        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                                            validationErrors.first_name
                                                ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50'
                                                : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
                                        }`}
                                    />
                                    {validationErrors.first_name && (
                                        <p className="mt-1 text-sm text-error-600 flex items-center">
                                            <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd"
                                                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                                                      clipRule="evenodd"/>
                                            </svg>
                                            {validationErrors.first_name}
                                        </p>
                                    )}
                                </div>
                                <div>
                                    <label htmlFor="last_name"
                                           className="block text-sm font-medium text-neutral-700 mb-2">
                                        Apellidos <span className="text-error-500">*</span>
                                    </label>
                                    <input
                                        type="text"
                                        id="last_name"
                                        name="last_name"
                                        value={formData.last_name}
                                        onChange={handleInputChange}
                                        placeholder="Pérez García"
                                        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                                            validationErrors.last_name
                                                ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50'
                                                : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
                                        }`}
                                    />
                                    {validationErrors.last_name && (
                                        <p className="mt-1 text-sm text-error-600 flex items-center">
                                            <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd"
                                                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                                                      clipRule="evenodd"/>
                                            </svg>
                                            {validationErrors.last_name}
                                        </p>
                                    )}
                                </div>
                            </div>
                            {/* Título y Género */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
                                <div>
                                    <label htmlFor="title" className="block text-sm font-medium text-neutral-700 mb-2">
                                        Título Académico
                                    </label>
                                    <input
                                        type="text"
                                        id="title"
                                        name="title"
                                        value={formData.title}
                                        onChange={handleInputChange}
                                        placeholder="Ej: Dr., Mg., Ing."
                                        className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="gender" className="block text-sm font-medium text-neutral-700 mb-2">
                                        Género <span className="text-error-500">*</span>
                                    </label>
                                    <select
                                        id="gender"
                                        name="gender"
                                        value={formData.gender}
                                        onChange={handleInputChange}
                                        className="w-full px-4 py-2.5 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white hover:border-neutral-400 transition-colors"
                                        disabled={true}
                                    >
                                        <option value="M">Masculino</option>
                                        <option value="F">Femenino</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Información Académica Section */}
                    <div className="border-t border-neutral-200 pt-8">
                        <div className="flex items-center mb-6">
                            <div className="flex items-center justify-center w-10 h-10 rounded-full bg-info-100 mr-3">
                                <GraduationCap className="h-5 w-5 text-info-600"/>
                            </div>
                            <div>
                                <h2 className="text-lg font-semibold text-neutral-900">Información Académica</h2>
                            </div>
                        </div>
                        <div className="space-y-6">
                            {/* Correo Institucional */}
                            <div>
                                <label htmlFor="institutional_email"
                                       className="block text-sm font-medium text-neutral-700 mb-2">
                                    Correo Institucional
                                </label>
                                <input
                                    type="text"
                                    id="institutional_email"
                                    name="institutional_email"
                                    value={formData.institutional_email}
                                    onChange={handleInputChange}
                                    placeholder="user@example.edu.ec"
                                    className="w-full px-4 py-2.5 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white hover:border-neutral-400 transition-colors"
                                    disabled={true}
                                />
                            </div>
                            {/* Departamento */}
                            <div>
                                <label htmlFor="department" className="block text-sm font-medium text-neutral-700 mb-2">
                                    Departamento <span className="text-error-500">*</span>
                                </label>
                                <select
                                    id="department"
                                    name="department_id"
                                    value={formData.department_id}
                                    onChange={handleInputChange}
                                    className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                                        validationErrors.department_id
                                            ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50'
                                            : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
                                    }`}
                                >
                                    <option value="">Seleccione un departamento</option>
                                    {departments.map((dept) => (
                                        <option key={dept.dep_id} value={dept.dep_id}>
                                            {dept.dep_name}
                                        </option>
                                    ))}
                                </select>
                                {validationErrors.department_id && (
                                    <p className="mt-1 text-sm text-error-600 flex items-center">
                                        <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd"
                                                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                                                  clipRule="evenodd"/>
                                        </svg>
                                        {validationErrors.department_id}
                                    </p>
                                )}
                            </div>

                            {/* Cargo */}
                            <div>
                                <label htmlFor="position" className="block text-sm font-medium text-neutral-700 mb-2">
                                    Cargo <span className="text-error-500">*</span>
                                </label>
                                <select
                                    id="position"
                                    name="job_position_id"
                                    value={formData.job_position_id}
                                    onChange={handleInputChange}
                                    className={`w-full px-4 py-2 border rounded-lg focus:ring-2 transition-colors ${
                                        validationErrors.job_position_id
                                            ? 'border-error-400 focus:ring-error-500 focus:border-error-500 bg-error-50'
                                            : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
                                    }`}
                                >
                                    <option value="">Seleccione un cargo</option>
                                    {positions.map((pos) => (
                                        <option key={pos.pos_id} value={pos.pos_id}>
                                            {pos.pos_name}
                                        </option>
                                    ))}
                                </select>
                                {validationErrors.job_position_id && (
                                    <p className="mt-1 text-sm text-error-600 flex items-center">
                                        <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd"
                                                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                                                  clipRule="evenodd"/>
                                        </svg>
                                        {validationErrors.job_position_id}
                                    </p>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Identificadores de Investigación Section */}
                    <div className="border-t border-neutral-200 pt-8">
                        <div className="flex items-center mb-6">
                            <div
                                className="flex items-center justify-center w-10 h-10 rounded-full bg-secondary-100 mr-3">
                                <BookOpen className="h-5 w-5 text-secondary-600"/>
                            </div>
                            <div>
                                <h2 className="text-lg font-semibold text-neutral-900">Cuentas Scopus</h2>
                            </div>
                        </div>

                        {/* Cuentas Scopus */}
                        <ScopusAccountsManager
                            author_id={author_id}
                            initialAccounts={scopusAccounts}
                            onChange={setScopusAccounts}
                        />
                    </div>

                    {/* Buttons */}
                    <div className="flex justify-end space-x-4 pt-6 border-t border-neutral-200">
                        <Link href="/authors">
                            <button
                                type="button"
                                className="px-6 py-2.5 border border-neutral-300 rounded-lg text-neutral-700 hover:bg-neutral-50 transition-colors font-medium"
                            >
                                Cancelar
                            </button>
                        </Link>
                        <button
                            type="submit"
                            disabled={updating}
                            className="px-6 py-2.5 bg-primary-500 hover:bg-primary-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-colors shadow-sm font-medium"
                        >
                            {updating ? (
                                <>
                                    <Loader2 className="h-4 w-4 mr-2 animate-spin"/>
                                    Actualizando...
                                </>
                            ) : (
                                <>
                                    <Save className="h-4 w-4 mr-2"/>
                                    Actualizar Autor
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
