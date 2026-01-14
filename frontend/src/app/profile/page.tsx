'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { authApi } from '@/services/authApi';
import { User, Lock, Save, Eye, EyeOff, AlertCircle, CheckCircle } from 'lucide-react';
import type { UserUpdateRequest, PasswordChangeRequest } from '@/types/auth';

export default function ProfilePage() {
  const { user, refreshUser } = useAuth();
  const [activeTab, setActiveTab] = useState<'info' | 'password'>('info');
  
  // Estado para información del perfil
  const [profileData, setProfileData] = useState({
    username: '',
    email: '',
    full_name: ''
  });
  const [isUpdatingProfile, setIsUpdatingProfile] = useState(false);
  const [profileMessage, setProfileMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  // Estado para cambio de contraseña
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [passwordMessage, setPasswordMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  // Cargar datos del usuario al montar
  useEffect(() => {
    if (user) {
      setProfileData({
        username: user.username,
        email: user.email,
        full_name: user.full_name || ''
      });
    }
  }, [user]);

  // Manejar actualización del perfil
  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileMessage(null);
    setIsUpdatingProfile(true);

    try {
      const updateData: UserUpdateRequest = {
        username: profileData.username,
        email: profileData.email,
        full_name: profileData.full_name || undefined
      };

      await authApi.updateMe(updateData);
      await refreshUser();
      
      setProfileMessage({
        type: 'success',
        text: 'Perfil actualizado correctamente'
      });
    } catch (error: any) {
      setProfileMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Error al actualizar el perfil'
      });
    } finally {
      setIsUpdatingProfile(false);
    }
  };

  // Manejar cambio de contraseña
  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordMessage(null);

    // Validar que las contraseñas coincidan
    if (passwordData.new_password !== passwordData.confirm_password) {
      setPasswordMessage({
        type: 'error',
        text: 'Las contraseñas nuevas no coinciden'
      });
      return;
    }

    // Validar longitud mínima
    if (passwordData.new_password.length < 8) {
      setPasswordMessage({
        type: 'error',
        text: 'La contraseña debe tener al menos 8 caracteres'
      });
      return;
    }

    setIsChangingPassword(true);

    try {
      const changeData: PasswordChangeRequest = {
        current_password: passwordData.current_password,
        new_password: passwordData.new_password
      };

      await authApi.changePassword(changeData);
      
      // Limpiar el formulario
      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });

      setPasswordMessage({
        type: 'success',
        text: 'Contraseña actualizada correctamente'
      });
    } catch (error: any) {
      setPasswordMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Error al cambiar la contraseña'
      });
    } finally {
      setIsChangingPassword(false);
    }
  };

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#042a53]"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-neutral-900">Mi Perfil</h1>
        <p className="text-neutral-600 mt-1">
          Gestiona tu información personal y configuración de cuenta
        </p>
      </div>

      {/* Información del usuario */}
      <div className="bg-white rounded-lg shadow-sm border border-neutral-200 p-6 mb-6">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 rounded-full bg-[#042a53] text-white flex items-center justify-center font-semibold text-xl">
            {user.full_name 
              ? user.full_name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
              : user.username.substring(0, 2).toUpperCase()
            }
          </div>
          <div>
            <h2 className="text-xl font-semibold text-neutral-900">
              {user.full_name || user.username}
            </h2>
            <p className="text-sm text-neutral-600">{user.email}</p>
            <span className="inline-block mt-1 px-3 py-1 text-xs font-medium rounded-full bg-[#ccdde8] text-[#042a53]">
              {user.role === 'admin' ? 'Administrador' : 'Usuario'}
            </span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-neutral-200">
        <div className="border-b border-neutral-200">
          <nav className="flex space-x-8 px-6" aria-label="Tabs">
            <button
              onClick={() => setActiveTab('info')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'info'
                  ? 'border-[#042a53] text-[#042a53]'
                  : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <User className="w-4 h-4" />
                <span>Información Personal</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('password')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'password'
                  ? 'border-[#042a53] text-[#042a53]'
                  : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Lock className="w-4 h-4" />
                <span>Cambiar Contraseña</span>
              </div>
            </button>
          </nav>
        </div>

        <div className="p-6">
          {/* Tab: Información Personal */}
          {activeTab === 'info' && (
            <form onSubmit={handleProfileSubmit} className="space-y-6">
              {/* Mensaje de éxito/error */}
              {profileMessage && (
                <div
                  className={`flex items-center space-x-2 p-4 rounded-lg ${
                    profileMessage.type === 'success'
                      ? 'bg-green-50 border border-green-200 text-green-700'
                      : 'bg-red-50 border border-red-200 text-red-700'
                  }`}
                >
                  {profileMessage.type === 'success' ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : (
                    <AlertCircle className="w-5 h-5" />
                  )}
                  <span className="text-sm">{profileMessage.text}</span>
                </div>
              )}

              {/* Nombre de usuario (editable) */}
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
                  value={profileData.username}
                  onChange={(e) => setProfileData({ ...profileData, username: e.target.value })}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
                  disabled={isUpdatingProfile}
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
                  value={profileData.email}
                  onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
                  disabled={isUpdatingProfile}
                />
              </div>

              {/* Nombre completo */}
              <div>
                <label htmlFor="full_name" className="block text-sm font-medium text-neutral-700 mb-2">
                  Nombre Completo
                </label>
                <input
                  id="full_name"
                  type="text"
                  value={profileData.full_name}
                  onChange={(e) => setProfileData({ ...profileData, full_name: e.target.value })}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
                  placeholder="Ej: Juan Pérez"
                  disabled={isUpdatingProfile}
                />
              </div>

              {/* Botón guardar */}
              <div className="flex justify-end pt-4">
                <button
                  type="submit"
                  disabled={isUpdatingProfile}
                  className="flex items-center space-x-2 bg-[#042a53] text-white px-6 py-2.5 rounded-lg hover:bg-[#021221] focus:ring-4 focus:ring-[#ccdde8] disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  {isUpdatingProfile ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      <span>Guardando...</span>
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5" />
                      <span>Guardar Cambios</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          )}

          {/* Tab: Cambiar Contraseña */}
          {activeTab === 'password' && (
            <form onSubmit={handlePasswordSubmit} className="space-y-6">
              {/* Mensaje de éxito/error */}
              {passwordMessage && (
                <div
                  className={`flex items-center space-x-2 p-4 rounded-lg ${
                    passwordMessage.type === 'success'
                      ? 'bg-green-50 border border-green-200 text-green-700'
                      : 'bg-red-50 border border-red-200 text-red-700'
                  }`}
                >
                  {passwordMessage.type === 'success' ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : (
                    <AlertCircle className="w-5 h-5" />
                  )}
                  <span className="text-sm">{passwordMessage.text}</span>
                </div>
              )}

              {/* Contraseña actual */}
              <div>
                <label htmlFor="current_password" className="block text-sm font-medium text-neutral-700 mb-2">
                  Contraseña Actual
                </label>
                <div className="relative">
                  <input
                    id="current_password"
                    type={showPasswords.current ? 'text' : 'password'}
                    required
                    value={passwordData.current_password}
                    onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                    className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition pr-10"
                    placeholder="Ingresa tu contraseña actual"
                    disabled={isChangingPassword}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPasswords({ ...showPasswords, current: !showPasswords.current })}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
                    disabled={isChangingPassword}
                  >
                    {showPasswords.current ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* Nueva contraseña */}
              <div>
                <label htmlFor="new_password" className="block text-sm font-medium text-neutral-700 mb-2">
                  Nueva Contraseña
                </label>
                <div className="relative">
                  <input
                    id="new_password"
                    type={showPasswords.new ? 'text' : 'password'}
                    required
                    value={passwordData.new_password}
                    onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                    className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition pr-10"
                    placeholder="Mínimo 8 caracteres"
                    disabled={isChangingPassword}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPasswords({ ...showPasswords, new: !showPasswords.new })}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
                    disabled={isChangingPassword}
                  >
                    {showPasswords.new ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                <p className="mt-1 text-xs text-neutral-500">
                  La contraseña debe tener al menos 8 caracteres
                </p>
              </div>

              {/* Confirmar nueva contraseña */}
              <div>
                <label htmlFor="confirm_password" className="block text-sm font-medium text-neutral-700 mb-2">
                  Confirmar Nueva Contraseña
                </label>
                <div className="relative">
                  <input
                    id="confirm_password"
                    type={showPasswords.confirm ? 'text' : 'password'}
                    required
                    value={passwordData.confirm_password}
                    onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                    className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition pr-10"
                    placeholder="Repite tu nueva contraseña"
                    disabled={isChangingPassword}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPasswords({ ...showPasswords, confirm: !showPasswords.confirm })}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
                    disabled={isChangingPassword}
                  >
                    {showPasswords.confirm ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* Botón guardar */}
              <div className="flex justify-end pt-4">
                <button
                  type="submit"
                  disabled={isChangingPassword}
                  className="flex items-center space-x-2 bg-[#042a53] text-white px-6 py-2.5 rounded-lg hover:bg-[#021221] focus:ring-4 focus:ring-[#ccdde8] disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  {isChangingPassword ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      <span>Cambiando...</span>
                    </>
                  ) : (
                    <>
                      <Lock className="w-5 h-5" />
                      <span>Cambiar Contraseña</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
