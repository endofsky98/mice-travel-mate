const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://3.36.108.114:8007';

function getLanguage(): string {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('language') || 'en';
  }
  return 'en';
}

function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
}

interface RequestOptions {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
  params?: Record<string, string | number | boolean | undefined>;
  noAuth?: boolean;
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, headers = {}, params = {}, noAuth = false } = options;

  const lang = getLanguage();
  const queryParams = new URLSearchParams();
  queryParams.set('lang', lang);

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      queryParams.set(key, String(value));
    }
  });

  const url = `${API_URL}${endpoint}?${queryParams.toString()}`;

  const requestHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    ...headers,
  };

  if (!noAuth) {
    const token = getToken();
    if (token) {
      requestHeaders['Authorization'] = `Bearer ${token}`;
    }
  }

  try {
    const response = await fetch(url, {
      method,
      headers: requestHeaders,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (response.status === 401) {
      const errorData = await response.json().catch(() => ({}));
      if (typeof window !== 'undefined') {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          try {
            const refreshResponse = await fetch(`${API_URL}/api/v1/auth/refresh`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ refresh_token: refreshToken }),
            });
            if (refreshResponse.ok) {
              const tokens = await refreshResponse.json();
              localStorage.setItem('access_token', tokens.access_token);
              localStorage.setItem('refresh_token', tokens.refresh_token);
              requestHeaders['Authorization'] = `Bearer ${tokens.access_token}`;
              const retryResponse = await fetch(url, {
                method,
                headers: requestHeaders,
                body: body ? JSON.stringify(body) : undefined,
              });
              if (!retryResponse.ok) {
                throw new Error(`API Error: ${retryResponse.status}`);
              }
              return retryResponse.json();
            }
          } catch {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/auth/login';
          }
        }
      }
      throw new Error(errorData.detail || errorData.message || 'Unauthorized');
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.message || `API Error: ${response.status}`);
    }

    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error. Please check your connection.');
    }
    throw error;
  }
}

export const api = {
  get: <T>(endpoint: string, params?: Record<string, string | number | boolean | undefined>) =>
    request<T>(endpoint, { params }),

  post: <T>(endpoint: string, body?: unknown, params?: Record<string, string | number | boolean | undefined>) =>
    request<T>(endpoint, { method: 'POST', body, params }),

  put: <T>(endpoint: string, body?: unknown, params?: Record<string, string | number | boolean | undefined>) =>
    request<T>(endpoint, { method: 'PUT', body, params }),

  patch: <T>(endpoint: string, body?: unknown, params?: Record<string, string | number | boolean | undefined>) =>
    request<T>(endpoint, { method: 'PATCH', body, params }),

  delete: <T>(endpoint: string, params?: Record<string, string | number | boolean | undefined>) =>
    request<T>(endpoint, { method: 'DELETE', params }),
};

export default api;
