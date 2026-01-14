'use client';

import React, { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Eye, EyeOff, LogIn } from 'lucide-react';
import Image from 'next/image';
import Link from 'next/link';

export default function LoginPage() {
  const { login, isLoading } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await login(formData);
    } catch (err: any) {
      setError(err.message || 'Error al iniciar sesión');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#042a53]"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-white px-4">
      <div className="max-w-md w-full space-y-8">
        {/* Logo y título */}
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="flex items-center justify-center">
              <Image
                src="/logo_viiv.png"
                alt="Logo Dirección de Investigación"
                width={200}
                height={200}
                
              />
            </div>
          </div>
          <h1 className="mt-2 font-bold text-2xl text-[#042a53]">
            DIRECCIÓN DE INVESTIGACIÓN
          </h1>
          <h2 className="text-xl font-bold text-neutral-700">
            Sistema de Certificaciones
          </h2>
        </div>

        {/* Formulario */}
        <div className="bg-neutral-50 py-8 px-6 shadow-lg rounded-lg border border-neutral-200">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Error message */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            {/* Usuario */}
            <div>
              <label htmlFor="username" className="block text-lg font-medium text-neutral-700 mb-2">
                Usuario o Correo Electrónico
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
                placeholder="Ingresa tu usuario o email"
                disabled={isSubmitting}
              />
            </div>

            {/* Contraseña */}
            <div>
              <label htmlFor="password" className="block text-lg font-medium text-neutral-700 mb-2">
                Contraseña
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition pr-10"
                  placeholder="Ingresa tu contraseña"
                  disabled={isSubmitting}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
                  disabled={isSubmitting}
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>

            {/* Botón de inicio de sesión */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full flex items-center justify-center space-x-2 bg-[#042a53] text-white py-2.5 px-4 rounded-lg hover:bg-[#021221] focus:ring-4 focus:ring-[#ccdde8] disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {isSubmitting ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Iniciando sesión...</span>
                </>
              ) : (
                <>
                  <LogIn className="w-5 h-5" />
                  <span>Iniciar Sesión</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Link a registro */}
        <div className="mt-6 text-center">
          <p className="text-sm text-neutral-400">
            ¿No tienes una cuenta?{' '}
            <Link
              href="/register"
              className="font-medium text-neutral-600 hover:underline"
            >
              Regístrate aquí
            </Link>
          </p>
        </div>

        {/* Información adicional */}
        <p className="text-center text-xs text-neutral-500 mt-4">
          Si tienes problemas para acceder, contacta al administrador
        </p>
      </div>
    </div>
  );
}
