'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { authApi } from '@/services/authApi';
import { Users, Trash2, Edit, Shield, User, Search, AlertCircle, CheckCircle, X } from 'lucide-react';
import type { User as UserType, UserUpdateRequest } from '@/types/auth';

export default function UsersManagementPage() {
  const { user: currentUser } = useAuth();
  const router = useRouter();
  const [users, setUsers] = useState<UserType[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<UserType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  
  // Modal de edición
  const [editingUser, setEditingUser] = useState<UserType | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Verificar que el usuario actual sea admin
  useEffect(() => {
    if (currentUser && currentUser.role !== 'admin') {
      router.push('/');
    }
  }, [currentUser, router]);

  // Cargar usuarios
  useEffect(() => {
    loadUsers();
  }, []);

  // Filtrar usuarios según el término de búsqueda
  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredUsers(users);
    } else {
      const term = searchTerm.toLowerCase();
      setFilteredUsers(
        users.filter(u =>
          u.username.toLowerCase().includes(term) ||
          u.email.toLowerCase().includes(term) ||
          (u.full_name && u.full_name.toLowerCase().includes(term))
        )
      );
    }
  }, [searchTerm, users]);

  const loadUsers = async () => {
    try {
      const response = await authApi.getAllUsers();
      setUsers(response.users);
      setFilteredUsers(response.users);
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Error al cargar usuarios'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (userId === currentUser?.id) {
      setMessage({
        type: 'error',
        text: 'No puedes eliminar tu propia cuenta'
      });
      return;
    }

    if (!confirm('¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.')) {
      return;
    }

    try {
      await authApi.deleteUser(userId);
      setMessage({
        type: 'success',
        text: 'Usuario eliminado correctamente'
      });
      await loadUsers();
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Error al eliminar usuario'
      });
    }
  };

  const openEditModal = (user: UserType) => {
    setEditingUser({ ...user });
    setIsModalOpen(true);
    setMessage(null);
  };

  const closeEditModal = () => {
    setEditingUser(null);
    setIsModalOpen(false);
    setMessage(null);
  };

  const handleSaveUser = async () => {
    if (!editingUser) return;

    setIsSaving(true);
    setMessage(null);

    try {
      const updateData: UserUpdateRequest = {
        role: editingUser.role,
        is_active: editingUser.is_active
      };

      await authApi.updateUser(editingUser.id, updateData);
      
      setMessage({
        type: 'success',
        text: 'Usuario actualizado correctamente'
      });
      
      await loadUsers();
      closeEditModal();
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Error al actualizar usuario'
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (!currentUser || currentUser.role !== 'admin') {
    return null;
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#042a53]"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-neutral-900 flex items-center space-x-2">
          <Users className="w-7 h-7" />
          <span>Gestión de Usuarios</span>
        </h1>
        <p className="text-neutral-600 mt-1">
          Administra los usuarios del sistema
        </p>
      </div>

      {/* Mensaje de éxito/error */}
      {message && (
        <div
          className={`flex items-center space-x-2 p-4 rounded-lg mb-6 ${
            message.type === 'success'
              ? 'bg-green-50 border border-green-200 text-green-700'
              : 'bg-red-50 border border-red-200 text-red-700'
          }`}
        >
          {message.type === 'success' ? (
            <CheckCircle className="w-5 h-5" />
          ) : (
            <AlertCircle className="w-5 h-5" />
          )}
          <span className="text-sm">{message.text}</span>
        </div>
      )}

      {/* Barra de búsqueda */}
      <div className="bg-white rounded-lg shadow-sm border border-neutral-200 p-4 mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400" />
          <input
            type="text"
            placeholder="Buscar por nombre de usuario, email o nombre completo..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
          />
        </div>
      </div>

      {/* Tabla de usuarios */}
      <div className="bg-white rounded-lg shadow-sm border border-neutral-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-neutral-50 border-b border-neutral-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Usuario
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Rol
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-neutral-200">
              {filteredUsers.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-neutral-500">
                    No se encontraron usuarios
                  </td>
                </tr>
              ) : (
                filteredUsers.map((user) => (
                  <tr key={user.id} className="hover:bg-neutral-50 transition">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 rounded-full bg-[#042a53] text-white flex items-center justify-center font-semibold text-sm">
                          {user.full_name
                            ? user.full_name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
                            : user.username.substring(0, 2).toUpperCase()
                          }
                        </div>
                        <div>
                          <div className="text-sm font-medium text-neutral-900">
                            {user.username}
                          </div>
                          {user.full_name && (
                            <div className="text-sm text-neutral-500">{user.full_name}</div>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-neutral-900">{user.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex items-center space-x-1 px-3 py-1 text-xs font-medium rounded-full ${
                          user.role === 'admin'
                            ? 'bg-purple-100 text-purple-700'
                            : 'bg-[#ccdde8] text-[#042a53]'
                        }`}
                      >
                        {user.role === 'admin' ? (
                          <Shield className="w-3 h-3" />
                        ) : (
                          <User className="w-3 h-3" />
                        )}
                        <span>{user.role === 'admin' ? 'Administrador' : 'Usuario'}</span>
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-3 py-1 text-xs font-medium rounded-full ${
                          user.is_active
                            ? 'bg-green-100 text-green-700'
                            : 'bg-red-100 text-red-700'
                        }`}
                      >
                        {user.is_active ? 'Activo' : 'Inactivo'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end space-x-2">
                        <button
                          onClick={() => openEditModal(user)}
                          className="text-[#042a53] hover:text-[#021221] p-2 rounded-lg hover:bg-[#ccdde8] transition"
                          title="Editar usuario"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        {user.id !== currentUser.id && (
                          <button
                            onClick={() => handleDeleteUser(user.id)}
                            className="text-red-600 hover:text-red-700 p-2 rounded-lg hover:bg-red-50 transition"
                            title="Eliminar usuario"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Footer con total */}
        <div className="bg-neutral-50 px-6 py-3 border-t border-neutral-200">
          <p className="text-sm text-neutral-600">
            Mostrando {filteredUsers.length} de {users.length} usuarios
          </p>
        </div>
      </div>

      {/* Modal de edición */}
      {isModalOpen && editingUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-neutral-900">Editar Usuario</h2>
              <button
                onClick={closeEditModal}
                className="text-neutral-400 hover:text-neutral-600 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4">
              {/* Información del usuario (solo lectura) */}
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Nombre de Usuario
                </label>
                <input
                  type="text"
                  value={editingUser.username}
                  disabled
                  className="w-full px-3 py-2 bg-neutral-100 border border-neutral-300 rounded-lg text-neutral-500 cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={editingUser.email}
                  disabled
                  className="w-full px-3 py-2 bg-neutral-100 border border-neutral-300 rounded-lg text-neutral-500 cursor-not-allowed"
                />
              </div>

              {/* Rol (editable) */}
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Rol
                </label>
                <select
                  value={editingUser.role}
                  onChange={(e) => setEditingUser({ ...editingUser, role: e.target.value as 'admin' | 'user' })}
                  className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-[#042a53] focus:border-transparent outline-none transition"
                  disabled={isSaving || editingUser.id === currentUser.id}
                >
                  <option value="user">Usuario</option>
                  <option value="admin">Administrador</option>
                </select>
                {editingUser.id === currentUser.id && (
                  <p className="mt-1 text-xs text-neutral-500">
                    No puedes cambiar tu propio rol
                  </p>
                )}
              </div>

              {/* Estado (editable) */}
              <div>
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={editingUser.is_active}
                    onChange={(e) => setEditingUser({ ...editingUser, is_active: e.target.checked })}
                    className="w-4 h-4 text-[#042a53] border-neutral-300 rounded focus:ring-[#042a53]"
                    disabled={isSaving || editingUser.id === currentUser.id}
                  />
                  <span className="text-sm font-medium text-neutral-700">Usuario activo</span>
                </label>
                {editingUser.id === currentUser.id && (
                  <p className="mt-1 text-xs text-neutral-500 ml-6">
                    No puedes desactivar tu propia cuenta
                  </p>
                )}
              </div>
            </div>

            {/* Botones */}
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={closeEditModal}
                disabled={isSaving}
                className="px-4 py-2 text-neutral-700 bg-neutral-100 rounded-lg hover:bg-neutral-200 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Cancelar
              </button>
              <button
                onClick={handleSaveUser}
                disabled={isSaving}
                className="px-4 py-2 bg-[#042a53] text-white rounded-lg hover:bg-[#021221] transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {isSaving ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Guardando...</span>
                  </>
                ) : (
                  <span>Guardar Cambios</span>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
