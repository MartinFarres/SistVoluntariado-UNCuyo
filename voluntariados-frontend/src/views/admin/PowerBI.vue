<template>
  <div class="powerbi-admin">
    <AdminLayout
      page-title="Conexión Power BI"
      :breadcrumbs="[{ label: 'Dashboard', to: '/admin/dashboard' }, { label: 'Power BI' }]"
    >
      <div class="row py-3">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <h5 class="mb-4 text-primary">
                <i class="bi bi-bar-chart-line me-2"></i>
                Credenciales para Power BI
              </h5>

              <p class="text-muted mb-4">
                Utiliza la siguiente URL y clave de API para conectar tus informes de Power BI
                con los datos del sistema de voluntariado. La clave es personal e intransferible.
              </p>

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

              <!-- Content -->
              <div v-else-if="apiKeyData">
                <div class="row">
                  <div class="col-lg-8">
                    <!-- URL del Endpoint -->
                    <div class="mb-4">
                      <label for="powerBiUrl" class="form-label fw-bold">
                        <i class="bi bi-link-45deg me-1"></i>
                        URL del Origen de Datos
                      </label>
                      <div class="input-group">
                        <input
                          id="powerBiUrl"
                          type="text"
                          class="form-control"
                          :value="powerBiUrl"
                          readonly
                        />
                        <button 
                          class="btn btn-outline-secondary" 
                          type="button"
                          @click="copyToClipboard(powerBiUrl, 'URL')"
                          title="Copiar URL"
                        >
                          <i class="bi bi-clipboard"></i>
                        </button>
                      </div>
                      <div class="form-text">
                        Usa esta URL como origen de datos en Power BI
                      </div>
                    </div>

                    <!-- Clave de API -->
                    <div class="mb-4">
                      <label for="apiKey" class="form-label fw-bold">
                        <i class="bi bi-key me-1"></i>
                        Clave de API (X-API-Key)
                      </label>
                      <div class="input-group">
                        <input
                          id="apiKey"
                          type="text"
                          class="form-control font-monospace"
                          :value="apiKeyData.key"
                          readonly
                        />
                        <button 
                          class="btn btn-outline-secondary" 
                          type="button"
                          @click="copyToClipboard(apiKeyData.key, 'Clave de API')"
                          title="Copiar clave"
                        >
                          <i class="bi bi-clipboard"></i>
                        </button>
                      </div>
                      <div class="form-text">
                        <i class="bi bi-calendar3 me-1"></i>
                        Creada el: {{ formatDate(apiKeyData.created_at) }}
                      </div>
                    </div>

                    <!-- Botón de Regenerar -->
                    <div class="border-top pt-4 mt-4">
                      <div class="d-flex justify-content-between align-items-center">
                        <div>
                          <h6 class="mb-1">Regenerar Clave de API</h6>
                          <small class="text-muted">
                            Al regenerar, la clave anterior quedará invalidada permanentemente.
                          </small>
                        </div>
                        <button
                          class="btn btn-danger"
                          @click="regenerateApiKey"
                          :disabled="regenerating"
                        >
                          <span 
                            v-if="regenerating" 
                            class="spinner-border spinner-border-sm me-1" 
                            role="status" 
                            aria-hidden="true"
                          ></span>
                          <i v-else class="bi bi-arrow-clockwise me-1"></i>
                          Regenerar Clave
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Sidebar con información -->
                  <div class="col-lg-4">
                    <div class="card bg-light border-0">
                      <div class="card-body">
                        <h6 class="card-title">
                          <i class="bi bi-info-circle me-1"></i>
                          Información
                        </h6>
                        <ul class="small mb-0 ps-3">
                          <li class="mb-2">Usa la URL como origen de datos Web en Power BI</li>
                          <li class="mb-2">Agrega la clave de API en los encabezados de autenticación</li>
                          <li class="mb-2">La clave debe mantenerse segura y no compartirse</li>
                          <li>Regenera la clave si sospechas que fue comprometida</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
import apiClient from '@/services/api'

interface ApiKeyData {
  key: string
  created_at: string
}

export default defineComponent({
  name: 'PowerBIAdmin',
  components: { AdminLayout },
  data() {
    // Construye la URL completa para el endpoint de Power BI usando la base del apiClient
    const baseUrl = (apiClient.defaults.baseURL || '').replace(/\/$/, ''); // Elimina la barra final si existe
    const powerBiUrl = `${baseUrl}/dashboard/powerbi/`;

    return {
      apiKeyData: null as ApiKeyData | null,
      loading: true,
      regenerating: false,
      error: '' as string,
      powerBiUrl: powerBiUrl,
    }
  },
  mounted() {
    this.fetchApiKey()
  },
  methods: {
    async fetchApiKey() {
      this.loading = true
      this.error = ''
      try {
        const response = await apiClient.get('/dashboard/powerbi/key/')
        this.apiKeyData = response.data
      } catch (err) {
        this.error = 'No se pudo cargar la clave de API. Por favor, recarga la página.'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async regenerateApiKey() {
      if (!confirm('¿Estás seguro de que quieres regenerar tu clave de API? La clave anterior dejará de funcionar inmediatamente.')) {
        return
      }
      this.regenerating = true
      this.error = ''
      try {
        const response = await apiClient.post('/dashboard/powerbi/key/')
        this.apiKeyData = response.data
        alert('¡Nueva clave de API generada exitosamente!')
      } catch (err) {
        this.error = 'Ocurrió un error al regenerar la clave.'
        console.error(err)
      } finally {
        this.regenerating = false
      }
    },
    copyToClipboard(text: string, type: string) {
      navigator.clipboard.writeText(text).then(() => {
        alert(`${type} copiada al portapapeles.`)
      }).catch(err => {
        alert(`No se pudo copiar la ${type}.`)
        console.error('Error al copiar: ', err)
      })
    },
    formatDate(dateString: string): string {
      if (!dateString) return ''
      const options: Intl.DateTimeFormatOptions = {
        year: 'numeric', month: 'long', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
      }
      return new Date(dateString).toLocaleDateString('es-AR', options)
    }
  }
})
</script>

<style scoped>
.powerbi-admin {
  min-height: 100vh;
}

.font-monospace {
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
}

.card {
  border-radius: 0.5rem;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}
</style>
