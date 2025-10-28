<!-- src/views/ForgotPassword.vue -->
<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
          <div class="card auth-card border-0 shadow-lg">
            <div class="card-header bg-transparent text-center pb-5">
              <div class="text-center mt-4 mb-3">
                <i class="bi bi-heart-fill" style="font-size: 3rem; color: var(--brand-accent);"></i>
              </div>
              <h2 class="mb-1 auth-heading">¿Olvidaste tu contraseña?</h2>
              <small class="text-muted auth-subtitle">Te enviaremos un enlace para restablecerla en</small>
              <br/>
              <small class="text-muted">{{ landingConfig.site_name }}</small>
            </div>

            <div class="card-body px-lg-5 py-lg-5">
              <!-- Error Alert -->
              <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ errorMessage }}
                <button type="button" class="btn-close" @click="errorMessage = ''"></button>
              </div>

              <!-- Success Alert -->
              <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                {{ successMessage }}
                <button type="button" class="btn-close" @click="successMessage = ''"></button>
              </div>

              <form v-if="!successMessage" @submit.prevent="handleSubmit">
                <div class="form-group mb-4">
                  <label class="form-label">Email</label>
                  <div class="input-group input-group-merge">
                    <span class="input-group-text">
                      <i class="bi bi-envelope"></i>
                    </span>
                    <input 
                      type="email" 
                      class="form-control" 
                      placeholder="nombre@ejemplo.com"
                      v-model="email"
                      required
                      :disabled="loading"
                      :class="{ 'is-invalid': emailError }"
                    >
                  </div>
                  <div v-if="emailError" class="invalid-feedback d-block">
                    {{ emailError }}
                  </div>
                </div>

                <div class="text-center">
                  <button 
                    type="submit" 
                    class="btn btn-primary w-100"
                    :disabled="loading || !email"
                  >
                    <span v-if="loading">
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                      Enviando enlace...
                    </span>
                    <span v-else>
                      <i class="bi bi-send me-2"></i>
                      Enviar enlace de recuperación
                    </span>
                  </button>
                </div>
              </form>
            </div>

            <div class="card-footer bg-transparent">
              <div class="text-center">
                <small>
                  <router-link to="/signin" class="text-primary fw-bold">Volver a iniciar sesión</router-link>
                </small>
              </div>
              <div class="text-center mt-2">
                <small class="text-muted">
                  ¿No tienes una cuenta?
                  <router-link to="/signup" class="text-primary fw-bold">Regístrate</router-link>
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
import authService from '@/services/authService'
import { useLandingConfig } from '@/composables/useLandingConfig'

export default defineComponent({
  name: 'ForgotPassword',
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig()
    return { landingConfig, fetchLandingConfig }
  },
  data() {
    return {
      email: '',
      emailError: '',
      loading: false,
      successMessage: '',
      errorMessage: ''
    }
  },
  methods: {
    validateEmail(): boolean {
      this.emailError = ''
      
      if (!this.email) {
        this.emailError = 'El email es requerido'
        return false
      }
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(this.email)) {
        this.emailError = 'Email inválido'
        return false
      }
      
      return true
    },

    async handleSubmit() {
      // Clear previous messages
      this.successMessage = ''
      this.errorMessage = ''

      // Validate email
      if (!this.validateEmail()) {
        return
      }

      this.loading = true

      try {
        await authService.requestPasswordReset(this.email)
        
        this.successMessage = 'Si el email existe en nuestro sistema, recibirás un correo con instrucciones para restablecer tu contraseña.'
        
        // Clear form
        this.email = ''
      } catch (error: any) {
        console.error('Password reset request error:', error)
        this.errorMessage = error.message || 'Error al solicitar restablecimiento de contraseña'
      } finally {
        this.loading = false
      }
    }
  }
})
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.input-group-text {
  background-color: #f8f9fa;
}
</style>
