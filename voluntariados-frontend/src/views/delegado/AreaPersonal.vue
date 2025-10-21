<!-- src/views/delegado/AreaPersonal.vue -->
<template>
  <div class="delegado-area-personal">
    <AppNavBar />

    <div class="container py-4">
      <div class="d-flex align-items-center mb-3">
        <i class="bi bi-person-badge me-2 text-primary" style="font-size: 1.5rem;"></i>
        <h2 class="mb-0">Área Personal • Delegado</h2>
      </div>
      <p class="text-muted mb-4">
        Bienvenido a tu área personal como <strong>Delegado</strong>. Aquí podrás gestionar información y acciones relacionadas a tu organización y voluntariados.
      </p>

      <!-- Upcoming Voluntariados Table (Non-clickable) -->
      <div class="voluntariados-table-container mb-5">
        <AdminTable
          title="Próximos Voluntariados"
          :columns="columnsUpcoming"
          :items="voluntariadosProximos"
          :loading="loadingUpcoming"
          :error="errorUpcoming ?? undefined"
          empty-text="No tenés voluntariados próximos programados."
          :show-create-button="false"
          :clickable-rows="false"
          :show-actions="false"
          @retry="loadUpcomingData"
        >
          <!-- Custom cell templates for upcoming -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="icon-wrapper-upcoming me-3">
                <i class="bi bi-calendar-event text-info fs-5"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }}</span>
                <span class="badge bg-info ms-2">Próximamente</span>
              </div>
            </div>
          </template>

          <template #cell-fecha_inicio="{ item }">
            <span>{{ formatDate(item.fecha_inicio) }}</span>
          </template>

          <template #cell-fecha_fin="{ item }">
            <span>{{ formatDate(item.fecha_fin) }}</span>
          </template>

          <template #cell-voluntarios_count="{ item }">
            <div class="d-flex align-items-center justify-content-center">
              <i class="bi bi-people-fill text-info me-2"></i>
              <span class="badge bg-info">
                {{ item.voluntarios_count ?? 0 }}
              </span>
            </div>
          </template>
        </AdminTable>
      </div>

      <!-- Active Voluntariados Table using AdminTable -->
      <div class="voluntariados-table-container">
        <AdminTable
          title="Mis Voluntariados Activos"
          :columns="columns"
          :items="voluntariados"
          :loading="loading"
          :error="error ?? undefined"
          empty-text="No tenés voluntariados activos asignados actualmente."
          :show-create-button="false"
          :clickable-rows="true"
          :show-actions="false"
          @retry="loadData"
          @row-click="handleRowClick"
        >
          <!-- Custom cell templates -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center" :class="{ 'selected-row-indicator': isExpanded(item.id) }">
              <div class="icon-wrapper me-3">
                <i class="bi bi-heart-fill text-danger fs-5"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }}</span>
              </div>
            </div>
          </template>

          <template #cell-fecha_inicio="{ item }">
            <span :class="{ 'text-primary fw-bold': isExpanded(item.id) }">
              {{ formatDate(item.fecha_inicio) }}
            </span>
          </template>

          <template #cell-fecha_fin="{ item }">
            <span :class="{ 'text-primary fw-bold': isExpanded(item.id) }">
              {{ formatDate(item.fecha_fin) }}
            </span>
          </template>

          <template #cell-voluntarios_count="{ item }">
            <div class="d-flex align-items-center justify-content-center">
              <i class="bi bi-people-fill text-primary me-2"></i>
              <span class="badge bg-primary" :class="{ 'fw-bold fs-6': isExpanded(item.id) }">
                {{ item.voluntarios_count ?? 0 }}
              </span>
            </div>
          </template>
        </AdminTable>

        <!-- Expandable Detail Panel -->
        <transition name="expand">
          <VoluntariadoDetailPanel
            v-if="selectedVoluntariado"
            :voluntariado="selectedVoluntariado"
            @close="closePanel"
            @view-detail="viewDetail"
            @manage-turnos="manageTurnos"
            @view-inscripciones="viewInscripciones"
            @edit-voluntariado="editVoluntariado"
          />
        </transition>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import VoluntariadoDetailPanel from '@/components/delegado/VoluntariadoDetailPanel.vue'
import { voluntariadoAPI } from '@/services/api'

