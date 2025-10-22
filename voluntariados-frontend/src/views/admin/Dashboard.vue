<template>
  <AdminLayout
    page-title="Dashboard"
    :breadcrumbs="[{ label: 'Dashboard' }]"
  >
    <div class="dashboard-container">
      <!-- Stats Cards -->
      <div class="row g-4 mb-4">
      <div class="col-xl-3 col-md-6">
        <div class="stat-card card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="stat-label text-muted mb-2">Total Voluntarios</h6>
                <h2 class="stat-value mb-0">{{ stats.voluntarios }}</h2>
              </div>
              <div class="stat-icon bg-primary bg-opacity-10 p-3 rounded-3">
                <i class="bi bi-people-fill text-primary fs-3"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6">
        <div class="stat-card card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h6 class="stat-label text-muted mb-2">Facultad con más Voluntarios</h6>
                <h2 class="stat-value mb-0">{{ topFacultad.count }}</h2>
                <small class="text-muted d-block mt-1">{{ topFacultad.nombre }}</small>
              </div>
              <div class="stat-icon bg-info bg-opacity-10 p-3 rounded-3">
                <i class="bi bi-trophy-fill text-info fs-3"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6">
        <div class="stat-card card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="stat-label text-muted mb-2">Certificados Emitidos</h6>
                <h2 class="stat-value mb-0">{{ stats.certificados }}</h2>
              </div>
              <div class="stat-icon bg-warning bg-opacity-10 p-3 rounded-3">
                <i class="bi bi-award-fill text-warning fs-3"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4 mb-4">
      <!-- Próximos Voluntariados -->
      <div class="col-12">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0">
              <i class="bi bi-calendar-event me-2 text-primary"></i>
              Próximos Voluntariados
            </h5>
          </div>
          <div class="card-body p-0">
            <div v-if="loadingVoluntariadosProximos" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>
            <div v-else-if="proximosVoluntariados.length === 0" class="text-center py-5 text-muted">
              <i class="bi bi-calendar-x fs-1 d-block mb-2"></i>
              <p class="mb-0">No hay voluntariados próximos</p>
            </div>
            <div v-else class="list-group list-group-flush">
              <div
                v-for="vol in proximosVoluntariados"
                :key="vol.id"
                class="list-group-item list-group-item-action"
              >
                <div class="d-flex justify-content-between align-items-start">
                  <div class="flex-grow-1">
                    <div class="d-flex align-items-center mb-2">
                      <h6 class="mb-0 me-2 fw-semibold">{{ vol.nombre }}</h6>
                      <span
                        class="badge"
                        :class="{
                          'bg-warning': vol.estado === 'DRAFT',
                          'bg-success': vol.estado === 'ACTIVE',
                          'bg-secondary': vol.estado === 'CLOSED'
                        }"
                      >
                        {{ getEstadoLabel(vol.estado) }}
                      </span>
                    </div>
                    <div v-if="vol.fecha_inicio" class="mb-1">
                      <small class="text-muted">
                        <i class="bi bi-calendar3 me-1"></i>
                        {{ formatDate(vol.fecha_inicio) }}
                        <span v-if="vol.fecha_fin"> - {{ formatDate(vol.fecha_fin) }}</span>
                      </small>
                    </div>
                    <div v-if="vol.descripcion_data?.texto" class="mb-1">
                      <small class="text-muted d-block">{{ truncateText(vol.descripcion_data.texto, 80) }}</small>
                    </div>
                    <div v-if="vol.turno_data">
                      <small class="text-muted">
                        <i class="bi bi-clock me-1"></i>
                        {{ vol.turno_data.hora_inicio }} - {{ vol.turno_data.hora_fin }}
                      </small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Estadísticas por Facultad -->
    <div class="row g-4">
      <div class="col-xl-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0">
              <i class="bi bi-building me-2 text-info"></i>
              Voluntarios por Facultad
            </h5>
          </div>
          <div class="card-body">
            <div v-if="loadingFacultades" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>
            <div v-else-if="voluntariosPorFacultad.length === 0" class="text-center py-5 text-muted">
              <i class="bi bi-bar-chart fs-1 d-block mb-2"></i>
              <p class="mb-0">No hay datos disponibles</p>
            </div>
            <div v-else>
              <div
                v-for="facultad in voluntariosPorFacultad"
                :key="facultad.nombre"
                class="mb-4"
              >
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="fw-medium">{{ facultad.nombre }}</span>
                  <span class="badge bg-primary">{{ facultad.count }}</span>
                </div>
                <div class="progress" style="height: 10px;">
                  <div
                    class="progress-bar"
                    :style="{ width: facultad.porcentaje + '%' }"
                    role="progressbar"
                    :aria-valuenow="facultad.porcentaje"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0">
              <i class="bi bi-pie-chart me-2 text-warning"></i>
              Voluntariados por Estado
            </h5>
          </div>
          <div class="card-body">
            <div v-if="loadingVoluntariados" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>
            <div v-else class="row text-center g-3">
              <div class="col-4">
                <div class="estado-card p-3 rounded-3 bg-info bg-opacity-10">
                  <i class="bi bi-hourglass-split fs-1 text-info d-block mb-2"></i>
                  <h3 class="text-info mb-1 fw-bold">{{ estadoVoluntariados.upcoming }}</h3>
                  <small class="text-muted fw-medium">Próximos</small>
                </div>
              </div>
              <div class="col-4">
                <div class="estado-card p-3 rounded-3 bg-success bg-opacity-10">
                  <i class="bi bi-check-circle fs-1 text-success d-block mb-2"></i>
                  <h3 class="text-success mb-1 fw-bold">{{ estadoVoluntariados.active }}</h3>
                  <small class="text-muted fw-medium">Activos</small>
                </div>
              </div>
              <div class="col-4">
                <div class="estado-card p-3 rounded-3 bg-secondary bg-opacity-10">
                  <i class="bi bi-check2-circle fs-1 text-secondary d-block mb-2"></i>
                  <h3 class="text-secondary mb-1 fw-bold">{{ estadoVoluntariados.finished }}</h3>
                  <small class="text-muted fw-medium">Finalizados</small>
                </div>
              </div>
            </div>
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
import { voluntariadoAPI, personaAPI, facultadAPI, certificadoAPI } from '@/services/api'
import authService from '@/services/authService'

