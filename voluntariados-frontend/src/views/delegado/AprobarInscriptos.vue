<!-- src/views/delegado/AprobarInscriptos.vue -->
<template>
  <div class="aprobar-inscriptos">
    <AppNavBar />

    <div class="container py-4">
      <!-- Header -->
      <div class="aprobar-header mb-4">
        <div class="d-flex align-items-center justify-content-between">
          <div class="d-flex align-items-center">
            <button class="btn btn-outline-light me-3" @click="goBack">
              <i class="bi bi-arrow-left me-2"></i>
              Volver
            </button>
            <i class="bi bi-clipboard-check me-3 text-white" style="font-size: 1.8rem;"></i>
            <div>
              <h2 class="mb-0 text-white">Aprobar Inscriptos</h2>
              <p class="mb-0 text-white-50" v-if="voluntariado">{{ voluntariado.nombre }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Voluntariado Info Card -->
      <div v-if="voluntariado" class="card mb-4">
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <p class="mb-2">
                <strong>Inicio de Convocatoria:</strong> 
                {{ formatDate(voluntariado.fecha_inicio_convocatoria) }}
              </p>
              <p class="mb-2">
                <strong>Fin de Convocatoria:</strong> 
                {{ formatDate(voluntariado.fecha_fin_convocatoria) }}
              </p>
            </div>
            <div class="col-md-6">
              <p class="mb-2">
                <strong>Inicio de Cursado:</strong> 
                {{ formatDate(voluntariado.fecha_inicio_cursado) }}
              </p>
              <p class="mb-2">
                <strong>Fin de Cursado:</strong> 
                {{ formatDate(voluntariado.fecha_fin_cursado) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Inscriptions Table -->
      <div class="inscripciones-table-container mb-5">
        <AdminTable
          title="Inscripciones Pendientes de Aprobación"
          :columns="columns"
          :items="inscripcionesPendientes"
          :loading="loading"
          :error="error ?? undefined"
          empty-text="No hay inscripciones pendientes de aprobación."
          :show-create-button="false"
          :clickable-rows="false"
          :show-actions="true"
          @retry="loadInscripciones"
        >
          <!-- Custom cell templates -->
          <template #cell-voluntario="{ item }">
            <div class="d-flex align-items-center">
              <div class="avatar-wrapper me-3">
                <i class="bi bi-person-circle text-primary fs-4"></i>
              </div>
              <div>
                <div class="fw-bold">
                  {{ getVoluntarioNombre(item.voluntario) }}
                </div>
                <small class="text-muted">{{ getVoluntarioEmail(item.voluntario) }}</small>
              </div>
            </div>
          </template>

          <template #cell-dni="{ item }">
            <span>{{ getVoluntarioDNI(item.voluntario) || '-' }}</span>
          </template>

          <template #cell-estado="{ item }">
            <span class="badge bg-warning text-dark">
              <i class="bi bi-hourglass-split me-1"></i>
              Pendiente
            </span>
          </template>

          <!-- Row actions -->
          <template #actions="{ item }">
            <div class="btn-group" role="group">
              <button 
                class="btn btn-sm btn-info" 
                @click.stop="viewVoluntarioDetail(item.voluntario)"
                title="Ver detalles"
              >
                <i class="bi bi-eye"></i>
              </button>
              <button 
                class="btn btn-sm btn-success" 
                @click.stop="aprobarInscripcion(item)"
                :disabled="processingIds.has(item.id)"
              >
                <span v-if="processingIds.has(item.id)" class="spinner-border spinner-border-sm me-1"></span>
                <i v-else class="bi bi-check-circle me-1"></i>
                Aprobar
              </button>
              <button 
                class="btn btn-sm btn-danger" 
                @click.stop="rechazarInscripcion(item)"
                :disabled="processingIds.has(item.id)"
              >
                <span v-if="processingIds.has(item.id)" class="spinner-border spinner-border-sm me-1"></span>
                <i v-else class="bi bi-x-circle me-1"></i>
                Rechazar
              </button>
            </div>
          </template>
        </AdminTable>
      </div>

      <!-- Approved Inscriptions Table -->
      <div class="inscripciones-table-container mb-5">
        <AdminTable
          title="Inscripciones Aprobadas"
          :columns="columns"
          :items="inscripcionesAprobadas"
          :loading="loading"
          :error="error ?? undefined"
          empty-text="No hay inscripciones aprobadas."
          :show-create-button="false"
          :clickable-rows="false"
          :show-actions="true"
          @retry="loadInscripciones"
        >
          <!-- Custom cell templates -->
          <template #cell-voluntario="{ item }">
            <div class="d-flex align-items-center">
              <div class="avatar-wrapper-success me-3">
                <i class="bi bi-person-check text-success fs-4"></i>
              </div>
              <div>
                <div class="fw-bold">
                  {{ getVoluntarioNombre(item.voluntario) }}
                </div>
                <small class="text-muted">{{ getVoluntarioEmail(item.voluntario) }}</small>
              </div>
            </div>
          </template>

          <template #cell-dni="{ item }">
            <span>{{ getVoluntarioDNI(item.voluntario) || '-' }}</span>
          </template>

          <template #cell-estado="{ item }">
            <span class="badge bg-success">
              <i class="bi bi-check-circle me-1"></i>
              Aprobado
            </span>
          </template>

          <!-- Row actions -->
          <template #actions="{ item }">
            <div class="btn-group" role="group">
              <button 
                class="btn btn-sm btn-info" 
                @click.stop="viewVoluntarioDetail(item.voluntario)"
                title="Ver detalles"
              >
                <i class="bi bi-eye"></i>
              </button>
              <button 
                class="btn btn-sm btn-warning" 
                @click.stop="revertirAprobar(item)"
                :disabled="processingIds.has(item.id)"
                title="Revertir aprobación"
              >
                <span v-if="processingIds.has(item.id)" class="spinner-border spinner-border-sm me-1"></span>
                <i v-else class="bi bi-arrow-counterclockwise me-1"></i>
                Revertir
              </button>
            </div>
          </template>
        </AdminTable>
      </div>

      <!-- Rejected Inscriptions Table -->
      <div class="inscripciones-table-container">
        <AdminTable
          title="Inscripciones Rechazadas"
          :columns="columns"
          :items="inscripcionesRechazadas"
          :loading="loading"
          :error="error ?? undefined"
          empty-text="No hay inscripciones rechazadas."
          :show-create-button="false"
          :clickable-rows="false"
          :show-actions="true"
          @retry="loadInscripciones"
        >
          <!-- Custom cell templates -->
          <template #cell-voluntario="{ item }">
            <div class="d-flex align-items-center">
              <div class="avatar-wrapper-danger me-3">
                <i class="bi bi-person-x text-danger fs-4"></i>
              </div>
              <div>
                <div class="fw-bold">
                  {{ getVoluntarioNombre(item.voluntario) }}
                </div>
                <small class="text-muted">{{ getVoluntarioEmail(item.voluntario) }}</small>
              </div>
            </div>
          </template>

          <template #cell-dni="{ item }">
            <span>{{ getVoluntarioDNI(item.voluntario) || '-' }}</span>
          </template>

          <template #cell-estado="{ item }">
            <span class="badge bg-danger">
              <i class="bi bi-x-circle me-1"></i>
              Rechazado
            </span>
          </template>

          <!-- Row actions -->
          <template #actions="{ item }">
            <div class="btn-group" role="group">
              <button 
                class="btn btn-sm btn-info" 
                @click.stop="viewVoluntarioDetail(item.voluntario)"
                title="Ver detalles"
              >
                <i class="bi bi-eye"></i>
              </button>
              <button 
                class="btn btn-sm btn-warning" 
                @click.stop="revertirRechazo(item)"
                :disabled="processingIds.has(item.id)"
                title="Revertir rechazo"
              >
                <span v-if="processingIds.has(item.id)" class="spinner-border spinner-border-sm me-1"></span>
                <i v-else class="bi bi-arrow-counterclockwise me-1"></i>
                Revertir
              </button>
            </div>
          </template>
        </AdminTable>
      </div>

      <!-- Bulk Actions -->
      <div v-if="inscripcionesPendientes.length > 0" class="card mt-4">
        <div class="card-body">
          <h5 class="card-title">Acciones en Masa</h5>
          <p class="text-muted mb-3">
            Aplicar acciones a todos los inscriptos pendientes simultáneamente.
          </p>
          <div class="btn-group" role="group">
            <button 
              class="btn btn-success" 
              @click="aprobarTodos"
              :disabled="bulkProcessing"
            >
              <span v-if="bulkProcessing" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-check-circle-fill me-2"></i>
              Aprobar Todos
            </button>
            <button 
              class="btn btn-danger" 
              @click="rechazarTodos"
              :disabled="bulkProcessing"
            >
              <span v-if="bulkProcessing" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-x-circle-fill me-2"></i>
              Rechazar Todos
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Voluntario Detail Modal -->
    <VoluntarioDetailModal
      :show="showDetailModal"
      :voluntario="selectedVoluntario as any"
      :localidades="localidades"
      :carreras="carreras"
      @close="showDetailModal = false"
      @edit="handleEditVoluntario"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import VoluntarioDetailModal from '@/components/admin/VoluntarioDetailModal.vue'
import { voluntariadoAPI, inscripcionConvocatoriaAPI, ubicacionAPI, facultadAPI } from '@/services/api'
import { formatDateShort } from '@/utils/dateUtils'

interface Voluntario {
  id: number
  // Nested structure (if voluntario has persona nested)
  persona?: {
    nombre?: string
    apellido?: string
    email?: string
    dni?: string
    facultad?: {
      nombre?: string
    }
    carrera?: {
      nombre?: string
    }
  }
  // Flattened structure (when serializer inherits from PersonaSerializer)
  nombre?: string
  apellido?: string
  email?: string
  dni?: string
  facultad?: {
    nombre?: string
  }
  carrera?: {
    nombre?: string
  }
}

interface InscripcionConvocatoria {
  id: number
  voluntario: Voluntario
  voluntariado: any
  estado: string
}

export default defineComponent({
  name: 'AprobarInscriptos',
  components: { AppNavBar, AdminTable, VoluntarioDetailModal },
  data() {
    return {
      loading: false as boolean,
      error: null as string | null,
      voluntariado: null as any,
      inscripciones: [] as InscripcionConvocatoria[],
      processingIds: new Set<number>(),
      bulkProcessing: false as boolean,
      showDetailModal: false as boolean,
      selectedVoluntario: null as Voluntario | null,
      localidades: [] as any[],
      carreras: [] as any[],
      columns: [
        { key: 'voluntario', label: 'Voluntario', sortable: true },
        { key: 'dni', label: 'DNI', sortable: true },
        { key: 'estado', label: 'Estado', sortable: false, align: 'center' }
      ] as TableColumn[]
    }
  },
  computed: {
    inscripcionesPendientes(): InscripcionConvocatoria[] {
      return this.inscripciones.filter(insc => insc.estado === 'INS')
    },
    inscripcionesAprobadas(): InscripcionConvocatoria[] {
      return this.inscripciones.filter(insc => insc.estado === 'ACE')
    },
    inscripcionesRechazadas(): InscripcionConvocatoria[] {
      return this.inscripciones.filter(insc => insc.estado === 'REJ')
    }
  },
  mounted() {
    this.loadVoluntariado()
    this.loadInscripciones()
    this.loadLocalidades()
    this.loadCarreras()
  },
  methods: {
    async loadVoluntariado() {
      const voluntariadoId = parseInt(this.$route.params.id as string)
      if (!voluntariadoId) {
        this.error = 'ID de voluntariado inválido'
        return
      }

      try {
        const res = await voluntariadoAPI.getById(voluntariadoId)
        this.voluntariado = res.data
      } catch (err: any) {
        console.error('Error loading voluntariado:', err)
        this.error = err?.response?.data?.detail || 'Error al cargar el voluntariado'
      }
    },
    async loadInscripciones() {
      this.loading = true
      this.error = null
      const voluntariadoId = parseInt(this.$route.params.id as string)

      if (!voluntariadoId) {
        this.error = 'ID de voluntariado inválido'
        this.loading = false
        return
      }

      try {
        const res = await inscripcionConvocatoriaAPI.getAll()
        const allInscripciones = (res.data && res.data.results) ? res.data.results : res.data

        // Debug: log the first inscription to see the structure
        if (Array.isArray(allInscripciones) && allInscripciones.length > 0) {
          console.log('First inscription structure:', allInscripciones[0])
        }

        // Filter for this voluntariado only (all estados: INS, ACE, REJ)
        this.inscripciones = Array.isArray(allInscripciones) 
          ? allInscripciones.filter((insc: any) => {
              const matchesVoluntariado = (insc.voluntariado === voluntariadoId) || (insc.voluntariado?.id === voluntariadoId)
              const isActive = insc.is_active !== false
              return matchesVoluntariado && isActive
            })
          : []
        
      } catch (err: any) {
        console.error('Error loading inscripciones:', err)
        this.error = err?.response?.data?.detail || 'Error al cargar las inscripciones'
      } finally {
        this.loading = false
      }
    },
    async aprobarInscripcion(item: InscripcionConvocatoria) {
      if (!confirm(`¿Estás seguro de que deseas aprobar a ${this.getVoluntarioNombre(item.voluntario)}?`)) {
        return
      }

      this.processingIds.add(item.id)
      try {
        await inscripcionConvocatoriaAPI.aceptar(item.id)
        // Update estado in local list
        const index = this.inscripciones.findIndex(i => i.id === item.id)
        if (index !== -1 && this.inscripciones[index]) {
          this.inscripciones[index].estado = 'ACE'
        }
        // Show success message
        alert('Inscripción aprobada correctamente')
      } catch (err: any) {
        console.error('Error aprobar inscripción:', err)
        alert(err?.response?.data?.detail || 'Error al aprobar la inscripción')
      } finally {
        this.processingIds.delete(item.id)
      }
    },
    async rechazarInscripcion(item: InscripcionConvocatoria) {
      if (!confirm(`¿Estás seguro de que deseas rechazar a ${this.getVoluntarioNombre(item.voluntario)}?`)) {
        return
      }

      this.processingIds.add(item.id)
      try {
        await inscripcionConvocatoriaAPI.rechazar(item.id)
        // Update estado in local list
        const index = this.inscripciones.findIndex(i => i.id === item.id)
        if (index !== -1 && this.inscripciones[index]) {
          this.inscripciones[index].estado = 'REJ'
        }
        // Show success message
        alert('Inscripción rechazada correctamente')
      } catch (err: any) {
        console.error('Error rechazar inscripción:', err)
        alert(err?.response?.data?.detail || 'Error al rechazar la inscripción')
      } finally {
        this.processingIds.delete(item.id)
      }
    },
    async revertirAprobar(item: InscripcionConvocatoria) {
      if (!confirm(`¿Estás seguro de que deseas revertir la aprobación de ${this.getVoluntarioNombre(item.voluntario)}? El voluntario volverá al estado INSCRITO.`)) {
        return
      }

      this.processingIds.add(item.id)
      try {
        // Update to INSCRITO state using the API's update method
        await (inscripcionConvocatoriaAPI as any).update(item.id, { estado: 'INS' })
        // Update estado in local list
        const index = this.inscripciones.findIndex(i => i.id === item.id)
        if (index !== -1 && this.inscripciones[index]) {
          this.inscripciones[index].estado = 'INS'
        }
        alert('Aprobación revertida correctamente')
      } catch (err: any) {
        console.error('Error revertir aprobación:', err)
        alert(err?.response?.data?.detail || 'Error al revertir la aprobación')
      } finally {
        this.processingIds.delete(item.id)
      }
    },
    async revertirRechazo(item: InscripcionConvocatoria) {
      if (!confirm(`¿Estás seguro de que deseas revertir el rechazo de ${this.getVoluntarioNombre(item.voluntario)}? El voluntario volverá al estado INSCRITO.`)) {
        return
      }

      this.processingIds.add(item.id)
      try {
        // Update to INSCRITO state using the API's update method
        await (inscripcionConvocatoriaAPI as any).update(item.id, { estado: 'INS' })
        // Update estado in local list
        const index = this.inscripciones.findIndex(i => i.id === item.id)
        if (index !== -1 && this.inscripciones[index]) {
          this.inscripciones[index].estado = 'INS'
        }
        alert('Rechazo revertido correctamente')
      } catch (err: any) {
        console.error('Error revertir rechazo:', err)
        alert(err?.response?.data?.detail || 'Error al revertir el rechazo')
      } finally {
        this.processingIds.delete(item.id)
      }
    },
    async aprobarTodos() {
      const pendientes = this.inscripcionesPendientes
      if (!confirm(`¿Estás seguro de que deseas aprobar TODAS las ${pendientes.length} inscripciones pendientes?`)) {
        return
      }

      this.bulkProcessing = true
      const errors: string[] = []

      for (const insc of pendientes) {
        try {
          await inscripcionConvocatoriaAPI.aceptar(insc.id)
          // Update estado in local list
          const index = this.inscripciones.findIndex(i => i.id === insc.id)
          if (index !== -1 && this.inscripciones[index]) {
            this.inscripciones[index].estado = 'ACE'
          }
        } catch (err: any) {
          console.error(`Error aprobar inscripción ${insc.id}:`, err)
          errors.push(`${this.getVoluntarioNombre(insc.voluntario)}: ${err?.response?.data?.detail || 'Error desconocido'}`)
        }
      }

      this.bulkProcessing = false

      if (errors.length > 0) {
        alert(`Se completó la aprobación con algunos errores:\n\n${errors.join('\n')}`)
      } else {
        alert('Todas las inscripciones fueron aprobadas correctamente')
      }
    },
    async rechazarTodos() {
      const pendientes = this.inscripcionesPendientes
      if (!confirm(`¿Estás seguro de que deseas rechazar TODAS las ${pendientes.length} inscripciones pendientes?`)) {
        return
      }

      this.bulkProcessing = true
      const errors: string[] = []

      for (const insc of pendientes) {
        try {
          await inscripcionConvocatoriaAPI.rechazar(insc.id)
          // Update estado in local list
          const index = this.inscripciones.findIndex(i => i.id === insc.id)
          if (index !== -1 && this.inscripciones[index]) {
            this.inscripciones[index].estado = 'REJ'
          }
        } catch (err: any) {
          console.error(`Error rechazar inscripción ${insc.id}:`, err)
          errors.push(`${this.getVoluntarioNombre(insc.voluntario)}: ${err?.response?.data?.detail || 'Error desconocido'}`)
        }
      }

      this.bulkProcessing = false

      if (errors.length > 0) {
        alert(`Se completó el rechazo con algunos errores:\n\n${errors.join('\n')}`)
      } else {
        alert('Todas las inscripciones fueron rechazadas correctamente')
      }
    },
    formatDate(date?: string | null): string {
      if (!date) return '-'
      try {
        return formatDateShort(date)
      } catch {
        return String(date)
      }
    },
    getVoluntarioNombre(voluntario: Voluntario): string {
      // Handle both nested (voluntario.persona.nombre) and flattened (voluntario.nombre) structures
      const nombre = voluntario?.persona?.nombre || voluntario?.nombre || ''
      const apellido = voluntario?.persona?.apellido || voluntario?.apellido || ''
      return `${nombre} ${apellido}`.trim() || 'Sin nombre'
    },
    getVoluntarioEmail(voluntario: Voluntario): string {
      return voluntario?.persona?.email || voluntario?.email || '-'
    },
    getVoluntarioDNI(voluntario: Voluntario): string {
      return voluntario?.persona?.dni || voluntario?.dni || ''
    },
    viewVoluntarioDetail(voluntario: Voluntario) {
      this.selectedVoluntario = voluntario
      this.showDetailModal = true
    },
    handleEditVoluntario(voluntario: any) {
      // Close the modal and optionally navigate to edit view
      this.showDetailModal = false
      // Note: This component is read-only for now, but you could add navigation to an edit view if needed
      console.log('Edit voluntario:', voluntario)
    },
    async loadLocalidades() {
      try {
        const res = await ubicacionAPI.getLocalidades()
        this.localidades = (res.data && res.data.results) ? res.data.results : res.data
      } catch (err: any) {
        console.error('Error loading localidades:', err)
      }
    },
    async loadCarreras() {
      try {
        const res = await facultadAPI.getCarreras()
        this.carreras = (res.data && res.data.results) ? res.data.results : res.data
      } catch (err: any) {
        console.error('Error loading carreras:', err)
      }
    },
    goBack() {
      this.$router.push({ name: 'DelegadoAreaPersonal' })
    }
  }
})
</script>

<style scoped>
.aprobar-inscriptos {
  display: block;
}

.inscripciones-table-container {
  position: relative;
}

.avatar-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(13, 110, 253, 0.1);
  border-radius: 50%;
}

.avatar-wrapper-success {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 135, 84, 0.1);
  border-radius: 50%;
}

.avatar-wrapper-danger {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 50%;
}

.aprobar-header {
  background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
  padding: 1.5rem 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(255, 193, 7, 0.2);
}

.btn-group .btn {
  min-width: 90px;
}

.btn-group .btn-info {
  min-width: 40px;
}
</style>
