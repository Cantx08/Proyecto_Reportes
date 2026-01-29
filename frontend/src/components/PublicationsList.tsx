'use client';

import React from 'react';

// Definimos la estructura del objeto de categoría que viene del backend
interface CategoryData {
    name: string;
    quartile: string;
    percentile: number;
    rank: number;
    total: number;
}

interface Publication {
    title: string;
    year: string;
    source: string;
    document_type: string;
    affiliation: string;
    doi: string;
    // Ahora aceptamos string O un array de objetos
    categories: string | CategoryData[];
}

interface PublicationsListProps {
    publications: Publication[];
}

export const PublicationsList: React.FC<PublicationsListProps> = ({
                                                                      publications
                                                                  }) => {
    // Ordenar publicaciones por año descendente (más reciente primero)
    const sortedPublications = [...publications].sort((a, b) => {
        const yearA = parseInt(a.year) || 0;
        const yearB = parseInt(b.year) || 0;
        return yearB - yearA;
    });

    // Función auxiliar para renderizar las categorías
    const renderCategories = (categories: string | CategoryData[]) => {
        // Caso 1: Es un array de objetos (Información rica del SJR)
        if (Array.isArray(categories)) {
            return (
                <div className="flex flex-wrap gap-2 mt-1">
                    {categories.map((cat, idx) => (
                        <span
                            key={idx}
                            className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium border ${
                                cat.quartile === 'Q1' ? 'bg-green-50 text-green-700 border-green-200' :
                                    cat.quartile === 'Q2' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                                        cat.quartile === 'Q3' ? 'bg-yellow-50 text-yellow-700 border-yellow-200' :
                                            'bg-gray-50 text-gray-700 border-gray-200'
                            }`}
                            title={`Ranking: ${cat.rank}/${cat.total}`}
                        >
              {cat.name}
                            <span className="ml-1 font-bold">({cat.quartile} - P{cat.percentile}%)</span>
            </span>
                    ))}
                </div>
            );
        }

        // Caso 2: Es un string (ej: "No indexada" o datos antiguos)
        return <span className="text-primary-600 font-medium">{categories}</span>;
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
                        key={index}
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
                                <span className="font-medium text-neutral-800">Fuente:</span> {pub.source}
                            </div>
                            <div className="md:col-span-2">
                                <span className="font-medium text-neutral-800">Filiación:</span> {pub.affiliation}
                            </div>

                            {/* Sección de Categorías Mejorada */}
                            {pub.categories && (
                                <div className="md:col-span-2">
                                    <span className="font-medium text-neutral-800">Categorías:</span>
                                    {renderCategories(pub.categories)}
                                </div>
                            )}

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