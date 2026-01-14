'use client';

import React, { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import Sidebar from './Sidebar';
import Header from './Header';
import Breadcrumb from './Breadcrumb';

export default function AuthenticatedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  // Rutas públicas que no requieren autenticación
  const publicRoutes = ['/login', '/register'];
  const isPublicRoute = publicRoutes.includes(pathname);

  useEffect(() => {
    // Si no está autenticado y no está en una ruta pública, redirigir a login
    if (!isLoading && !isAuthenticated && !isPublicRoute) {
      router.push('/login');
    }
    
    // Si está autenticado y está en una ruta pública, redirigir al dashboard
    if (!isLoading && isAuthenticated && isPublicRoute) {
      router.push('/');
    }
  }, [isAuthenticated, isLoading, pathname, router, isPublicRoute]);

  // Mostrar loading mientras se verifica la autenticación
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#042a53] mx-auto mb-4"></div>
          <p className="text-neutral-600">Cargando...</p>
        </div>
      </div>
    );
  }

  // Si está en una ruta pública, mostrar solo el contenido sin layout
  if (isPublicRoute) {
    return <>{children}</>;
  }

  // Si no está autenticado, no mostrar nada (se redirigirá)
  if (!isAuthenticated) {
    return null;
  }

  // Layout completo para usuarios autenticados
  return (
    <div className="flex h-screen bg-neutral-50">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header />

        {/* Page Content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto px-6 py-4 bg-neutral-50">
          <Breadcrumb />
          {children}
        </main>
      </div>
    </div>
  );
}
