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
            <div class="row align-items-center py-4">
              <div class="col-lg-6 col-7">
                <h6 class="h2 text-white d-inline-block mb-0">{{ pageTitle }}</h6>
                <nav v-if="breadcrumbs.length > 0" aria-label="breadcrumb" class="d-none d-md-inline-block ml-md-4">
                  <ol class="breadcrumb breadcrumb-links breadcrumb-dark">
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
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
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
  margin-left: 250px;
  transition: margin-left 0.3s ease;
}

.main-content.sidebar-collapsed {
  margin-left: 80px;
}

.bg-gradient-primary {
  background: linear-gradient(87deg, #5e72e4 0, #825ee4 100%);
}

.header {
  position: relative;
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