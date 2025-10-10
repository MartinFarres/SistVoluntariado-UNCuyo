<script setup lang="ts">
import { RouterView } from 'vue-router'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Check if we're in admin route to apply sidebar-aware styling
const isAdminRoute = computed(() => {
  return route.path.startsWith('/admin')
})
</script>

<template>
  <div id="app">
   
    <!-- Main Content Area - Router View -->
    <main>
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-3" :class="{ 'admin-footer': isAdminRoute }">
      <div class="container-fluid" :class="{ 'admin-footer-content': isAdminRoute }">
        <div class="text-center">
          <p class="mb-0 text-white">&copy; 2025 Voluntariado UNCuyo. </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
export default {
  name: 'App'
}
</script>

<style>
/* Import Bootstrap Icons */
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css');
@import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

/* Admin Footer Styles */
.admin-footer {
  margin-left: var(--sidebar-width, 300px);
  transition: margin-left 0.3s ease;
}

.admin-footer-content {
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Responsive behavior for admin footer */
@media (max-width: 768px) {
  .admin-footer {
    margin-left: 0;
  }
}

/* Footer link hover */
footer a:hover {
  color: #ffffff !important;
}

.social-links a {
  transition: color 0.2s;
}

.social-links a:hover {
  color: #ffffff !important;
}
</style>