export default defineComponent({
  name: 'DelegadoAreaPersonal',
  components: { AppNavBar, AdminTable, VoluntariadoDetailPanel },
  data() {
    return {
      loading: false as boolean,
      error: null as string | null,
      voluntariados: [] as Array<{ id: number; nombre: string; fecha_inicio?: string | null; fecha_fin?: string | null; estado: string; voluntarios_count?: number }>,
      columns: [
        { key: 'nombre', label: 'Nombre del Voluntariado', sortable: true },
        { key: 'fecha_inicio', label: 'Fecha de Inicio', sortable: true },
        { key: 'fecha_fin', label: 'Fecha de Fin', sortable: true },
        { key: 'voluntarios_count', label: 'Voluntarios Inscritos', sortable: true, align: 'center' }
      ] as TableColumn[],
      selectedVoluntariado: null as any,
      // Upcoming voluntariados
      loadingUpcoming: false as boolean,
      errorUpcoming: null as string | null,
      voluntariadosProximos: [] as Array<{ id: number; nombre: string; fecha_inicio?: string | null; fecha_fin?: string | null; estado: string; voluntarios_count?: number }>,
      columnsUpcoming: [
        { key: 'nombre', label: 'Nombre del Voluntariado', sortable: true },
        { key: 'fecha_inicio', label: 'Fecha de Inicio', sortable: true },
        { key: 'fecha_fin', label: 'Fecha de Fin', sortable: true },
        { key: 'voluntarios_count', label: 'Voluntarios Inscritos', sortable: true, align: 'center' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.loadUpcomingData()
    this.loadData()
  },
  methods: {
    async loadUpcomingData() {
      this.loadingUpcoming = true
      this.errorUpcoming = null
      try {
        const res = await voluntariadoAPI.getMineUpcoming()
        const data = (res.data && res.data.results) ? res.data.results : res.data
        this.voluntariadosProximos = Array.isArray(data) ? data : []
      } catch (err: any) {
        console.error('Error loading próximos voluntariados:', err)
        this.errorUpcoming = err?.response?.data?.detail || 'Error al cargar los voluntariados próximos'
      } finally {
        this.loadingUpcoming = false
      }
    },
    async loadData() {
      this.loading = true
      this.error = null
      try {
        const res = await voluntariadoAPI.getMineActive()
        // If paginated, DRF returns { results: [...] }
        const data = (res.data && res.data.results) ? res.data.results : res.data
        this.voluntariados = Array.isArray(data) ? data : []
      } catch (err: any) {
        console.error('Error loading mis voluntariados activos:', err)
        this.error = err?.response?.data?.detail || 'Error al cargar los voluntariados'
      } finally {
        this.loading = false
      }
    },
    formatDate(date?: string | null): string {
      if (!date) return '-'
      try {
        const d = new Date(date)
        return d.toLocaleDateString()
      } catch {
        return String(date)
      }
    },
    handleRowClick(item: any) {
      // Toggle expansion on row click
      if (this.selectedVoluntariado?.id === item.id) {
        this.selectedVoluntariado = null
      } else {
        this.selectedVoluntariado = item
      }
    },
    toggleExpand(item: any) {
      // Toggle expansion via button
      this.handleRowClick(item)
    },
    isExpanded(id: number): boolean {
      return this.selectedVoluntariado?.id === id
    },
    closePanel() {
      this.selectedVoluntariado = null
    },
    viewDetail() {
      if (this.selectedVoluntariado) {
        this.$router.push(`/voluntariados/${this.selectedVoluntariado.id}`)
      }
    },
    manageTurnos() {
      // TODO: Navigate to turnos management view
      if (this.selectedVoluntariado) {
        console.log('Manage turnos for:', this.selectedVoluntariado.id)
        // this.$router.push(`/delegado/voluntariados/${this.selectedVoluntariado.id}/turnos`)
        alert('Gestión de turnos - próximamente')
      }
    },
    viewInscripciones() {
      // TODO: Navigate to inscripciones view
      if (this.selectedVoluntariado) {
        console.log('View inscripciones for:', this.selectedVoluntariado.id)
        // this.$router.push(`/delegado/voluntariados/${this.selectedVoluntariado.id}/inscripciones`)
        alert('Ver inscripciones - próximamente')
      }
    },
    editVoluntariado() {
      // TODO: Open edit modal or navigate to edit view
      if (this.selectedVoluntariado) {
        console.log('Edit voluntariado:', this.selectedVoluntariado.id)
        // Could open a modal or navigate to an edit page
        alert('Editar voluntariado - próximamente')
      }
    },
    estadoBadgeClass(estado: string): string {
      switch (estado) {
        case 'ACTIVE': return 'bg-success'
        case 'DRAFT': return 'bg-secondary'
        case 'CLOSED': return 'bg-dark'
        default: return 'bg-secondary'
      }
    },
    getEstadoDisplay(estado: string): string {
      const displays: Record<string, string> = {
        'DRAFT': 'Borrador',
        'ACTIVE': 'Activo',
        'CLOSED': 'Cerrado'
      }
      return displays[estado] || estado
    }
  }
})
</script>

<style scoped>
.delegado-area-personal {
  display: block;
}

.voluntariados-table-container {
  position: relative;
}

.icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 0.5rem;
}

.icon-wrapper-upcoming {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(13, 202, 240, 0.1);
  border-radius: 0.5rem;
}

/* Selected row indicator */
.selected-row-indicator {
  position: relative;
}

.selected-row-indicator::before {
  content: '';
  position: absolute;
  left: -12px;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #0d6efd 0%, #0a58ca 100%);
  border-radius: 2px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    height: 0;
    opacity: 0;
  }
  to {
    height: 100%;
    opacity: 1;
  }
}

/* Global style to highlight the entire row */
:deep(.table tbody tr:has(.selected-row-indicator)) {
  background-color: rgba(13, 110, 253, 0.05) !important;
  border-left: 3px solid #0d6efd;
  transition: all 0.3s ease;
}

:deep(.table tbody tr:has(.selected-row-indicator)):hover {
  background-color: rgba(13, 110, 253, 0.1) !important;
}

/* Expandable panel transition */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
