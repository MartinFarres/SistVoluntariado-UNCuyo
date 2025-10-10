<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/SignUp.vue -->
<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-6 col-md-8">
          <div class="card border-0 shadow-lg">
            <div class="card-header bg-transparent text-center pb-5">
              <div class="text-center mt-4 mb-3">
                <i class="bi bi-heart-fill text-danger" style="font-size: 3rem;"></i>
              </div>
              <h2 class="mb-1">Create Account</h2>
              <small class="text-muted">Join Voluntariado UNCuyo today and make a difference</small>
            </div>
            <div class="card-body px-lg-5 py-lg-5">
              <!-- Error Alert -->
              <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
                <button type="button" class="btn-close" @click="error = null"></button>
              </div>

              <form @submit.prevent="handleRegister">
                <div class="form-group mb-3">
                  <label class="form-label">Email address</label>
                  <div class="input-group input-group-merge">
                    <span class="input-group-text">
                      <i class="bi bi-envelope"></i>
                    </span>
                    <input 
                      type="email" 
                      class="form-control" 
                      placeholder="name@example.com"
                      v-model="formData.email"
                      required
                      :disabled="loading"
                    >
                  </div>
                  <small class="text-muted">We'll never share your email with anyone else.</small>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label class="form-label">Password</label>
                      <div class="input-group input-group-merge">
                        <span class="input-group-text">
                          <i class="bi bi-lock"></i>
                        </span>
                        <input 
                          :type="showPassword ? 'text' : 'password'" 
                          class="form-control" 
                          placeholder="Password"
                          v-model="formData.password"
                          required
                          minlength="8"
                          :disabled="loading"
                          @input="validatePassword"
                        >
                      </div>
                      <small class="text-muted">Minimum 8 characters</small>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label class="form-label">Confirm Password</label>
                      <div class="input-group input-group-merge">
                        <span class="input-group-text">
                          <i class="bi bi-lock-fill"></i>
                        </span>
                        <input 
                          :type="showPassword ? 'text' : 'password'" 
                          class="form-control" 
                          placeholder="Confirm Password"
                          v-model="confirmPassword"
                          required
                          :disabled="loading"
                          @input="validatePassword"
                        >
                      </div>
                    </div>
                  </div>
                </div>

                <div class="form-check mb-3">
                  <input 
                    class="form-check-input" 
                    type="checkbox"
                    @click="showPassword = !showPassword"
                    :disabled="loading"
                  >
                  <label class="form-check-label">
                    Show password
                  </label>
                </div>

                <!-- Password strength indicator -->
                <div v-if="formData.password" class="mb-3">
                  <small class="text-muted">Password strength:</small>
                  <div class="progress" style="height: 5px;">
                    <div 
                      class="progress-bar" 
                      :class="passwordStrengthClass"
                      :style="{ width: passwordStrength + '%' }"
                    ></div>
                  </div>
                  <small :class="passwordStrengthTextClass">{{ passwordStrengthText }}</small>
                </div>

                <!-- Password match indicator -->
                <div v-if="confirmPassword" class="mb-3">
                  <small :class="passwordsMatch ? 'text-success' : 'text-danger'">
                    <i class="bi" :class="passwordsMatch ? 'bi-check-circle-fill' : 'bi-x-circle-fill'"></i>
                    {{ passwordsMatch ? 'Passwords match' : 'Passwords do not match' }}
                  </small>
                </div>

                <div class="form-group mb-3">
                  <label class="form-label">I want to register as:</label>
                  <select 
                    class="form-select" 
                    v-model="formData.role"
                    :disabled="loading"
                  >
                    <option value="VOL">Volunteer</option>
                    <option value="DELEG">Organization Delegate</option>
                  </select>
                  <small class="text-muted">
                    <i class="bi bi-info-circle"></i>
                    Delegates represent organizations. Choose Volunteer if you're unsure.
                  </small>
                </div>

                <div class="form-check mb-4">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    id="agreeTerms"
                    v-model="agreeToTerms"
                    required
                    :disabled="loading"
                  >
                  <label class="form-check-label" for="agreeTerms">
                    I agree to the 
                    <router-link to="/terms" target="_blank" class="text-primary">Terms and Conditions</router-link>
                    and 
                    <router-link to="/privacy" target="_blank" class="text-primary">Privacy Policy</router-link>
                  </label>
                </div>

                <div class="text-center">
                  <button 
                    type="submit" 
                    class="btn btn-primary w-100"
                    :disabled="loading || !passwordsMatch || !agreeToTerms"
                  >
                    <span v-if="loading">
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                      Creating account...
                    </span>
                    <span v-else>
                      <i class="bi bi-person-plus me-2"></i>
                      Create Account
                    </span>
                  </button>
                </div>
              </form>
            </div>
            <div class="card-footer bg-transparent">
              <div class="text-center">
                <small class="text-muted">
                  Already have an account? 
                  <router-link to="/signin" class="text-primary fw-bold">Sign In</router-link>
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

