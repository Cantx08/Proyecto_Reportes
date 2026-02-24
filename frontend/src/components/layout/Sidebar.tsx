'use client';

import React from 'react';
import Link from 'next/link';
import {usePathname} from 'next/navigation';
import {useSidebar} from '@/src/contexts/SidebarContext';
import {
    Home,
    Users,
    Building2,
    BookOpen,
    ClipboardCheck,
    ChevronsLeft,
    ChevronsRight
} from 'lucide-react';
import Image from "next/image";

const navigation = [
    {name: 'Inicio', href: '/', icon: Home},
    {name: 'Autores', href: '/authors', icon: Users},
    {name: 'Departamentos y Cargos', href: '/departments-and-positions', icon: Building2},
    {name: 'Publicaciones', href: '/publications', icon: BookOpen},
    {name: 'Certificados', href: '/reports', icon: ClipboardCheck},
];
const Sidebar: React.FC = () => {
    const pathname = usePathname();
    const {isCollapsed, toggleSidebar} = useSidebar();

    return (
        <div className={`flex h-full flex-col bg-primary-500 transition-all duration-300 ${
            isCollapsed ? 'w-16' : 'w-64'
        }`}>
            {/* Logo del Departamento */}
            <div className={`relative flex h-20 items-center border-b border-primary-400/30 bg-white ${
                isCollapsed ? 'px-2 justify-center' : 'px-6 justify-between'
            }`}>
                <div className="flex items-center space-x-3">
                    <div className="flex h-10 w-10 items-center justify-center">
                        <Image
                            src="/logo_viiv.png"
                            alt="Logo Departamento"
                            width={40}
                            height={40}
                            className="h-10 w-10 object-contain"
                            priority
                        />
                    </div>
                    {!isCollapsed && (
                        <div>
                            <h1 className="text-xl font-bold text-center text-primary-500">VIIV</h1>
                            <p className="text-xs text-center text-primary-400">Dirección de Investigación</p>
                        </div>
                    )}
                </div>

                {/* Toggle Button - Always visible */}
                <button
                    onClick={toggleSidebar}
                    className={`p-1 rounded transition-colors z-20 ${
                        isCollapsed
                            ? 'absolute -right-3 top-1/2 transform -translate-y-1/2 bg-primary-500 text-white hover:bg-primary-600 shadow-lg'
                            : 'text-neutral-400 hover:text-neutral-600 hover:bg-neutral-100'
                    }`}
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
                                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200 group relative ${
                                        isActive
                                            ? 'bg-primary-600 text-white shadow-md'
                                            : 'text-primary-100 hover:bg-primary-600/80 hover:text-white'
                                    } ${isCollapsed ? 'justify-center' : ''}`}
                                    title={isCollapsed ? item.name : undefined}
                                >
                                    <item.icon className={`h-5 w-5 ${
                                        !isCollapsed ? 'mr-3' : ''
                                    }`}/>
                                    {!isCollapsed && item.name}
                                    {isCollapsed && (
                                        <span
                                            className="absolute left-16 bg-neutral-900 text-white text-xs rounded px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-20 shadow-lg">
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
            <div className={`p-4 border-t border-primary-400/30 ${isCollapsed ? 'px-2' : ''}`}>
                <div className={`flex items-center px-3 py-2 ${
                    isCollapsed ? 'justify-center' : 'space-x-3'
                }`}>
                    <div className="flex h-8 w-8 items-center justify-center">
                        <Image
                            src="/logo_epn_bn.png"
                            alt="Logo EPN"
                            width={32}
                            height={32}
                            className="h-8 w-8 object-contain"
                        />
                    </div>
                    {!isCollapsed && (
                        <div>
                            <p className="text-sm font-medium text-white">Certificaciones EPN</p>
                            <p className="text-xs text-primary-200">v1.0.0</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Sidebar;