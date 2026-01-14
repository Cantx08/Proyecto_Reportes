/**
 * Tipos para el sistema de autenticación
 */

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
  role: 'admin' | 'user';
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
  role?: 'admin' | 'user';
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthResponse {
  user: User;
  token: TokenResponse;
}

export interface UserUpdateRequest {
  username?: string;
  email?: string;
  full_name?: string;
  is_active?: boolean;
  role?: 'admin' | 'user';
}

export interface PasswordChangeRequest {
  current_password: string;
  new_password: string;
}
