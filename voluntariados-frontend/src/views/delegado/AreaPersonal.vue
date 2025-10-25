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
        Bienvenido a tu área personal. Aquí podrás gestionar los voluntariados y realizar seguimiento de turnos y asistencias.
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

          <template #cell-convocatoria_inicio="{ item }">
            <span>
              {{ getConvocatoriaStart(item) ? formatDate(getConvocatoriaStart(item)) : '-' }}
            </span>
          </template>

          <template #cell-dias_para_convocatoria="{ item }">
            <div class="text-center">
              <i class="bi bi-hourglass-split text-info me-1"></i>
              <span>{{ daysUntil(getConvocatoriaStart(item)) ?? '-' }}</span>
            </div>
          </template>

          <template #cell-turnos_count="{ item }">
            <div class="d-flex align-items-center justify-content-center">
              <i class="bi bi-clock-history text-info me-2"></i>
              <span class="badge bg-info">{{ turnosCountMap[item.id] ?? 0 }}</span>
            </div>
          </template>
        </AdminTable>
      </div>

      <!-- Convocatoria Voluntariados Table -->
      <div class="voluntariados-table-container mb-5">
        <AdminTable
          title="Voluntariados en Convocatoria"
          :columns="columnsConvocatoria"
          :items="voluntariadosConvocatoria"
          :loading="loadingConvocatoria"
          :error="errorConvocatoria ?? undefined"
          empty-text="No hay voluntariados en convocatoria."
          :show-create-button="false"
          :clickable-rows="false"
          :show-actions="false"
          @retry="loadConvocatoriaData"
        >
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="icon-wrapper-upcoming me-3">
                <i class="bi bi-megaphone text-primary fs-5"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }}</span>
                <span class="badge bg-primary ms-2">Convocatoria</span>
              </div>
            </div>
          </template>
          <template #cell-fecha_activo_inicio="{ item }">
            <span>{{ getActiveStart(item) ? formatDate(getActiveStart(item)) : '-' }}</span>
          </template>
          <template #cell-dias_para_activo="{ item }">
            <div class="text-center">
              <i class="bi bi-hourglass-split text-primary me-1"></i>
              <span>{{ daysUntil(getActiveStart(item)) ?? '-' }}</span>
            </div>
          </template>
          <template #cell-inscriptos_count="{ item }">
            <div class="d-flex align-items-center justify-content-center">
              <i class="bi bi-people-fill text-primary me-2"></i>
              <span class="badge bg-primary">{{ item.inscriptos_count ?? item.voluntarios_count ?? 0 }}</span>
            </div>
          </template>
        </AdminTable>
      </div>

      <!-- Preparación Voluntariados Table -->
      <div class="voluntariados-table-container mb-5">
        <AdminTable
          title="Voluntariados en Preparación (Pendientes de Aprobación)"
          :columns="columnsPreparacion"
          :items="voluntariadosPreparacion"
          :loading="loadingPreparacion"
          :error="errorPreparacion ?? undefined"
          empty-text="No hay voluntariados en preparación."
          :show-create-button="false"
          :clickable-rows="false"
          :show-actions="true"
          @retry="loadPreparacionData"
        >
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="icon-wrapper-preparacion me-3">
                <i class="bi bi-hourglass-split text-warning fs-5"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }}</span>
                <span class="badge bg-warning text-dark ms-2">Preparación</span>
              </div>
            </div>
          </template>
          <template #cell-fecha_activo_inicio="{ item }">
            <span>{{ getActiveStart(item) ? formatDate(getActiveStart(item)) : '-' }}</span>
          </template>
          <template #cell-dias_para_activo="{ item }">
            <div class="text-center">
              <i class="bi bi-hourglass-split text-warning me-1"></i>
              <span>{{ daysUntil(getActiveStart(item)) ?? '-' }}</span>
            </div>
          </template>
          <template #cell-inscriptos_totales="{ item }">
            <div class="d-flex align-items-center justify-content-center">
              <i class="bi bi-people-fill text-info me-2"></i>
              <span class="badge bg-info">{{ inscriptosTotalesMap[item.id] ?? 0 }}</span>
            </div>
          </template>
          <template #cell-inscriptos_pendientes="{ item }">
            <div class="d-flex align-items-center justify-content-center">
              <i class="bi bi-person-exclamation text-warning me-2"></i>
              <span class="badge bg-warning text-dark">{{ inscriptosPendientesMap[item.id] ?? 0 }}</span>
            </div>
          </template>
          <template #actions="{ item }">
            <button class="btn btn-sm btn-outline-warning" @click.stop="aprobarInscriptos(item)">
              <i class="bi bi-clipboard-check me-1"></i>
              Aprobar Inscriptos
            </button>
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
            <span>{{ formatDate(item.fecha_inicio_cursado) }}</span>
          </template>

          <template #cell-fecha_fin="{ item }">
            <span>{{ formatDate(item.fecha_fin_cursado) }}</span>
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
                <span v-if="asistenciaCompletaMap[item.id] === false" class="badge bg-warning text-dark ms-2">
                  <i class="bi bi-exclamation-triangle-fill me-1"></i>
                  Asistencia Incompleta
                </span>
              </div>
            </div>
          </template>

          <template #cell-fecha_inicio="{ item }">
            <span>{{ formatDate(item.fecha_inicio_cursado) }}</span>
          </template>

          <template #cell-fecha_fin="{ item }">
            <span>{{ formatDate(item.fecha_fin_cursado) }}</span>
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
import { formatDateShort, parseLocalDate } from '@/utils/dateUtils'

