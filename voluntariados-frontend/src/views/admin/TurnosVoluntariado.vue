<!-- src/views/admin/TurnosVoluntariado.vue -->
<template>
  <AdminLayout
    :page-title="voluntariado ? `Turnos de ${voluntariado.nombre}` : 'Turnos'"
    :breadcrumbs="[
      { label: 'Voluntariados' },
      { label: voluntariado ? voluntariado.nombre : '...' },
      { label: 'Turnos' }
    ]"
  >

    <div class="row">
      <div class="col">
        <AdminTable
          title="Turnos"
          :columns="columns"
          :items="turnos"
          :loading="loading"
          :error="error || undefined"
          :show-create-button="true"
          create-button-text="Nuevo Turno"
          empty-text="No hay turnos creados"
          @create="openCreate"
          @edit="onEdit"
          @delete="onDelete"
          @retry="loadData"
        >
          <template #cell-fecha="{ value }">
            {{ formatDate(value) }}
          </template>
          <template #cell-hora_inicio="{ value }">
            {{ formatTime(value) }}
          </template>
          <template #cell-hora_fin="{ value }">
            {{ formatTime(value) }}
          </template>
          <template #cell-inscripciones_count="{ value }">
            <span class="badge bg-info">{{ value ?? 0 }}</span>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Turno Modal -->
    <TurnoModal
      v-if="showTurnoModal"
      :show="showTurnoModal"
      :turno-data="editingTurno"
      :initial-date="defaultDate"
      @close="closeTurnoModal"
      @save="handleSaveTurno"
    />
    <!-- Confirmation Modal for delete -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar turno"
      :message="deleteTurnoMessage()"
      :processing="deleteProcessing"
      processing-text="Eliminando..."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      @confirm="confirmDeleteTurno"
      @cancel="cancelDeleteTurno"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import TurnoModal from '@/components/admin/TurnoModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { voluntariadoAPI, turnoAPI } from '@/services/api'
import { formatDateShort } from '@/utils/dateUtils'

interface Voluntariado { id: number; nombre: string }
interface Turno {
  id?: number
  fecha: string
  hora_inicio: string
  hora_fin: string
  cupo: number
  lugar: string
  inscripciones_count?: number
}

export default defineComponent({
  name: 'AdminTurnosVoluntariado',
  components: { AdminLayout, AdminTable, TurnoModal, ConfirmationModal },
  data() {
    return {
      loading: false as boolean,
      error: null as string | null,
      voluntariado: null as Voluntariado | null,
      turnos: [] as Turno[],
      columns: [
        { key: 'fecha', label: 'Fecha' },
        { key: 'hora_inicio', label: 'Hora Inicio' },
        { key: 'hora_fin', label: 'Hora Fin' },
        { key: 'cupo', label: 'Cupo' },
        { key: 'lugar', label: 'Lugar' },
        { key: 'inscripciones_count', label: 'Inscriptos' }
      ] as TableColumn[],
      showTurnoModal: false,
  editingTurno: null as Turno | null,
  // Delete confirmation modal state
  showDeleteModal: false,
  deleteProcessing: false,
  deleteTargetTurno: null as Turno | null,
    }
  },
  computed: {
  voluntariadoId(): number { return parseInt(this.$route.params.id as string) },
  defaultDate(): string { const parts = new Date().toISOString().split('T'); return parts[0] || '' }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      this.error = null
      try {
        const [vRes, tRes] = await Promise.all([
          voluntariadoAPI.getById(this.voluntariadoId),
          voluntariadoAPI.getTurnos(this.voluntariadoId)
        ])
        this.voluntariado = vRes.data
        this.turnos = Array.isArray(tRes.data) ? tRes.data : []
      } catch (err: any) {
        console.error(err)
        this.error = err?.response?.data?.detail || 'Error al cargar turnos'
      } finally {
        this.loading = false
      }
    },
    openCreate() {
      this.editingTurno = null
      this.showTurnoModal = true
    },
    onEdit(turno: Turno) {
      this.editingTurno = { ...turno, lugar: turno.lugar || '' }
      this.showTurnoModal = true
    },
    async onDelete(turno: Turno) {
      this.deleteTargetTurno = turno
      this.showDeleteModal = true
    },
    deleteTurnoMessage(): string {
      if (!this.deleteTargetTurno) return '¿Eliminar turno?'
      const f = this.formatDate(this.deleteTargetTurno.fecha)
      const hi = this.formatTime(this.deleteTargetTurno.hora_inicio)
      const hf = this.formatTime(this.deleteTargetTurno.hora_fin)
      return `¿Eliminar el turno del ${f} ${hi} - ${hf}?`
    },
    async confirmDeleteTurno() {
      if (!this.deleteTargetTurno || !this.deleteTargetTurno.id) return
      this.deleteProcessing = true
      try {
        await turnoAPI.delete(this.deleteTargetTurno.id)
        this.showDeleteModal = false
        this.deleteTargetTurno = null
        await this.loadData()
      } catch (err) {
        alert('No se pudo eliminar el turno')
      } finally {
        this.deleteProcessing = false
      }
    },
    cancelDeleteTurno() {
      this.showDeleteModal = false
      this.deleteTargetTurno = null
      this.deleteProcessing = false
    },
    closeTurnoModal() {
      this.showTurnoModal = false
    },
    async handleSaveTurno(turnoData: Turno) {
      try {
        if (this.editingTurno && this.editingTurno.id) {
          await turnoAPI.update(this.editingTurno.id, {
            fecha: turnoData.fecha,
            hora_inicio: turnoData.hora_inicio,
            hora_fin: turnoData.hora_fin,
            cupo: turnoData.cupo,
            lugar: turnoData.lugar || ''
          })
        } else {
          await turnoAPI.create({
            fecha: turnoData.fecha,
            hora_inicio: turnoData.hora_inicio,
            hora_fin: turnoData.hora_fin,
            cupo: turnoData.cupo,
            lugar: turnoData.lugar || '',
            voluntariado_id: this.voluntariadoId
          })
        }
        this.showTurnoModal = false
        await this.loadData()
      } catch (err) {
        console.error('Error al guardar turno', err)
        alert('No se pudo guardar el turno')
      }
    },
    formatDate(date: string) {
      try { return formatDateShort(date) } catch { return date }
    },
    formatTime(time: string) {
      try { const [h,m] = time.split(':'); return `${h}:${m}` } catch { return time }
    }
  }
})
</script>

<style scoped>
</style>
