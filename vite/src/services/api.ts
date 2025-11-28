const API_BASE_URL = 'http://localhost:5000';

// Helper function for API calls
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    credentials: 'include', // Important for session cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(error.message || error.error || 'Request failed');
  }

  return response.json();
}

// Authentication APIs
export const authAPI = {
  register: async (data: {
    username: string;
    email: string;
    password: string;
    user_type: 'farmer' | 'transporter' | 'user';
  }) => {
    return apiCall<{ message: string; user: any; access_token: string }>(
      '/api/register',
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  },

  login: async (data: {
    username: string;
    password: string;
    user_type?: string;
  }) => {
    return apiCall<{ message: string; user: any; access_token: string }>(
      '/api/login',
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  },

  logout: async () => {
    return apiCall<{ message: string }>('/api/logout', {
      method: 'POST',
    });
  },

  getProfile: async () => {
    return apiCall<{ user: any }>('/api/profile');
  },

  getSession: async () => {
    return apiCall<{
      logged_in: boolean;
      user_id?: number;
      username?: string;
      user_type?: string;
    }>('/api/session');
  },
};

// Farmer Application APIs
export const farmerAPI = {
  apply: async (data: {
    username: string;
    email: string;
    password: string;
    farm_name: string;
    location: string;
    phone?: string;
    description?: string;
  }) => {
    return apiCall<{ success: boolean; message: string; application: any }>(
      '/api/farmers/apply',
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  },

  getApplications: async (status?: string) => {
    const url = status
      ? `/api/admin/farmers/applications?status=${status}`
      : '/api/admin/farmers/applications';
    return apiCall<{ success: boolean; count: number; applications: any[] }>(
      url
    );
  },

  approveApplication: async (applicationId: number) => {
    return apiCall<{
      success: boolean;
      message: string;
      application: any;
      user?: any;
    }>(`/api/admin/farmers/applications/${applicationId}/approve`, {
      method: 'POST',
    });
  },

  denyApplication: async (applicationId: number, reason?: string) => {
    return apiCall<{ success: boolean; message: string; application: any }>(
      `/api/admin/farmers/applications/${applicationId}/deny`,
      {
        method: 'POST',
        body: JSON.stringify({ reason }),
      }
    );
  },

  getStats: async () => {
    return apiCall<{
      success: boolean;
      stats: {
        total: number;
        pending: number;
        approved: number;
        denied: number;
      };
    }>('/api/admin/farmers/applications/stats');
  },
};

// Product APIs
export const productAPI = {
  create: async (formData: FormData) => {
    const response = await fetch(`${API_BASE_URL}/api/products`, {
      method: 'POST',
      credentials: 'include',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(error.message || error.error || 'Request failed');
    }

    return response.json();
  },

  search: async (query: string) => {
    return apiCall<{
      success: boolean;
      query: string;
      count: number;
      products: any[];
    }>(`/api/products/search?q=${encodeURIComponent(query)}`);
  },
};

// Seller APIs
export const sellerAPI = {
  getAll: async (status?: string) => {
    const url = status
      ? `/api/admin/sellers?status=${status}`
      : '/api/admin/sellers';
    return apiCall<{ success: boolean; count: number; sellers: any[] }>(url);
  },

  create: async (data: {
    name: string;
    email: string;
    business_type: string;
    phone?: string;
    location?: string;
    description?: string;
  }) => {
    return apiCall<{ success: boolean; message: string; seller: any }>(
      '/api/admin/sellers',
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  },
};

