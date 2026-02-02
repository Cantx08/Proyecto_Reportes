'use client';

import React, {useState} from 'react';
import {useRouter} from 'next/navigation';
import {useAuthors} from '@/features/authors/hooks/useAuthors';
import {useDepartments} from '@/features/departments/hooks/useDepartments';
import {useJobPositions} from '@/features/job-positions/hooks/useJobPositions';
import {scopusAccountsService} from "@/features/scopus-accounts/services/scopusAccountService";
import {ArrowLeft, Save, Loader2, UserPlus, User, AlertCircle, GraduationCap, BookOpen} from 'lucide-react';
import Link from 'next/link';
import ScopusAccountsManager from '@/features/scopus-accounts/components/ScopusAccountsManager';

export default function NewAuthorPage() {
    const router = useRouter();
    const {createAuthor, creating, error} = useAuthors();
    const {departments, loading: loadingDepartments} = useDepartments();
    const {positions, loading: loadingPositions} = useJobPositions();

    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        institutional_email: '',
        title: '',
        gender: 'M',
        job_position_id: '',
        department_id: ''
    });

    const [scopusAccounts, setScopusAccounts] = useState<any[]>([]);

    const [validationErrors, setValidationErrors] = useState<{
        first_name?: string;
        last_name?: string;
        job_position_id?: string;
        department_id?: string;
    }>({});

    const [submitError, setSubmitError] = useState<string | null>(null);
    const [submitSuccess, setSubmitSuccess] = useState(false);
    const [savingAccounts, setSavingAccounts] = useState(false);

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

        const newAuthor = await createAuthor(formData);

        if (newAuthor) {
            if (scopusAccounts.length > 0) {
                setSavingAccounts(true);
                try {
                    const accountPromises = scopusAccounts.map(account =>
                    scopusAccountsService.create({
                        scopus_id: account.scopus_id,
                        author_id: newAuthor.author_id,
                    }));
                    await Promise.all(accountPromises);
                } catch (error) {
                    console.error("Error al guardar cuentas Scopus:", error);
                } finally {
                    setSavingAccounts(false);
                }
            }
            setSubmitSuccess(true);
            setTimeout(() => {
                router.push('/authors');
            }, 1500);
        } else {
            setSubmitError(error || 'Error al crear el autor');
        }
    };

    if (loadingDepartments || loadingPositions) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-center">
                    <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-primary-500"/>
                    <p className="text-neutral-600">Cargando datos...</p>
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
                        <UserPlus className="h-8 w-8 mr-3 text-primary-500"/>
                        <div>
                            <h1 className="text-2xl font-bold text-neutral-900">Agregar Autor</h1>
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
                            <h3 className="text-sm font-medium text-error-800">Error al crear autor</h3>
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
                            <p className="mt-2 text-sm text-success-700">El autor se creó correctamente.
                                Redirigiendo...</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Form */}
            <div className="bg-white shadow-md rounded-lg p-8">
                <form onSubmit={handleSubmit} className="space-y-8">
                    {/* Personal Information Section */}
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
                                        placeholder="Ej: Juan Carlos"
                                        className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                                            validationErrors.first_name ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
                                        }`}
                                    />
                                    {validationErrors.first_name && (
                                        <div className="flex items-center mt-2 text-error-600">
                                            <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0"/>
                                            <p className="text-sm">{validationErrors.first_name}</p>
                                        </div>
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
                                        placeholder="Ej: Pérez González"
                                        className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                                            validationErrors.last_name ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
                                        }`}
                                    />
                                    {validationErrors.last_name && (
                                        <div className="flex items-center mt-2 text-error-600">
                                            <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0"/>
                                            <p className="text-sm">{validationErrors.last_name}</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                            {/* Título y Género */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                                        className="w-full px-4 py-2.5 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white hover:border-neutral-400 transition-colors"
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
                                    >
                                        <option value="M">Masculino</option>
                                        <option value="F">Femenino</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Academic Information Section */}
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
                                <label htmlFor="institutional_email" className="block text-sm font-medium text-neutral-700 mb-2">
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
                                />
                            </div>

                            {/* Departamento */}
                            <div>
                                <label htmlFor="department_id" className="block text-sm font-medium text-neutral-700 mb-2">
                                    Departamento <span className="text-error-500">*</span>
                                </label>
                                <select
                                    id="department_id"
                                    name="department_id"
                                    value={formData.department_id}
                                    onChange={handleInputChange}
                                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                                        validationErrors.department_id ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
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
                                    <div className="flex items-center mt-2 text-error-600">
                                        <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0"/>
                                        <p className="text-sm">{validationErrors.department_id}</p>
                                    </div>
                                )}
                            </div>

                            {/* Cargo */}
                            <div>
                                <label htmlFor="job_position_id" className="block text-sm font-medium text-neutral-700 mb-2">
                                    Cargo <span className="text-error-500">*</span>
                                </label>
                                <select
                                    id="job_position_id"
                                    name="job_position_id"
                                    value={formData.job_position_id}
                                    onChange={handleInputChange}
                                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                                        validationErrors.job_position_id ? 'border-error-300 bg-error-50' : 'border-neutral-300 bg-white hover:border-neutral-400'
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
                                    <div className="flex items-center mt-2 text-error-600">
                                        <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0"/>
                                        <p className="text-sm">{validationErrors.job_position_id}</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Research IDs Section */}
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
                            initialAccounts={scopusAccounts}
                            onChange={setScopusAccounts}
                        />
                    </div>

                    {/* Action Buttons */}
                    <div className="flex justify-end space-x-4 pt-6 border-t border-neutral-200">
                        <Link href="/authors">
                            <button
                                type="button"
                                className="px-6 py-2.5 border-2 border-neutral-300 rounded-lg text-neutral-700 font-medium hover:bg-neutral-50 hover:border-neutral-400 transition-all"
                            >
                                Cancelar
                            </button>
                        </Link>
                        <button
                            type="submit"
                            disabled={creating || savingAccounts}
                            className="px-6 py-2.5 bg-success-600 text-white rounded-lg font-medium hover:bg-success-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center shadow-sm hover:shadow transition-all"
                        >
                            {(creating || savingAccounts) ? (
                                <>
                                    <Loader2 className="h-4 w-4 mr-2 animate-spin"/>
                                    {creating ? 'Creando Autor...' : 'Vinculando Scopus...'}
                                </>
                            ) : (
                                <>
                                    <Save className="h-4 w-4 mr-2"/>
                                    Guardar Autor
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}