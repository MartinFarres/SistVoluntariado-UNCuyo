<!-- src/views/delegado/InscripcionesManagement.vue -->
<template>
  <div class="aprobar-inscriptos">
    <AppNavBar />

    <div class="container py-4">
      <!-- Back Button - Outside header -->
      <button class="btn btn-outline-secondary mb-3" @click="goBack">
        <i class="bi bi-arrow-left me-2"></i>
        Volver
      </button>

      <!-- Header -->
      <div class="aprobar-header mb-4">
        <div class="d-flex align-items-center justify-content-between">
          <div class="d-flex align-items-center">
            <i class="bi bi-clipboard-check me-3 text-white" style="font-size: 1.8rem;"></i>
            <div>
              <h2 class="mb-0 text-white">Gestionar Inscriptos</h2>
              <p class="mb-0 text-white-50" v-if="voluntariado">{{ voluntariado.nombre }}</p>
            </div>
          </div>
          <!-- Stats badges -->
          <div class="d-flex gap-2">
            <span class="badge bg-white text-warning fs-6 px-3 py-2">
              <i class="bi bi-hourglass-split me-2"></i>
              {{ inscripcionesPendientes.length }} Pendientes
            </span>
            <span class="badge bg-white text-success fs-6 px-3 py-2">
              <i class="bi bi-check-circle me-2"></i>
              {{ inscripcionesAprobadas.length }} Aprobados
            </span>
            <span class="badge bg-white text-danger fs-6 px-3 py-2">
              <i class="bi bi-x-circle me-2"></i>
              {{ inscripcionesRechazadas.length }} Rechazados
            </span>
          </div>
        </div>
        <div class="mt-3 pt-3 border-top border-white border-opacity-25">
          <p class="mb-0 text-white">
            <i class="bi bi-info-circle me-2"></i>
            En esta etapa puedes revisar y aprobar/rechazar las inscripciones de los voluntarios. 
            Los voluntarios aprobados podrán participar en el voluntariado, mientras que los rechazados no.
          </p>
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

      <!-- All Inscriptions Table -->
      <div class="inscripciones-table-container mb-5">
        <AdminTable
          title="Todas las Inscripciones"
          :columns="columns"
          :items="inscripcionesOrdenadas"
          :loading="loading"
          :error="error ?? undefined"
          empty-text="No hay inscripciones para este voluntariado."
          :show-create-button="false"
          :clickable-rows="false"
          :show-actions="true"
          @retry="loadInscripciones"
        >
          <!-- Custom cell templates -->
          <template #cell-voluntario="{ item }">
            <div class="d-flex align-items-center">
              <div :class="getAvatarClass(item.estado)" class="me-3">
                <i :class="getAvatarIcon(item.estado)" class="fs-4"></i>
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
            <span :class="getEstadoBadgeClass(item.estado)">
              <i :class="getEstadoIcon(item.estado)" class="me-1"></i>
              {{ getEstadoLabel(item.estado) }}
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
              <!-- Show approve/reject buttons for pending inscriptions -->
              <template v-if="item.estado === 'INS'">
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
              </template>
              <!-- Show revert button for approved inscriptions -->
              <template v-else-if="item.estado === 'ACE'">
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
              </template>
              <!-- Show revert button for rejected inscriptions -->
              <template v-else-if="item.estado === 'REJ'">
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
              </template>
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

    <!-- Confirmation Modal -->
    <ConfirmationModal
      :show="showConfirmModal"
      :title="confirmModalTitle"
      :message="confirmModalMessage"
      :description="confirmModalDescription"
      :type="confirmModalType"
      :confirm-text="confirmModalConfirmText"
      :processing="confirmModalProcessing"
      @confirm="handleConfirmAction"
      @cancel="handleCancelConfirm"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import VoluntarioDetailModal from '@/components/admin/VoluntarioDetailModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
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
  name: 'InscripcionesManagement',
  components: { AppNavBar, AdminTable, VoluntarioDetailModal, ConfirmationModal },
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
      showConfirmModal: false as boolean,
      confirmModalTitle: '' as string,
      confirmModalMessage: '' as string,
      confirmModalDescription: '' as string,
      confirmModalType: 'warning' as 'danger' | 'warning' | 'info' | 'success',
      confirmModalConfirmText: 'Confirmar' as string,
      confirmModalProcessing: false as boolean,
      pendingAction: null as (() => Promise<void>) | null,
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
    },
    inscripcionesOrdenadas(): InscripcionConvocatoria[] {
      // Sort inscriptions: INS first, then ACE, then REJ
      const order = { INS: 1, ACE: 2, REJ: 3 }
      return [...this.inscripciones].sort((a, b) => {
        const orderA = order[a.estado as keyof typeof order] || 999
        const orderB = order[b.estado as keyof typeof order] || 999
        return orderA - orderB
      })
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
      this.showConfirmation(
        'Aprobar Inscripción',
        `¿Estás seguro de que deseas aprobar a ${this.getVoluntarioNombre(item.voluntario)}?`,
        'Esta acción cambiará el estado de la inscripción a APROBADO.',
        'success',
        'Aprobar',
        async () => {
          this.processingIds.add(item.id)
          try {
            await inscripcionConvocatoriaAPI.aceptar(item.id)
            // Update estado in local list
            const index = this.inscripciones.findIndex(i => i.id === item.id)
            if (index !== -1 && this.inscripciones[index]) {
              this.inscripciones[index].estado = 'ACE'
            }
          } catch (err: any) {
            console.error('Error aprobar inscripción:', err)
            alert(err?.response?.data?.detail || 'Error al aprobar la inscripción')
          } finally {
            this.processingIds.delete(item.id)
          }
        }
      )
    },
    async rechazarInscripcion(item: InscripcionConvocatoria) {
      this.showConfirmation(
        'Rechazar Inscripción',
        `¿Estás seguro de que deseas rechazar a ${this.getVoluntarioNombre(item.voluntario)}?`,
        'Esta acción cambiará el estado de la inscripción a RECHAZADO.',
        'danger',
        'Rechazar',
        async () => {
          this.processingIds.add(item.id)
          try {
            await inscripcionConvocatoriaAPI.rechazar(item.id)
            // Update estado in local list
            const index = this.inscripciones.findIndex(i => i.id === item.id)
            if (index !== -1 && this.inscripciones[index]) {
              this.inscripciones[index].estado = 'REJ'
            }
          } catch (err: any) {
            console.error('Error rechazar inscripción:', err)
            alert(err?.response?.data?.detail || 'Error al rechazar la inscripción')
          } finally {
            this.processingIds.delete(item.id)
          }
        }
      )
    },
    async revertirAprobar(item: InscripcionConvocatoria) {
      this.showConfirmation(
        'Revertir Aprobación',
        `¿Estás seguro de que deseas revertir la aprobación de ${this.getVoluntarioNombre(item.voluntario)}?`,
        'El voluntario volverá al estado INSCRITO (pendiente de aprobación).',
        'warning',
        'Revertir',
        async () => {
          this.processingIds.add(item.id)
          try {
            // Update to INSCRITO state using the API's update method
            await (inscripcionConvocatoriaAPI as any).update(item.id, { estado: 'INS' })
            // Update estado in local list
            const index = this.inscripciones.findIndex(i => i.id === item.id)
            if (index !== -1 && this.inscripciones[index]) {
              this.inscripciones[index].estado = 'INS'
            }
          } catch (err: any) {
            console.error('Error revertir aprobación:', err)
            alert(err?.response?.data?.detail || 'Error al revertir la aprobación')
          } finally {
            this.processingIds.delete(item.id)
          }
        }
      )
    },
    async revertirRechazo(item: InscripcionConvocatoria) {
      this.showConfirmation(
        'Revertir Rechazo',
        `¿Estás seguro de que deseas revertir el rechazo de ${this.getVoluntarioNombre(item.voluntario)}?`,
        'El voluntario volverá al estado INSCRITO (pendiente de aprobación).',
        'warning',
        'Revertir',
        async () => {
          this.processingIds.add(item.id)
          try {
            // Update to INSCRITO state using the API's update method
            await (inscripcionConvocatoriaAPI as any).update(item.id, { estado: 'INS' })
            // Update estado in local list
            const index = this.inscripciones.findIndex(i => i.id === item.id)
            if (index !== -1 && this.inscripciones[index]) {
              this.inscripciones[index].estado = 'INS'
            }
          } catch (err: any) {
            console.error('Error revertir rechazo:', err)
            alert(err?.response?.data?.detail || 'Error al revertir el rechazo')
          } finally {
            this.processingIds.delete(item.id)
          }
        }
      )
    },
    async aprobarTodos() {
      const pendientes = this.inscripcionesPendientes
      this.showConfirmation(
        'Aprobar Todas las Inscripciones',
        `¿Estás seguro de que deseas aprobar TODAS las ${pendientes.length} inscripciones pendientes?`,
        'Esta acción aprobará todas las inscripciones pendientes de forma masiva.',
        'success',
        'Aprobar Todas',
        async () => {
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
          }
        }
      )
    },
    async rechazarTodos() {
      const pendientes = this.inscripcionesPendientes
      this.showConfirmation(
        'Rechazar Todas las Inscripciones',
        `¿Estás seguro de que deseas rechazar TODAS las ${pendientes.length} inscripciones pendientes?`,
        'Esta acción rechazará todas las inscripciones pendientes de forma masiva.',
        'danger',
        'Rechazar Todas',
        async () => {
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
          }
        }
      )
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
    getAvatarClass(estado: string): string {
      const classes = {
        INS: 'avatar-wrapper',
        ACE: 'avatar-wrapper-success',
        REJ: 'avatar-wrapper-danger'
      }
      return classes[estado as keyof typeof classes] || 'avatar-wrapper'
    },
    getAvatarIcon(estado: string): string {
      const icons = {
        INS: 'bi bi-person-circle text-primary',
        ACE: 'bi bi-person-check text-success',
        REJ: 'bi bi-person-x text-danger'
      }
      return icons[estado as keyof typeof icons] || 'bi bi-person-circle text-primary'
    },
    getEstadoBadgeClass(estado: string): string {
      const classes = {
        INS: 'badge bg-warning text-dark',
        ACE: 'badge bg-success',
        REJ: 'badge bg-danger'
      }
      return classes[estado as keyof typeof classes] || 'badge bg-secondary'
    },
    getEstadoIcon(estado: string): string {
      const icons = {
        INS: 'bi bi-hourglass-split',
        ACE: 'bi bi-check-circle',
        REJ: 'bi bi-x-circle'
      }
      return icons[estado as keyof typeof icons] || 'bi bi-question-circle'
    },
    getEstadoLabel(estado: string): string {
      const labels = {
        INS: 'Pendiente',
        ACE: 'Aprobado',
        REJ: 'Rechazado'
      }
      return labels[estado as keyof typeof labels] || 'Desconocido'
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
    showConfirmation(title: string, message: string, description: string, type: 'danger' | 'warning' | 'info' | 'success', confirmText: string, action: () => Promise<void>) {
      this.confirmModalTitle = title
      this.confirmModalMessage = message
      this.confirmModalDescription = description
      this.confirmModalType = type
      this.confirmModalConfirmText = confirmText
      this.pendingAction = action
      this.showConfirmModal = true
    },
    async handleConfirmAction() {
      if (this.pendingAction) {
        this.confirmModalProcessing = true
        try {
          await this.pendingAction()
        } finally {
          this.confirmModalProcessing = false
          this.showConfirmModal = false
          this.pendingAction = null
        }
      }
    },
    handleCancelConfirm() {
      this.showConfirmModal = false
      this.pendingAction = null
      this.confirmModalProcessing = false
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

.aprobar-header .badge {
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .aprobar-header .d-flex.gap-2 {
    flex-direction: column;
    align-items: stretch !important;
  }
  
  .aprobar-header .badge {
    text-align: center;
  }
}

.btn-group .btn {
  min-width: 90px;
}

.btn-group .btn-info {
  min-width: 40px;
}
</style>
