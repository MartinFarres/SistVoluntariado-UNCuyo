<script setup lang="ts">
import { RouterView } from 'vue-router'
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { landingConfigAPI } from './services/api'

const route = useRoute()

// Landing configuration state
const landingConfig = ref({
  contact_email: '',
  phone_number: '',
  instagram_handle: '',
  instagram_url: '',
  footer_text: '© 2025 Voluntariado UNCuyo.'
})

// Check if we're in admin route to apply sidebar-aware styling
const isAdminRoute = computed(() => {
  return route.path.startsWith('/admin')
})

// Fetch landing configuration on component mount
onMounted(async () => {
  try {
    const response = await landingConfigAPI.getPublicConfig()
    if (response.data) {
      landingConfig.value = {
        contact_email: response.data.contact_email || '',
        phone_number: response.data.phone_number || '',
        instagram_handle: response.data.instagram_handle || '',
        instagram_url: response.data.instagram_url || '',
        footer_text: response.data.footer_text || '© 2025 Voluntariado UNCuyo.'
      }
    }
  } catch (error) {
    console.warn('Error fetching landing config:', error)
    // Keep default values if API fails
  }
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
        <div class="row">
          <!-- Footer Text -->
          <div class="col-md-6 text-center text-md-start">
            <p class="mb-0" v-text="landingConfig.footer_text"></p>
          </div>
          
          <!-- Contact Information -->
          <div class="col-md-6 text-center text-md-end">
            <div class="d-flex justify-content-center justify-content-md-end align-items-center gap-3 flex-wrap">
              <!-- Email -->
              <span v-if="landingConfig.contact_email" class="footer-contact">
                <i class="bi bi-envelope"></i>
                <a :href="`mailto:${landingConfig.contact_email}`" class="text-white text-decoration-none ms-1">
                  {{ landingConfig.contact_email }}
                </a>
              </span>
              
              <!-- Phone -->
              <span v-if="landingConfig.phone_number" class="footer-contact">
                <i class="bi bi-telephone"></i>
                <a :href="`tel:${landingConfig.phone_number}`" class="text-white text-decoration-none ms-1">
                  {{ landingConfig.phone_number }}
                </a>
              </span>
              
              <!-- Instagram -->
              <span v-if="landingConfig.instagram_handle" class="footer-contact">
                <i class="bi bi-instagram"></i>
                <a :href="landingConfig.instagram_url" target="_blank" rel="noopener noreferrer" class="text-white text-decoration-none ms-1">
                  @{{ landingConfig.instagram_handle }}
                </a>
              </span>
            </div>
          </div>
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

/* Footer contact styles */
.footer-contact {
  display: inline-flex;
  align-items: center;
  font-size: 0.9rem;
}

.footer-contact i {
  font-size: 1rem;
}

.footer-contact a {
  transition: opacity 0.2s;
}

.footer-contact a:hover {
  opacity: 0.8;
}

/* Responsive footer */
@media (max-width: 768px) {
  .footer-contact {
    font-size: 0.8rem;
    margin-bottom: 0.25rem;
  }
}
</style>