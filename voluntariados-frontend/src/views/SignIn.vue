<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/SignIn.vue -->
<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
          <div class="card auth-card border-0 shadow-lg">
            <div class="card-header bg-transparent text-center pb-5">

              <div class="text-center mt-4 mb-3">
                <i class="bi bi-heart-fill text-danger" style="font-size: 3rem;"></i>
              </div>
              <h2 class="mb-1 auth-heading">¡Bienvenido!</h2>
              <small class="text-muted auth-subtitle">Inicia sesión para continuar en</small>
              <br/>
              <small class="text-muted">{{ landingConfig.site_name }}</small>

            </div>
            <div class="card-body px-lg-5 py-lg-5">
              <!-- Error Alert -->
              <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
                <button type="button" class="btn-close" @click="error = null"></button>
              </div>

              <!-- Success Alert -->
              <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                {{ successMessage }}
                <button type="button" class="btn-close" @click="successMessage = null"></button>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="form-group mb-3">
                  <label class="form-label">Email</label>
                  <div class="input-group input-group-merge">
                    <span class="input-group-text">
                      <i class="bi bi-envelope"></i>
                    </span>
                    <input 
                      type="email" 
                      class="form-control" 
                      placeholder="nombre@ejemplo.com"
                      v-model="formData.email"
                      required
                      :disabled="loading"
                    >
                  </div>
                </div>
                <div class="form-group mb-3">
                  <label class="form-label">Contraseña</label>
                  <div class="input-group input-group-merge">
                    <span class="input-group-text">
                      <i class="bi bi-lock"></i>
                    </span>
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      class="form-control" 
                      placeholder="Contraseña"
                      v-model="formData.password"
                      required
                      :disabled="loading"
                    >
                    <button 
                      class="btn btn-outline-secondary" 
                      type="button"
                      @click="showPassword = !showPassword"
                      :disabled="loading"
                    >
                      <i class="bi" :class="showPassword ? 'bi-eye-slash' : 'bi-eye'"></i>
                    </button>
                  </div>
                </div>
                <div class="form-check mb-3">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    id="rememberMe"
                    v-model="rememberMe"
                    :disabled="loading"
                  >
                  <label class="form-check-label" for="rememberMe">
                    Recordarme
                  </label>
                </div>
                <div class="text-center">
                  <button 
                    type="submit" 
                    class="btn btn-primary w-100"
                    :disabled="loading"
                  >
                    <span v-if="loading">
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                      Iniciando sesión...
                    </span>
                    <span v-else>
                      <i class="bi bi-box-arrow-in-right me-2"></i>
                      Iniciar sesión
                    </span>
                  </button>
                </div>
              </form>
            </div>
            <div class="card-footer bg-transparent">
              <div class="text-center">
                <small class="text-muted">
                  No tienes una cuenta?
                  <router-link to="/signup" class="text-primary fw-bold">Regístrate</router-link>
                </small>
              </div>
              <div class="text-center mt-2">
                <small>
                  <a href="#" class="text-muted">¿Olvidaste tu contraseña?</a>
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AuthService from '@/services/authService'
import { useLandingConfig } from '@/composables/useLandingConfig'

export default defineComponent({
  name: 'SignIn',
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig()
    return {
      landingConfig,
      fetchLandingConfig
    }
  },
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      rememberMe: false,
      showPassword: false,
      loading: false,
      error: null as string | null,
      successMessage: null as string | null
    }
  },
  mounted() {
    // Check if user is already logged in
    if (AuthService.isAuthenticated()) {
      this.$router.push('/admin/dashboard')
    }

    // Check for success message from registration
    const registered = this.$route.query.registered
    if (registered === 'true') {
      this.successMessage = 'Registration successful! Please sign in.'
    }

    // Fetch landing config for site name
    this.fetchLandingConfig()
  },
  methods: {
    async handleLogin() {
      this.error = null
      this.loading = true

      try {
        const { user } = await AuthService.login(this.formData)
        this.loading = false

        // Check if user needs to complete setup
        if (!user.settled_up) {
          this.$router.push('/setup')
          return
        }

        // Redirect based on user role
        if (user.role === 'ADMIN' || user.is_staff) {
          this.$router.push('/admin/dashboard')
        } else if (user.role === 'DELEG') {
          this.$router.push('/delegado/dashboard')
        } else {
          this.$router.push('/') // Volunteer dashboard or home
        }
      } catch (err: any) {
        // Set error BEFORE setting loading to false
        this.error = err.response?.data?.detail || err.message || 'Invalid email or password'
        this.loading = false
        // DO NOT clear the form - user can see what they tried and correct it
      }
    }
  }
})
</script>

<style scoped>
/* No local overrides; styles centralized in auth.css */
</style>