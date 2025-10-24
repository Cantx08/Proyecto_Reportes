'use client';

import React from 'react';
import Link from 'next/link';
import {
    Users,
    Building2,
    FileText,
    FileEdit,
    ClipboardCheck,
    TrendingUp,
    Calendar,
    Award
} from 'lucide-react';

const modules = [
    {
        name: 'Autores',
        href: '/authors',
        icon: Users
    },
    {
        name: 'Departamentos y Cargos',
        href: '/departments-and-positions',
        icon: Building2
    },
    {
        name: 'Publicaciones',
        href: '/publications',
        icon: FileText
    },
    {
        name: 'Borradores',
        href: '/borradores',
        icon: FileEdit
    },
    {
        name: 'Certificaciones',
        href: '/reports',
        icon: ClipboardCheck
    }
];

export default function HomePage() {
    return (
        <div className="max-w-7xl mx-auto">
            {/* Home Section */}
            <div className="bg-white p-8 mb-8">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-primary-500 text-4xl font-bold mb-2">
                            SISTEMA DE CERTIFICADOS DE PUBLICACIONES
                        </h1>
                        <p className="text-neutral-600 text-lg">
                            Escuela Politécnica Nacional
                        </p>
                    </div>
                    <div className="text-right px-6 py-4">
                        <div
                            className="text-primary-500 text-center text-3xl font-bold">{new Date().toLocaleDateString('es-ES', {day: 'numeric'})}</div>
                        <div className="text-primary-400 font-medium">{new Date().toLocaleDateString('es-ES', {
                            month: 'long',
                            year: 'numeric'
                        })}</div>
                    </div>
                </div>
            </div>

            {/* Main Modules */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mb-8">
                {modules.map((module) => (
                    <Link key={module.name} href={module.href}>
                        <div 
                            className="h-48 bg-primary-500 rounded-xl p-8 shadow-lg hover:shadow-2xl hover:bg-primary-600 transition-all duration-300 cursor-pointer transform hover:-translate-y-2 border-b-4 border-secondary-500"
                        >
                            <div className="h-full flex flex-col items-center justify-center space-y-4">
                                <module.icon className="h-14 w-14 text-white" strokeWidth={1.5} />
                                <h3 className="text-base font-semibold text-white text-center leading-tight">
                                    {module.name}
                                </h3>
                            </div>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