interface Stats {
  voluntarios: number
  voluntariadosActivos: number
  certificados: number
}

interface Voluntariado {
  id: number
  nombre: string
  estado: 'DRAFT' | 'ACTIVE' | 'CLOSED'
  fecha_inicio?: string
  fecha_fin?: string
  descripcion_data?: { texto: string }
  turno_data?: {
    hora_inicio: string
    hora_fin: string
  }
}

interface FacultadStat {
  nombre: string
  count: number
  porcentaje: number
}

interface EstadoVoluntariados {
  upcoming: number
  active: number
  finished: number
}

interface TopFacultad {
  nombre: string
  count: number
}

export default defineComponent({
  name: 'AdminDashboard',
  components: { AdminLayout },
  data() {
    return {
      stats: {
        voluntarios: 0,
        voluntariadosActivos: 0,
        certificados: 0
      } as Stats,
      proximosVoluntariados: [] as Voluntariado[],
      voluntariosPorFacultad: [] as FacultadStat[],
      estadoVoluntariados: {
        upcoming: 0,
        active: 0,
        finished: 0
      } as EstadoVoluntariados,
      loadingVoluntariadosProximos: false,
      loadingFacultades: false,
      loadingVoluntariados: false
    }
  },
  computed: {
    topFacultad(): TopFacultad {
      if (this.voluntariosPorFacultad.length === 0) {
        return { nombre: 'No hay datos', count: 0 }
      }
      const topFac = this.voluntariosPorFacultad[0]
      return {
        nombre: topFac?.nombre || 'No hay datos',
        count: topFac?.count || 0
      }
    }
  },
  mounted() {
    this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      await Promise.all([
        this.loadStats(),
        this.loadProximosVoluntariados(),
        this.loadVoluntariosPorFacultad(),
        this.loadEstadoVoluntariados()
      ])
    },
    async loadStats() {
      try {
        // Choose active voluntariados source based on role to keep numbers consistent with Delegado view
        const isDeleg = authService.hasRole('DELEG') && !authService.isAdmin()
        const [volCountRes, activosRes, certificados] = await Promise.all([
          personaAPI.getVoluntariosCount(),
          isDeleg ? voluntariadoAPI.getMineActive() : voluntariadoAPI.getAllActive(),
          certificadoAPI.getAll()
        ])



        // Total voluntarios via lightweight count endpoint (supports plain count)
        this.stats.voluntarios = typeof volCountRes?.data?.count === 'number' ? volCountRes.data.count : 0
        console.log('Final stats.voluntarios:', this.stats.voluntarios)
        // Support both paginated and array responses
        const activosData = activosRes?.data
        this.stats.voluntariadosActivos = Array.isArray(activosData)
          ? activosData.length
          : (typeof activosData?.count === 'number'
              ? activosData.count
              : Array.isArray(activosData?.results) ? activosData.results.length : 0)
        this.stats.certificados = certificados.data.length
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },
    async loadProximosVoluntariados() {
      this.loadingVoluntariadosProximos = true
      try {
        const isDeleg = authService.hasRole('DELEG') && !authService.isAdmin()
        const res = await (isDeleg ? voluntariadoAPI.getMineUpcoming() : voluntariadoAPI.getAllUpcoming())
        const data = Array.isArray(res.data)
          ? res.data
          : (Array.isArray(res.data?.results) ? res.data.results : [])

        const today = new Date()
        today.setHours(0, 0, 0, 0)

        this.proximosVoluntariados = data
          .filter((vol: Voluntariado) => {
            // Safety filter: exclude closed just in case
            if (vol.estado === 'CLOSED') return false
            if (!vol.fecha_inicio) return true
            return new Date(vol.fecha_inicio) >= today
          })
          .sort((a: Voluntariado, b: Voluntariado) => {
            if (!a.fecha_inicio) return 1
            if (!b.fecha_inicio) return -1
            return new Date(a.fecha_inicio).getTime() - new Date(b.fecha_inicio).getTime()
          })
          .slice(0, 5)
      } catch (error) {
        console.error('Error loading voluntariados:', error)
      } finally {
        this.loadingVoluntariadosProximos = false
      }
    },
    async loadVoluntariosPorFacultad() {
      this.loadingFacultades = true
      try {
        const [voluntarios, facultades, carreras] = await Promise.all([
          personaAPI.getVoluntarios(),
          facultadAPI.getFacultades(),
          facultadAPI.getCarreras()
        ])

        const carreraMap = new Map<number, number>()
        carreras.data.forEach((c: any) => {
          if (c.facultad) {
            carreraMap.set(c.id, c.facultad)
          }
        })

        const facultadMap = new Map<number, string>()
        facultades.data.forEach((f: any) => {
          facultadMap.set(f.id, f.nombre)
        })

        const counts = new Map<string, number>()
        voluntarios.data.forEach((vol: any) => {
          let facultadId = null

          if (vol.carrera_data?.facultad) {
            facultadId = vol.carrera_data.facultad
          } else if (vol.carrera) {
            facultadId = carreraMap.get(vol.carrera)
          }

          if (facultadId) {
            const nombre = facultadMap.get(facultadId) || 'Sin Facultad'
            counts.set(nombre, (counts.get(nombre) || 0) + 1)
          }
        })

        const total = voluntarios.data.length
        this.voluntariosPorFacultad = Array.from(counts.entries())
          .map(([nombre, count]) => ({
            nombre,
            count,
            porcentaje: total > 0 ? (count / total) * 100 : 0
          }))
          .sort((a, b) => b.count - a.count)
          .slice(0, 5)
      } catch (error) {
        console.error('Error loading voluntarios por facultad:', error)
      } finally {
        this.loadingFacultades = false
      }
    },
    async loadEstadoVoluntariados() {
      this.loadingVoluntariados = true
      try {
        const isDeleg = authService.hasRole('DELEG') && !authService.isAdmin()
        // Use endpoints consistent with Delegado view when applicable
        const [upcomingRes, activeRes, finalizedRes] = await Promise.all([
          isDeleg ? voluntariadoAPI.getMineUpcoming() : voluntariadoAPI.getAllUpcoming(),
          isDeleg ? voluntariadoAPI.getMineActive() : voluntariadoAPI.getAllActive(),
          isDeleg ? voluntariadoAPI.getMineFinished() : voluntariadoAPI.getAllFinalized()
        ])

        const getCount = (res: any): number => {
          const data = res?.data
          if (Array.isArray(data)) return data.length
          if (data && typeof data === 'object') {
            if (typeof data.count === 'number') return data.count
            if (Array.isArray(data.results)) return data.results.length
          }
          return 0
        }

        this.estadoVoluntariados = {
          upcoming: getCount(upcomingRes),
          active: getCount(activeRes),
          // Backend may use "finalized" as status param; we map it to UI's "finished"
          finished: getCount(finalizedRes)
        }
      } catch (error) {
        console.error('Error loading estado voluntariados:', error)
      } finally {
        this.loadingVoluntariados = false
      }
    },
    formatDate(dateString: string | undefined): string {
      if (!dateString) return 'Sin fecha'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('es-AR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        })
      } catch {
        return 'Fecha inválida'
      }
    },
    formatDateTime(dateString: string): string {
      try {
        const date = new Date(dateString)
        const now = new Date()
        const diff = now.getTime() - date.getTime()
        const minutes = Math.floor(diff / 60000)
        const hours = Math.floor(minutes / 60)
        const days = Math.floor(hours / 24)

        if (minutes < 1) return 'Hace un momento'
        if (minutes < 60) return `Hace ${minutes} minuto${minutes !== 1 ? 's' : ''}`
        if (hours < 24) return `Hace ${hours} hora${hours !== 1 ? 's' : ''}`
        if (days < 7) return `Hace ${days} día${days !== 1 ? 's' : ''}`
        return this.formatDate(dateString)
      } catch {
        return 'Fecha desconocida'
      }
    },
    getEstadoLabel(estado: string): string {
      const labels: Record<string, string> = {
        DRAFT: 'Borrador',
        ACTIVE: 'Activo',
        CLOSED: 'Cerrado'
      }
      return labels[estado] || estado
    },
    truncateText(text: string, maxLength: number): string {
      if (!text) return ''
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }
  }
})
</script>

