<!-- src/views/ResetPassword.vue -->
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
              <h2 class="mb-1 auth-heading">Restablecer Contraseña</h2>
              <small class="text-muted auth-subtitle">Ingresá tu nueva contraseña para</small>
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
                <div class="form-group mb-3">
                  <label class="form-label">Nueva Contraseña</label>
                  <div class="input-group input-group-merge">
                    <span class="input-group-text">
                      <i class="bi bi-lock"></i>
                    </span>
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      class="form-control" 
                      placeholder="Mínimo 8 caracteres"
                      v-model="formData.newPassword"
                      @input="validatePassword"
                      required
                      minlength="8"
                      :disabled="loading"
                      :class="{ 'is-invalid': errors.newPassword }"
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
                  <div v-if="errors.newPassword" class="invalid-feedback d-block">
                    {{ errors.newPassword }}
                  </div>
                  <!-- Password strength indicator -->
                  <div v-if="formData.newPassword" class="mt-2">
                    <small class="text-muted">Seguridad de contraseña</small>
                    <div class="progress" style="height: 5px;">
                      <div 
                        class="progress-bar" 
                        :class="passwordStrengthClass"
                        :style="{ width: passwordStrength + '%' }"
                      ></div>
                    </div>
                    <small :class="passwordStrengthTextClass">{{ passwordStrengthText }}</small>
                  </div>
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">Confirmar Contraseña</label>
                  <div class="input-group input-group-merge">
                    <span class="input-group-text">
                      <i class="bi bi-lock"></i>
                    </span>
                    <input 
                      :type="showConfirmPassword ? 'text' : 'password'" 
                      class="form-control" 
                      placeholder="Repetí la contraseña"
                      v-model="formData.confirmPassword"
                      @input="validatePassword"
                      required
                      minlength="8"
                      :disabled="loading"
                      :class="{ 'is-invalid': errors.confirmPassword }"
                    >
                    <button 
                      class="btn btn-outline-secondary" 
                      type="button"
                      @click="showConfirmPassword = !showConfirmPassword"
                      :disabled="loading"
                    >
                      <i class="bi" :class="showConfirmPassword ? 'bi-eye-slash' : 'bi-eye'"></i>
                    </button>
                  </div>
                  <div v-if="errors.confirmPassword" class="invalid-feedback d-block">
                    {{ errors.confirmPassword }}
                  </div>
                  <!-- Password match indicator -->
                  <div v-if="formData.confirmPassword" class="mt-2">
                    <small :class="passwordsMatch ? 'text-success' : 'text-danger'">
                      <i class="bi" :class="passwordsMatch ? 'bi-check-circle-fill' : 'bi-x-circle-fill'"></i>
                      {{ passwordsMatch ? 'Las contraseñas coinciden' : 'Las contraseñas no coinciden' }}
                    </small>
                  </div>
                </div>

                <div class="text-center">
                  <button 
                    type="submit" 
                    class="btn btn-primary w-100"
                    :disabled="loading || !isFormValid"
                  >
                    <span v-if="loading">
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                      Guardando...
                    </span>
                    <span v-else>
                      <i class="bi bi-check-circle me-2"></i>
                      Restablecer Contraseña
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
  name: 'ResetPassword',
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig()
    return { landingConfig, fetchLandingConfig }
  },
  data() {
    return {
      formData: {
        newPassword: '',
        confirmPassword: ''
      },
      errors: {
        newPassword: '',
        confirmPassword: ''
      } as Record<string, string>,
      loading: false,
      successMessage: '',
      errorMessage: '',
      token: '',
      showPassword: false,
      showConfirmPassword: false
    }
  },
  computed: {
    isFormValid(): boolean {
      return (
        this.formData.newPassword.length >= 8 &&
        this.formData.confirmPassword.length >= 8 &&
        this.formData.newPassword === this.formData.confirmPassword
      )
    },
    passwordsMatch(): boolean {
      if (!this.formData.confirmPassword) return false
      return this.formData.newPassword === this.formData.confirmPassword
    },
    passwordStrength(): number {
      const password = this.formData.newPassword
      if (!password) return 0
      let strength = 0
      if (password.length >= 8) strength += 25
      if (password.length >= 12) strength += 25
      if (/[a-z]/.test(password)) strength += 12.5
      if (/[A-Z]/.test(password)) strength += 12.5
      if (/[0-9]/.test(password)) strength += 12.5
      if (/[^a-zA-Z0-9]/.test(password)) strength += 12.5
      return Math.min(strength, 100)
    },
    passwordStrengthText(): string {
      const s = this.passwordStrength
      if (s === 0) return ''
      if (s < 40) return 'Débil'
      if (s < 70) return 'Media'
      return 'Fuerte'
    },
    passwordStrengthClass(): string {
      const s = this.passwordStrength
      if (s < 40) return 'bg-danger'
      if (s < 70) return 'bg-warning'
      return 'bg-success'
    },
    passwordStrengthTextClass(): string {
      const s = this.passwordStrength
      if (s < 40) return 'text-danger'
      if (s < 70) return 'text-warning'
      return 'text-success'
    }
  },
  mounted() {
    // Get token from route params
    this.token = this.$route.params.token as string
    
    if (!this.token) {
      this.errorMessage = 'Token inválido o faltante'
    }
  },
  methods: {
    validatePassword() {
      // Intentionally empty: triggers computed updates via v-model
    },
    validateForm(): boolean {
      this.errors = {
        newPassword: '',
        confirmPassword: ''
      }
      let isValid = true

      // Validate new password
      if (!this.formData.newPassword) {
        this.errors.newPassword = 'La contraseña es requerida'
        isValid = false
      } else if (this.formData.newPassword.length < 8) {
        this.errors.newPassword = 'La contraseña debe tener al menos 8 caracteres'
        isValid = false
      }

      // Validate password confirmation
      if (!this.formData.confirmPassword) {
        this.errors.confirmPassword = 'Debe confirmar la contraseña'
        isValid = false
      } else if (this.formData.newPassword !== this.formData.confirmPassword) {
        this.errors.confirmPassword = 'Las contraseñas no coinciden'
        isValid = false
      }

      return isValid
    },

    async handleSubmit() {
      // Clear previous messages
      this.successMessage = ''
      this.errorMessage = ''

      // Validate form
      if (!this.validateForm()) {
        return
      }

      // Validate token exists
      if (!this.token) {
        this.errorMessage = 'Token inválido'
        return
      }

      this.loading = true

      try {
        await authService.confirmPasswordReset(
          this.token,
          this.formData.newPassword,
          this.formData.confirmPassword
        )

        this.successMessage = 'Contraseña restablecida exitosamente'
        
        // Clear form
        this.formData = {
          newPassword: '',
          confirmPassword: ''
        }

        // Redirect after success
        setTimeout(() => {
          this.$router.push({ name: 'SignIn' })
        }, 3000)
      } catch (error: any) {
        console.error('Reset password error:', error)
        this.errorMessage = error.message || 'Error al restablecer la contraseña'
      } finally {
        this.loading = false
      }
    }
  }
})
</script>

<style scoped>
.auth-page { min-height: 100vh; background-color: #f8f9fa; }
.input-group-text { background-color: #f8f9fa; }
</style>
