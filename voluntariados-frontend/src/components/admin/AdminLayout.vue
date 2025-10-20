<!-- src/components/admin/AdminLayout.vue -->
<template>
  <div class="admin-dashboard">
    <!-- Navigation Bar -->
  
    
    
    <!-- Sidebar -->
    <AdminSidebar :isCollapsed="sidebarCollapsed" @toggle="toggleSidebar" />
    
    <!-- Main Content -->
    <div class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      
      <AppNavbar />

      <!-- Header -->
      <div class="header bg-gradient-primary pb-6 pt-5 pt-md-7">
        <div class="container-fluid">
          <div class="header-body">
            <div class="row py-4">
              <div class="col-12">
                <div class="header-content d-flex flex-column">
                  <!-- Page Title -->
                  <h1 class="h2 text-white mb-3">{{ pageTitle }}</h1>
                  
                  <!-- Breadcrumbs -->
                  <nav v-if="breadcrumbs.length > 0" aria-label="breadcrumb">
                    <ol class="breadcrumb breadcrumb-links breadcrumb-dark mb-0">
                      <li class="breadcrumb-item">
                        <router-link to="/admin/dashboard" class="text-white">
                          <i class="bi bi-house"></i>
                        </router-link>
                      </li>
                      <li 
                        v-for="(crumb, index) in breadcrumbs" 
                        :key="index"
                        class="breadcrumb-item"
                        :class="{ active: index === breadcrumbs.length - 1 }"
                      >
                        <router-link 
                          v-if="crumb.to && index !== breadcrumbs.length - 1" 
                          :to="crumb.to" 
                          class="text-white"
                        >
                          {{ crumb.label }}
                        </router-link>
                        <span v-else class="text-white">{{ crumb.label }}</span>
                      </li>
                    </ol>
                  </nav>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Page Content -->
      <div class="container-fluid mt--6">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import AdminSidebar from './AdminSidebar.vue'
import AppNavbar from '../Navbar.vue'

interface Breadcrumb {
  label: string
  to?: string
}

export default defineComponent({
  name: 'AdminLayout',
  components: {
    AdminSidebar,
    AppNavbar
  },
  props: {
    pageTitle: {
      type: String,
      required: true
    },
    breadcrumbs: {
      type: Array as PropType<Breadcrumb[]>,
      default: () => []
    }
  },
  data() {
    return {
      sidebarCollapsed: false
    }
  },
  mounted() {
    // Set initial CSS custom property for sidebar width
    this.updateSidebarWidth()
  },
  watch: {
    sidebarCollapsed() {
      this.updateSidebarWidth()
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    updateSidebarWidth() {
      const width = this.sidebarCollapsed ? '80px' : '300px'
      document.documentElement.style.setProperty('--sidebar-width', width)
    }
  }
})
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  min-height: 100vh;
  background-color: #f7fafc;
}

.main-content {
  flex: 1;
  margin-left: 300px;
  transition: margin-left 0.3s ease;
}

.main-content.sidebar-collapsed {
  margin-left: 80px;
}

.bg-gradient-primary {
  /* Match HomeView primary gradient */
  background: linear-gradient(135deg, #8B0000, #DC143C);
}

.header {
  position: relative;
}

.header-content {
  width: 100%;
}

.header-content h1 {
  display: block;
  width: 100%;
}

.header-content nav {
  display: block;
  width: 100%;
  clear: both;
}

.navbar-top {
  position: sticky;
  top: 0;
  z-index: 1000;
}

.breadcrumb-dark .breadcrumb-item + .breadcrumb-item::before {
  color: rgba(255, 255, 255, 0.6);
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
}
</style>