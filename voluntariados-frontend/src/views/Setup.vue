<!-- Setup.vue -->
<template>
  <div class="setup-bg min-vh-100 d-flex flex-column justify-content-center align-items-center">
    <div class="container py-4">
      <div class="row justify-content-center">
        <div class="col-lg-8 col-md-10">
          <div class="card shadow-lg rounded-4 border-0">
            <div class="card-header bg-gradient-primary text-white d-flex justify-content-between align-items-center rounded-top-4">
              <span class="h4 mb-0">Completa tu Perfil</span>
              <button 
                class="btn btn-outline-light btn-sm"
                @click="logout"
              >
                Cerrar Sesión
              </button>
            </div>
            <div class="card-body px-4 py-4">
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

<style scoped>
/* Setup background and theme colors from HomeView */
.setup-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #8B0000, #DC143C 80%);
  padding-top: 40px;
  padding-bottom: 40px;
}

.card {
  border-radius: 1.5rem;
  box-shadow: 0 4px 20px rgba(139, 0, 0, 0.15);
}

.card-header.bg-gradient-primary {
  background: linear-gradient(135deg, #8B0000, #DC143C);
  color: #fff;
  border-radius: 1.5rem 1.5rem 0 0;
  padding: 1.5rem 2rem;
}

.btn-outline-light {
  border-color: #fff;
  color: #fff;
}
.btn-outline-light:hover {
  background: #fff;
  color: #8B0000;
}

.card-body {
  background: #fff;
  border-radius: 0 0 1.5rem 1.5rem;
}

.container {
  max-width: 900px;
}
</style>