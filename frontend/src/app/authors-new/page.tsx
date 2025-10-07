'use client';

import React from 'react';
import AuthorsManagerNew from '@/components/AuthorsManagerNew';

const AuthorsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-sm">
          <div className="border-b border-gray-200 px-6 py-4">
            <h1 className="text-2xl font-bold text-gray-900">Gestión de Autores</h1>
            <p className="text-gray-600 mt-1">
              Administra los autores y su información personal
            </p>
          </div>
          
          <div className="p-6">
            <AuthorsManagerNew />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthorsPage;