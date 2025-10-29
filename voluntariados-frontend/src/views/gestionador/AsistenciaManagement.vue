<!-- src/views/delegado/AsistenciaManagement.vue -->
<template>
  <div class="asistencia-management">
    <AppNavBar />

    <section class="page-header shared-hero">
      <div class="page-overlay"></div>
      <div class="container">
        <!-- Main header with stats -->
        <div class="turnos-header-content">
          <!-- Back button inside the card -->
          <div class="d-flex align-items-center mb-3">
            <button class="btn btn-outline-light back-button" @click="goBack">
              <i class="bi bi-arrow-left me-2"></i>Volver
            </button>
          </div>
          <div class="d-flex align-items-center justify-content-between flex-wrap gap-3">
            <div class="d-flex align-items-center">
              <i class="bi bi-calendar-event me-3 text-white" style="font-size: 2.5rem;"></i>
              <div>
                <h2 class=" mb-1">Gestión de Asistencia</h2>
                <p class="hero-subtitle mb-0" v-if="voluntariado">
                  {{ voluntariado.nombre }}
                </p>
              </div>
            </div>
          </div>

          <!-- Info footer -->
          <div class="mt-4 pt-3 border-top border-white border-opacity-25">
            <p class="mb-0 text-white-50">
              <i class="bi bi-calendar-event me-2"></i>
              <strong>Fecha:</strong> {{ formatDate(turno?.fecha) }}
            </p>
            <p class="mb-0 text-white-50">
              <i class="bi bi-clock-fill me-2"></i>
              <strong>Horario:</strong> {{ formatTime(turno?.hora_inicio) }} - {{ formatTime(turno?.hora_fin) }}
            </p>
            <p v-if="turno?.lugar" class="mb-0 text-white-50">
              <i class="bi bi-geo-alt-fill me-2"></i>
              <strong>Lugar:</strong> {{ turno?.lugar }}
            </p> 
          </div>
        </div>
      </div>
    </section>

    <div class="container py-4">

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
            <div class="d-flex gap-1 align-items-center">
              <input
                type="number"
                class="form-control form-control-sm text-end"
                style="width: 4.5rem;"
                v-model.number="getAsistenciaData(item.id).horas_h"
                :disabled="!getAsistenciaData(item.id).presente"
                min="0"
                step="1"
                placeholder="hh"
              >
              <span class="mx-1">:</span>
              <select
                class="form-select form-select-sm"
                style="width: 4.2rem;"
                v-model.number="getAsistenciaData(item.id).horas_m"
                :disabled="!getAsistenciaData(item.id).presente"
              >
                <option :value="0">00</option>
                <option :value="15">15</option>
                <option :value="30">30</option>
                <option :value="45">45</option>
              </select>
            </div>
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
  horas_h?: number | null
  horas_m?: number | null
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
        { key: 'horas', label: 'Horas y minutos', sortable: false, align: 'left' },
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
        const allInscripciones = Array.isArray(inscripcionesRes.data) 
          ? inscripcionesRes.data 
          : (inscripcionesRes.data.results || [])
        
        // Filter out cancelled inscriptions - only show active ones
        this.inscripciones = allInscripciones.filter((insc: Inscripcion) => 
          insc.estado !== 'CAN' && insc.estado !== 'CANCELADO'
        )

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
          if (existing) {
            // convert float horas to hours/minutes
            const horasFloat = Number(existing.horas ?? 0)
            const totalMinutes = Math.round((isNaN(horasFloat) ? 0 : horasFloat) * 60)
            const hh = Math.floor(totalMinutes / 60)
            const mm = totalMinutes % 60

            this.asistenciaMap[inscripcion.id] = {
              id: existing.id,
              inscripcion_id: inscripcion.id,
              presente: existing.presente,
              horas: existing.horas,
              horas_h: hh,
              horas_m: mm,
              observaciones: existing.observaciones || ''
            }
          } else {
            this.asistenciaMap[inscripcion.id] = {
              inscripcion_id: inscripcion.id,
              presente: false,
              horas: null,
              horas_h: null,
              horas_m: null,
              observaciones: ''
            }
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
          horas_h: null,
          horas_m: null,
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
          horas_h: d.horas_h ?? null,
          horas_m: d.horas_m ?? null,
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
          // Set default horas to turno duration (rounded to nearest 15 minutes)
          if ((d.horas_h == null && d.horas_m == null) || (d.horas_h === 0 && (d.horas_m == null || d.horas_m === 0))) {
            const dur = this.getTurnoDurationHours() ?? 1
            let totalMinutes = Math.round(dur * 60)
            // Round to nearest 15 minutes
            totalMinutes = Math.round(totalMinutes / 15) * 15
            let hh = Math.floor(totalMinutes / 60)
            let mm = totalMinutes % 60
            if (mm === 60) { hh += 1; mm = 0 }
            d.horas_h = hh
            d.horas_m = mm
            d.horas = Math.round(((hh * 60 + mm) / 60) * 100) / 100
          }
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
        // If marking as absent, clear hours fields
        data.horas = null
        data.horas_h = null
        data.horas_m = null
      }
    },

    async saveAsistencia() {
      this.saving = true
      this.saveSuccess = false
      this.error = null

      // Clear previous per-row errors
      Object.values(this.asistenciaMap).forEach((d: any) => { d._error = '' })

      // Validation: if presente === true, horas (hours+minutes) must be provided and > 0 minutes
      let valid = true
      Object.values(this.asistenciaMap).forEach((d: any) => {
        if (d.presente) {
          const hh = Number(d.horas_h ?? 0)
          const mm = Number(d.horas_m ?? 0)
          const totalMinutes = (isNaN(hh) ? 0 : hh * 60) + (isNaN(mm) ? 0 : mm)
          if (totalMinutes <= 0) {
            d._error = 'Ingrese una duración válida (> 0 minutos)'
            valid = false
          } else if (![0,15,30,45].includes(mm)) {
            d._error = 'Minutos debe ser 0, 15, 30 o 45'
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
          // compute float hours from horas_h and horas_m
          let horasFloat = null as number | null
          if (data.presente) {
            const hh = Number(data.horas_h ?? 0)
            const mm = Number(data.horas_m ?? 0)
            const totalMinutes = (isNaN(hh) ? 0 : hh * 60) + (isNaN(mm) ? 0 : mm)
            horasFloat = Math.round((totalMinutes / 60) * 100) / 100
          }

          const payload = {
            inscripcion: data.inscripcion_id,
            presente: data.presente,
            horas: data.presente ? horasFloat : null,
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

.back-button {
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-weight: 500;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}


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
