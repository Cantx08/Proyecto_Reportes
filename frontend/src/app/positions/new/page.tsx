'use client';

import React, {useState} from 'react';
import Link from 'next/link';
import {useRouter} from 'next/navigation';
import {useJobPositions} from '@/features/job-positions/hooks/useJobPositions';
import {ErrorNotification} from '@/components/ErrorNotification';
import {Briefcase, Save, ArrowLeft} from 'lucide-react';
import {JobPositionCreateRequest} from "@/features/job-positions/types";

const NewPositionPage: React.FC = () => {
    const router = useRouter();
    const {createPosition, creating, error} = useJobPositions();

    const [formData, setFormData] = useState<JobPositionCreateRequest>({
        pos_name: '',
    });

    const [validationErrors, setValidationErrors] = useState<{
        pos_name?: string;
    }>({});

    const validateForm = (): boolean => {
        const errors: typeof validationErrors = {};

        if (!formData.pos_name.trim()) {
            errors.pos_name = 'El nombre del cargo es requerido';
        }

        setValidationErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        const result = await createPosition({
            pos_name: formData.pos_name.trim(),
        });

        if (result) {
            router.push('/departments-and-positions');
        }
    };

    const handleChange = (field: keyof JobPositionCreateRequest, value: string) => {
        setFormData(prev => ({...prev, [field]: value}));
        // Limpiar error de validación del campo cuando el usuario empieza a escribir
        if (field === 'pos_name' && validationErrors.pos_name) {
            setValidationErrors({});
        }
    };

    return (
        <div className="max-w-4xl mx-auto">

            {/* Header */}
            <div className="mb-8 mt-6">
                <Link href="/departments-and-positions"
                      className="inline-flex items-center text-sm text-neutral-600 hover:text-primary-600 mb-4 transition-colors">
                    <ArrowLeft className="h-4 w-4 mr-1"/>
                    Volver a Departamentos y Cargos
                </Link>
                <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
                    <Briefcase className="h-6 w-6 mr-3 text-primary-600"/>
                    Nuevo Cargo
                </h1>
                <p className="text-neutral-600 mt-1">
                    Crea un nuevo cargo en el sistema
                </p>
            </div>

            {/* Error Message */}
            {error && (
                <ErrorNotification
                    error={error}
                    onDismiss={() => {
                    }}
                />
            )}

            {/* Form */}
            <div className="bg-white rounded-lg border border-neutral-200 shadow-sm p-6">
                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Nombre del Cargo */}
                    <div>
                        <label htmlFor="pos_name" className="block text-sm font-medium text-neutral-700 mb-2">
                            Nombre del Cargo <span className="text-error-500">*</span>
                        </label>
                        <input
                            type="text"
                            id="pos_name"
                            value={formData.pos_name}
                            onChange={(e) => handleChange('pos_name', e.target.value)}
                            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                                validationErrors.pos_name ? 'border-error-500' : 'border-neutral-300'
                            }`}
                            placeholder="Ej: Profesor Principal"
                        />
                        {validationErrors.pos_name && (
                            <p className="mt-1 text-sm text-error-600">{validationErrors.pos_name}</p>
                        )}
                        <p className="mt-1 text-sm text-neutral-500">
                            El código se generará automáticamente a partir del nombre
                        </p>
                    </div>

                    {/* Buttons */}
                    <div className="flex justify-end space-x-3 pt-4 border-t border-neutral-200">
                        <Link href="/departments-and-positions"
                              className="px-4 py-2 text-sm font-medium text-neutral-700 bg-white border border-neutral-300 rounded-lg hover:bg-neutral-50 transition-colors">
                            Cancelar
                        </Link>
                        <button
                            type="submit"
                            disabled={creating}
                            className="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-colors"
                        >
                            {creating ? (
                                <>
                                    <span className="mr-2">Creando...</span>
                                    <div
                                        className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                                </>
                            ) : (
                                <>
                                    <Save className="h-4 w-4 mr-2"/>
                                    Crear Cargo
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default NewPositionPage;
