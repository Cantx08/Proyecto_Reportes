'use client';

import React from 'react';
import { Publication } from '@/src/features/publications/types';

interface PublicationsListProps {
    publications: Publication[];
}

/**
 * Extrae el cuartil de una categoría con formato "Nombre (Q1)"
 */
const extractQuartile = (category: string): string | null => {
    const match = category.match(/\(Q[1-4]\)/);
    return match ? match[0].replace(/[()]/g, '') : null;
};

/**
 * Obtiene los estilos de color según el cuartil
 */
const getQuartileStyles = (quartile: string | null): string => {
    switch (quartile) {
        case 'Q1':
            return 'bg-green-50 text-green-700 border-green-200';
        case 'Q2':
            return 'bg-blue-50 text-blue-700 border-blue-200';
        case 'Q3':
            return 'bg-yellow-50 text-yellow-700 border-yellow-200';
        case 'Q4':
            return 'bg-orange-50 text-orange-700 border-orange-200';
        default:
            return 'bg-gray-50 text-gray-700 border-gray-200';
    }
};

export const PublicationsList: React.FC<PublicationsListProps> = ({
    publications
}) => {
    // Ordenar publicaciones por año descendente (más reciente primero)
    const sortedPublications = [...publications].sort((a, b) => b.year - a.year);

    // Renderizar las categorías con cuartiles
    const renderCategories = (categories: string[], sjrYearUsed: number | null) => {
        if (!categories || categories.length === 0) {
            return <span className="text-neutral-500 italic">No indexada en SJR</span>;
        }

        return (
            <div className="flex flex-wrap gap-2 mt-1">
                {categories.map((category, idx) => {
                    const quartile = extractQuartile(category);
                    return (
                        <span
                            key={idx}
                            className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium border ${getQuartileStyles(quartile)}`}
                            title={sjrYearUsed ? `Datos SJR del año ${sjrYearUsed}` : undefined}
                        >
                            {category}
                        </span>
                    );
                })}
                {sjrYearUsed && (
                    <span className="text-xs text-neutral-400 self-center ml-1">
                        (SJR {sjrYearUsed})
                    </span>
                )}
            </div>
        );
    };

    // Renderizar áreas temáticas
    const renderSubjectAreas = (areas: string[]) => {
        if (!areas || areas.length === 0) return null;

        return (
            <div className="flex flex-wrap gap-1 mt-1">
                {areas.map((area, idx) => (
                    <span
                        key={idx}
                        className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-primary-50 text-primary-700 border border-primary-200"
                    >
                        {area}
                    </span>
                ))}
            </div>
        );
    };

    if (publications.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6">
                <h3 className="text-lg font-semibold text-neutral-800 mb-4">
                    Publicaciones
                </h3>
                <p className="text-neutral-500 text-center py-8">
                    No hay publicaciones para mostrar
                </p>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6">
            <h3 className="text-lg font-semibold text-neutral-800 mb-4">
                {publications.length} publicaciones obtenidas
            </h3>

            <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
                {sortedPublications.map((pub, index) => (
                    <div
                        key={pub.scopus_id || index}
                        className="border border-neutral-200 rounded-md p-4 hover:shadow-sm hover:border-primary-300 transition-all"
                    >
                        <h4 className="font-semibold text-neutral-900 mb-2">
                            {pub.title}
                        </h4>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-y-2 gap-x-4 text-sm text-neutral-600">
                            <div>
                                <span className="font-medium text-neutral-800">Año:</span> {pub.year}
                            </div>
                            <div>
                                <span className="font-medium text-neutral-800">Tipo:</span> {pub.document_type}
                            </div>
                            <div className="md:col-span-2">
                                <span className="font-medium text-neutral-800">Fuente:</span> {pub.source_title}
                            </div>
                            <div className="md:col-span-2">
                                <span className="font-medium text-neutral-800">Filiación:</span> {pub.affiliation_name}
                            </div>

                            {/* Áreas temáticas */}
                            {pub.subject_areas && pub.subject_areas.length > 0 && (
                                <div className="md:col-span-2">
                                    <span className="font-medium text-neutral-800">Áreas temáticas:</span>
                                    {renderSubjectAreas(pub.subject_areas)}
                                </div>
                            )}

                            {/* Categorías con cuartiles */}
                            <div className="md:col-span-2">
                                <span className="font-medium text-neutral-800">Categorías:</span>
                                {renderCategories(pub.categories_with_quartiles, pub.sjr_year_used)}
                            </div>

                            {pub.doi && (
                                <div className="md:col-span-2 mt-1">
                                    <span className="font-medium text-neutral-800">DOI:</span>{' '}
                                    <a
                                        href={`https://doi.org/${pub.doi}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-primary-600 hover:text-primary-700 hover:underline transition-colors break-all"
                                    >
                                        {pub.doi}
                                    </a>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};