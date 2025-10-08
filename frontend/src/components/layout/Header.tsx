'use client';

import React from 'react';
import {usePathname} from 'next/navigation';

const Header: React.FC = () => {
    const pathname = usePathname();

    const getPageTitle = () => {
        const routes: { [key: string]: string } = {
            '/': 'Home',
            '/authors': 'Autores',
            '/departments': 'Departamentos y Cargos',
            '/publications': 'Publicaciones',
            '/borradores': 'Borradores',
            '/reports': 'Certificaciones'
        };
        return routes[pathname] || 'Sistema de Reportes';
    };

    return (
        <header className="px-6 py-4 border-b border-gray-200" style={{backgroundColor: '#042a53'}}>
            <div className="flex items-center justify-between">
                {/* Page Title */}
                <div>
                    <h1 className="text-2xl font-semibold text-white">{getPageTitle()}</h1>
                </div>
            </div>
        </header>
    );
};

export default Header;