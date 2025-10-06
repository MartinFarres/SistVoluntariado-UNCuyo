/* eslint-disable @typescript-eslint/no-explicit-any */
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
  
  // Get current user
  getCurrentUser: () => apiClient.get('/users/me/'),
  
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
    apiClient.post('/token/', credentials),
  
  logout: () => apiClient.post('/auth/logout/'),
  
  register: (userData: {
    email: string
    password: string
    role?: 'VOL'
  }) => apiClient.post('/users/', userData),
  
  refreshToken: (refreshToken: string) =>
    apiClient.post('/token/refresh/', { refresh: refreshToken }),
}

// Voluntariado API endpoints
export const voluntariadoAPI = {
  // Get all voluntariados
  getAll: () => apiClient.get('/voluntariado/voluntariados/'),
  
  // Get specific voluntariado by id
  getById: (id: number) => apiClient.get(`/voluntariado/voluntariados/${id}/`),
  
  // Create new voluntariado
  create: (data: {
    nombre: string
    turno?: number | null
    descripcion?: number | null
    fecha_inicio?: string | null
    fecha_fin?: string | null
    Gestionadores?: number | null
    estado: 'DRAFT' | 'ACTIVE' | 'CLOSED'
  }) => apiClient.post('/voluntariado/voluntariados/', data),
  
  // Update voluntariado
  update: (id: number, data: Partial<{
    nombre: string
    turno: number | null
    descripcion: number | null
    fecha_inicio: string | null
    fecha_fin: string | null
    Gestionadores: number | null
    estado: 'DRAFT' | 'ACTIVE' | 'CLOSED'
  }>) => apiClient.patch(`/voluntariado/voluntariados/${id}/`, data),
  
  // Delete voluntariado
  delete: (id: number) => apiClient.delete(`/voluntariado/voluntariados/${id}/`),
}

// Turno API endpoints
export const turnoAPI = {
  getAll: () => apiClient.get('/voluntariado/turnos/'),
  getById: (id: number) => apiClient.get(`/voluntariado/turnos/${id}/`),
  create: (data: {
    fecha: string
    hora_inicio: string
    hora_fin: string
    cupo: number
    lugar?: string
  }) => apiClient.post('/voluntariado/turnos/', data),
  update: (id: number, data: Partial<{
    fecha: string
    hora_inicio: string
    hora_fin: string
    cupo: number
    lugar: string
  }>) => apiClient.patch(`/voluntariado/turnos/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/voluntariado/turnos/${id}/`),
}

// Persona API endpoints
export const personaAPI = {
  // Personas
  getAll: () => apiClient.get('/persona/'),
  getById: (id: number) => apiClient.get(`/persona/${id}/`),
  create: (data: any) => apiClient.post('/persona/', data),
  update: (id: number, data: any) => apiClient.patch(`/persona/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/persona/${id}/`),
  
  // Voluntarios
  getVoluntarios: () => apiClient.get('/persona/voluntario/'),
  getVoluntarioById: (id: number) => apiClient.get(`/persona/voluntario/${id}/`),
  
  // Administrativos
  getAdministrativos: () => apiClient.get('/persona/administrativo/'),
  
  // Delegados
  getDelegados: () => apiClient.get('/persona/delegado/'),
}

// Organizacion API endpoints
export const organizacionAPI = {
  getAll: () => apiClient.get('/organizacion/organizaciones/'),
  getById: (id: number) => apiClient.get(`/organizacion/organizaciones/${id}/`),
  create: (data: any) => apiClient.post('/organizacion/organizaciones/', data),
  update: (id: number, data: any) => apiClient.patch(`/organizacion/organizaciones/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/organizacion/organizaciones/${id}/`),
}

// Facultad API endpoints
export const facultadAPI = {
  // Facultades
  getFacultades: () => apiClient.get('/facultad/facultades/'),
  getFacultadById: (id: number) => apiClient.get(`/facultad/facultades/${id}/`),
  createFacultad: (data: any) => apiClient.post('/facultad/facultades/', data),
  updateFacultad: (id: number, data: any) => apiClient.patch(`/facultad/facultades/${id}/`, data),
  deleteFacultad: (id: number) => apiClient.delete(`/facultad/facultades/${id}/`),
  
  // Carreras
  getCarreras: () => apiClient.get('/facultad/carreras/'),
  getCarreraById: (id: number) => apiClient.get(`/facultad/carreras/${id}/`),
  createCarrera: (data: any) => apiClient.post('/facultad/carreras/', data),
  updateCarrera: (id: number, data: any) => apiClient.patch(`/facultad/carreras/${id}/`, data),
  deleteCarrera: (id: number) => apiClient.delete(`/facultad/carreras/${id}/`),
}

// Ubicacion API endpoints
export const ubicacionAPI = {
  // Paises
  getPaises: () => apiClient.get('/ubicacion/pais'),
  getPaisById: (id: number) => apiClient.get(`/ubicacion/pais/${id}/`),
  
  // Provincias
  getProvincias: () => apiClient.get('/ubicacion/provincia'),
  getProvinciaById: (id: number) => apiClient.get(`/ubicacion/provincia/${id}/`),
  
  // Departamentos
  getDepartamentos: () => apiClient.get('/ubicacion/departamento'),
  getDepartamentoById: (id: number) => apiClient.get(`/ubicacion/departamento/${id}/`),
  
  // Localidades
  getLocalidades: () => apiClient.get('/ubicacion/localidad'),
  getLocalidadById: (id: number) => apiClient.get(`/ubicacion/localidad/${id}/`),
}

export default apiClient