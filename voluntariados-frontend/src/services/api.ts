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
    // List of public endpoints that don't require authentication
    const publicEndpoints = [
      '/token/',
      '/users/',
      '/voluntariado/voluntariados/',
      '/organizacion/',
      '/core/landing-config/public/'
    ]
    
    // Protected endpoints that should fail gracefully without redirect
    const protectedNoRedirect = [
      '/users/me/',
      '/persona/voluntario/',
      '/persona/delegado/',
      '/persona/administrativo/',
      '/facultad/carreras/',
      '/ubicacion/'
    ]
    
    const isPublicEndpoint = publicEndpoints.some(endpoint => 
      error.config?.url?.includes(endpoint)
    )
    
    const isProtectedNoRedirect = protectedNoRedirect.some(endpoint =>
      error.config?.url?.includes(endpoint)
    )
    
    // Only redirect on 401 if NOT a login attempt, public endpoint, or protected no-redirect endpoint
    if (error.response?.status === 401 && !isPublicEndpoint && !isProtectedNoRedirect) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
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

  // Setup persona for current user (after registration)
  setupPersona: (personaData: any) => apiClient.post('/users/setup_persona/', personaData),
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
  getAllValid: () => apiClient.get('/voluntariado/voluntariados/all-valid/'),
  getAllActive: () => apiClient.get('/voluntariado/voluntariados/?status=active'),
  // Use 'finished' for consistency with backend and other views
  getAllFinalized: () => apiClient.get('/voluntariado/voluntariados/?status=finished'),
  getAllUpcoming: () => apiClient.get('/voluntariado/voluntariados/?status=upcoming'),
  // Get voluntariados managed by current Gestionador (Delegado/Administrativo)
  getMineActive: () => apiClient.get('/voluntariado/voluntariados/mis-voluntariados/?status=active'),
  getMineUpcoming: () => apiClient.get('/voluntariado/voluntariados/mis-voluntariados/?status=upcoming'),
  getMineFinished: () => apiClient.get('/voluntariado/voluntariados/mis-voluntariados/?status=finished'),
  getMineAll: () => apiClient.get('/voluntariado/voluntariados/mis-voluntariados/'),

  // Get specific voluntariado by id
  getById: (id: number) => apiClient.get(`/voluntariado/voluntariados/${id}/`),

  // Create new voluntariado
  create: (data: {
    nombre: string
    descripcion_id?: number | null
    fecha_inicio?: string | null
    fecha_fin?: string | null
    gestionadores_id?: number | null
    estado: 'DRAFT' | 'ACTIVE' | 'CLOSED'
  }) => apiClient.post('/voluntariado/voluntariados/', data),

  // Update voluntariado
  update: (id: number, data: Partial<{
    nombre: string
    descripcion_id: number | null
    fecha_inicio: string | null
    fecha_fin: string | null
    gestionadores_id: number | null
    estado: 'DRAFT' | 'ACTIVE' | 'CLOSED'
  }>) => apiClient.patch(`/voluntariado/voluntariados/${id}/`, data),

  // Delete voluntariado
  delete: (id: number) => apiClient.delete(`/voluntariado/voluntariados/${id}/`),

  getTurnos: (id: number) => apiClient.get(`/voluntariado/voluntariados/${id}/turnos/`),
  getProgress: (id: number) => apiClient.get(`/voluntariado/voluntariados/${id}/progreso/`),
  getAsistenciaCompleta: (id: number) => apiClient.get(`/voluntariado/voluntariados/${id}/asistencia-completa/`),
  
  // Get inscripciones by turno
  getInscripcionesByTurno: (turnoId: number) => apiClient.get(`/voluntariado/inscripciones/?turno=${turnoId}`)
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
    voluntariado_id: number
  }) => apiClient.post('/voluntariado/turnos/', data),

  update: (id: number, data: Partial<{
    fecha: string
    hora_inicio: string
    hora_fin: string
    cupo: number
    lugar: string
  }>) => apiClient.patch(`/voluntariado/turnos/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/voluntariado/turnos/${id}/`),
  inscribirse: (id: number) => apiClient.post(`/voluntariado/turnos/${id}/inscribirse/`),
  cancelarInscripcion: (id: number) => apiClient.post(`/voluntariado/turnos/${id}/cancelar-inscripcion/`),
  getInscripciones: () => apiClient.get('/voluntariado/inscripciones/')
}

