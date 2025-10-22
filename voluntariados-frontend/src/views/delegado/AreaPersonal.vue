<!-- src/views/delegado/AreaPersonal.vue -->
<template>
  <div class="delegado-area-personal">
    <AppNavBar />

    <div class="container py-4">
      <div class="area-personal-header mb-4">
        <div class="d-flex align-items-center">
          <i class="bi bi-person-badge me-3 text-white" style="font-size: 1.8rem;"></i>
          <h2 class="mb-0 text-white">Área Personal</h2>
        </div>
      </div>
      <p class="text-muted mb-4">
        Bienvenido a tu área personal. Aquí podrás gestionar información y acciones relacionadas a tu organización y voluntariados.
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
          :clickable-rows="false"
          :show-actions="true"
          @retry="loadData"
        >
          <!-- Custom cell templates -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="icon-wrapper me-3">
                <i class="bi bi-heart-fill text-danger fs-5"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }}</span>
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
              <i class="bi bi-people-fill text-primary me-2"></i>
              <span class="badge bg-primary">
                {{ item.voluntarios_count ?? 0 }}
              </span>
            </div>
          </template>

          <!-- Progress cell -->
          <template #cell-progress="{ item }">
            <div class="progress w-100" style="height: 10px;">
              <div
                class="progress-bar"
                role="progressbar"
                :style="{ width: (progressMap[item.id] ?? 0) + '%' }"
                :aria-valuenow="progressMap[item.id] ?? 0"
                aria-valuemin="0"
                aria-valuemax="100"
              ></div>
            </div>
            <small class="text-muted ms-1">{{ progressMap[item.id] ?? 0 }}%</small>
          </template>

          <!-- Row actions -->
          <template #actions="{ item }">
            <button class="btn btn-sm btn-outline-primary" @click.stop="manageTurnos(item)">
              <i class="bi bi-calendar-check me-1"></i>
              Gestionar Turnos
            </button>
          </template>
        </AdminTable>
      </div>

      <!-- Finished Voluntariados Table -->
      <div class="voluntariados-table-container mt-5">
        <AdminTable
          title="Voluntariados Finalizados"
          :columns="columnsFinished"
          :items="voluntariadosFinalizados"
          :loading="loadingFinished"
          :error="errorFinished ?? undefined"
          empty-text="No tenés voluntariados finalizados."
          :show-create-button="false"
          :clickable-rows="false"
          :show-actions="true"
          @retry="loadFinishedData"
        >
          <!-- Custom cell templates for finished -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="icon-wrapper-finished me-3">
                <i class="bi bi-check-circle-fill text-success fs-5"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }}</span>
                <span class="badge bg-secondary ms-2">Finalizado</span>
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
              <i class="bi bi-people-fill text-secondary me-2"></i>
              <span class="badge bg-secondary">
                {{ item.voluntarios_count ?? 0 }}
              </span>
            </div>
          </template>

          <!-- Row actions -->
          <template #actions="{ item }">
            <button class="btn btn-sm btn-outline-secondary" @click.stop="manageTurnos(item)">
              <i class="bi bi-calendar-check me-1"></i>
              Gestionar Turnos
            </button>
          </template>
        </AdminTable>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import { voluntariadoAPI } from '@/services/api'

export default defineComponent({
  name: 'DelegadoAreaPersonal',
  components: { AppNavBar, AdminTable },
  watch: {
    '$route'(to, from) {
      // Reload data when navigating back to this view from turnos or asistencia management
      if (to.name === 'DelegadoAreaPersonal' && from.name) {
        this.loadUpcomingData()
        this.loadData()
        this.loadFinishedData()
      }
    }
  },
  data() {
    return {
      loading: false as boolean,
      error: null as string | null,
      voluntariados: [] as Array<{ id: number; nombre: string; fecha_inicio?: string | null; fecha_fin?: string | null; estado: string; voluntarios_count?: number }>,
      columns: [
        { key: 'nombre', label: 'Nombre del Voluntariado', sortable: true },
        { key: 'fecha_inicio', label: 'Fecha de Inicio', sortable: true },
        { key: 'fecha_fin', label: 'Fecha de Fin', sortable: true },
        { key: 'voluntarios_count', label: 'Voluntarios Inscritos', sortable: true, align: 'center' },
        { key: 'progress', label: 'Progreso', sortable: false, align: 'left' }
      ] as TableColumn[],
      progressMap: {} as Record<number, number>,
      // Upcoming voluntariados
      loadingUpcoming: false as boolean,
      errorUpcoming: null as string | null,
      voluntariadosProximos: [] as Array<{ id: number; nombre: string; fecha_inicio?: string | null; fecha_fin?: string | null; estado: string; voluntarios_count?: number }>,
      columnsUpcoming: [
        { key: 'nombre', label: 'Nombre del Voluntariado', sortable: true },
        { key: 'fecha_inicio', label: 'Fecha de Inicio', sortable: true },
        { key: 'fecha_fin', label: 'Fecha de Fin', sortable: true },
        { key: 'voluntarios_count', label: 'Voluntarios Inscritos', sortable: true, align: 'center' }
      ] as TableColumn[],
      // Finished voluntariados
      loadingFinished: false as boolean,
      errorFinished: null as string | null,
      voluntariadosFinalizados: [] as Array<{ id: number; nombre: string; fecha_inicio?: string | null; fecha_fin?: string | null; estado: string; voluntarios_count?: number }>,
      columnsFinished: [
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
    this.loadFinishedData()
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
    async loadFinishedData() {
      this.loadingFinished = true
      this.errorFinished = null
      try {
        const res = await voluntariadoAPI.getMineFinished()
        const data = (res.data && res.data.results) ? res.data.results : res.data
        this.voluntariadosFinalizados = Array.isArray(data) ? data : []
      } catch (err: any) {
        console.error('Error loading voluntariados finalizados:', err)
        this.errorFinished = err?.response?.data?.detail || 'Error al cargar los voluntariados finalizados'
      } finally {
        this.loadingFinished = false
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
        // Load progress for each voluntariado
        await this.loadProgressForVoluntariados(this.voluntariados)
      } catch (err: any) {
        console.error('Error loading mis voluntariados activos:', err)
        this.error = err?.response?.data?.detail || 'Error al cargar los voluntariados'
      } finally {
        this.loading = false
      }
    },
    async loadProgressForVoluntariados(items: Array<{ id: number }>) {
      const requests = items.map(v => (
        voluntariadoAPI.getProgress(v.id)
          .then(resp => {
            console.log(`Progress for voluntariado ${v.id}:`, resp.data)
            return { id: v.id, progreso: resp.data?.progreso ?? 0 }
          })
          .catch(err => {
            console.error(`Error loading progress for voluntariado ${v.id}:`, err)
            return { id: v.id, progreso: 0 }
          })
      ))
      const results = await Promise.all(requests)
      results.forEach(r => { this.progressMap[r.id] = r.progreso })
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
    manageTurnos(item: any) {
      // Navigate to turnos management view for the selected row
      if (item && item.id) {
        this.$router.push({
          name: 'DelegadoTurnosManagement',
          params: { id: item.id }
        })
      }
    },
    refreshAll() {
      // Manually refresh all data
      this.loadUpcomingData()
      this.loadData()
      this.loadFinishedData()
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

.icon-wrapper-finished {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 135, 84, 0.1);
  border-radius: 0.5rem;
}

.area-personal-header {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  padding: 1.5rem 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(220, 53, 69, 0.2);
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.spin {
  animation: spin 1s linear infinite;
}

</style>
