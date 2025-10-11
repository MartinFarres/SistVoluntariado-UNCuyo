<!-- src/components/Navbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
    <div class="container-fluid px-4">
      <router-link to="/" class="navbar-brand fw-bold text-decoration-none">
        <i class="bi text-danger me-2"></i>
        {{ landingConfig.site_name }}
      </router-link>
      <button 
        class="navbar-toggler" 
        type="button" 
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" :class="{ show: mobileMenuOpen }" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          
          <!-- Admin Links -->
          <li v-if="isAuthenticated && isAdmin" class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link">
              <i class="bi bi-speedometer2 me-1"></i>
              Dashboard
            </router-link>
          </li>
          
          <li v-if="!isAuthenticated" class="nav-item">
            <router-link to="/about" class="nav-link">About</router-link>
          </li>
        </ul>
        
        <!-- Push content to the right -->
        <div class="ms-auto d-flex align-items-center">
          <!-- Auth Buttons -->
          <div v-if="!isAuthenticated" class="d-flex">
            <router-link to="/signin" class="btn btn-outline-primary me-2">
              <i class="bi bi-box-arrow-in-right me-1"></i>
              Sign In
            </router-link>
            <router-link to="/signup" class="btn btn-primary">
              <i class="bi bi-person-plus me-1"></i>
              Sign Up
            </router-link>
          </div>
          
          <!-- User Menu (when authenticated) - Manual Toggle -->
          <div v-else class="dropdown dropdown-menu-right" ref="dropdownContainer">
          <button 
            class="btn btn-light dropdown-toggle d-flex align-items-center" 
            type="button" 
            @click="dropdownOpen = !dropdownOpen"
          >
            <div class="avatar-sm bg-primary text-white rounded-circle me-2 d-flex align-items-center justify-content-center">
              <i class="bi bi-person"></i>
            </div>
            <span class="d-none d-md-inline">{{ userEmail }}</span>
          </button>
          <ul class="dropdown-menu" :class="{ show: dropdownOpen }">
            <li>
              <div class="dropdown-header">
                <div class="d-flex flex-column">
                  <span class="fw-bold">{{ userEmail }}</span>
                  <small class="text-muted">{{ userRoleDisplay }}</small>
                </div>
              </div>
            </li>
            <li><hr class="dropdown-divider"></li>
            <li>
              <router-link to="/profile" class="dropdown-item" @click="dropdownOpen = false">
                <i class="bi bi-person me-2"></i>
                My Profile
              </router-link>
            </li>
            <li v-if="isAdmin">
              <router-link to="/admin/dashboard" class="dropdown-item" @click="dropdownOpen = false">
                <i class="bi bi-speedometer2 me-2"></i>
                Admin Dashboard
              </router-link>
            </li>
            <li>
              <router-link to="/settings" class="dropdown-item" @click="dropdownOpen = false">
                <i class="bi bi-gear me-2"></i>
                Settings
              </router-link>
            </li>
            <li><hr class="dropdown-divider"></li>
            <li>
              <button @click="handleLogout" class="dropdown-item text-danger">
                <i class="bi bi-box-arrow-right me-2"></i>
                Sign Out
              </button>
            </li>
          </ul>
        </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import authService from '@/services/authService'
import { useLandingConfig } from '@/composables/useLandingConfig'

export default defineComponent({
  name: 'AppNavbar',
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig()
    return {
      landingConfig,
      fetchLandingConfig
    }
  },
  data() {
    return {
      isAuthenticated: false,
      isAdmin: false,
      userEmail: '',
      userRole: '',
      dropdownOpen: false,
      mobileMenuOpen: false
    }
  },
  computed: {
    userRoleDisplay(): string {
      const roles: Record<string, string> = {
        'ADMIN': 'Administrador',
        'DELEG': 'Delegado',
        'VOL': 'Voluntario'
      }
      return roles[this.userRole] || 'Usuario'
    }
  },
  mounted() {
    this.updateAuthStatus()
    this.fetchLandingConfig()
    
    // Listen for route changes to update auth status
    this.$router.afterEach(() => {
      this.updateAuthStatus()
      this.dropdownOpen = false
      this.mobileMenuOpen = false
    })

    // Close dropdown when clicking outside
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    updateAuthStatus() {
      this.isAuthenticated = authService.isAuthenticated()
      this.isAdmin = authService.isAdmin()
      
      if (this.isAuthenticated) {
        const user = authService.getStoredUser()
        if (user) {
          this.userEmail = user.email
          this.userRole = user.role
        }
      }
    },
    async handleLogout() {
      if (confirm('Are you sure you want to sign out?')) {
        authService.logout()
        this.dropdownOpen = false
        this.$router.push('/signin')
      }
    },
    handleClickOutside(event: MouseEvent) {
      const dropdown = this.$refs.dropdownContainer as HTMLElement
      if (dropdown && !dropdown.contains(event.target as Node)) {
        this.dropdownOpen = false
      }
    }
  }
})
</script>

<style scoped>
.navbar {
  transition: all 0.3s ease;
}

.avatar-sm {
  width: 32px;
  height: 32px;
  font-size: 0.875rem;
}

.dropdown-header {
  padding: 0.75rem 1rem;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

.dropdown-item.text-danger:hover {
  background-color: #fff5f5;
  color: #dc3545 !important;
}

.btn-light:hover {
  background-color: #e9ecef;
}

.nav-link.router-link-active {
  color: #0d6efd !important;
  font-weight: 500;
}

/* Manual dropdown positioning */
.dropdown {
  position: relative;
  z-index: 1050;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: auto;
  right: 0;
  z-index: 1051;
  display: none;
  min-width: 200px;
  transform: translateX(0);
}

.dropdown-menu.show {
  display: block;
}

/* Ensure navbar is above other content */
.navbar {
  position: relative;
  z-index: 1040;
}

/* Make sure the wrapper doesn't interfere with positioning */
.ms-auto {
  margin-left: auto !important;
}

@media (max-width: 991.98px) {
  .dropdown-menu {
    right: 1rem;
  }
}
</style>