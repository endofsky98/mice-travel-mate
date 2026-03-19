import { AuthTokens, User } from '@/types';
import api from './api';

export function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

export function getRefreshToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('refresh_token');
}

export function setTokens(tokens: AuthTokens): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('access_token', tokens.access_token);
  localStorage.setItem('refresh_token', tokens.refresh_token);
}

export function clearTokens(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

export function isAuthenticated(): boolean {
  return !!getAccessToken();
}

export async function login(email: string, password: string): Promise<AuthTokens> {
  const tokens = await api.post<AuthTokens>('/api/auth/login', { email, password });
  setTokens(tokens);
  return tokens;
}

export async function register(data: {
  name: string;
  email: string;
  password: string;
  nationality?: string;
}): Promise<AuthTokens> {
  const tokens = await api.post<AuthTokens>('/api/auth/register', data);
  setTokens(tokens);
  return tokens;
}

export async function logout(): Promise<void> {
  try {
    await api.post('/api/auth/logout');
  } catch {
    // Ignore error on logout
  }
  clearTokens();
}

export async function getCurrentUser(): Promise<User | null> {
  try {
    const token = getAccessToken();
    if (!token) return null;
    return await api.get<User>('/api/auth/me');
  } catch {
    return null;
  }
}

export async function forgotPassword(email: string): Promise<void> {
  await api.post('/api/auth/forgot-password', { email });
}

export async function adminLogin(email: string, password: string): Promise<AuthTokens> {
  const tokens = await api.post<AuthTokens>('/api/auth/admin/login', { email, password });
  setTokens(tokens);
  return tokens;
}
