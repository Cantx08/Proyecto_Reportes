'use client';

import React from 'react';

interface Publicacion {
  title: string;           // Cambio: titulo -> title
  year: string;           // Cambio: anio -> year
  source: string;         // Cambio: fuente -> source
  document_type: string;  // Cambio: tipo_documento -> document_type
  affiliation: string;    // Cambio: filiacion -> affiliation
  doi: string;
  categories: string;     // Cambio: categorias -> categories
}

interface PublicacionesListProps {
  publicaciones: Publicacion[];
}

export const PublicacionesList: React.FC<PublicacionesListProps> = ({
  publicaciones
}) => {
  if (publicaciones.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Publicaciones
        </h3>
        <p className="text-gray-500 text-center py-8">
          No hay publicaciones para mostrar
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        Publicaciones ({publicaciones.length})
      </h3>
      
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {publicaciones.map((pub, index) => (
          <div
            key={index}
            className="border border-gray-200 rounded-md p-4 hover:shadow-sm transition-shadow"
          >
            <h4 className="font-semibold text-gray-900 mb-2 line-clamp-2">
              {pub.title}
            </h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
              <div>
                <span className="font-medium">Año:</span> {pub.year}
              </div>
              <div>
                <span className="font-medium">Tipo:</span> {pub.document_type}
              </div>
              <div className="md:col-span-2">
                <span className="font-medium">Fuente:</span> {pub.source}
              </div>
              <div className="md:col-span-2">
                <span className="font-medium">Filiación:</span> {pub.affiliation}
              </div>
              {pub.categories && (
                <div className="md:col-span-2">
                  <span className="font-medium">Categorías:</span>{' '}
                  <span style={{ color: '#2c5f7f' }}>{pub.categories}</span>
                </div>
              )}
              {pub.doi && (
                <div className="md:col-span-2">
                  <span className="font-medium">DOI:</span>{' '}
                  <a
                    href={`https://doi.org/${pub.doi}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:underline"
                    style={{ color: '#2c5f7f' }}
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
