<!-- src/views/delegado/AsistenciaManagement.vue -->
<template>
  <div class="asistencia-management">
    <AppNavBar />

    <div class="container py-4">
      <!-- Header -->
      <div class="mb-4">
        <button class="btn btn-outline-secondary mb-3" @click="goBack">
          <i class="bi bi-arrow-left me-2"></i>Volver a Turnos
        </button>
        
        <div class="card bg-light border-0 mb-3">
          <div class="card-body">
            <h2 class="mb-3">
              <i class="bi bi-clipboard-check text-primary me-2"></i>
              Gestión de Asistencia
            </h2>
            <div v-if="turno && voluntariado" class="turno-info">
              <p class="mb-1"><strong>Voluntariado:</strong> {{ voluntariado.nombre }}</p>
              <p class="mb-1"><strong>Fecha:</strong> {{ formatDate(turno.fecha) }}</p>
              <p class="mb-0"><strong>Horario:</strong> {{ formatTime(turno.hora_inicio) }} - {{ formatTime(turno.hora_fin) }}</p>
              <p v-if="turno.lugar" class="mb-0"><strong>Lugar:</strong> {{ turno.lugar }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions + Table -->
      <div>
        <!-- Save button -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4>Voluntarios Inscritos ({{ inscripciones.length }})</h4>
          <button 
            class="btn btn-primary"
            @click="saveAsistencia"
            :disabled="saving || loading || inscripciones.length === 0"
          >
            <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-save me-2"></i>
            {{ saving ? 'Guardando...' : 'Guardar Asistencia' }}
          </button>
        </div>

        <!-- Asistencia table using AdminTable -->
        <AdminTable
          :title="`Asistencia del Turno`"
          :columns="columns"
          :items="inscripciones"
          item-key="id"
          :loading="loading"
          :error="error ?? undefined"
          empty-text="No hay voluntarios inscritos en este turno."
          :show-create-button="false"
          :show-actions="false"
          :clickable-rows="false"
          :page-size="10"
          @retry="loadData"
        >
          <!-- Voluntario cell -->
          <template #cell-voluntario="{ item }">
            <div class="d-flex align-items-center">
              <div class="persona-avatar me-3">
                <i class="bi bi-person-fill"></i>
              </div>
              <div>
                <div class="fw-bold">
                  {{ getVoluntarioName(item) }}
                </div>
                <small class="text-muted">
                  {{ getVoluntarioEmail(item) }}
                </small>
              </div>
            </div>
          </template>

          <!-- Presente checkbox -->
          <template #cell-presente="{ item }">
            <div class="text-center">
              <div class="form-check d-inline-block">
                <input 
                  class="form-check-input"
                  type="checkbox"
                  :id="`presente-${item.id}`"
                  v-model="getAsistenciaData(item.id).presente"
                  @change="onPresenteChange(item.id)"
                >
                <label 
                  class="form-check-label visually-hidden" 
                  :for="`presente-${item.id}`"
                >
                  Presente
                </label>
              </div>
            </div>
          </template>

          <!-- Horas input -->
          <template #cell-horas="{ item }">
            <input 
              type="number"
              class="form-control form-control-sm"
              v-model.number="getAsistenciaData(item.id).horas"
              :disabled="!getAsistenciaData(item.id).presente"
              min="0"
              max="24"
              step="0.5"
              placeholder="0.0"
            >
          </template>

          <!-- Observaciones input -->
          <template #cell-observaciones="{ item }">
            <input 
              type="text"
              class="form-control form-control-sm"
              v-model="getAsistenciaData(item.id).observaciones"
              placeholder="Opcional"
            >
          </template>
        </AdminTable>

        <!-- Success message -->
        <div v-if="saveSuccess" class="alert alert-success mt-3" role="alert">
          <i class="bi bi-check-circle me-2"></i>
          Asistencia guardada exitosamente.
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import { voluntariadoAPI, asistenciaAPI, turnoAPI } from '@/services/api'

interface Inscripcion {
  id: number
  turno: number
  voluntario: {
    id: number
    nombre: string
    apellido: string
    email: string
  }
  estado: string
}

interface AsistenciaData {
  id?: number
  inscripcion_id: number
  presente: boolean
  horas: number | null
  observaciones: string
}

export default defineComponent({
  name: 'AsistenciaManagement',
  components: { AppNavBar, AdminTable },
  data() {
    return {
      loading: false as boolean,
      error: null as string | null,
      saving: false as boolean,
      saveSuccess: false as boolean,
      voluntariado: null as any,
      turno: null as any,
      inscripciones: [] as Inscripcion[],
      asistenciaMap: {} as Record<number, AsistenciaData>,
      columns: [
        { key: 'voluntario', label: 'Voluntario', sortable: false, align: 'left' },
        { key: 'presente', label: 'Presente', sortable: false, align: 'center' },
        { key: 'horas', label: 'Horas', sortable: false, align: 'left' },
        { key: 'observaciones', label: 'Observaciones', sortable: false, align: 'left' }
      ] as TableColumn[]
    }
  },
  computed: {
    voluntariadoId(): number {
      return parseInt(this.$route.params.voluntariadoId as string)
    },
    turnoId(): number {
      return parseInt(this.$route.params.turnoId as string)
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      this.error = null
      
      try {
        // Load voluntariado
        const voluntariadoRes = await voluntariadoAPI.getById(this.voluntariadoId)
        this.voluntariado = voluntariadoRes.data

        // Load turno
        const turnoRes = await turnoAPI.getById(this.turnoId)
        this.turno = turnoRes.data

        // Load inscripciones for this turno
        const inscripcionesRes = await voluntariadoAPI.getInscripcionesByTurno(this.turnoId)
        this.inscripciones = Array.isArray(inscripcionesRes.data) 
          ? inscripcionesRes.data 
          : (inscripcionesRes.data.results || [])

        // Load existing asistencia records
        await this.loadAsistencia()
      } catch (err: any) {
        console.error('Error loading data:', err)
        this.error = err?.response?.data?.detail || 'Error al cargar los datos'
      } finally {
        this.loading = false
      }
    },

    async loadAsistencia() {
      try {
        // Get all asistencia records for this turno
        const asistenciaRes = await asistenciaAPI.getByTurno(this.turnoId)
        const asistenciaRecords = Array.isArray(asistenciaRes.data)
          ? asistenciaRes.data
          : (asistenciaRes.data.results || [])

        // Initialize asistencia map
        this.inscripciones.forEach(inscripcion => {
          const existing = asistenciaRecords.find((a: any) => a.inscripcion === inscripcion.id)
          
          this.asistenciaMap[inscripcion.id] = existing
            ? {
                id: existing.id,
                inscripcion_id: inscripcion.id,
                presente: existing.presente,
                horas: existing.horas,
                observaciones: existing.observaciones || ''
              }
            : {
                inscripcion_id: inscripcion.id,
                presente: false,
                horas: null,
                observaciones: ''
              }
        })
      } catch (err: any) {
        console.error('Error loading asistencia:', err)
        // Initialize with default values if error
        this.inscripciones.forEach(inscripcion => {
          this.asistenciaMap[inscripcion.id] = {
            inscripcion_id: inscripcion.id,
            presente: false,
            horas: null,
            observaciones: ''
          }
        })
      }
    },

    getAsistenciaData(inscripcionId: number): AsistenciaData {
      if (!this.asistenciaMap[inscripcionId]) {
        this.asistenciaMap[inscripcionId] = {
          inscripcion_id: inscripcionId,
          presente: false,
          horas: null,
          observaciones: ''
        }
      }
      return this.asistenciaMap[inscripcionId]
    },

    onPresenteChange(inscripcionId: number) {
      const data = this.getAsistenciaData(inscripcionId)
      if (!data.presente) {
        // If marking as absent, clear hours
        data.horas = null
      }
    },

    async saveAsistencia() {
      this.saving = true
      this.saveSuccess = false
      this.error = null

      try {
        const promises = Object.values(this.asistenciaMap).map(async (data) => {
          const payload = {
            inscripcion: data.inscripcion_id,
            presente: data.presente,
            horas: data.presente ? data.horas : null,
            observaciones: data.observaciones || null
          }

          if (data.id) {
            // Update existing
            return asistenciaAPI.update(data.id, payload)
          } else {
            // Create new
            return asistenciaAPI.create(payload)
          }
        })

        await Promise.all(promises)
        this.saveSuccess = true
        
        // Reload to get updated IDs
        await this.loadAsistencia()

        // Hide success message after 3 seconds
        setTimeout(() => {
          this.saveSuccess = false
        }, 3000)
      } catch (err: any) {
        console.error('Error saving asistencia:', err)
        this.error = err?.response?.data?.detail || 'Error al guardar la asistencia'
      } finally {
        this.saving = false
      }
    },

    goBack() {
      this.$router.push({
        name: 'DelegadoTurnosManagement',
        params: { id: this.voluntariadoId }
      })
    },

    getVoluntarioName(inscripcion: Inscripcion): string {
      const vol = inscripcion.voluntario
      return vol ? `${vol.nombre ?? ''} ${vol.apellido ?? ''}`.trim() || 'Sin nombre' : 'Sin nombre'
    },

    getVoluntarioEmail(inscripcion: Inscripcion): string {
      return inscripcion.voluntario?.email || ''
    },

    formatDate(date: string): string {
      try {
        const d = new Date(date)
        return d.toLocaleDateString('es-AR', { 
          weekday: 'long', 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        })
      } catch {
        return date
      }
    },

    formatTime(time: string): string {
      try {
        const [hours, minutes] = time.split(':')
        return `${hours}:${minutes}`
      } catch {
        return time
      }
    }
  }
})
</script>

<style scoped>
.asistencia-management {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.turno-info {
  font-size: 0.95rem;
}

.turno-info p {
  margin-bottom: 0.5rem;
}

.persona-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
}

.form-check-input {
  width: 1.5rem;
  height: 1.5rem;
  cursor: pointer;
}

.form-check-input:checked {
  background-color: #198754;
  border-color: #198754;
}

.table td {
  vertical-align: middle;
}
</style>
