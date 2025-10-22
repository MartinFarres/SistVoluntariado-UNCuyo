<template>
  <AdminLayout
    page-title="Conexión Power BI"
    :breadcrumbs="[{ label: 'Dashboard', to: '/admin/dashboard' }, { label: 'Power BI' }]"
  >
    <div class="row">
      <div class="col-lg-8 mx-auto">
        <div class="card border-0 shadow-sm">
          <div class="card-body p-4">
            <h4 class="card-title mb-4">Credenciales para Power BI</h4>

            <p class="text-muted">
              Utiliza la siguiente URL y clave de API para conectar tus informes de Power BI
              con los datos del sistema de voluntariado. La clave es personal e intransferible.
            </p>

            <div v-if="loading" class="text-center my-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>

            <div v-if="!loading && apiKeyData">
              <!-- URL del Endpoint -->
              <div class="mb-4">
                <label for="powerBiUrl" class="form-label fw-bold">URL del Origen de Datos</label>
                <div class="input-group">
                  <input
                    id="powerBiUrl"
                    type="text"
                    class="form-control"
                    :value="powerBiUrl"
                    readonly
                  />
                  <button class="btn btn-outline-secondary" @click="copyToClipboard(powerBiUrl, 'URL')">
                    <i class="bi bi-clipboard"></i>
                  </button>
                </div>
              </div>

              <!-- Clave de API -->
              <div class="mb-4">
                <label for="apiKey" class="form-label fw-bold">Clave de API (X-API-Key)</label>
                <div class="input-group">
                  <input
                    id="apiKey"
                    type="text"
                    class="form-control"
                    :value="apiKeyData.key"
                    readonly
                  />
                  <button class="btn btn-outline-secondary" @click="copyToClipboard(apiKeyData.key, 'Clave de API')">
                    <i class="bi bi-clipboard"></i>
                  </button>
                </div>
                <div class="form-text">
                  Creada el: {{ formatDate(apiKeyData.created_at) }}
                </div>
              </div>

              <!-- Botón de Regenerar -->
              <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button
                  class="btn btn-danger"
                  @click="regenerateApiKey"
                  :disabled="regenerating"
                >
                  <span v-if="regenerating" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <i v-else class="bi bi-arrow-clockwise"></i>
                  Regenerar Clave
                </button>
              </div>
              <div class="form-text text-end mt-1">
                Al regenerar, la clave anterior quedará invalidada permanentemente.
              </div>
            </div>

            <div v-if="error" class="alert alert-danger mt-4">
              {{ error }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
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
