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

        <!-- Imagen de plantilla + Dropzone (click or drag & drop) -->
        <div class="row mb-4 align-items-center">
          <div class="col-lg-6 mb-3 mb-lg-0">
            <h5>Plantilla actual</h5>
            <div v-if="templateUrl" class="border p-2 rounded bg-light d-flex align-items-center justify-content-center template-preview">
              <img :src="templateUrl" alt="Plantilla actual" class="img-fluid">
            </div>
            <div v-else class="alert alert-secondary">
              No hay plantilla cargada
            </div>
          </div>

          <div class="col-lg-6">
            <h5>Actualizar plantilla</h5>
            <div
              class="template-dropzone rounded d-flex flex-column align-items-center justify-content-center text-center p-4"
              :class="{ 'is-dragover': dragOver }"
              @click="triggerFileInput"
              @dragover.prevent="onDragOver"
              @dragleave.prevent="onDragLeave"
              @drop.prevent="onDrop"
            >
              <input
                ref="fileInput"
                type="file"
                class="d-none"
                accept="image/png, image/jpeg"
                @change="onFileSelected"
              />

              <div class="mb-2">
                <i class="bi bi-upload fs-1"></i>
              </div>
              <div class="mb-2">
                <strong>{{ selectedFile ? selectedFile.name : 'Haz clic o arrastra una imagen aquí' }}</strong>
              </div>
              <div class="small text-muted mb-2">Formatos permitidos: PNG, JPG. Tamaño recomendado: ancho ≥ 1200px</div>

              <button
                v-if="selectedFile && !uploading"
                class="btn btn-success mt-2"
                @click.stop="uploadTemplate"
              >
                <i class="bi bi-cloud-upload-fill me-2"></i>
                Subir plantilla
              </button>

              <div v-else-if="uploading" class="mt-2">
                <span class="spinner-border spinner-border-sm me-2"></span>Subiendo...
              </div>

              <div v-else class="mt-2 text-muted small">Al seleccionar el archivo, podrás subirlo desde aquí.</div>
            </div>
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
              :error="error ?? undefined"
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
  dragOver: false,

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
        // Auto-upload when a file is selected
        if (!this.uploading) this.uploadTemplate()
      }
    },

    triggerFileInput() {
      const el = (this.$refs.fileInput as HTMLInputElement | undefined)
      if (el) el.click()
    },

    onDragOver() {
      this.dragOver = true
    },

    onDragLeave() {
      this.dragOver = false
    },

    onDrop(e: DragEvent) {
      this.dragOver = false
      const files = e.dataTransfer?.files
      if (!files || files.length === 0) return
      const f = files.item(0)
      if (!f) return
      // basic validation
      if (!f.type || !f.type.startsWith('image/')) return
      this.selectedFile = f as File
      // Auto-upload when a file is dropped
      if (!this.uploading) this.uploadTemplate()
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

.template-dropzone {
  border: 2px dashed rgba(13,110,253,0.15);
  background: rgba(13,110,253,0.02);
  min-height: 160px;
  cursor: pointer;
}
.template-dropzone.is-dragover {
  border-color: rgba(13,110,253,0.6);
  background: rgba(13,110,253,0.04);
  box-shadow: 0 8px 24px rgba(13,110,253,0.06);
}
.template-preview img.img-fluid { max-height: 300px; }
</style>