export default defineComponent({
  name: 'DelegadoAreaPersonal',
  components: { AppNavBar, AdminTable },
  watch: {
    '$route'(to, from) {
      // Reload data when navigating back to this view from turnos or asistencia management
      if (to.name === 'DelegadoAreaPersonal' && from.name) {
        this.loadUpcomingData()
        this.loadConvocatoriaData()
        this.loadPreparacionData()
        this.loadData()
        this.loadFinishedData()
      }
    }
  },
  data() {
    return {
      loading: false as boolean,
      error: null as string | null,
      voluntariados: [] as Array<{ id: number; nombre: string; fecha_inicio_cursado?: string | null; fecha_fin_cursado?: string | null; estado: string; voluntarios_count?: number }>,
      columns: [
        { key: 'nombre', label: 'Nombre', sortable: true },
        { key: 'fecha_inicio', label: 'Fecha de Inicio', sortable: true },
        { key: 'fecha_fin', label: 'Fecha de Fin', sortable: true },
        { key: 'voluntarios_count', label: 'Voluntarios Inscritos', sortable: true, align: 'center' },
        { key: 'progress', label: 'Progreso', sortable: false, align: 'left' }
      ] as TableColumn[],
      progressMap: {} as Record<number, number>,
      // Upcoming voluntariados
      loadingUpcoming: false as boolean,
      errorUpcoming: null as string | null,
      voluntariadosProximos: [] as Array<{ id: number; nombre: string; fecha_inicio_convocatoria?: string | null; fecha_fin_convocatoria?: string | null; fecha_inicio_cursado?: string | null; fecha_fin_cursado?: string | null; estado: string; voluntarios_count?: number }>,
      columnsUpcoming: [
        { key: 'nombre', label: 'Nombre', sortable: true },
        { key: 'convocatoria_inicio', label: 'Inicio de Convocatoria', sortable: true },
        { key: 'dias_para_convocatoria', label: 'Días para Convocatoria', sortable: false, align: 'center' },
        { key: 'turnos_count', label: 'Turnos Definidos', sortable: false, align: 'center' }
      ] as TableColumn[],
      turnosCountMap: {} as Record<number, number>,
      // Convocatoria voluntariados
      loadingConvocatoria: false as boolean,
      errorConvocatoria: null as string | null,
      voluntariadosConvocatoria: [] as Array<{ id: number; nombre: string; fecha_inicio_convocatoria?: string | null; fecha_fin_convocatoria?: string | null; fecha_inicio_cursado?: string | null; fecha_fin_cursado?: string | null; estado: string; voluntarios_count?: number; inscriptos_count?: number }>,
      columnsConvocatoria: [
        { key: 'nombre', label: 'Nombre', sortable: true },
        { key: 'fecha_activo_inicio', label: 'Inicio del voluntariado', sortable: true },
        { key: 'dias_para_activo', label: 'Días para comenzar', sortable: false, align: 'center' },
        { key: 'inscriptos_count', label: 'Inscriptos', sortable: true, align: 'center' }
      ] as TableColumn[],
      // Preparación voluntariados
      loadingPreparacion: false as boolean,
      errorPreparacion: null as string | null,
      voluntariadosPreparacion: [] as Array<{ id: number; nombre: string; fecha_inicio_convocatoria?: string | null; fecha_fin_convocatoria?: string | null; fecha_inicio_cursado?: string | null; fecha_fin_cursado?: string | null; estado: string; voluntarios_count?: number; inscriptos_count?: number }>,
      columnsPreparacion: [
        { key: 'nombre', label: 'Nombre', sortable: true },
        { key: 'fecha_activo_inicio', label: 'Inicio del voluntariado', sortable: true },
        { key: 'dias_para_activo', label: 'Días para comenzar', sortable: false, align: 'center' },
        { key: 'inscriptos_totales', label: 'Total Inscriptos', sortable: true, align: 'center' },
        { key: 'inscriptos_pendientes', label: 'Pendientes de Aprobación', sortable: true, align: 'center' }
      ] as TableColumn[],
      inscriptosPendientesMap: {} as Record<number, number>,
      inscriptosTotalesMap: {} as Record<number, number>,
      // Finished voluntariados
      loadingFinished: false as boolean,
      errorFinished: null as string | null,
      voluntariadosFinalizados: [] as Array<{ id: number; nombre: string; fecha_inicio_cursado?: string | null; fecha_fin_cursado?: string | null; estado: string; voluntarios_count?: number }>,
      asistenciaCompletaMap: {} as Record<number, boolean>,
      columnsFinished: [
        { key: 'nombre', label: 'Nombre', sortable: true },
        { key: 'fecha_inicio', label: 'Fecha de Inicio', sortable: true },
        { key: 'fecha_fin', label: 'Fecha de Fin', sortable: true },
        { key: 'voluntarios_count', label: 'Voluntarios Inscritos', sortable: true, align: 'center' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.loadUpcomingData()
    this.loadConvocatoriaData()
    this.loadPreparacionData()
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
        // Load turnos count for each upcoming voluntariado
        await this.loadTurnosCountForVoluntariados(this.voluntariadosProximos)
      } catch (err: any) {
        console.error('Error loading próximos voluntariados:', err)
        this.errorUpcoming = err?.response?.data?.detail || 'Error al cargar los voluntariados próximos'
      } finally {
        this.loadingUpcoming = false
      }
    },
    async loadConvocatoriaData() {
      this.loadingConvocatoria = true
      this.errorConvocatoria = null
      try {
        // Try specific endpoint if available
        const res = await (voluntariadoAPI as any).getMineConvocatoria?.()
        if (res) {
          const data = (res.data && res.data.results) ? res.data.results : res.data
          this.voluntariadosConvocatoria = Array.isArray(data) ? data : []
        } else {
          // Fallback to empty list if endpoint not available
          this.voluntariadosConvocatoria = []
        }
      } catch (err: any) {
        console.error('Error loading voluntariados en convocatoria:', err)
        this.errorConvocatoria = err?.response?.data?.detail || 'Error al cargar los voluntariados en convocatoria'
        this.voluntariadosConvocatoria = []
      } finally {
        this.loadingConvocatoria = false
      }
    },
    async loadPreparacionData() {
      this.loadingPreparacion = true
      this.errorPreparacion = null
      try {
        const res = await (voluntariadoAPI as any).getMinePreparacion?.()
        if (res) {
          const data = (res.data && res.data.results) ? res.data.results : res.data
          this.voluntariadosPreparacion = Array.isArray(data) ? data : []
          // Load pending inscriptions count for each preparación voluntariado
          await this.loadInscriptosPendientesForVoluntariados(this.voluntariadosPreparacion)
          // Load total inscriptions count for each preparación voluntariado
          await this.loadInscriptosTotalesForVoluntariados(this.voluntariadosPreparacion)
        } else {
          this.voluntariadosPreparacion = []
        }
      } catch (err: any) {
        console.error('Error loading voluntariados en preparación:', err)
        this.errorPreparacion = err?.response?.data?.detail || 'Error al cargar los voluntariados en preparación'
        this.voluntariadosPreparacion = []
      } finally {
        this.loadingPreparacion = false
      }
    },
    async loadFinishedData() {
      this.loadingFinished = true
      this.errorFinished = null
      try {
        const res = await voluntariadoAPI.getMineFinished()
        const data = (res.data && res.data.results) ? res.data.results : res.data
        this.voluntariadosFinalizados = Array.isArray(data) ? data : []
        // Load asistencia completion status for each finished voluntariado
        await this.loadAsistenciaCompletaForVoluntariados(this.voluntariadosFinalizados)
      } catch (err: any) {
        console.error('Error loading voluntariados finalizados:', err)
        this.errorFinished = err?.response?.data?.detail || 'Error al cargar los voluntariados finalizados'
      } finally {
        this.loadingFinished = false
      }
    },
    async loadTurnosCountForVoluntariados(items: Array<{ id: number }>) {
      const requests = items.map(v => (
        (voluntariadoAPI as any).getTurnos(v.id)
          .then((resp: any) => {
            const arr = (resp.data && resp.data.results) ? resp.data.results : resp.data
            const count = Array.isArray(arr) ? arr.length : 0
            return { id: v.id, count }
          })
          .catch(() => ({ id: v.id, count: 0 }))
      ))
      const results = await Promise.all(requests)
      results.forEach(r => { this.turnosCountMap[r.id] = r.count })
    },
    async loadInscriptosPendientesForVoluntariados(items: Array<{ id: number }>) {
      const { inscripcionConvocatoriaAPI } = await import('@/services/api')
      const requests = items.map(v => (
        inscripcionConvocatoriaAPI.getAll()
          .then((resp: any) => {
            const arr = (resp.data && resp.data.results) ? resp.data.results : resp.data
            // Count inscriptions with estado INSCRITO (pending approval) for this specific voluntariado
            const pending = Array.isArray(arr) 
              ? arr.filter((insc: any) => {
                  // Check if the inscription belongs to this voluntariado
                  const matchesVoluntariado = (insc.voluntariado === v.id) || (insc.voluntariado?.id === v.id)
                  // Check if it's in INSCRITO state (pending approval)
                  const isPending = insc.estado === 'INS'
                  // Check if it's active
                  const isActive = insc.is_active !== false
                  // All conditions must be true
                  return matchesVoluntariado && isPending && isActive
                }).length
              : 0
            return { id: v.id, count: pending }
          })
          .catch(() => ({ id: v.id, count: 0 }))
      ))
      const results = await Promise.all(requests)
      results.forEach(r => { this.inscriptosPendientesMap[r.id] = r.count })
    },
    async loadInscriptosTotalesForVoluntariados(items: Array<{ id: number }>) {
      const { inscripcionConvocatoriaAPI } = await import('@/services/api')
      const requests = items.map(v => (
        inscripcionConvocatoriaAPI.getAll()
          .then((resp: any) => {
            const arr = (resp.data && resp.data.results) ? resp.data.results : resp.data
            // Count all inscriptions (INS, ACE, REJ) for this specific voluntariado
            const total = Array.isArray(arr) 
              ? arr.filter((insc: any) => {
                  // Check if the inscription belongs to this voluntariado
                  const matchesVoluntariado = (insc.voluntariado === v.id) || (insc.voluntariado?.id === v.id)
                  // Check if it's active
                  const isActive = insc.is_active !== false
                  // Both conditions must be true
                  return matchesVoluntariado && isActive
                }).length
              : 0
            return { id: v.id, count: total }
          })
          .catch(() => ({ id: v.id, count: 0 }))
      ))
      const results = await Promise.all(requests)
      results.forEach(r => { this.inscriptosTotalesMap[r.id] = r.count })
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
    async loadAsistenciaCompletaForVoluntariados(items: Array<{ id: number }>) {
      const requests = items.map(v => (
        voluntariadoAPI.getAsistenciaCompleta(v.id)
          .then(resp => ({ id: v.id, completa: resp.data?.completa ?? true }))
          .catch(() => ({ id: v.id, completa: true })) // Default to true on error to avoid false warnings
      ))
      const results = await Promise.all(requests)
      results.forEach(r => { this.asistenciaCompletaMap[r.id] = r.completa })
    },
    formatDate(date?: string | null): string {
      if (!date) return '-'
      try {
        return formatDateShort(date)
      } catch {
        return String(date)
      }
    },
    // Helpers for stage-specific fields
    getConvocatoriaStart(item: any): string | null {
      return item?.fecha_inicio_convocatoria || null
    },
    getActiveStart(item: any): string | null {
      return item?.fecha_inicio_cursado || null
    },
    daysUntil(dateString?: string | null): number | null {
      if (!dateString) return null
      try {
        // If a full ISO datetime arrives, use only the date part for day math
  const datePart = (dateString.split('T')[0]) as string
        const d = parseLocalDate(datePart)
        if (isNaN(d.getTime())) return null
        const today = new Date()
        // Normalize both to local midnight to avoid partial day rounding issues
        const start = new Date(today.getFullYear(), today.getMonth(), today.getDate())
        const target = new Date(d.getFullYear(), d.getMonth(), d.getDate())
        const diffMs = target.getTime() - start.getTime()
        if (diffMs <= 0) return 0
        const days = Math.ceil(diffMs / 86400000)
        return isNaN(days) ? null : days
      } catch { return null }
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
    aprobarInscriptos(item: any) {
      // Navigate to aprobar inscriptos view for the selected row
      if (item && item.id) {
        this.$router.push({
          name: 'DelegadoAprobarInscriptos',
          params: { id: item.id }
        })
      }
    },
    refreshAll() {
      // Manually refresh all data
      this.loadUpcomingData()
      this.loadConvocatoriaData()
      this.loadPreparacionData()
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

.icon-wrapper-preparacion {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 193, 7, 0.1);
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
