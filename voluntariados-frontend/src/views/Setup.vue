<!-- Setup.vue -->
<template>
  <div class="min-vh-100 bg-light">
    <nav class="navbar navbar-light bg-white shadow-sm">
      <div class="container">
        <span class="navbar-brand mb-0 h1">Sistema de Voluntariado</span>
        <button 
          class="btn btn-outline-secondary btn-sm"
          @click="logout"
        >
          Cerrar Sesión
        </button>
      </div>
    </nav>

    <PersonaSetup 
      v-if="user"
      :user-role="user.role"
      :user-email="user.email"
      @setup-complete="onSetupComplete"
    />
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
        this.$router.push('/delegado/dashboard')
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