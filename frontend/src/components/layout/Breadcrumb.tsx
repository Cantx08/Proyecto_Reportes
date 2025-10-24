'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronRight, Home, LucideIcon } from 'lucide-react';

interface BreadcrumbItem {
  name: string;
  href: string;
  icon?: LucideIcon;
}

const Breadcrumb: React.FC = () => {
  const pathname = usePathname();
  
  const generateBreadcrumbs = (): BreadcrumbItem[] => {
    const paths = pathname.split('/').filter(Boolean);
    const breadcrumbs: BreadcrumbItem[] = [{ name: 'Home', href: '/', icon: Home }];
    
    const routeNames: { [key: string]: string } = {
      'authors': 'Autores',
      'departments': 'Departamentos',
      'departments-and-positions': 'Departamentos y Cargos',
      'positions': 'Cargos',
      'publications': 'Publicaciones',
      'reports': 'Certificaciones'
    };
    
    let currentPath = '';
    paths.forEach((path) => {
      currentPath += `/${path}`;
      if (routeNames[path]) {
        breadcrumbs.push({
          name: routeNames[path],
          href: currentPath
        });
      }
    });
    
    return breadcrumbs;
  };

  const breadcrumbs = generateBreadcrumbs();

  if (pathname === '/') {
    return null; // No mostrar breadcrumbs en la página principal
  }

  return (
    <nav className="flex items-center space-x-2 text-sm text-neutral-500 mb-6">
      {breadcrumbs.map((breadcrumb, index) => (
        <React.Fragment key={breadcrumb.href}>
          {index > 0 && <ChevronRight className="h-4 w-4 text-neutral-400" />}
          <Link
            href={breadcrumb.href}
            className={`flex items-center space-x-1 hover:text-primary-600 transition-colors ${
              index === breadcrumbs.length - 1 ? 'text-primary-700 font-medium' : ''
            }`}
          >
            {breadcrumb.icon && <breadcrumb.icon className="h-4 w-4" />}
            <span>{breadcrumb.name}</span>
          </Link>
        </React.Fragment>
      ))}
    </nav>
  );
};

export default Breadcrumb;