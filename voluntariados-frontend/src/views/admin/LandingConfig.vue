<template>
  <div class="landing-config-admin">
        <AdminLayout 
            page-title="Configuración del Sitio" 
            :breadcrumbs="[{ label: 'Configuración del Sitio' }]"
        >

      <div class="row py-3">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-body ">
              <!-- Loading State -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>

              <!-- Success Message -->
              <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                {{ successMessage }}
                <button type="button" class="btn-close" @click="successMessage = ''" aria-label="Close"></button>
              </div>

              <!-- Configuration Form -->
              <form v-else @submit.prevent="saveConfiguration">
                <div class="row">
                  <!-- Basic Information -->
                  <div class="col-lg-6">
                    <h5 class="mb-3 text-primary">
                      <i class="bi bi-info-circle me-2"></i>
                      Información Básica
                    </h5>

                    <div class="mb-3">
                      <label for="page_title" class="form-label">Título de la Página</label>
                      <input
                        type="text"
                        class="form-control"
                        id="page_title"
                        v-model="formData.page_title"
                        placeholder="Ej: Sistema de Voluntariado"
                        maxlength="100"
                      >
                      <div class="form-text">Aparece en la pestaña del navegador</div>
                    </div>

                    <div class="mb-3">
                      <label for="site_name" class="form-label">Nombre del Sitio</label>
                      <input
                        type="text"
                        class="form-control"
                        id="site_name"
                        v-model="formData.site_name"
                        placeholder="Ej: Voluntariado UNCuyo"
                        maxlength="100"
                      >
                      <div class="form-text">Aparece en el header y navegación</div>
                    </div>

                    <div class="mb-3">
                      <label for="welcome_message" class="form-label">Mensaje de Bienvenida</label>
                      <textarea
                        class="form-control"
                        id="welcome_message"
                        v-model="formData.welcome_message"
                        rows="3"
                        placeholder="Ej: Convertite en el cambio que querés ver."
                      ></textarea>
                      <div class="form-text">Título principal de la página de inicio</div>
                    </div>

                    <div class="mb-3">
                      <label for="description" class="form-label">Descripción</label>
                      <textarea
                        class="form-control"
                        id="description"
                        v-model="formData.description"
                        rows="3"
                        placeholder="Ej: ¡Sumáte a los voluntariados!"
                      ></textarea>
                      <div class="form-text">Subtítulo de la página de inicio y descripción SEO</div>
                    </div>
                  </div>

                  <!-- Contact & Media -->
                  <div class="col-lg-6">
                    <h5 class="mb-3 text-primary">
                      <i class="bi bi-envelope me-2"></i>
                      Contacto y Medios
                    </h5>

                    <div class="mb-3">
                      <label for="contact_email" class="form-label">Email de Contacto</label>
                      <input
                        type="email"
                        class="form-control"
                        id="contact_email"
                        v-model="formData.contact_email"
                        placeholder="Ej: contacto@voluntariado.uncuyo.edu.ar"
                      >
                      <div class="form-text">Aparece en el footer del sitio</div>
                    </div>

                    <div class="mb-3">
                      <label for="phone_number" class="form-label">Número de Teléfono</label>
                      <input
                        type="tel"
                        class="form-control"
                        id="phone_number"
                        v-model="formData.phone_number"
                        placeholder="Ej: +542614123456"
                        pattern="^\+?1?\d{9,15}$"
                      >
                      <div class="form-text">Formato: +542614123456</div>
                    </div>

                    <div class="mb-3">
                      <label for="instagram_handle" class="form-label">Instagram</label>
                      <div class="input-group">
                        <span class="input-group-text">@</span>
                        <input
                          type="text"
                          class="form-control"
                          id="instagram_handle"
                          v-model="formData.instagram_handle"
                          placeholder="voluntariado_uncuyo"
                          pattern="^[a-zA-Z0-9_.]+$"
                          maxlength="50"
                        >
                      </div>
                      <div class="form-text">Solo letras, números, puntos y guiones bajos</div>
                    </div>

                    <div class="mb-3">
                      <label for="hero_image" class="form-label">Imagen Principal</label>
                      <input
                        type="file"
                        class="form-control"
                        id="hero_image"
                        @change="handleFileChange"
                        accept="image/*"
                      >
                      <div class="form-text">
                        <div v-if="formData.hero_image && typeof formData.hero_image === 'string'">
                          <i class="bi bi-file-image me-1"></i>
                          Archivo actual: {{ getImageFileName() }}
                        </div>
                        <div v-else-if="selectedFile">
                          <i class="bi bi-upload me-1"></i>
                          Nuevo archivo: {{ selectedFile.name }}
                        </div>
                        <div v-else>
                          Selecciona una imagen para la página principal
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Footer Configuration -->
                <div class="row mt-4">
                  <div class="col-12">
                    <h5 class="mb-3 text-primary">
                      <i class="bi bi-layout-text-window me-2"></i>
                      Configuración del Footer
                    </h5>

                    <div class="mb-4">
                      <label for="footer_text" class="form-label">Texto del Footer</label>
                      <textarea
                        class="form-control"
                        id="footer_text"
                        v-model="formData.footer_text"
                        rows="2"
                        placeholder="Ej: © 2025 Universidad Nacional de Cuyo. Todos los derechos reservados."
                      ></textarea>
                      <div class="form-text">Texto de copyright que aparece en el pie de página</div>
                    </div>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                  <button type="button" class="btn btn-outline-secondary" @click="resetForm">
                    <i class="bi bi-arrow-clockwise me-1"></i>
                    Resetear
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="saving">
                    <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    <i v-else class="bi bi-check-lg me-1"></i>
                    {{ saving ? 'Guardando...' : 'Guardar Configuración' }}
                  </button>
                </div>
                <ConfirmationModal
                  :show="showResetModal"
                  title="Confirmar reseteo"
                  message="¿Estás seguro de que quieres resetear el formulario?"
                  description="Se perderán los cambios no guardados."
                  confirmText="Resetear"
                  cancelText="Cancelar"
                  type="warning"
                  @confirm="handleResetConfirm"
                  @cancel="handleResetCancel"
                />
              </form>
            </div>
          </div>
        </div>
      </div>

    </AdminLayout>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { landingConfigAPI } from '@/services/api'
