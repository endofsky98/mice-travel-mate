'use client';

import { useState, useEffect, useCallback } from 'react';
import { User } from '@/types';
import { isAuthenticated, getCurrentUser, logout as authLogout, login as authLogin, register as authRegister } from '@/lib/auth';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      if (isAuthenticated()) {
        const currentUser = await getCurrentUser();
        if (currentUser) {
          setUser(currentUser);
          setIsLoggedIn(true);
        }
      }
      setIsLoading(false);
    };
    init();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    await authLogin(email, password);
    const currentUser = await getCurrentUser();
    setUser(currentUser);
    setIsLoggedIn(true);
  }, []);

  const register = useCallback(async (data: { name: string; email: string; password: string; nationality?: string }) => {
    await authRegister(data);
    const currentUser = await getCurrentUser();
    setUser(currentUser);
    setIsLoggedIn(true);
  }, []);

  const logout = useCallback(async () => {
    await authLogout();
    setUser(null);
    setIsLoggedIn(false);
  }, []);

  const refreshUser = useCallback(async () => {
    const currentUser = await getCurrentUser();
    setUser(currentUser);
    setIsLoggedIn(!!currentUser);
  }, []);

  return { user, isLoggedIn, isLoading, login, register, logout, refreshUser };
}
