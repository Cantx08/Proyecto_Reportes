'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authApi } from '@/services/authApi';
import { Eye, EyeOff, AlertCircle, UserPlus } from 'lucide-react';
import type { RegisterRequest } from '@/types/auth';

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<RegisterRequest>({
    username: '',
    email: '',
    password: '',
    full_name: ''
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validar que las contraseñas coincidan
    if (formData.password !== confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    // Validar longitud mínima de contraseña
    if (formData.password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    setIsLoading(true);

    try {
      const response = await authApi.register(formData);
      
      // Guardar token y usuario
      localStorage.setItem('auth_token', response.token.access_token);
      localStorage.setItem('auth_user', JSON.stringify(response.user));
      
      // Redirigir al home
      router.push('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al registrar usuario. Por favor, intenta nuevamente.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#042a53] via-[#063d75] to-[#0a4d8c] flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo/Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-white rounded-full mb-4 shadow-lg">
            <UserPlus className="w-10 h-10 text-[#042a53]" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Crear Cuenta</h1>
          <p className="text-[#ccdde8]">Sistema de Reportes - EPN</p>
        </div>

        {/* Formulario de registro */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Mensaje de error */}
            {error && (
              <div className="flex items-center space-x-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <span className="text-sm">{error}</span>
              </div>
            )}

            {/* Nombre de usuario */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-neutral-700 mb-2">
                Nombre de Usuario
              </label>
              <input
                id="username"
                type="text"
                required
                minLength={3}
                maxLength={50}
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
                placeholder="Ej: johndoe"
                disabled={isLoading}
              />
            </div>

            {/* Correo electrónico */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-neutral-700 mb-2">
                Correo Electrónico
              </label>
              <input
                id="email"
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
                placeholder="correo@example.com"
                disabled={isLoading}
              />
            </div>

            {/* Nombre completo */}
            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-neutral-700 mb-2">
                Nombre Completo (Opcional)
              </label>
              <input
                id="full_name"
                type="text"
                maxLength={255}
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
                placeholder="Ej: Juan Pérez"
                disabled={isLoading}
              />
            </div>

            {/* Contraseña */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-neutral-700 mb-2">
                Contraseña
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  minLength={8}
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition pr-12"
                  placeholder="Mínimo 8 caracteres"
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600 transition"
                  disabled={isLoading}
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Confirmar contraseña */}
            <div>
              <label htmlFor="confirm_password" className="block text-sm font-medium text-neutral-700 mb-2">
                Confirmar Contraseña
              </label>
              <div className="relative">
                <input
                  id="confirm_password"
                  type={showConfirmPassword ? 'text' : 'password'}
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition pr-12"
                  placeholder="Repite tu contraseña"
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600 transition"
                  disabled={isLoading}
                >
                  {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Botón de registro */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-[#042a53] text-white py-3 px-4 rounded-lg hover:bg-[#021221] focus:ring-4 focus:ring-[#ccdde8] disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Creando cuenta...</span>
                </div>
              ) : (
                'Crear Cuenta'
              )}
            </button>
          </form>

          {/* Link a login */}
          <div className="mt-6 text-center">
            <p className="text-sm text-neutral-600">
              ¿Ya tienes una cuenta?{' '}
              <Link
                href="/login"
                className="text-[#042a53] font-medium hover:underline"
              >
                Inicia sesión
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
