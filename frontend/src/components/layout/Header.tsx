'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import { Search } from 'lucide-react';

const Header: React.FC = () => {
  const pathname = usePathname();
  
  const getPageTitle = () => {
    const routes: { [key: string]: string } = {
      '/': 'Home',
      '/author_page': 'Gestión de Autores',
      '/departments_page': 'Gestión de Departamentos',
      '/publications_page': 'Gestión de Publicaciones',
      '/borradores': 'Generación de Borradores',
      '/reports_page': 'Informes Finales'
    };
    return routes[pathname] || 'Sistema de Reportes';
  };

  return (
    <header className="px-6 py-4 border-b border-gray-200" style={{ backgroundColor: '#042a53' }}>
      <div className="flex items-center justify-between">
        {/* Page Title */}
        <div>
          <h1 className="text-2xl font-semibold text-white">{getPageTitle()}</h1>
        </div>

        {/* Search */}
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar publicaciones, autores, departamentos..."
            className="w-full pl-10 pr-4 py-2 border border-white/20 rounded-lg text-sm bg-white/10 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent focus:bg-white/20"
          />
        </div>
      </div>
    </header>
  );
};

export default Header;