import { useLandingConfig } from '@/composables/useLandingConfig'

export default defineComponent({
  name: 'LandingConfigAdmin',
  components: {
    AdminLayout,
    ConfirmationModal
  },
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig()
    return {
      sharedLandingConfig: landingConfig,
      refreshLandingConfig: fetchLandingConfig
    }
  },
  data() {
    return {
      loading: true,
      saving: false,
      error: '',
      successMessage: '',
      selectedFile: null as File | null,
      showResetModal: false,
      formData: {
        page_title: '',
        site_name: '',
        welcome_message: '',
        description: '',
        contact_email: '',
        phone_number: '',
        instagram_handle: '',
        hero_image: '',
        footer_text: ''
      }
    }
  },
  async mounted() {
    await this.loadConfiguration()
  },
  methods: {
    async loadConfiguration() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await landingConfigAPI.getConfig()
        if (response.data) {
          this.formData = {
            page_title: response.data.page_title || '',
            site_name: response.data.site_name || '',
            welcome_message: response.data.welcome_message || '',
            description: response.data.description || '',
            contact_email: response.data.contact_email || '',
            phone_number: response.data.phone_number || '',
            instagram_handle: response.data.instagram_handle || '',
            hero_image: response.data.hero_image || '',
            footer_text: response.data.footer_text || ''
          }
        }
      } catch (err: any) {
        console.error('Error loading landing config:', err)
        this.error = err.response?.data?.detail || 'Error al cargar la configuración'
      } finally {
        this.loading = false
      }
    },

    async saveConfiguration() {
      this.saving = true
      this.error = ''
      this.successMessage = ''

      try {
        const updateData: any = { ...this.formData }
        
        // If there's a selected file, include it
        if (this.selectedFile) {
          updateData.hero_image = this.selectedFile
        } else {
          // Remove hero_image from update if no new file selected
          delete updateData.hero_image
        }

        const response = await landingConfigAPI.updateConfig(updateData)
        
        if (response.data) {
          this.successMessage = 'Configuración guardada exitosamente'
          
          // Update form data with response (in case the API returns updated values)
          this.formData = {
            page_title: response.data.page_title || '',
            site_name: response.data.site_name || '',
            welcome_message: response.data.welcome_message || '',
            description: response.data.description || '',
            contact_email: response.data.contact_email || '',
            phone_number: response.data.phone_number || '',
            instagram_handle: response.data.instagram_handle || '',
            hero_image: response.data.hero_image || '',
            footer_text: response.data.footer_text || ''
          }
          
          // Clear selected file after successful upload
          this.selectedFile = null
          const fileInput = document.getElementById('hero_image') as HTMLInputElement
          if (fileInput) fileInput.value = ''
          
          // Refresh the shared landing config to update all components
          await this.refreshLandingConfig()
          
          // Auto-hide success message after 5 seconds
          setTimeout(() => {
            this.successMessage = ''
          }, 5000)
        }
      } catch (err: any) {
        console.error('Error saving landing config:', err)
        this.error = err.response?.data?.detail || 'Error al guardar la configuración'
      } finally {
        this.saving = false
      }
    },

    handleFileChange(event: Event) {
      const target = event.target as HTMLInputElement
      if (target.files && target.files[0]) {
        this.selectedFile = target.files[0]
        
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
        if (!allowedTypes.includes(this.selectedFile.type)) {
          this.error = 'Tipo de archivo no válido. Solo se permiten imágenes (JPEG, PNG, GIF, WebP, SVG)'
          this.selectedFile = null
          target.value = ''
          return
        }
        
        // Validate file size (10MB max)
        if (this.selectedFile.size > 10 * 1024 * 1024) {
          this.error = 'El archivo es demasiado grande. Tamaño máximo: 10MB'
          this.selectedFile = null
          target.value = ''
          return
        }
        
        this.error = ''
      }
    },

    getImageFileName() {
      if (this.formData.hero_image && typeof this.formData.hero_image === 'string') {
        return this.formData.hero_image.split('/').pop() || 'archivo_actual'
      }
      return ''
    },

    resetForm() {
      this.showResetModal = true
    },
    handleResetConfirm() {
      this.loadConfiguration()
      this.selectedFile = null
      const fileInput = document.getElementById('hero_image') as HTMLInputElement
      if (fileInput) fileInput.value = ''
      this.error = ''
      this.successMessage = ''
      this.showResetModal = false
    },
    handleResetCancel() {
      this.showResetModal = false
    },
  }
})
</script>

<style scoped>
.landing-config-admin {
  min-height: 100vh;
}

.card {
  border: none;
  border-radius: 0.5rem;
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-control, .form-select {
  border-radius: 0.375rem;
  border: 1px solid #dee2e6;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus, .form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.text-primary {
  color: #0d6efd !important;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.alert {
  border-radius: 0.375rem;
}

.border-top {
  border-top: 1px solid #dee2e6 !important;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.preview-section {
  background-color: #f8f9fa;
  border-radius: 0.375rem;
  padding: 1rem;
}
</style>