export default defineComponent({
  name: 'SignUp',
  data() {
    return {
      formData: {
        email: '',
        password: '',
        role: 'VOL' as 'VOL' | 'DELEG'
      },
      confirmPassword: '',
      showPassword: false,
      agreeToTerms: false,
      loading: false,
      error: null as string | null
    }
  },
  computed: {
    passwordsMatch(): boolean {
      if (!this.confirmPassword) return false
      return this.formData.password === this.confirmPassword
    },
    passwordStrength(): number {
      const password = this.formData.password
      if (!password) return 0
      
      let strength = 0
      
      // Length check
      if (password.length >= 8) strength += 25
      if (password.length >= 12) strength += 25
      
      // Character variety checks
      if (/[a-z]/.test(password)) strength += 12.5
      if (/[A-Z]/.test(password)) strength += 12.5
      if (/[0-9]/.test(password)) strength += 12.5
      if (/[^a-zA-Z0-9]/.test(password)) strength += 12.5
      
      return Math.min(strength, 100)
    },
    passwordStrengthText(): string {
      const strength = this.passwordStrength
      if (strength === 0) return ''
      if (strength < 40) return 'Weak'
      if (strength < 70) return 'Medium'
      return 'Strong'
    },
    passwordStrengthClass(): string {
      const strength = this.passwordStrength
      if (strength < 40) return 'bg-danger'
      if (strength < 70) return 'bg-warning'
      return 'bg-success'
    },
    passwordStrengthTextClass(): string {
      const strength = this.passwordStrength
      if (strength < 40) return 'text-danger'
      if (strength < 70) return 'text-warning'
      return 'text-success'
    }
  },
  mounted() {
    // Check if user is already logged in
    if (AuthService.isAuthenticated()) {
      this.$router.push('/admin/dashboard')
    }
  },
  methods: {
    validatePassword() {
      // This method is called on input to trigger computed properties
    },
    async handleRegister() {
      this.error = null

      // Validate passwords match
      if (!this.passwordsMatch) {
        this.error = 'Passwords do not match'
        return
      }

      // Validate terms agreement
      if (!this.agreeToTerms) {
        this.error = 'You must agree to the Terms and Conditions'
        return
      }

      this.loading = true

      try {
        // Register the user
        await AuthService.register(this.formData)

        // Redirect to login with success message
        this.$router.push({
          path: '/signin',
          query: { registered: 'true' }
        })
      } catch (err: any) {
        this.error = err.message || 'Registration failed. Please try again.'
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
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 0;
}

.card {
  border-radius: 1rem;
  overflow: hidden;
}

.card-header {
  padding: 2rem 0 0;
  background: linear-gradient(87deg, #5e72e4 0, #825ee4 100%);
  color: white;
}

.card-header h2 {
  color: white;
}

.input-group-text {
  background-color: #f7fafc;
  border-right: 0;
}

.form-control,
.form-select {
  border-left: 0;
}

.form-control:focus,
.form-select:focus {
  border-color: #5e72e4;
  box-shadow: none;
}

.input-group:focus-within .input-group-text {
  border-color: #5e72e4;
}

.btn-primary {
  background: linear-gradient(87deg, #5e72e4 0, #825ee4 100%);
  border: none;
  padding: 0.75rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.card-footer {
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
}

a {
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: #5e72e4 !important;
}

.alert {
  border-radius: 0.5rem;
  border: none;
}

.progress {
  border-radius: 10px;
  overflow: hidden;
}

.form-select {
  cursor: pointer;
}

.form-check-input:checked {
  background-color: #5e72e4;
  border-color: #5e72e4;
}
</style>