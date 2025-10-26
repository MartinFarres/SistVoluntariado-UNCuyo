<!-- src/views/delegado/TurnosManagement.vue -->
<template>
  <div class="turnos-management">
    <AppNavBar />

    <div class="container py-4">
      <!-- Header with back button -->
      <div class="d-flex align-items-center mb-3">
        <button class="btn btn-outline-secondary me-3" @click="goBack">
          <i class="bi bi-arrow-left me-2"></i>Volver
        </button>
      </div>

      <!-- Big header with stats (style matched to AprobarInscriptos) -->
      <div class="aprobar-header mb-4">
        <div class="d-flex align-items-center justify-content-between">
          <div class="d-flex align-items-center">
            <i class="bi bi-calendar-event me-3 text-white" style="font-size: 1.8rem;"></i>
            <div>
              <h2 class="mb-0 text-white">Gestión de Turnos</h2>
              <p class="mb-0 text-white-50" v-if="voluntariado">{{ voluntariado.nombre }}</p>
            </div>
          </div>
          <!-- Stats badges -->
          <div class="d-flex gap-2">
            <span
              class="badge bg-white text-success fs-6 px-3 py-2"
              :class="{ 'badge-active': badgeFilter === 'completed' }"
              @click="onBadgeClick('completed')"
              role="button"
            >
              <i class="bi bi-check-circle me-2"></i>
              {{ turnosCompletedCount }} Completados
            </span>
            <span
              class="badge bg-white text-warning fs-6 px-3 py-2"
              :class="{ 'badge-active': badgeFilter === 'pending' }"
              @click="onBadgeClick('pending')"
              role="button"
            >
              <i class="bi bi-exclamation-circle me-2"></i>
              {{ turnosPendingCount }} Pendientes
            </span>
          </div>
        </div>
        <div class="mt-3 pt-3 border-top border-white border-opacity-25">
          <p class="mb-0 text-white">
            <i class="bi bi-info-circle me-2"></i>
            Revisa y gestiona las asistencias por turno desde este panel.
          </p>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="loadData">
          Reintentar
        </button>
      </div>

      <!-- Turnos list with calendar -->
      <div v-else>
        <div v-if="turnos.length === 0" class="alert alert-info">
          <i class="bi bi-info-circle me-2"></i>
          No hay turnos programados para este voluntariado.
        </div>

        <div v-else>
          <div class="row g-3">
            <!-- Calendar full width (add ref to scroll back) -->
            <div class="col-12">
              <div ref="calendarSection">
                <TurnosManagementCalendar
                  :turnos="turnos"
                  :selectedDate="selectedCalendarDate"
                  @date-selected="onDateSelected"
                />
              </div>
            </div>

            <!-- Turnos list under calendar -->
            <div class="col-12">
              <div ref="turnosSection">
                <div v-if="filteredTurnos.length === 0" class="alert alert-light">
                  <i class="bi bi-info-circle me-2"></i>
                  Seleccioná una fecha con turnos (no bloqueados) para ver y gestionar las asistencias.
                </div>

                <div v-else class="row g-3">
                  <div v-for="turno in filteredTurnos" :key="turno.id" class="col-md-6 col-lg-4">
                    <div
                      class="turno-card"
                      :class="{
                        'turno-full': isTurnoFull(turno),
                        'turno-enrolled': false,
                        'turno-completed': isTurnoCompleted(turno),
                        'turno-incomplete': !isTurnoCompleted(turno) && !isTurnoProximamente(turno),
                        'day-highlight': turno.fecha === selectedCalendarDate
                      }"
                      :data-fecha="turno.fecha"
                    >
                      <!-- Card Header with Day and Status Badge -->
                      <div class="turno-header">
                        <div class="turno-day-section">
                          <div class="turno-day">{{ formatTurnoDate(turno) }}</div>
                          <div class="turno-date-full">{{ formatTurnoFullDate(turno) }}</div>
                        </div>

                        <!-- Status Badge -->
                        <div class="turno-status-badge">
                          <span v-if="isTurnoCompleted(turno)" class="badge bg-secondary">
                            <i class="bi bi-dash-circle"></i> Finalizado
                          </span>
                          <span v-else-if="isTurnoProximamente(turno)" class="badge bg-warning text-dark">
                            <i class="bi bi-lock-fill"></i> Bloqueado
                          </span>
                          <span v-else class="badge bg-warning text-dark">
                            <i class="bi bi-calendar-check"></i> Pendiente
                          </span>
                        </div>
                      </div>

                      <!-- Card Body with Details -->
                      <div class="turno-body">
                        <div class="turno-info-row">
                          <i class="bi bi-clock-fill text-primary"></i>
                          <span>{{ formatTime(turno.hora_inicio) }} - {{ formatTime(turno.hora_fin) }}</span>
                        </div>

                        <div class="turno-info-row">
                          <i class="bi bi-people-fill text-success"></i>
                          <span v-if="turno.inscripciones_count !== undefined">
                            <strong>{{ turno.inscripciones_count }}/{{ turno.cupo }}</strong> inscriptos
                          </span>
                          <span v-else>
                            <strong>{{ turno.cupo }}</strong> cupos disponibles
                          </span>
                        </div>
                      </div>

                      <!-- Card Footer with Action Button -->
                      <div class="turno-footer">
                        <!-- Only block future turnos. Finalizados should still allow editing of asistencia. -->
                        <button
                          v-if="isTurnoProximamente(turno)"
                          class="btn btn-sm btn-warning w-100"
                          disabled
                        >
                          <i class="bi bi-lock"></i> No Disponible
                        </button>

                        <button
                          v-else
                          :class="['btn btn-sm w-100', isTurnoCompleted(turno) ? 'btn-outline-secondary' : 'btn-primary']"
                          @click="viewAsistencia(turno)"
                        >
                          <i class="bi bi-clipboard-check me-2"></i>
                          {{ isTurnoCompleted(turno) ? 'Editar Asistencia' : 'Gestionar Asistencia' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { parseLocalDate, formatDateLong, formatDateShort, getWeekdayName } from '@/utils/dateUtils'
import AppNavBar from '@/components/Navbar.vue'
import { voluntariadoAPI } from '@/services/api'
import TurnosManagementCalendar from '@/components/delegado/TurnosManagementCalendar.vue'

interface Turno {
  id: number
  fecha: string
  hora_inicio?: string
  hora_fin?: string
  cupo: number
  lugar?: string
  inscripciones_count?: number
  // optional asistencia indicators
  asistencia_completa?: boolean
  asistencia?: { completa?: boolean } | null
}

interface Voluntariado {
  id: number
  nombre: string
}

export default defineComponent({
  name: 'TurnosManagement',
  components: { AppNavBar, TurnosManagementCalendar },
  data() {
    return {
      loading: false as boolean,
      error: null as string | null,
      voluntariado: null as Voluntariado | null,
      turnos: [] as Turno[],
      selectedTurno: null as Turno | null,
      selectedCalendarDate: null as string | null,
      // filter applied by header badges: 'all' | 'completed' | 'pending' | null
      badgeFilter: null as string | null
    }
  },
  computed: {
    voluntariadoId(): number {
      return parseInt(this.$route.params.id as string)
    },
    filteredTurnos(): Turno[] {
      // If a badge filter is active, show all matching turnos
      if (this.badgeFilter === 'completed') {
        return this.turnos.filter(t => this.isTurnoCompleted(t) && this.isTurnoStarted(t))
      }
      if (this.badgeFilter === 'pending') {
        return this.turnos.filter(t => !this.isTurnoCompleted(t) && this.isTurnoStarted(t) && !this.isTurnoProximamente(t))
      }
  // Otherwise fall back to calendar selection
  if (!this.selectedCalendarDate) return []
  // When the user selects a date from the calendar we want to show all turnos
  // for that date (including 'Próximamente' ones). Actions will remain blocked
  // for not-started turnos via the card buttons.
  return this.turnos.filter(t => t.fecha === this.selectedCalendarDate)
    },
    // number of completed turnos (uses backend canonical field when available)
    turnosCompletedCount(): number {
      return this.turnos.filter(t => this.isTurnoCompleted(t) && this.isTurnoStarted(t)).length
    },
    // pending = not completed and not in the future
    turnosPendingCount(): number {
      return this.turnos.filter(t => !this.isTurnoCompleted(t) && this.isTurnoStarted(t) && !this.isTurnoProximamente(t)).length
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
        // Load voluntariado details
        const voluntariadoRes = await voluntariadoAPI.getById(this.voluntariadoId)
        this.voluntariado = voluntariadoRes.data

        // Load turnos for this voluntariado
        const turnosRes = await voluntariadoAPI.getTurnos(this.voluntariadoId)
        this.turnos = Array.isArray(turnosRes.data) ? turnosRes.data : []
      } catch (err: any) {
        console.error('Error loading turnos:', err)
        this.error = err?.response?.data?.detail || 'Error al cargar los turnos'
      } finally {
        this.loading = false
      }
    },

    onDateSelected(dateString: string) {
      // Toggle selection same as VoluntariadoDetail behavior
      if (this.selectedCalendarDate === dateString) {
        this.selectedCalendarDate = null
      } else {
        this.selectedCalendarDate = dateString
      }
      // clear any badge filter when selecting a calendar date
      this.badgeFilter = null
      // clear selected turno when changing date
      this.selectedTurno = null
      // scroll to the turnos list and highlight the selected day's turnos
      this.scrollToSelectedDateTurnos()
    },

    onBadgeClick(filter: string) {
      // Toggle filter: clicking same filter clears it
      if (this.badgeFilter === filter) {
        this.badgeFilter = null
      } else {
        this.badgeFilter = filter
      }
      // clear calendar selection
      this.selectedCalendarDate = null
      this.selectedTurno = null
      // scroll to the turnos list
      this.scrollToTurnosSection()
    },

    scrollToTurnosSection() {
      this.$nextTick(() => {
        const turnosSection = (this.$refs.turnosSection as HTMLElement | undefined)
        const calendarSection = (this.$refs.calendarSection as HTMLElement | undefined)
        if (turnosSection && typeof turnosSection.scrollIntoView === 'function') {
          turnosSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
        } else if (calendarSection && typeof calendarSection.scrollIntoView === 'function') {
          calendarSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      })
    },

    scrollToSelectedDateTurnos() {
      // after DOM updates, scroll to first turno of the selected date
      this.$nextTick(() => {
        const selected = this.selectedCalendarDate
        const turnosSection = (this.$refs.turnosSection as HTMLElement | undefined)
        const calendarSection = (this.$refs.calendarSection as HTMLElement | undefined)
        if (!selected) {
          // if deselect, scroll back to calendar
          if (calendarSection && typeof calendarSection.scrollIntoView === 'function') {
            calendarSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
          return
        }

        if (!turnosSection) return
        const selector = `.turno-card[data-fecha="${selected}"]`
        const first = turnosSection.querySelector(selector) as HTMLElement | null
        if (first) {
          first.scrollIntoView({ behavior: 'smooth', block: 'start' })
          // flash outline for a moment
          first.classList.add('flash-highlight')
          setTimeout(() => first.classList.remove('flash-highlight'), 1200)
        } else {
          // fallback: scroll the whole section into view
          if (typeof turnosSection.scrollIntoView === 'function') {
            turnosSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        }
      })
    },

    selectTurno(turno: Turno) {
      this.selectedTurno = turno
    },

    viewAsistencia(turno: Turno) {
      this.$router.push({
        name: 'DelegadoAsistenciaManagement',
        params: {
          voluntariadoId: this.voluntariadoId,
          turnoId: turno.id
        }
      })
    },

    goBack() {
      this.$router.push('/area-personal/gestionador')
    },

    // Use dateUtils to format dates consistently and avoid timezone issues

    formatTime(time?: string): string {
      try {
        if (!time) return ''
        const [hours, minutes] = time.split(':')
        return `${hours}:${minutes}`
      } catch {
        return time ?? ''
      }
    },

    formatDateDisplay(date: string): string {
      try {
        return formatDateLong(date)
      } catch {
        return date
      }
    },

    getInscriptosCount(turno: Turno): number {
      return turno.inscripciones_count ?? 0
    },

    getTurnoStatus(turno: Turno): string {
      const now = new Date()
      const turnoDate = parseLocalDate(turno.fecha)
      if (turnoDate.getTime() > now.getTime()) {
        return 'Próximo'
      } else if (turnoDate.toDateString() === now.toDateString()) {
        return 'Hoy'
      } else {
        return 'Finalizado'
      }
    },

    getTurnoBadgeClass(turno: Turno): string {
      const now = new Date()
      const turnoDate = parseLocalDate(turno.fecha)
      if (turnoDate.getTime() > now.getTime()) {
        return 'bg-info'
      } else if (turnoDate.toDateString() === now.toDateString()) {
        return 'bg-warning'
      } else {
        return 'bg-secondary'
      }
    },

    // Whether the turno is full (based on inscripciones_count vs cupo)
    isTurnoFull(turno: Turno): boolean {
      const inscritos = this.getInscriptosCount(turno)
      return turno.cupo > 0 && inscritos >= turno.cupo
    },

    // Small helpers to format the turno date similarly to VoluntariadoDetail
    formatTurnoDate(turno: Turno): string {
      try {
        const weekday = getWeekdayName(turno.fecha)
        const short = formatDateShort(turno.fecha)
        return `${weekday} ${short}`
      } catch {
        return turno.fecha
      }
    },

    formatTurnoFullDate(turno: Turno): string {
      try {
        return formatDateLong(turno.fecha)
      } catch {
        return turno.fecha
      }
    },

    // Prefer canonical backend field `asistencia_completa`. Keep safe legacy fallbacks.
    isTurnoCompleted(turno: Turno): boolean {
      if (turno == null) return false
      if (typeof (turno as any).asistencia_completa !== 'undefined') return !!(turno as any).asistencia_completa
      // legacy nested asistencia
      if ((turno as any).asistencia) {
        const a = (turno as any).asistencia
        return !!(a.completa || a.presente)
      }
      // legacy numeric comparison
      if ((turno as any).asistencias_registradas != null && typeof (turno as any).inscripciones_count !== 'undefined') {
        return (turno as any).asistencias_registradas >= (turno as any).inscripciones_count
      }
      if ((turno as any).asistenciaCompleted !== undefined) return !!(turno as any).asistenciaCompleted
      return false
    },

    isTurnoProximamente(turno: Turno): boolean {
      const today = new Date()
      today.setHours(0,0,0,0)
      const turnoDate = parseLocalDate(turno.fecha)
      return turnoDate.getTime() > today.getTime()
    },


    // Determine if a turno has already started (based on hora_inicio when available)
    isTurnoStarted(turno: Turno): boolean {
      try {
        const now = new Date()
        // If hora_inicio is provided, use datetime comparison
        if (turno.hora_inicio) {
          const dt = new Date(`${turno.fecha}T${turno.hora_inicio}`)
          if (!isNaN(dt.getTime())) {
            return dt.getTime() <= now.getTime()
          }
        }
        // Fallback: consider started if the turno date is today or in the past
        const d = parseLocalDate(turno.fecha)
        d.setHours(23,59,59,999)
        return d.getTime() <= now.getTime()
      } catch {
        return false
      }
    },
  }
})
</script>

<style scoped>
/* ...existing code... */
.turnos-management {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* keep existing styles, plus small adjustments for calendar layout */
@media (max-width: 767px) {
  .turnos-management .col-md-4,
  .turnos-management .col-md-8 {
    padding-left: 0;
    padding-right: 0;
  }
}

/* Constrain turno cards so they don't become too wide on large screens.
   Keep them centered inside their column. */
.turno-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 2px solid #e9ecef;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 820px;
  margin: 0 auto;
  width: 100%;
}

/* Slight lift on hover to match VoluntariadoDetail */
.turno-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(139, 0, 0, 0.15);
  border-color: #8b0000;
}

/* Full / enrolled variants keep subtle backgrounds but still white base */
.turno-card.turno-full {
  background: #f8f9fa;
  border-color: #dee2e6;
  opacity: 0.95;
}

.turno-card.turno-enrolled {
  border-color: #28a745;
  background: linear-gradient(to bottom, #ffffff 0%, #f8fff9 100%);
}

/* Header / day styles copied from VoluntariadoDetail for parity */
.turno-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dee2e6;
}

.turno-day-section { flex: 1; }

.turno-day {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  text-transform: capitalize;
  margin-bottom: 0.25rem;
}

.turno-date-full {
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 500;
}

.turno-status-badge { flex-shrink: 0; }

.turno-body {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.turno-info-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #495057;
  font-size: 0.9rem;
}

.turno-info-row i { font-size: 1.1rem; width: 20px; text-align: center; flex-shrink: 0; }

.turno-info-row strong { color: #2c3e50; font-weight: 700; }

.turno-footer { padding: 0 1.25rem 1.25rem 1.25rem; margin-top: auto; }

.turno-footer .btn { font-size: 0.9rem; font-weight: 600; padding: 0.6rem 1rem; border-radius: 8px; transition: all 0.2s ease; }

.turno-footer .btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }

/* Keep highlight and flash behavior */
.turno-card.day-highlight {
  border-color: #0d6efd !important;
  box-shadow: 0 6px 20px rgba(13,110,253,0.08);
  /* Keep background white for consistency */
  background: white;
}

.flash-highlight {
  outline: 3px solid rgba(13,110,253,0.18);
  transition: outline 0.18s ease;
}

/* Instead of coloring the full background, apply a colored left edge to indicate state */
.turno-card.turno-incomplete {
  background: white; /* keep card white */
  /* make full outline yellow with uniform thickness */
  border: 3px solid #ffca2c;
  color: #2c3e50;
}

.turno-card.turno-completed {
  background: white; /* keep card white */
  /* full outline gray for completed */
  border: 3px solid #ced4da;
  color: #6c757d;
}

/* If a pendiente (incomplete) card is selected, keep its outline yellow instead of blue */
.turno-card.turno-incomplete.day-highlight {
  border-color: #ffca2c !important;
  box-shadow: 0 6px 20px rgba(255, 202, 44, 0.12);
  background: white;
}

@media (max-width: 991px) {
  .turno-card { max-width: 100%; }
}

/* Header style similar to AprobarInscriptos for parity */
.aprobar-header {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%);
  padding: 1.25rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 6px 12px rgba(13, 110, 253, 0.12);
}
.aprobar-header .badge {
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

@media (max-width: 768px) {
  .aprobar-header .d-flex.gap-2 { flex-direction: column; align-items: stretch !important; }
  .aprobar-header .badge { text-align: center; }
}
/* active badge visual */
.aprobar-header .badge.badge-active {
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
  transform: translateY(-2px);
}
</style>