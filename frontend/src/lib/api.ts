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

// Auth API
export const authApi = {
  register: async (data: { email: string; password: string; full_name: string }) => {
    try {
      const response = await api.post('/users/', data);
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
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const response = await axios.post(`${BASE_URL}/auth/token`, params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
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

// Prompts API
export const promptsApi = {
  getPrompts: async () => {
    try {
      const response = await api.get('/prompts');
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

  getPrompt: async (id: number) => {
    try {
      const response = await api.get(`/prompts/${id}`);
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

  createPrompt: async (data: {
    name: string;
    description?: string;
    prompt_text: string;
    system_prompt?: string;
    is_public?: boolean;
    refresh_interval?: number;
    max_articles?: number;
    custom_categories?: Record<string, any>;
    source_preferences?: Record<string, any>;
    llm_provider?: string;
    llm_config?: Record<string, any>;
  }) => {
    try {
      const response = await api.post('/prompts', data);
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

  updatePrompt: async (id: number, data: Partial<{
    name: string;
    description: string;
    prompt_text: string;
    system_prompt: string;
    is_public: boolean;
    refresh_interval: number;
    max_articles: number;
    custom_categories: Record<string, any>;
    source_preferences: Record<string, any>;
    llm_provider: string;
    llm_config: Record<string, any>;
  }>) => {
    try {
      const response = await api.put(`/prompts/${id}`, data);
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

  deletePrompt: async (id: number) => {
    try {
      const response = await api.delete(`/prompts/${id}`);
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
};

// News API
export const newsApi = {
  getPromptNews: async ({ promptId, skip = 0, limit = 10 }: {
    promptId: number;
    skip?: number;
    limit?: number;
  }) => {
    try {
      const response = await api.get(`/news/prompt/${promptId}?skip=${skip}&limit=${limit}`);
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

  getPromptCategories: async (promptId: number) => {
    try {
      const response = await api.get(`/news/prompt/${promptId}/categories`);
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

  getPromptNewsByCategory: async ({ 
    promptId, 
    category, 
    skip = 0, 
    limit = 10 
  }: {
    promptId: number;
    category: string;
    skip?: number;
    limit?: number;
  }) => {
    try {
      const response = await api.get(
        `/news/prompt/${promptId}/category/${category}?skip=${skip}&limit=${limit}`
      );
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

  refreshPromptNews: async (promptId: number) => {
    try {
      const response = await api.post(`/news/prompt/${promptId}/refresh`);
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
};

export default api;