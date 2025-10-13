<template>
  <AdminLayout
    page-title="Dashboard"
    :breadcrumbs="[{ label: 'Dashboard' }]"
  >
    <!-- Stats Cards -->
    <div class="row g-3 mb-4">
      <div class="col-xl-3 col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-2">Total Voluntarios</h6>
                <h3 class="mb-0">{{ stats.voluntarios }}</h3>
              </div>
              <div class="bg-primary bg-opacity-10 p-3 rounded">
                <i class="bi bi-people-fill text-primary fs-4"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-2">Voluntariados Activos</h6>
                <h3 class="mb-0">{{ stats.voluntariadosActivos }}</h3>
              </div>
              <div class="bg-success bg-opacity-10 p-3 rounded">
                <i class="bi bi-calendar-check-fill text-success fs-4"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-2">Capacitaciones</h6>
                <h3 class="mb-0">{{ stats.capacitaciones }}</h3>
              </div>
              <div class="bg-info bg-opacity-10 p-3 rounded">
                <i class="bi bi-book-fill text-info fs-4"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-2">Certificados Emitidos</h6>
                <h3 class="mb-0">{{ stats.certificados }}</h3>
              </div>
              <div class="bg-warning bg-opacity-10 p-3 rounded">
                <i class="bi bi-award-fill text-warning fs-4"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <!-- Próximos Voluntariados -->
      <div class="col-xl-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0">Próximos Voluntariados</h5>
          </div>
          <div class="card-body">
            <div v-if="loadingVoluntariadosProximos" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>
            <div v-else-if="proximosVoluntariados.length === 0" class="text-center py-4 text-muted">
              No hay voluntariados próximos
            </div>
            <div v-else class="list-group list-group-flush">
              <div
                v-for="vol in proximosVoluntariados"
                :key="vol.id"
                class="list-group-item px-0"
              >
                <div class="d-flex justify-content-between align-items-start">
                  <div class="flex-grow-1">
                    <div class="d-flex align-items-center mb-1">
                      <h6 class="mb-0 me-2">{{ vol.nombre }}</h6>
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
                    <small class="text-muted">
                      <i class="bi bi-calendar3"></i>
                      {{ formatDate(vol.fecha_inicio) }}
                      <span v-if="vol.fecha_fin"> - {{ formatDate(vol.fecha_fin) }}</span>
                    </small>
                    <div v-if="vol.descripcion_data?.texto" class="mt-1">
                      <small class="text-muted">{{ truncateText(vol.descripcion_data.texto, 80) }}</small>
                    </div>
                    <div v-if="vol.turno_data" class="mt-1">
                      <small class="text-muted">
                        <i class="bi bi-clock"></i> {{ vol.turno_data.hora_inicio }} - {{ vol.turno_data.hora_fin }}
                      </small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actividad Reciente -->
      <div class="col-xl-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0">Actividad Reciente</h5>
          </div>
          <div class="card-body">
            <div v-if="loadingActividad" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>
            <div v-else-if="actividadReciente.length === 0" class="text-center py-4 text-muted">
              No hay actividad reciente
            </div>
            <div v-else class="list-group list-group-flush">
              <div
                v-for="(actividad, index) in actividadReciente"
                :key="index"
                class="list-group-item px-0"
              >
                <div class="d-flex align-items-start">
                  <div
                    class="rounded-circle p-2 me-3"
                    :class="getActivityIconClass(actividad.tipo)"
                  >
                    <i :class="getActivityIcon(actividad.tipo)"></i>
                  </div>
                  <div class="flex-grow-1">
                    <p class="mb-1">{{ actividad.descripcion }}</p>
                    <small class="text-muted">{{ formatDateTime(actividad.fecha) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Estadísticas por Facultad -->
    <div class="row g-3">
      <div class="col-xl-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0">Voluntarios por Facultad</h5>
          </div>
          <div class="card-body">
            <div v-if="loadingFacultades" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>
            <div v-else-if="voluntariosPorFacultad.length === 0" class="text-center py-4 text-muted">
              No hay datos disponibles
            </div>
            <div v-else>
              <div
                v-for="facultad in voluntariosPorFacultad"
                :key="facultad.nombre"
                class="mb-3"
              >
                <div class="d-flex justify-content-between mb-1">
                  <span>{{ facultad.nombre }}</span>
                  <span class="fw-bold">{{ facultad.count }}</span>
                </div>
                <div class="progress" style="height: 8px;">
                  <div
                    class="progress-bar"
                    :style="{ width: facultad.porcentaje + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0">Estado de Voluntariados</h5>
          </div>
          <div class="card-body">
            <div v-if="loadingVoluntariados" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>
            <div v-else class="row text-center">
              <div class="col-4">
                <div class="p-3">
                  <h3 class="text-warning mb-1">{{ estadoVoluntariados.draft }}</h3>
                  <small class="text-muted">Borradores</small>
                </div>
              </div>
              <div class="col-4">
                <div class="p-3">
                  <h3 class="text-success mb-1">{{ estadoVoluntariados.active }}</h3>
                  <small class="text-muted">Activos</small>
                </div>
              </div>
              <div class="col-4">
                <div class="p-3">
                  <h3 class="text-secondary mb-1">{{ estadoVoluntariados.closed }}</h3>
                  <small class="text-muted">Cerrados</small>
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
import { voluntariadoAPI, turnoAPI, personaAPI, facultadAPI } from '@/services/api'
import apiClient from '@/services/api'

interface Stats {
  voluntarios: number
  voluntariadosActivos: number
  capacitaciones: number
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

interface Actividad {
  tipo: 'inscripcion' | 'certificado' | 'voluntariado' | 'capacitacion'
  descripcion: string
  fecha: string
}

interface FacultadStat {
  nombre: string
  count: number
  porcentaje: number
}

interface EstadoVoluntariados {
  draft: number
  active: number
  closed: number
}

export default defineComponent({
  name: 'AdminDashboard',
  components: { AdminLayout },
  data() {
    return {
      stats: {
        voluntarios: 0,
        voluntariadosActivos: 0,
        capacitaciones: 0,
        certificados: 0
      } as Stats,
      proximosVoluntariados: [] as Voluntariado[],
      actividadReciente: [] as Actividad[],
      voluntariosPorFacultad: [] as FacultadStat[],
      estadoVoluntariados: {
        draft: 0,
        active: 0,
        closed: 0
      } as EstadoVoluntariados,
      loadingVoluntariadosProximos: false,
      loadingActividad: false,
      loadingFacultades: false,
      loadingVoluntariados: false
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
        this.loadActividadReciente(),
        this.loadVoluntariosPorFacultad(),
        this.loadEstadoVoluntariados()
      ])
    },
    async loadStats() {
      try {
        const [voluntarios, voluntariados, capacitaciones, certificados] = await Promise.all([
          personaAPI.getVoluntarios(),
          voluntariadoAPI.getAll(),
          apiClient.get('/capacitacion/capacitaciones/'),
          apiClient.get('/certificado/certificados/')
        ])

        this.stats.voluntarios = voluntarios.data.length
        this.stats.voluntariadosActivos = voluntariados.data.filter(
          (v: any) => v.estado === 'ACTIVE'
        ).length
        this.stats.capacitaciones = capacitaciones.data.length
        this.stats.certificados = certificados.data.length
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },
    async loadProximosVoluntariados() {
      this.loadingVoluntariadosProximos = true
      try {
        const response = await voluntariadoAPI.getAll()
        const today = new Date()
        today.setHours(0, 0, 0, 0)

        this.proximosVoluntariados = response.data
          .filter((vol: Voluntariado) => {
            // Filtrar voluntariados activos o con fecha futura
            if (vol.estado === 'CLOSED') return false
            if (!vol.fecha_inicio) return true // Si no tiene fecha, mostrarlo
            return new Date(vol.fecha_inicio) >= today
          })
          .sort((a: Voluntariado, b: Voluntariado) => {
            // Ordenar por fecha de inicio, los sin fecha al final
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
    async loadActividadReciente() {
      this.loadingActividad = true
      try {
        // Simulación de actividad reciente - en producción obtener de endpoints reales
        const [inscripciones, certificados] = await Promise.all([
          apiClient.get('/voluntariado/inscripciones-turno/'),
          apiClient.get('/certificado/certificados/')
        ])

        const actividades: Actividad[] = []

        // Últimas inscripciones
        inscripciones.data.slice(0, 3).forEach((insc: any) => {
          actividades.push({
            tipo: 'inscripcion',
            descripcion: `Nueva inscripción al turno`,
            fecha: insc.created_at || new Date().toISOString()
          })
        })

        // Últimos certificados
        certificados.data.slice(0, 2).forEach((cert: any) => {
          actividades.push({
            tipo: 'certificado',
            descripcion: `Certificado emitido`,
            fecha: cert.fecha_emision || new Date().toISOString()
          })
        })

        this.actividadReciente = actividades
          .sort((a, b) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime())
          .slice(0, 5)
      } catch (error) {
        console.error('Error loading actividad:', error)
        this.actividadReciente = []
      } finally {
        this.loadingActividad = false
      }
    },
    async loadVoluntariosPorFacultad() {
      this.loadingFacultades = true
      try {
        const [voluntarios, facultades] = await Promise.all([
          personaAPI.getVoluntarios(),
          facultadAPI.getFacultades()
        ])

        const facultadMap = new Map<number, string>()
        facultades.data.forEach((f: any) => {
          facultadMap.set(f.id, f.nombre)
        })

        const counts = new Map<string, number>()
        voluntarios.data.forEach((vol: any) => {
          const facultadId = vol.carrera_data?.facultad
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
        const response = await voluntariadoAPI.getAll()
        const estados = response.data.reduce((acc: any, vol: any) => {
          acc[vol.estado.toLowerCase()] = (acc[vol.estado.toLowerCase()] || 0) + 1
          return acc
        }, {})

        this.estadoVoluntariados = {
          draft: estados.draft || 0,
          active: estados.active || 0,
          closed: estados.closed || 0
        }
      } catch (error) {
        console.error('Error loading estado voluntariados:', error)
      } finally {
        this.loadingVoluntariados = false
      }
    },
    formatDate(dateString: string): string {
      const date = new Date(dateString)
      return date.toLocaleDateString('es-AR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    },
    formatDateTime(dateString: string): string {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now.getTime() - date.getTime()
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(minutes / 60)
      const days = Math.floor(hours / 24)

      if (minutes < 60) return `Hace ${minutes} minutos`
      if (hours < 24) return `Hace ${hours} horas`
      if (days < 7) return `Hace ${days} días`
      return this.formatDate(dateString)
    },
    getActivityIcon(tipo: string): string {
      const icons: Record<string, string> = {
        inscripcion: 'bi bi-person-plus-fill',
        certificado: 'bi bi-award-fill',
        voluntariado: 'bi bi-calendar-plus-fill',
        capacitacion: 'bi bi-book-fill'
      }
      return icons[tipo] || 'bi bi-circle-fill'
    },
    getActivityIconClass(tipo: string): string {
      const classes: Record<string, string> = {
        inscripcion: 'bg-primary bg-opacity-10 text-primary',
        certificado: 'bg-warning bg-opacity-10 text-warning',
        voluntariado: 'bg-success bg-opacity-10 text-success',
        capacitacion: 'bg-info bg-opacity-10 text-info'
      }
      return classes[tipo] || 'bg-secondary bg-opacity-10 text-secondary'
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
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }
  }
})
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.list-group-item {
  border-left: none;
  border-right: none;
}

.list-group-item:first-child {
  border-top: none;
}

.list-group-item:last-child {
  border-bottom: none;
}
</style>