// Inscripcion API endpoints
export const inscripcionAPI = {
  getAll: () => apiClient.get('/voluntariado/inscripciones/')
}

// Asistencia API endpoints
export const asistenciaAPI = {
  getAll: () => apiClient.get('/asistencia/'),
  getById: (id: number) => apiClient.get(`/asistencia/${id}/`),
  getByTurno: (turnoId: number) => apiClient.get(`/asistencia/?turno=${turnoId}`),
  create: (data: {
    inscripcion: number
    presente: boolean
    horas: number | null
    observaciones: string | null
  }) => apiClient.post('/asistencia/', data),
  update: (id: number, data: {
    inscripcion: number
    presente: boolean
    horas: number | null
    observaciones: string | null
  }) => apiClient.patch(`/asistencia/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/asistencia/${id}/`)
}

// Persona API endpoints
export const personaAPI = {
  // Personas
  getAll: () => apiClient.get('/persona/personas/'),
  getById: (id: number) => apiClient.get(`/persona/personas/${id}/`),
  create: (data: any) => apiClient.post('/persona/personas/', data),
  update: (id: number, data: any) => apiClient.patch(`/persona/personas/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/persona/personas/${id}/`),

  // Voluntarios
  getVoluntarios: () => apiClient.get('/persona/voluntarios/'),
  getVoluntariosCount: () => apiClient.get('/persona/voluntarios/count/'),
  getVoluntarioById: (id: number) => apiClient.get(`/persona/voluntarios/${id}/`),
  createVoluntario: (data: any) => apiClient.post('/persona/voluntarios/', data),
  updateVoluntario: (id: number, data: any) => apiClient.patch(`/persona/voluntarios/${id}/`, data),
  deleteVoluntario: (id: number) => apiClient.delete(`/persona/voluntarios/${id}/`),
  getVoluntariadosVoluntario: (personaId: number) => apiClient.get(`/persona/voluntarios/${personaId}/voluntariados/`),


  // Gestionadores
  getGestionadores: () => apiClient.get('/persona/gestionadores/'),
  getGestionadorById: (id: number) => apiClient.get(`/persona/gestionadores/${id}/`),
  createGestionador: (data: any) => apiClient.post('/persona/gestionadores/', data),
  updateGestionador: (id: number, data: any) => apiClient.patch(`/persona/gestionadores/${id}/`, data),
  deleteGestionador: (id: number) => apiClient.delete(`/persona/gestionadores/${id}/`),

  // Administradores
  getAdministradores: () => apiClient.get('/persona/administrativos/'),
  getAdministradorById: (id: number) => apiClient.get(`/persona/administrativos/${id}/`),
  createAdministrador: (data: any) => apiClient.post('/persona/administrativos/', data),
  updateAdministrador: (id: number, data: any) => apiClient.patch(`/persona/administrativos/${id}/`, data),
  deleteAdministrador: (id: number) => apiClient.delete(`/persona/administrativos/${id}/`),

  // Delegados
  getDelegados: () => apiClient.get('/persona/delegados/'),
  getDelegadoById: (id: number) => apiClient.get(`/persona/delegados/${id}/`),
  createDelegado: (data: any) => apiClient.post('/persona/delegados/', data),
  updateDelegado: (id: number, data: any) => apiClient.patch(`/persona/delegados/${id}/`, data),
  deleteDelegado: (id: number) => apiClient.delete(`/persona/delegados/${id}/`),
}

