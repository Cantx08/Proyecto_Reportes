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
      'author_page': 'Autores',
      'departments_page': 'Departamentos', 
      'publications_page': 'Publicaciones',
      'borradores': 'Borradores',
      'reports_page': 'Informes Finales'
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
    <nav className="flex items-center space-x-2 text-sm text-gray-500 mb-6">
      {breadcrumbs.map((breadcrumb, index) => (
        <React.Fragment key={breadcrumb.href}>
          {index > 0 && <ChevronRight className="h-4 w-4" />}
          <Link
            href={breadcrumb.href}
            className={`flex items-center space-x-1 hover:text-gray-700 transition-colors ${
              index === breadcrumbs.length - 1 ? 'text-gray-900 font-medium' : ''
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