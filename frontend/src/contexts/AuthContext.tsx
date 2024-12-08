'use client'

import { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '@/lib/api';
import { useRouter } from 'next/navigation';

type User = {
  id: number;
  email: string;
  full_name: string;
};

type AuthContextType = {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; password: string; full_name: string }) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const userData = await authApi.me();
        setUser(userData);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      localStorage.removeItem('token');
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      setError(null);
      setIsLoading(true);
      
      const response = await authApi.login(email, password);
      
      if (response.access_token) {
        localStorage.setItem('token', response.access_token);
        await checkAuth();
        router.push('/news');
      }
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Login failed. Please try again.';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: { email: string; password: string; full_name: string }) => {
    try {
      setError(null);
      setIsLoading(true);
      
      // First register
      const registerResponse = await authApi.register(data);
      
      // Then login
      await login(data.email, data.password);
      
    } catch (err: any) {
      let message = 'Registration failed. Please try again.';
      if (err.response?.data?.detail) {
        message = err.response.data.detail;
      } else if (err.message) {
        message = err.message;
      }
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    router.push('/auth/login');
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}