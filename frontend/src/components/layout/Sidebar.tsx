'use client';

import React from 'react';
import Link from 'next/link';
import {usePathname} from 'next/navigation';
import {useSidebar} from '@/contexts/SidebarContext';
import {
    Home,
    Users,
    Building2,
    BookOpen,
    FileEdit,
    ClipboardCheck,
    ChevronsLeft,
    ChevronsRight
} from 'lucide-react';

const navigation = [
    {name: 'Home', href: '/', icon: Home},
    {name: 'Autores', href: '/authors', icon: Users},
    {name: 'Departamentos', href: '/departments', icon: Building2},
    {name: 'Publicaciones', href: '/publications', icon: BookOpen},
    {name: 'Borradores', href: '/borradores', icon: FileEdit},
    {name: 'Certificados', href: '/reports', icon: ClipboardCheck},
];

const Sidebar: React.FC = () => {
    const pathname = usePathname();
    const {isCollapsed, toggleSidebar} = useSidebar();

    return (
        <div className={`flex h-full flex-col transition-all duration-300 ${
            isCollapsed ? 'w-16' : 'w-64'
        }`} style={{backgroundColor: '#042a53'}}>
            {/* Logo del Departamento */}
            <div className={`relative flex h-16 items-center border-b border-white/20 bg-white ${
                isCollapsed ? 'px-2 justify-center' : 'px-6 justify-between'
            }`}>
                <div className="flex items-center space-x-3">
                    <div className="flex h-10 w-10 items-center justify-center">
                        <img
                            src="/logo_viiv.png"
                            alt="Logo Departamento"
                            className="h-8 w-8 object-contain"
                        />
                    </div>
                    {!isCollapsed && (
                        <div>
                            <h1 className="text-xl font-bold text-center text-[#042a53]">VIIV</h1>
                            <p className="text-xs text-center text-[#042a53]/80">Dirección de Investigación</p>
                        </div>
                    )}
                </div>

                {/* Toggle Button - Always visible */}
                <button
                    onClick={toggleSidebar}
                    className={`p-1 rounded transition-colors z-20 ${
                        isCollapsed
                            ? 'absolute -right-3 top-1/2 transform -translate-y-1/2 text-white hover:text-gray-200 shadow-lg'
                            : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
                    }`}
                    style={isCollapsed ? {backgroundColor: '#042a53'} : {}}
                >
                    {isCollapsed ? (
                        <ChevronsRight className="h-4 w-4"/>
                    ) : (
                        <ChevronsLeft className="h-4 w-4"/>
                    )}
                </button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-2 py-6">
                <ul className="space-y-2">
                    {navigation.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <li key={item.name}>
                                <Link
                                    href={item.href}
                                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors group relative ${
                                        isActive
                                            ? 'bg-white/20 text-white border-r-2 border-white'
                                            : 'text-white/80 hover:bg-white/10 hover:text-white'
                                    } ${isCollapsed ? 'justify-center' : ''}`}
                                    title={isCollapsed ? item.name : undefined}
                                >
                                    <item.icon className={`h-5 w-5 ${isActive ? 'text-white' : 'text-white/80'} ${
                                        !isCollapsed ? 'mr-3' : ''
                                    }`}/>
                                    {!isCollapsed && item.name}
                                    {isCollapsed && (
                                        <span
                                            className="absolute left-16 bg-gray-900 text-white text-xs rounded px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-20">
                      {item.name}
                    </span>
                                    )}
                                </Link>
                            </li>
                        );
                    })}
                </ul>
            </nav>

            {/* Footer */}
            <div className={`p-4 border-t border-white/20 ${isCollapsed ? 'px-2' : ''}`}>
                <div className={`flex items-center px-3 py-2 ${
                    isCollapsed ? 'justify-center' : 'space-x-3'
                }`}>
                    <div className="flex h-8 w-8 items-center justify-center">
                        <img src="/logo_epn_bn.png"
                             alt="Logo EPN b/n"
                             className="h-7 w-7 object-contain"/>
                    </div>
                    {!isCollapsed && (
                        <div>
                            <p className="text-sm font-medium text-white">Certificaciones EPN</p>
                            <p className="text-xs text-white/60">v1.0.0</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Sidebar;