// Organizacion API endpoints
export const organizacionAPI = {
  getAll: () => apiClient.get('/organizacion/'),
  getById: (id: number) => apiClient.get(`/organizacion/${id}/`),
  create: (data: any) => apiClient.post('/organizacion/', data),
  update: (id: number, data: any) => apiClient.patch(`/organizacion/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/organizacion/${id}/`),
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
  getPaises: () => apiClient.get('/ubicacion/pais/'),
  getPaisById: (id: number) => apiClient.get(`/ubicacion/pais/${id}/`),
  deletePais: (id: number) => apiClient.delete(`/ubicacion/pais/${id}/`),
  createPais: (data: any) => apiClient.post('/ubicacion/pais/', data),
  updatePais: (id: number, data: any) => apiClient.patch(`/ubicacion/pais/${id}/`, data),

  // Provincias
  getProvincias: () => apiClient.get('/ubicacion/provincia/'),
  createProvincia: (data: { nombre: string; pais_id: number }) => apiClient.post('/ubicacion/provincia/', data),
  updateProvincia: (id: number, data: { nombre: string; pais_id: number }) => apiClient.patch(`/ubicacion/provincia/${id}/`, data),
  deleteProvincia: (id: number) => apiClient.delete(`/ubicacion/provincia/${id}/`),

  // Departamentos
  getDepartamentos: () => apiClient.get('/ubicacion/departamento/'),
  createDepartamento: (data: { nombre: string; provincia_id: number }) => apiClient.post('/ubicacion/departamento/', data),
  updateDepartamento: (id: number, data: { nombre: string; provincia_id: number }) => apiClient.patch(`/ubicacion/departamento/${id}/`, data),
  deleteDepartamento: (id: number) => apiClient.delete(`/ubicacion/departamento/${id}/`),

  // Localidades
  getLocalidades: () => apiClient.get('/ubicacion/localidad/'),
  getLocalidadById: (id: number) => apiClient.get(`/ubicacion/localidad/${id}/`),
  createLocalidad: (data: { nombre: string; codigo_postal: string; departamento_id: number }) => apiClient.post('/ubicacion/localidad/', data),
  updateLocalidad: (id: number, data: { nombre: string; codigo_postal: string; departamento_id: number }) => apiClient.patch(`/ubicacion/localidad/${id}/`, data),
  deleteLocalidad: (id: number) => apiClient.delete(`/ubicacion/localidad/${id}/`)
}

// Landing Config API endpoints
export const landingConfigAPI = {
  // Get public landing configuration (no auth required)
  getPublicConfig: () => apiClient.get('/core/landing-config/public/'),

  // Get full landing configuration (admin only)
  getConfig: () => apiClient.get('/core/landing-config/admin/'),

  // Update landing configuration (admin only)
  updateConfig: (data: {
    page_title?: string;
    site_name?: string;
    hero_image?: File | string;
    contact_email?: string;
    phone_number?: string;
    instagram_handle?: string;
    footer_text?: string;
    welcome_message?: string;
    description?: string;
  }) => {
    // If data contains a file, use FormData
    if (data.hero_image instanceof File) {
      const formData = new FormData();
      Object.entries(data).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          formData.append(key, value as string | Blob);
        }
      });
      return apiClient.patch('/core/landing-config/admin/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } else {
      // Regular JSON update
      return apiClient.patch('/core/landing-config/admin/', data);
    }
  }
}

// Descripcion API endpoints
export const descripcionAPI = {
  getAll: () => apiClient.get('/voluntariado/descripcion/'),
  getById: (id: number) => apiClient.get(`/voluntariado/descripcion/${id}/`),
  create: (data: {
    descripcion: string
    logo?: File | string
    portada?: File | string
    resumen: string
  }) => apiClient.post('/voluntariado/descripcion/', data),
  update: (id: number, data: Partial<{
    descripcion: string
    logo?: File | string
    portada?: File | string
    resumen: string
  }>) => apiClient.patch(`/voluntariado/descripcion/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/voluntariado/descripcion/${id}/`),
}

// Certificado API endpoints
export const certificadoAPI = {
  getAll: () => apiClient.get('/certificado/certificado/'),
  download: (id: number) => apiClient.get(`/certificado/certificado/${id}/download/`, { responseType: 'blob' })
}

export default apiClient
