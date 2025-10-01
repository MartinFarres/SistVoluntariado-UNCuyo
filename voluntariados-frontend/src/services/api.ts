// src/services/api.ts
import axios, { type AxiosInstance, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'

// Create axios instance with base configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token if available
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('auth_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle common errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - clear token and redirect to login
      localStorage.removeItem('auth_token')
      window.location.href = '/signin'
    }
    return Promise.reject(error)
  }
)

// User API endpoints
export const userAPI = {
  // Get all users (admin only)
  getAllUsers: () => apiClient.get('/users/'),
  
  // Get specific user by id
  getUserById: (id: number) => apiClient.get(`/users/${id}/`),
  
  // Create new user
  createUser: (userData: {
    email: string
    password: string
    role: 'ADMIN' | 'DELEG' | 'VOL'
    persona?: number | null
  }) => apiClient.post('/users/', userData),
  
  // Update user
  updateUser: (id: number, userData: Partial<{
    email: string
    password: string
    role: 'ADMIN' | 'DELEG' | 'VOL'
    persona: number | null
    is_active: boolean
  }>) => apiClient.patch(`/users/${id}/`, userData),
  
  // Delete user
  deleteUser: (id: number) => apiClient.delete(`/users/${id}/`),
}

// Auth API endpoints
export const authAPI = {
  login: (credentials: { email: string; password: string }) =>
    apiClient.post('/auth/login/', credentials),
  
  logout: () => apiClient.post('/auth/logout/'),
  
  register: (userData: {
    email: string
    password: string
    role?: 'VOL'
  }) => apiClient.post('/auth/register/', userData),
  
  getCurrentUser: () => apiClient.get('/auth/me/'),
}

export default apiClient