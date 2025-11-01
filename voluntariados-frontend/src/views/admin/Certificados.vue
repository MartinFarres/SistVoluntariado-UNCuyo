<template>
  <AdminLayout
    page-title="Certificados"
    :breadcrumbs="[{ label: 'Certificados' }]"
  >
    <div class="card shadow-sm border-0 mb-4 mt-4">
      <div class="card-body">
        <div class="dynamic-content-header mb-4">
          <h5 class="text-primary mb-2">
            <i class="bi bi-list-stars me-2"></i>
            Generación de certificados
          </h5>
          <div class="alert alert-info d-flex align-items-start">
            <i class="bi bi-info-circle-fill me-3 fs-5"></i>
            <div>
              <strong>¿Qué es esto?</strong>
              <p class="mb-0 small">
                Aquí podrás editar el formato de los certificados que se generan para los voluntarios. Además, podés generar los cetificados desde esta sección.
              </p>
            </div>
          </div>
        </div>
        <!-- Plantilla: collapsible section -->
        <div class="config-section-card mb-4">
          <div class="config-section-header" @click="toggleSection('plantilla')">
            <div class="d-flex align-items-center">
              <i class="bi bi-card-image me-2 text-primary"></i>
              <h5 class="mb-0">Plantilla de fondo</h5>
            </div>
            <i :class="['bi', expandedSections.plantilla ? 'bi-chevron-up' : 'bi-chevron-down']"></i>
          </div>
          <div v-show="expandedSections.plantilla" class="config-section-body">
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
          </div>
        </div>

        <!-- Buscar voluntario: collapsible -->
        <div class="config-section-card mb-4">
          <div class="config-section-header" @click="toggleSection('buscarVoluntario')">
            <div class="d-flex align-items-center">
              <i class="bi bi-award me-2 text-primary"></i>
              <h5 class="mb-0">Generar certificados</h5>
            </div>
            <i :class="['bi', expandedSections.buscarVoluntario ? 'bi-chevron-up' : 'bi-chevron-down']"></i>
          </div>
          <div v-show="expandedSections.buscarVoluntario" class="config-section-body">
            <div class="row mb-3 align-items-end">
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
          </div>
        </div>

        <!-- Generar desde valores: collapsible -->
        <div class="config-section-card mb-4">
          <div class="config-section-header" @click="toggleSection('generarValores')">
            <div class="d-flex align-items-center">
              <i class="bi bi-pencil-square me-2 text-primary"></i>
              <h5 class="mb-0">Generar desde valores</h5>
            </div>
            <i :class="['bi', expandedSections.generarValores ? 'bi-chevron-up' : 'bi-chevron-down']"></i>
          </div>
          <div v-show="expandedSections.generarValores" class="config-section-body">
            <div class="mb-3">
              <div class="alert alert-info mb-3">
                <i class="bi bi-info-circle-fill me-2"></i>
                Esta herramienta permite probar y generar certificados personalizados a partir de
                valores arbitrarios — útil para testing o para emitir certificados manuales.
                Uso exclusivo administrativo.
              </div>
            </div>

            <div class="row g-3">
              <div class="col-md-4">
                <label class="form-label">Nombre</label>
                <input v-model="form.nombre" type="text" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">Apellido</label>
                <input v-model="form.apellido" type="text" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">DNI</label>
                <input v-model="form.dni" type="text" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Nombre del voluntariado</label>
                <input v-model="form.voluntariado_nombre" type="text" class="form-control" />
              </div>

              <div class="col-md-3">
                <label class="form-label">Última fecha (último turno)</label>
                <input v-model="form.ultima_fecha" type="date" class="form-control" />
              </div>

              <div class="col-md-3">
                <label class="form-label">Fecha fin cursado (opcional)</label>
                <input v-model="form.fecha_fin_cursado" type="date" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Último lugar</label>
                <input v-model="form.ultimo_lugar" type="text" class="form-control" />
              </div>

              <div class="col-md-3">
                <label class="form-label">Total horas</label>
                <input v-model="form.total_horas" type="number" step="0.25" class="form-control" />
                <div class="form-text small text-muted">Ingresar horas totales (puede incluir decimales, ej. 12.5)</div>
              </div>
              <div class="col-12 mt-3">
                <div class="d-flex flex-wrap gap-2">
                  <button class="btn btn-primary" :disabled="generating" @click="generateFromValues('pdf')">
                    <i class="bi bi-file-earmark-pdf me-1"></i> Generar
                  </button>

                  <button class="btn btn-secondary" type="button" @click="resetForm">Limpiar campos</button>
                </div>
              </div>
            </div>
            <div v-if="previewImageUrl" class="mt-3 border rounded p-3 bg-light text-center preview-block">
              <h6 class="mb-2">Vista previa</h6>
              <img :src="previewImageUrl" alt="Preview" class="img-fluid preview-image" />
              <div class="mt-2 small text-muted">La vista previa corresponde a la primera página convertida a imagen.</div>
            </div>
          </div>
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
      
      // Form for generar-por-valores
      form: {
        nombre: '',
        apellido: '',
        dni: '' ,
        voluntariado_nombre: '',
        ultima_fecha: '',
        fecha_fin_cursado: '',
        ultimo_lugar: '',
        total_horas: ''
      } as any,
      generating: false,
      previewImageUrl: '' as string,

      // UI state for collapsible sections
      expandedSections: {
        plantilla: true,
        buscarVoluntario: true,
        generarValores: true,
      } as Record<string, boolean>,

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
    ,

    toggleSection(section: keyof typeof this.expandedSections) {
      // toggle the named section
      // @ts-ignore
      this.expandedSections[section] = !this.expandedSections[section]
    },

    // Generate from arbitrary values (admin endpoint)
    async generateFromValues(format: 'pdf' | 'image') {
      // basic validation
      const required = ['nombre','apellido','dni','voluntariado_nombre','ultima_fecha','ultimo_lugar','total_horas']
      const missing = required.filter(k => !this.form[k])
      if (missing.length) {
        alert(`Faltan campos requeridos: ${missing.join(', ')}`)
        return
      }

      this.generating = true
      this.previewImageUrl && URL.revokeObjectURL(this.previewImageUrl)
      this.previewImageUrl = ''

      const payload: any = {
        nombre: this.form.nombre,
        apellido: this.form.apellido,
        dni: this.form.dni,
        voluntariado_nombre: this.form.voluntariado_nombre,
        ultima_fecha: this.form.ultima_fecha,
        ultimo_lugar: this.form.ultimo_lugar,
        total_horas: this.form.total_horas,
      }
      if (this.form.fecha_fin_cursado) payload.fecha_fin_cursado = this.form.fecha_fin_cursado
      if (format) payload.format = format

      try {
        const response = await certificadoAPI.generarPorValores(payload)

        const contentType = (response.headers && response.headers['content-type']) || ''
        const blobData = response.data instanceof Blob ? response.data : new Blob([response.data], { type: contentType || 'application/octet-stream' })

        if (contentType.includes('image')) {
          // show preview
          this.previewImageUrl = window.URL.createObjectURL(blobData)
        } else {
          // treat as PDF and download
          const filename = `certificado_${this.form.dni || 'sin_dni'}.pdf`
          const url = window.URL.createObjectURL(blobData)
          const a = document.createElement('a')
          a.href = url
          a.download = filename
          a.click()
          window.URL.revokeObjectURL(url)
        }
      } catch (err: any) {
        console.error(err)
        alert(err.response?.data?.detail || 'Error al generar certificado')
      } finally {
        this.generating = false
      }
    },

    resetForm() {
      this.form = {
        nombre: '',
        apellido: '',
        dni: this.dni || '',
        voluntariado_nombre: '',
        ultima_fecha: '',
        fecha_fin_cursado: '',
        ultimo_lugar: '',
        total_horas: ''
      }
      if (this.previewImageUrl) {
        URL.revokeObjectURL(this.previewImageUrl)
        this.previewImageUrl = ''
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

/* Minimal collapsible section styles (copied from LandingConfig) */
.config-section-card {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.config-section-header {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.config-section-header h5 { font-weight: 600; color: #495057; margin: 0; font-size: 1.05rem; }
.config-section-header i.bi-chevron-up, .config-section-header i.bi-chevron-down { font-size: 1.2rem; color: #6c757d; }
.config-section-body { padding: 1.5rem; animation: slideDown 0.2s ease; }

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

.preview-block { max-width: 720px; margin-left: auto; margin-right: auto; }
.preview-image { max-height: 520px; object-fit: contain; }
</style>
