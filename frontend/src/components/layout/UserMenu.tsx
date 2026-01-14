'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { User, LogOut, ChevronDown } from 'lucide-react';

export default function UserMenu() {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Cerrar el menú cuando se hace clic fuera
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!user) return null;

  // Obtener las iniciales del usuario
  const getInitials = () => {
    if (user.full_name) {
      const names = user.full_name.trim().split(' ');
      if (names.length >= 2) {
        return `${names[0][0]}${names[1][0]}`.toUpperCase();
      }
      return names[0].substring(0, 2).toUpperCase();
    }
    return user.username.substring(0, 2).toUpperCase();
  };

  const handleLogout = () => {
    setIsOpen(false);
    logout();
  };

  return (
    <div className="relative" ref={menuRef}>
      {/* Botón de usuario */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 hover:bg-neutral-100 rounded-lg px-3 py-2 transition-colors"
      >
        {/* Avatar circular con iniciales */}
        <div className="w-10 h-10 rounded-full bg-[#042a53] text-white flex items-center justify-center font-semibold text-sm">
          {getInitials()}
        </div>

        {/* Información del usuario */}
        <div className="hidden md:block text-left">
          <p className="text-sm font-medium text-neutral-900">
            {user.full_name || user.username}
          </p>
          <p className="text-xs text-neutral-500 capitalize">
            {user.role === 'admin' ? 'Administrador' : 'Usuario'}
          </p>
        </div>

        {/* Icono de flecha */}
        <ChevronDown 
          className={`w-4 h-4 text-neutral-500 transition-transform ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </button>

      {/* Menú desplegable */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-neutral-200 py-1 z-50">
          {/* Información del usuario en el menú */}
          <div className="px-4 py-3 border-b border-neutral-200">
            <p className="text-sm font-medium text-neutral-900">
              {user.full_name || user.username}
            </p>
            <p className="text-xs text-neutral-500 mt-1">{user.email}</p>
            <span className="inline-block mt-2 px-2 py-1 text-xs font-medium rounded-full bg-[#ccdde8] text-[#042a53]">
              {user.role === 'admin' ? 'Administrador' : 'Usuario'}
            </span>
          </div>

          {/* Opciones del menú */}
          <div className="py-1">
            <button
              onClick={() => {
                setIsOpen(false);
                // TODO: Implementar navegación a perfil
              }}
              className="w-full text-left px-4 py-2 text-sm text-neutral-700 hover:bg-neutral-100 flex items-center space-x-2"
            >
              <User className="w-4 h-4" />
              <span>Ver perfil</span>
            </button>

            <button
              onClick={handleLogout}
              className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2"
            >
              <LogOut className="w-4 h-4" />
              <span>Cerrar sesión</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
