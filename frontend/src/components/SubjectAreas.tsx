'use client';

import React from 'react';

interface SubjectAreasProps {
  areas: string[];
}

export const SubjectAreas: React.FC<SubjectAreasProps> = ({ areas }) => {
  if (areas.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Áreas Temáticas
        </h3>
        <p className="text-gray-500 text-center py-8">
          No hay áreas temáticas para mostrar
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        {areas.length} Áreas Temáticas
      </h3>
      
      <div className="space-y-2 max-h-80 overflow-y-auto">
        {areas.map((area, index) => (
          <div
            key={index}
            className="py-2 text-gray-500 text-sm"
          >
            - {area}
          </div>
        ))}
      </div>
    </div>
  );
};