<style scoped>
.dashboard-container {
  padding: 1rem 0;
}

/* Stat Cards */
.stat-card {
  transition: all 0.3s ease;
  border-radius: 12px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12) !important;
}

.stat-card .card-body {
  padding: 1.5rem;
}

.stat-label {
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.stat-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

/* General Cards */
.card {
  transition: all 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
}

.card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  padding: 1.25rem 1.5rem;
  font-weight: 600;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

.card-header h5 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2c3e50;
}

.card-header i {
  font-size: 1.25rem;
}

.card-body {
  padding: 1.5rem;
}

/* List Items */
.list-group-item {
  border-left: none;
  border-right: none;
  transition: background-color 0.2s ease;
  padding: 1rem 1.5rem;
}

.list-group-item:first-child {
  border-top: none;
}

.list-group-item:last-child {
  border-bottom: none;
}

.list-group-item-action:hover {
  background-color: #f8f9fa;
}

/* Badges */
.badge {
  padding: 0.35rem 0.75rem;
  font-weight: 500;
  font-size: 0.75rem;
  border-radius: 6px;
}

.bg-primary-subtle {
  background-color: rgba(13, 110, 253, 0.1);
}

.text-primary {
  color: #0d6efd !important;
}

/* Progress Bars */
.progress {
  border-radius: 8px;
  background-color: #e9ecef;
  overflow: hidden;
}

.progress-bar {
  background: linear-gradient(90deg, #0d6efd 0%, #0a58ca 100%);
  transition: width 0.6s ease;
}

/* Activity Icons */
.rounded-circle {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Estado Stats */
.estado-card {
  transition: all 0.3s ease;
}

.estado-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.estado-card i {
  transition: transform 0.3s ease;
}

.estado-card:hover i {
  transform: scale(1.1);
}

.row.text-center .col-4 .p-3 {
  border-radius: 8px;
  transition: all 0.2s ease;
}

.row.text-center .col-4 .p-3:hover {
  background-color: #f8f9fa;
}

/* Loading States */
.spinner-border {
  width: 2rem;
  height: 2rem;
}

/* Responsive Adjustments */
@media (max-width: 1199.98px) {
  .stat-value {
    font-size: 1.75rem;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
  }
  
  .stat-icon i {
    font-size: 1.25rem !important;
  }
}

@media (max-width: 767.98px) {
  .dashboard-container {
    padding: 1rem 0;
  }
  
  .stat-card .card-body {
    padding: 1rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .card-header,
  .card-body {
    padding: 1rem;
  }
  
  .list-group-item {
    padding: 0.75rem 1rem;
  }
}
</style>

