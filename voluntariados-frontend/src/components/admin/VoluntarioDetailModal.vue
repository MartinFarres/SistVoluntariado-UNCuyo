<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/VoluntarioDetailModal.vue -->
<template>
  <div class="modal fade show d-block align-items-center justify-content-center" tabindex="-1" v-if="show" @click.self="close" style="display: flex; min-height: 100vh;">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-person-heart me-2"></i>
            Detalles del Voluntario
          </h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>

        <div class="modal-body" v-if="voluntario">
          <!-- Header with name and avatar -->
          <div class="row mb-4">
            <div class="col-12">
              <div class="d-flex align-items-center p-3 bg-light rounded">
                <div class="avatar-large rounded-circle bg-primary text-white me-3 d-flex align-items-center justify-content-center">
                  <i class="bi bi-person-heart" style="font-size: 2rem;"></i>
                </div>
                <div>
                  <h4 class="mb-1">{{ voluntario.apellido }}, {{ voluntario.nombre }}</h4>
                  <p class="text-muted mb-0" v-if="voluntario.dni">DNI: {{ voluntario.dni }}</p>
                  <span v-if="voluntario.interno" class="badge bg-primary mt-1">
                    <i class="bi bi-check-circle me-1"></i>Voluntario Interno
                  </span>
                  <span v-else class="badge bg-outline-secondary mt-1">
                    <i class="bi bi-x-circle me-1"></i>Voluntario Externo
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Information sections -->
          <div class="row">
            <!-- Personal Information -->
            <div class="col-md-6 mb-4">
              <div class="card h-100">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-person me-2"></i>Información Personal</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label class="form-label text-muted small">Fecha de Nacimiento</label>
                    <p class="mb-0">{{ voluntario.fecha_nacimiento ? formatDate(voluntario.fecha_nacimiento) : 'No especificada' }}</p>
                  </div>
                  <div class="mb-3">
                    <label class="form-label text-muted small">Dirección</label>
                    <p class="mb-0">{{ voluntario.direccion || 'No especificada' }}</p>
                  </div>
                  <div class="mb-0">
                    <label class="form-label text-muted small">Ubicación</label>
                    <p class="mb-0">
                      <span class="badge bg-info">
                        <i class="bi bi-geo-alt me-1"></i>{{ getCompleteLocation(voluntario.localidad) }}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Contact Information -->
            <div class="col-md-6 mb-4">
              <div class="card h-100">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-telephone me-2"></i>Información de Contacto</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label class="form-label text-muted small">Email</label>
                    <p class="mb-0">
                      <span v-if="voluntario.email">
                        <i class="bi bi-envelope me-2"></i>
                        <a :href="`mailto:${voluntario.email}`" class="text-decoration-none">{{ voluntario.email }}</a>
                      </span>
                      <span v-else class="text-muted">No especificado</span>
                    </p>
                  </div>
                  <div class="mb-0">
                    <label class="form-label text-muted small">Teléfono</label>
                    <p class="mb-0">
                      <span v-if="voluntario.telefono">
                        <i class="bi bi-telephone me-2"></i>
                        <a :href="`tel:${voluntario.telefono}`" class="text-decoration-none">{{ voluntario.telefono }}</a>
                      </span>
                      <span v-else class="text-muted">No especificado</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Academic Information -->
          <div class="row" v-if="voluntario.carrera">
            <div class="col-12 mb-4">
              <div class="card">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-mortarboard me-2"></i>Información Académica</h6>
                </div>
                <div class="card-body">
                  <label class="form-label text-muted small">Carrera</label>
                  <p class="mb-0">
                    <span v-if="voluntario.carrera && typeof voluntario.carrera === 'object'" class="badge bg-success">
                      {{ voluntario.carrera.nombre }}
                    </span>
                    <span v-else-if="voluntario.carrera" class="badge bg-success">
                      {{ getCarreraName(voluntario.carrera) }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- General Observations -->
          <div class="row" v-if="voluntario.observaciones">
            <div class="col-12 mb-4">
              <div class="card">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-chat-text me-2"></i>Observaciones Generales</h6>
                </div>
                <div class="card-body">
                  <p class="mb-0" style="white-space: pre-wrap;">{{ voluntario.observaciones }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Attendance Observations -->
          <div class="row">
            <div class="col-12 mb-4">
              <div class="card">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-calendar-check me-2"></i>Observaciones de Asistencia</h6>
                </div>
                <div class="card-body">
                  <div v-if="loadingObservaciones" class="text-center">
                    <div class="spinner-border spinner-border-sm" role="status">
                      <span class="visually-hidden">Cargando...</span>
                    </div>
                  </div>
                  <div v-else-if="errorObservaciones" class="alert alert-danger small">
                    {{ errorObservaciones }}
                  </div>
                  <ul v-else-if="observacionesAsistencia.length > 0" class="list-group list-group-flush">
                    <li v-for="(obs, index) in observacionesAsistencia" :key="index" class="list-group-item">
                      {{ obs }}
                    </li>
                  </ul>
                  <p v-else class="text-muted mb-0">No tiene observaciones de asistencia.</p>
                </div>
              </div>
            </div>
          </div>

        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-outline-primary" @click="$emit('edit', voluntario)">
            <i class="bi bi-pencil me-2"></i>Editar
          </button>
          <button type="button" class="btn btn-secondary" @click="close">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" v-if="show"></div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { personaAPI } from '@/services/api'

interface Localidad {
  id: number;
  nombre: string;
  departamento?: {
    id: number;
    nombre: string;
    provincia?: {
      id: number;
      nombre: string;
      pais?: {
        id: number;
        nombre: string;
      }
    }
  }
}
interface Carrera { id: number; nombre: string }

interface Voluntario {
  id: number
  nombre: string
  apellido: string
  dni: string | null
  fecha_nacimiento: string | null
  telefono: string | null
  email: string | null
  direccion: string | null
  localidad: number | Localidad | null
  interno: boolean
  observaciones: string | null
  carrera: number | Carrera | null
}

export default defineComponent({
  name: 'VoluntarioDetailModal',
  props: {
    show: { type: Boolean, required: true },
    voluntario: { type: Object as PropType<Voluntario | null>, default: null },
    localidades: { type: Array as PropType<Localidad[]>, default: () => [] },
    carreras: { type: Array as PropType<Carrera[]>, default: () => [] }
  },
  emits: ['close', 'edit'],
  data() {
    return {
      loadingObservaciones: false,
      errorObservaciones: null as string | null,
      observacionesAsistencia: [] as string[]
    }
  },
  watch: {
    show(newValue) {
      if (newValue && this.voluntario) {
        this.fetchObservacionesAsistencia(this.voluntario.id)
      } else {
        // Clear data when modal is hidden
        this.observacionesAsistencia = []
        this.errorObservaciones = null
      }
    }
  },
  methods: {
    async fetchObservacionesAsistencia(voluntarioId: number) {
      this.loadingObservaciones = true
      this.errorObservaciones = null
      try {
        const response = await personaAPI.getObservacionesAsistencia(voluntarioId)
        this.observacionesAsistencia = response.data
      } catch (err: any) {
        this.errorObservaciones = err.response?.data?.detail || 'Error al cargar las observaciones de asistencia.'
      } finally {
        this.loadingObservaciones = false
      }
    },
    close() {
      this.$emit('close')
    },
    formatDate(dateString: string): string {
      try {
        return new Date(dateString).toLocaleDateString('es-ES', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      } catch {
        return dateString
      }
    },
    getLocalidadName(localidadId: number): string {
      const loc = this.localidades?.find?.((l: Localidad) => l.id === localidadId)
      return loc ? loc.nombre : `ID ${localidadId}`
    },
    getCarreraName(carreraId: number): string {
      const car = this.carreras?.find?.((c: Carrera) => c.id === carreraId)
      return car ? car.nombre : `ID ${carreraId}`
    },
    getCompleteLocation(localidad: number | Localidad | null): string {
      if (!localidad) return 'No especificada'

      // If it's just an ID, try to find the localidad in the list
      if (typeof localidad === 'number') {
        const loc = this.localidades?.find?.((l: Localidad) => l.id === localidad)
        if (loc) {
          return this.buildLocationString(loc)
        }
        return `ID ${localidad}`
      }

      // If it's an object, build the location string
      if (typeof localidad === 'object') {
        return this.buildLocationString(localidad)
      }

      return 'No especificada'
    },
    buildLocationString(localidad: Localidad): string {
      const parts = [localidad.nombre]

      if (localidad.departamento) {
        parts.push(localidad.departamento.nombre)

        if (localidad.departamento.provincia) {
          parts.push(localidad.departamento.provincia.nombre)

          if (localidad.departamento.provincia.pais) {
            parts.push(localidad.departamento.provincia.pais.nombre)
          }
        }
      }

      return parts.join(', ')
    }
  }
})
</script>

<style scoped>
.modal { background: rgba(0, 0, 0, 0.5); }

.avatar-large {
  width: 80px;
  height: 80px;
}

.card {
  border: 1px solid #e9ecef;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding: 0.75rem 1rem;
}

.card-header h6 {
  color: #495057;
  font-weight: 600;
}

.form-label.small {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.badge.bg-outline-secondary {
  color: #6c757d;
  border: 1px solid #6c757d;
  background-color: transparent;
}
</style>
