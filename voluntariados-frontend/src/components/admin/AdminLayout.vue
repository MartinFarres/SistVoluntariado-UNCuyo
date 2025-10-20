<!-- src/components/admin/AdminLayout.vue -->
<template>
  <div>
    <!-- Global Topbar (full width) -->
    <div ref="adminTopbar" class="admin-topbar">
      <AppNavbar />
    </div>

    <div class="admin-dashboard">
      <!-- Fixed Sidebar below topbar -->
      <AdminSidebar :isCollapsed="sidebarCollapsed" @toggle="toggleSidebar" />

      <!-- Main area to the right of sidebar -->
      <div class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">

      <div class="header bg-gradient-primary admin-header">
        <div class="container-fluid">
          <div class="header-body">
            <div class="row py-2">
              <div class="col-12">
                <div class="header-content d-flex flex-column">
                  <h1 class="h2 text-white mb-2">{{ pageTitle }}</h1>
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

        <div class="container-fluid mt--6">
          <slot></slot>
        </div>
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
    // Set initial CSS custom properties
    this.updateSidebarWidth()
    this.updateTopbarHeight()
    window.addEventListener('resize', this.updateTopbarHeight)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateTopbarHeight)
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
    },
    updateTopbarHeight() {
      const el = this.$refs.adminTopbar as HTMLElement | undefined
      const height = el ? el.offsetHeight : 0
      document.documentElement.style.setProperty('--topbar-height', height + 'px')
    }
  }
})
</script>

<style scoped>
.admin-topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1100;
}

.admin-dashboard {
  display: flex;
  height: calc(100vh - var(--topbar-height, 0px));
  margin-top: var(--topbar-height, 0px);
  background-color: #f7fafc;
  overflow: hidden; /* prevent page scroll; only main content should scroll */
}

.main-content {
  flex: 1;
  margin-left: var(--sidebar-width, 300px);
  transition: margin-left 0.3s ease;
  height: calc(100vh - var(--topbar-height, 0px));
  overflow-y: auto; /* scroll only content */
}

/* Collapsed state is handled via --sidebar-width var */

.bg-gradient-primary {
  /* Match HomeView primary gradient */
  background: linear-gradient(135deg, #8B0000, #DC143C);
}

.header {
  position: relative;
}

/* Slimmer header for admin pages */
.admin-header {
  padding-top: 0.75rem;   /* was pt-5/pt-md-7 */
  padding-bottom: 0.75rem; /* was pb-6 */
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