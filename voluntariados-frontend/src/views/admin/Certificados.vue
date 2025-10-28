<template>
  <AdminLayout
    page-title="Certificados"
    :breadcrumbs="[{ label: 'Certificados' }]"
  >
    <div class="card shadow-sm border-0 mb-4 mt-4">
      <div class="card-body">
        <!-- Título principal -->
        <h5 class="mb-4 text-primary">
            <i class="bi bi-card-image me-2"></i> Plantilla de fondo
          </h5>

        <!-- Imagen de plantilla -->
        <div class="row mb-4">
          <div class="col-md-6">
            <h5>Plantilla actual</h5>
            <div v-if="templateUrl" class="border p-2 rounded bg-light">
              <img :src="templateUrl" alt="Plantilla actual" class="img-fluid">
            </div>
            <div v-else class="alert alert-secondary">
              No hay plantilla cargada
            </div>
          </div>
          <div class="col-md-6">
            <h5>Actualizar plantilla</h5>
            <input
              type="file"
              class="form-control mb-2"
              accept="image/png, image/jpeg"
              @change="onFileSelected"
            />
            <button
              class="btn btn-primary"
              :disabled="uploading"
              @click="uploadTemplate"
            >
              <i class="bi bi-upload"></i>
              {{ uploading ? 'Subiendo...' : 'Subir nueva plantilla' }}
            </button>
          </div>
        </div>

        <hr>

        <!-- Buscar voluntario -->
        <div class="row mb-3 align-items-end">
          <h5 class="mb-4 text-primary">
            <i class="bi bi-award me-2"></i> Generar certificados
          </h5>
          <div class="col-md-4">
            <label for="dni" class="form-label fw-semibold">DNI del voluntario</label>
            <input
              id="dni"
              type="text"
              class="form-control"
              placeholder="Ingrese DNI..."
              v-model="dni"
            />
          </div>
          <div class="col-md-3">
            <button
              class="btn btn-outline-primary mt-3 mt-md-0"
              :disabled="loadingVoluntariados || !dni"
              @click="buscarVoluntariados"
            >
              <i class="bi bi-search"></i> Buscar
            </button>
          </div>
        </div>

        <!-- Tabla de voluntariados -->
        <div class="row" v-if="voluntariados.length > 0">
          <div class="col">
            <AdminTable
              title="Voluntariados del voluntario"
              :columns="columns"
              :items="voluntariados"
              :loading="loadingVoluntariados"
              :error="error"
              :footer-text="`Mostrando ${voluntariados.length} voluntariados`"
              :show-create-button="false"
              :show-actions="false"
            >
              <template #cell-acciones="{ item }">
                <button
                  class="btn btn-sm btn-outline-success"
                  @click="generarCertificado(item)"
                >
                  <i class="bi bi-file-earmark-pdf"></i> Descargar
                </button>
              </template>
            </AdminTable>
          </div>
        </div>

        <!-- Alerta cuando no hay resultados -->
        <div
          v-else-if="hasSearched && dni && !loadingVoluntariados && !error"
          class="alert alert-warning"
        >
          No se encontraron voluntariados para este DNI.
        </div>

        <div v-if="error" class="alert alert-danger mt-3">
          {{ error }}
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent, watch } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import { certificadoAPI, voluntariadoAPI } from '@/services/api'

interface Voluntariado {
  id: number
  nombre: string
  fecha_inicio_cursado: string
  fecha_fin_cursado: string
}

export default defineComponent({
  name: 'AdminCertificados',
  components: {
    AdminLayout,
    AdminTable
  },
  data() {
    return {
      templateUrl: '',
      selectedFile: null as File | null,
      uploading: false,

      dni: '',
      voluntariados: [] as Voluntariado[],
      loadingVoluntariados: false,
      error: null as string | null,
      hasSearched: false,

      columns: [
        { key: 'id', label: 'ID', align: 'center' },
        { key: 'nombre', label: 'Nombre' },
        { key: 'fecha_inicio_cursado', label: 'Fecha inicio' },
        { key: 'fecha_fin_cursado', label: 'Fecha fin' },
        { key: 'acciones', label: 'Acciones', align: 'center' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.loadTemplate()
  },
  watch: {
    dni(newVal: string) {
      if (!newVal) {
        this.voluntariados = []
        this.hasSearched = false
        this.error = null
      }
    }
  },
  methods: {
    async loadTemplate() {
      const timestamp = Date.now()
      const baseUrl = import.meta.env.VITE_MEDIA_BASE_URL
      this.templateUrl = `${baseUrl}/media/plantillas/template_certificado.png?${timestamp}`
    },

    onFileSelected(event: Event) {
      const input = event.target as HTMLInputElement
      if (input.files && input.files[0]) {
        this.selectedFile = input.files[0]
      }
    },

    async uploadTemplate() {
      if (!this.selectedFile) return
      this.uploading = true
      const formData = new FormData()
      formData.append('imagen', this.selectedFile)

      try {
        await certificadoAPI.uploadTemplate(formData)
        this.loadTemplate()
        alert('Plantilla actualizada correctamente.')
      } catch (err: any) {
        console.error(err)
        alert(err.response?.data?.detail || 'Error al subir plantilla')
      } finally {
        this.uploading = false
      }
    },

    async buscarVoluntariados() {
      this.loadingVoluntariados = true
      this.error = null
      this.voluntariados = []
      this.hasSearched = true

      try {
        const response = await voluntariadoAPI.buscarPorDNI(this.dni, "")
        this.voluntariados = response.data
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al buscar voluntariados'
      } finally {
        this.loadingVoluntariados = false
      }
    },

    async generarCertificado(voluntariado: Voluntariado) {
      try {
        const response = await certificadoAPI.generarDesdeAdmin({
          dni: this.dni,
          voluntariado_id: voluntariado.id
        })
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `certificado_${this.dni}_${voluntariado.nombre}.pdf`
        a.click()
        window.URL.revokeObjectURL(url)
      } catch (err: any) {
        console.error(err)
        alert(err.response?.data?.detail || 'Error al generar certificado')
      }
    }
  }
})
</script>

<style scoped>
.card {
  background: #fff;
  border-radius: 0.5rem;
}
img.img-fluid {
  max-height: 250px;
  object-fit: contain;
}
</style>
