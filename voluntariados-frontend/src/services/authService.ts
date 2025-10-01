/* eslint-disable @typescript-eslint/no-explicit-any */
// src/services/authService.ts
import apiClient from './api'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  role?: 'VOL' | 'DELEG' | 'ADMIN'
}

export interface AuthTokens {
  access: string
  refresh: string
}

export interface User {
  id: number
  email: string
  role: 'VOL' | 'DELEG' | 'ADMIN'
  is_active: boolean
  is_staff: boolean
  persona: number | null
}

class AuthService {
  private readonly TOKEN_KEY = 'auth_token'
  private readonly REFRESH_TOKEN_KEY = 'refresh_token'
  private readonly USER_KEY = 'user_data'

  /**
   * Login user and store tokens
   */
  async login(credentials: LoginCredentials): Promise<{ user: User; tokens: AuthTokens }> {
    try {
      const response = await apiClient.post<AuthTokens>('/token/', credentials)
      const tokens = response.data

      // Store tokens
      this.setTokens(tokens.access, tokens.refresh)

      // Fetch user data
      const user = await this.getCurrentUser()

      return { user, tokens }
    } catch (error: any) {
      console.error('Login error:', error)
      throw new Error(error.response?.data?.detail || 'Login failed')
    }
  }

  /**
   * Register new user
   */
  async register(data: RegisterData): Promise<User> {
    try {
      // Create user account
      const response = await apiClient.post<User>('/users/', {
        ...data,
        role: data.role || 'VOL'
      })

      return response.data
    } catch (error: any) {
      console.error('Registration error:', error)
      const errorData = error.response?.data
      
      // Handle specific validation errors
      if (errorData?.email) {
        throw new Error(errorData.email[0] || 'Email validation failed')
      }
      if (errorData?.password) {
        throw new Error(errorData.password[0] || 'Password validation failed')
      }
      
      throw new Error(errorData?.detail || 'Registration failed')
    }
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User> {
    try {
      // First try to get from localStorage
      const cachedUser = this.getStoredUser()
      if (cachedUser) {
        return cachedUser
      }

      // If not in cache, fetch from API
      const response = await apiClient.get<User>('/users/me/')
      const user = response.data
      
      // Store user data
      this.setStoredUser(user)
      
      return user
    } catch (error: any) {
      console.error('Get current user error:', error)
      throw new Error(error.response?.data?.detail || 'Failed to get user data')
    }
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<string> {
    try {
      const refreshToken = this.getRefreshToken()
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }

      const response = await apiClient.post<{ access: string }>('/token/refresh/', {
        refresh: refreshToken
      })

      const newAccessToken = response.data.access
      this.setToken(newAccessToken)

      return newAccessToken
    } catch (error: any) {
      console.error('Token refresh error:', error)
      this.logout()
      throw new Error('Session expired. Please login again.')
    }
  }

  /**
   * Logout user and clear tokens
   */
  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY)
    localStorage.removeItem(this.REFRESH_TOKEN_KEY)
    localStorage.removeItem(this.USER_KEY)
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getToken()
  }

  /**
   * Get stored access token
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY)
  }

  /**
   * Get stored refresh token
   */
  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY)
  }

  /**
   * Set access token
   */
  private setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token)
  }

  /**
   * Set both access and refresh tokens
   */
  private setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.TOKEN_KEY, accessToken)
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken)
  }

  /**
   * Get stored user data
   */
  getStoredUser(): User | null {
    const userData = localStorage.getItem(this.USER_KEY)
    return userData ? JSON.parse(userData) : null
  }

  /**
   * Set stored user data
   */
  private setStoredUser(user: User): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user))
  }

  /**
   * Check if user has specific role
   */
  hasRole(role: 'VOL' | 'DELEG' | 'ADMIN'): boolean {
    const user = this.getStoredUser()
    return user?.role === role
  }

  /**
   * Check if user is admin
   */
  isAdmin(): boolean {
    const user = this.getStoredUser()
    return user?.is_staff || user?.role === 'ADMIN'
  }
}

export default new AuthService()