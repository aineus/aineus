import axios, { AxiosError } from 'axios';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authApi = {
  register: async (data: { email: string; password: string; full_name: string }) => {
    try {
      const response = await api.post('/users', data);
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.data?.detail) {
          throw new Error(error.response.data.detail);
        }
      }
      throw error;
    }
  },

  login: async (email: string, password: string) => {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/auth/token', formData, {
        headers: {
          'Accept': 'application/json',
        },
      });

      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.data?.detail) {
          throw new Error(error.response.data.detail);
        }
      }
      throw error;
    }
  },

  me: async () => {
    try {
      const response = await api.get('/users/me');
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.data?.detail) {
          throw new Error(error.response.data.detail);
        }
      }
      throw error;
    }
  }
};

export default api;