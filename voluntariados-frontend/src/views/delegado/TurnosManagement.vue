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
        <div>
          <h2 class="mb-0">Gestión de Turnos</h2>
          <p class="text-muted mb-0" v-if="voluntariado">{{ voluntariado.nombre }}</p>
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

      <!-- Turnos list -->
      <div v-else>
        <div v-if="turnos.length === 0" class="alert alert-info">
          <i class="bi bi-info-circle me-2"></i>
          No hay turnos programados para este voluntariado.
        </div>

        <div v-else class="row g-3">
          <div v-for="turno in turnos" :key="turno.id" class="col-md-6 col-lg-4">
            <div 
              class="card turno-card h-100" 
              :class="{ 'border-primary': selectedTurno?.id === turno.id }"
              @click="selectTurno(turno)"
              role="button"
            >
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <div class="turno-icon">
                    <i class="bi bi-calendar-check text-primary"></i>
                  </div>
                  <span class="badge" :class="getTurnoBadgeClass(turno)">
                    {{ getTurnoStatus(turno) }}
                  </span>
                </div>

                <h5 class="card-title">{{ formatDate(turno.fecha) }}</h5>
                
                <div class="turno-details">
                  <div class="detail-row">
                    <i class="bi bi-clock text-muted me-2"></i>
                    <span>{{ formatTime(turno.hora_inicio) }} - {{ formatTime(turno.hora_fin) }}</span>
                  </div>
                  
                  <div class="detail-row" v-if="turno.lugar">
                    <i class="bi bi-geo-alt text-muted me-2"></i>
                    <span>{{ turno.lugar }}</span>
                  </div>

                  <div class="detail-row">
                    <i class="bi bi-people text-muted me-2"></i>
                    <span>{{ getInscriptosCount(turno) }} / {{ turno.cupo }} inscriptos</span>
                  </div>
                </div>

                <button 
                  class="btn btn-primary btn-sm w-100 mt-3"
                  @click.stop="viewAsistencia(turno)"
                >
                  <i class="bi bi-clipboard-check me-2"></i>
                  Gestionar Asistencia
                </button>
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
import AppNavBar from '@/components/Navbar.vue'
import { voluntariadoAPI } from '@/services/api'

interface Turno {
  id: number
  fecha: string
  hora_inicio: string
  hora_fin: string
  cupo: number
  lugar?: string
  inscripciones_count?: number
}

interface Voluntariado {
  id: number
  nombre: string
}

export default defineComponent({
  name: 'TurnosManagement',
  components: { AppNavBar },
  data() {
    return {
      loading: false as boolean,
      error: null as string | null,
      voluntariado: null as Voluntariado | null,
      turnos: [] as Turno[],
      selectedTurno: null as Turno | null
    }
  },
  computed: {
    voluntariadoId(): number {
      return parseInt(this.$route.params.id as string)
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
        // time is in HH:MM:SS format
        const [hours, minutes] = time.split(':')
        return `${hours}:${minutes}`
      } catch {
        return time
      }
    },

    getInscriptosCount(turno: Turno): number {
      return turno.inscripciones_count ?? 0
    },

    getTurnoStatus(turno: Turno): string {
      const now = new Date()
      const turnoDate = new Date(turno.fecha)
      
      if (turnoDate > now) {
        return 'Próximo'
      } else if (turnoDate.toDateString() === now.toDateString()) {
        return 'Hoy'
      } else {
        return 'Finalizado'
      }
    },

    getTurnoBadgeClass(turno: Turno): string {
      const now = new Date()
      const turnoDate = new Date(turno.fecha)
      
      if (turnoDate > now) {
        return 'bg-info'
      } else if (turnoDate.toDateString() === now.toDateString()) {
        return 'bg-warning'
      } else {
        return 'bg-secondary'
      }
    }
  }
})
</script>

<style scoped>
.turnos-management {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.turno-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.turno-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.turno-card.border-primary {
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
}

.turno-icon {
  width: 48px;
  height: 48px;
  background: rgba(13, 110, 253, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.turno-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1rem;
}

.detail-row {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.detail-row i {
  width: 20px;
}
</style>
