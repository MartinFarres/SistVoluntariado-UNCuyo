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
        <!-- Save button + quick actions -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="mb-0">Voluntarios Inscritos ({{ inscripciones.length }})</h4>
            <small class="text-muted">Presentes: <strong>{{ presentCount }}</strong></small>
          </div>

          <div class="d-flex gap-2">
            <div class="btn-group me-2" role="group" aria-label="Marcar presentes">
              <button class="btn btn-sm btn-outline-success" @click="markAllPresent" :disabled="inscripciones.length === 0">Marcar todos presentes</button>
              <button class="btn btn-sm btn-outline-secondary" @click="markAllAbsent" :disabled="inscripciones.length === 0">Marcar todos ausentes</button>
            </div>

            <button 
              class="btn btn-primary"
              @click="saveAsistencia"
              :disabled="saving || loading || inscripciones.length === 0 || !hasChanges"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-save me-2"></i>
              {{ saving ? 'Guardando...' : 'Guardar Asistencia' }}
            </button>
          </div>
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
            <div v-if="asistenciaMap[item.id]?._error" class="form-text text-danger mt-1">
              {{ asistenciaMap[item.id]?._error }}
            </div>
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
  _error?: string
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
  initialAsistenciaSnapshot: '' as string,
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
    ,
    presentCount(): number {
      return Object.values(this.asistenciaMap).filter((d: any) => d && d.presente).length
    },
    hasChanges(): boolean {
      try {
        const current = this.snapshotAsistencia()
        return current !== (this.initialAsistenciaSnapshot || '')
      } catch {
        return true
      }
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
        // capture initial snapshot to detect changes
        this.initialAsistenciaSnapshot = this.snapshotAsistencia()
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
        // even on error, set initial snapshot
        this.initialAsistenciaSnapshot = this.snapshotAsistencia()
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
      // ensure error field exists
      if (!this.asistenciaMap[inscripcionId]._error) this.asistenciaMap[inscripcionId]._error = ''
      return this.asistenciaMap[inscripcionId]
    },

    // Create a small JSON snapshot only containing meaningful fields to detect changes
    snapshotAsistencia(): string {
      try {
        const arr = Object.values(this.asistenciaMap).map((d: any) => ({
          inscripcion_id: d.inscripcion_id,
          presente: !!d.presente,
          horas: d.horas,
          observaciones: d.observaciones || ''
        }))
        return JSON.stringify(arr)
      } catch {
        return ''
      }
    },

    markAllPresent() {
      this.inscripciones.forEach(i => {
        const d = this.getAsistenciaData(i.id)
        d.presente = true
        if (d.horas == null || d.horas === 0) d.horas = this.getTurnoDurationHours() ?? 1
        d._error = ''
      })
    },

    getTurnoDurationHours(): number | null {
      try {
        // Prefer backend-provided duration if available on this.turno
        if (this.turno && (this.turno.duracion_horas || this.turno.duracion_horas === 0)) {
          return Number(this.turno.duracion_horas)
        }
        // Fallback: compute from hora_inicio / hora_fin strings
        const hi = this.turno?.hora_inicio
        const hf = this.turno?.hora_fin
        if (!hi || !hf) return null
        const parse = (v: any) => {
          if (typeof v === 'string') {
            const parts = v.split(':')
            const h = parseInt(parts[0] || '0', 10)
            const m = parseInt(parts[1] || '0', 10)
            const s = parseInt(parts[2] || '0', 10)
            return { h, m, s }
          }
          if (v instanceof Date) return { h: v.getHours(), m: v.getMinutes(), s: v.getSeconds() }
          return null
        }
        const t1 = parse(hi)
        const t2 = parse(hf)
        if (!t1 || !t2) return null
        const dt1 = new Date(2000,0,1,t1.h,t1.m,t1.s)
        let dt2 = new Date(2000,0,1,t2.h,t2.m,t2.s)
        if (dt2 < dt1) dt2 = new Date(dt2.getTime() + 24*3600*1000)
        const diff = (dt2.getTime() - dt1.getTime())/1000/3600
        return Math.round(diff * 100) / 100
      } catch {
        return null
      }
    },

    markAllAbsent() {
      this.inscripciones.forEach(i => {
        const d = this.getAsistenciaData(i.id)
        d.presente = false
        d.horas = null
        d._error = ''
      })
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

      // Clear previous per-row errors
      Object.values(this.asistenciaMap).forEach((d: any) => { d._error = '' })

      // Validation: if presente === true, horas must be provided and > 0
      let valid = true
      Object.values(this.asistenciaMap).forEach((d: any) => {
        if (d.presente) {
          if (d.horas == null || Number(d.horas) <= 0) {
            d._error = 'Ingrese horas válidas (> 0)'
            valid = false
          }
        }
      })

      if (!valid) {
        this.error = 'Corrige los errores antes de guardar.'
        this.saving = false
        return
      }

      try {
        const entries = Object.values(this.asistenciaMap)
        const promises = entries.map((data: any) => {
          const payload = {
            inscripcion: data.inscripcion_id,
            presente: data.presente,
            horas: data.presente ? data.horas : null,
            observaciones: data.observaciones || null
          }

          if (data.id) return asistenciaAPI.update(data.id, payload)
          return asistenciaAPI.create(payload)
        })

        const results = await Promise.allSettled(promises)

        let anyFailed = false
        results.forEach((r: any, idx: number) => {
          if (r.status === 'rejected') {
            anyFailed = true
            const entry = entries[idx] as any
            if (!entry) return
            const inscId = entry.inscripcion_id
            const msg = r.reason?.response?.data?.detail || r.reason?.message || 'Error al guardar'
            if (this.asistenciaMap[inscId]) this.asistenciaMap[inscId]._error = String(msg)
          }
        })

        if (anyFailed) {
          this.error = 'Algunos registros no pudieron guardarse. Revisa los errores por fila.'
        } else {
          this.saveSuccess = true
          // Reload to get updated IDs and canonical data
          await this.loadAsistencia()
          // Update snapshot
          this.initialAsistenciaSnapshot = this.snapshotAsistencia()
          // Hide success message after 3 seconds
          setTimeout(() => { this.saveSuccess = false }, 3000)
        }
      } catch (err: any) {
        console.error('Error saving asistencia:', err)
        this.error = err?.response?.data?.detail || 'Error al guardar la asistencia'
      } finally {
        this.saving = false
      }
    },

    goBack() {
      this.$router.push({
        name: 'GestionadorTurnosManagement',
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
