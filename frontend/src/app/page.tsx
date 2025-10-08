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
        description: 'Gestión y búsqueda de información de investigadores.',
        href: '/authors',
        icon: Users,
        color: 'text-white',
        bgColor: '#042a53',
        stats: '1,234 autores',
        recent: 'Último acceso: hace 2 horas'
    },
    {
        name: 'Departamentos',
        description: 'Gestión de departamentos institucionales y cargos académicos.',
        href: '/departments',
        icon: Building2,
        color: 'text-white',
        bgColor: '#042a53',
        stats: '45 departamentos',
        recent: 'Actualizado ayer'
    },
    {
        name: 'Publicaciones',
        description: 'Búsqueda y análisis de publicaciones indexadas en Scopus.',
        href: '/publications',
        icon: FileText,
        color: 'text-white',
        bgColor: '#042a53',
        stats: '5,678 publicaciones',
        recent: 'Sincronizado hace 1 hora'
    },
    {
        name: 'Generar Borradores',
        description: 'Crear versiones preliminares de reportes para revisión',
        href: '/borradores',
        icon: FileEdit,
        color: 'text-white',
        bgColor: '#042a53',
        stats: '23 borradores',
        recent: 'Último borrador: hoy'
    },
    {
        name: 'Certificaciones',
        description: 'Generación de certificados finales de publicaciones.',
        href: '/reports',
        icon: ClipboardCheck,
        color: 'text-white',
        bgColor: '#042a53',
        stats: '156 informes',
        recent: 'Último informe: hace 3 días'
    }
];

const quickStats = [
    {name: 'Publicaciones este mes', value: '89', change: '+12%', icon: TrendingUp, color: '#042a53'},
    {name: 'Reportes generados', value: '34', change: '+8%', icon: ClipboardCheck, color: '#042a53'},
    {name: 'Autores activos', value: '1,234', change: '+3%', icon: Users, color: '#042a53'},
    {name: 'Índice de productividad', value: '94%', change: '+5%', icon: Award, color: '#042a53'}
];

export default function HomePage() {
    return (
        <div className="max-w-7xl mx-auto">
            {/* Home Section */}
            <div className="bg-white p-6 mb-8 text-gray-900">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-[#042a53] text-4xl rounded-lg font-bold mb-2">
                            SISTEMA DE CERTIFICADOS DE PUBLICACIONES
                        </h1>
                    </div>
                    <div className="text-right">
                        <div
                            className="text-gray-600 text-center text-3xl font-bold">{new Date().toLocaleDateString('es-ES', {day: 'numeric'})}</div>
                        <div className="text-gray-600">{new Date().toLocaleDateString('es-ES', {
                            month: 'long',
                            year: 'numeric'
                        })}</div>
                    </div>
                </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {quickStats.map((stat) => (
                    <div key={stat.name} className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                                <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                                <p className="text-sm flex items-center mt-1" style={{color: stat.color}}>
                                    <TrendingUp className="h-4 w-4 mr-1"/>
                                    {stat.change}
                                </p>
                            </div>
                            <div className="p-3 rounded-lg" style={{backgroundColor: `${stat.color}20`}}>
                                <stat.icon className="h-6 w-6" style={{color: stat.color}}/>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Main Modules */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {modules.map((module) => (
                    <Link key={module.name} href={module.href}>
                        <div
                            className="bg-white rounded-lg p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
                            <div className="flex items-start justify-between mb-4">
                                <div className="p-3 rounded-lg" style={{backgroundColor: module.bgColor}}>
                                    <module.icon className={`h-6 w-6 ${module.color}`}/>
                                </div>
                                <div className="text-right">
                                    <div className="text-sm font-medium text-gray-900">{module.stats}</div>
                                    <div className="text-xs text-gray-500">{module.recent}</div>
                                </div>
                            </div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                {module.name}
                            </h3>
                            <p className="text-gray-600 text-sm">
                                {module.description}
                            </p>
                        </div>
                    </Link>
                ))}
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                <div className="px-6 py-4 border-b border-gray-200">
                    <h2 className="text-lg font-semibold text-gray-900 flex items-center">
                        <Calendar className="h-5 w-5 mr-2"/>
                        Actividad Reciente
                    </h2>
                </div>
                <div className="divide-y divide-gray-200">
                    {[
                        {action: 'Reporte generado', target: 'Dr. Juan Pérez', time: 'hace 2 horas', type: 'success'},
                        {action: 'Borrador creado', target: 'Dra. María García', time: 'hace 4 horas', type: 'info'},
                        {
                            action: 'Publicaciones sincronizadas',
                            target: 'Sistema Scopus',
                            time: 'hace 6 horas',
                            type: 'info'
                        },
                        {action: 'Nuevo autor registrado', target: 'Dr. Carlos López', time: 'ayer', type: 'success'},
                        {
                            action: 'Departamento actualizado',
                            target: 'Ingeniería Civil',
                            time: 'hace 2 días',
                            type: 'warning'
                        }
                    ].map((activity, index) => (
                        <div key={index} className="px-6 py-4 flex items-center justify-between">
                            <div className="flex items-center">
                                <div className={`h-2 w-2 rounded-full mr-3 ${
                                    activity.type === 'success' ? 'bg-green-400' :
                                        activity.type === 'warning' ? 'bg-yellow-400' : 'bg-[#042a53]'
                                }`}></div>
                                <div>
                                    <p className="text-sm font-medium text-gray-900">
                                        {activity.action}
                                    </p>
                                    <p className="text-sm text-gray-500">
                                        {activity.target}
                                    </p>
                                </div>
                            </div>
                            <span className="text-sm text-gray-500">{activity.time}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
