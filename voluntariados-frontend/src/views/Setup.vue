<!-- Setup.vue -->
<template>
  <div class="auth-page d-flex flex-column justify-content-center align-items-center">
    <div class="container py-4">
      <div class="row justify-content-center">
        <div class="col-lg-7 col-md-9">
          <div class="card auth-card auth-compact border-0 shadow-lg">
            <div class="card-header bg-transparent text-center pb-3 position-relative">
              <button 
                class="btn btn-primary btn-sm position-absolute top-0 end-0 m-3"
                @click="logout"
              >Cerrar Sesión</button>
              <div class="text-center mt-2 mb-2">
                <i class="bi bi-heart-fill text-danger" style="font-size: 2.5rem; color: var(--brand-accent);"></i>

              </div>
              <h2 class="mb-0 auth-heading">Completa tu Perfil</h2>
            </div>
            <div class="card-body px-5 py-4 bg-white">
              <PersonaSetup 
                v-if="user"
                :user-role="user.role"
                :user-email="user.email"
                @setup-complete="onSetupComplete"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import PersonaSetup from '@/components/PersonaSetup.vue'
import { userAPI } from '@/services/api'
import AuthService from '@/services/authService'

export default defineComponent({
  name: 'Setup',
  components: {
    PersonaSetup
  },
  data() {
    return {
      user: null as any
    }
  },
  async mounted() {
    try {
      const response = await userAPI.getCurrentUser()
      this.user = response.data
      
      // If user is already settled up, redirect to dashboard
      if (this.user.settled_up) {
        this.$router.push('/dashboard')
      }
    } catch (error) {
      console.error('Error loading user:', error)
      this.$router.push('/signin')
    }
  },
  methods: {
    async onSetupComplete() {
      // Force refresh user data after persona setup
      try {
        const user = await AuthService.refreshCurrentUser()
        this.user = user
      } catch (error) {
        this.$router.push('/')
        return
      }

      // Redirect based on user role after successful setup
      if (this.user.role === 'VOL') {
        this.$router.push('/')
      } else if (this.user.role === 'DELEG') {
        this.$router.push('/')
      } else {
        this.$router.push('/admin/dashboard')
      }
    },
    
    logout() {
      localStorage.removeItem('auth_token')
      this.$router.push('/signin')
    }
  }
})
</script>

<style scoped>
/* No local overrides; relies on shared auth.css */
</style>