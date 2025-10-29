<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Delegados.vue -->
<template>
  <AdminLayout
    page-title="Administración de delegados"
    :breadcrumbs="[{ label: 'Delegados' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nuevo Delegado
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Delegados"
          :columns="columns"
          :items="filteredDelegados"
          :export-formatters="exportFormatters"
          :show-create-button="false"
          :loading="loading"
          :error="error || undefined"
          :footer-text="`Mostrando ${filteredDelegados.length} de ${delegados.length} delegados`"
          :clickable-rows="true"
          @create="showCreateModal = true"
          @edit="editDelegado"
          @delete="confirmDelete"
          @retry="fetchDelegados"
          @row-click="viewDelegadoDetails"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por nombre o apellido..."
                v-model="searchQuery"
                @input="filterDelegados"
              >
            </div>
            <div class="col-md-3">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por DNI..."
                v-model="dniSearchQuery"
                @input="filterDelegados"
              >
            </div>
            <div class="col-md-3">
              <input
                type="email"
                class="form-control form-control-sm"
                placeholder="Buscar por email..."
                v-model="emailSearchQuery"
                @input="filterDelegados"
              >
            </div>
            <div class="col-md-2 text-end">
              <button class="btn btn-sm btn-outline-primary" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Limpiar
              </button>
            </div>
          </template>

          <!-- Custom Cell Templates -->
          <template #cell-nombre_completo="{ item }">
            <div class="d-flex align-items-center">
                <div class="avatar rounded-circle bg-success text-white me-3 d-flex align-items-center justify-content-center">
                  <i class="bi bi-person-badge" style="font-size: 1rem;"></i>
                </div>
              <div>
                <span class="fw-bold">{{ item.apellido }}, {{ item.nombre }}</span>
                <small v-if="item.dni" class="d-block text-muted">DNI: {{ item.dni }}</small>
              </div>
            </div>
          </template>

          <template #cell-email="{ value }">
            <span v-if="value">
              <i class="bi bi-envelope me-1"></i>
              {{ value }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>

          <template #cell-telefono="{ value }">
            <span v-if="value">
              <i class="bi bi-telephone me-1"></i>
              {{ value }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>

          <template #cell-fecha_nacimiento="{ value }">
            {{ value ? formatDate(value) : '-' }}
          </template>

          <template #cell-localidad="{ item }">
            <span v-if="item.localidad && typeof item.localidad === 'object'" class="badge bg-info">
              <i class="bi bi-geo-alt me-1"></i>{{ getCompleteLocationFromObject(item.localidad) }}
            </span>
            <span v-else-if="item.localidad" class="badge bg-info">
              <i class="bi bi-geo-alt me-1"></i>{{ getCompleteLocationFromId(item.localidad) }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>

          <template #cell-organizacion="{ item }">
            <span v-if="item.organizacion && typeof item.organizacion === 'object'" class="badge bg-secondary">
              {{ item.organizacion.nombre }}
            </span>
            <span v-else-if="item.organizacion" class="badge bg-secondary">
              {{ getOrganizacionName(item.organizacion) }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Delegado Modal -->
    <DelegadoModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :delegado-data="formData"
      @close="closeModal"
      @save="saveDelegado"
    />

    <!-- Delegado Detail Modal -->
    <DelegadoDetailModal
      :show="showDetailModal"
      :delegado="selectedDelegado"
      :localidades="localidades"
      :organizaciones="organizaciones"
      @close="closeDetailModal"
      @edit="editFromDetail"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar Delegado"
      :message="`¿Estás seguro de que quieres eliminar a ${delegadoToDelete?.apellido}, ${delegadoToDelete?.nombre}?`"
      description="Esta acción no se puede deshacer. El delegado y su usuario serán eliminados permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deleteDelegado"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import DelegadoModal from '@/components/admin/DelegadoModal.vue'
import DelegadoDetailModal from '@/components/admin/DelegadoDetailModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { personaAPI, organizacionAPI, ubicacionAPI } from '@/services/api'
import { formatDateShort } from '@/utils/dateUtils'

interface Localidad {
  id: number;
  nombre: string;
  departamento?: {
    id: number;
    nombre: string;
    provincia?: {
      id: number;
      nombre: string;
      pais?: {
        id: number;
        nombre: string;
      }
    }
  }
}
interface Organizacion { id: number; nombre: string }

interface Delegado {
  id: number
  nombre: string
  apellido: string
  dni: string | null
  fecha_nacimiento: string | null
  telefono: string | null
  email: string | null
  direccion: string | null
  localidad: number | Localidad | null
  organizacion: number | Organizacion | null
}

export default defineComponent({
  name: 'AdminDelegados',
  components: { AdminLayout, AdminTable, DelegadoModal, DelegadoDetailModal, ConfirmationModal },
  data() {
    return {
      loading: false,
      error: null as string | null,
      delegados: [] as Delegado[],
      filteredDelegados: [] as Delegado[],
      localidades: [] as Localidad[],
      organizaciones: [] as Organizacion[],
      searchQuery: '',
      dniSearchQuery: '',
      emailSearchQuery: '',
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      showDetailModal: false,
      deleting: false,
      delegadoToDelete: null as Delegado | null,
      selectedDelegado: null as Delegado | null,
      formData: {
        id: null as number | null,
        nombre: '',
        apellido: '',
        dni: '',
        fecha_nacimiento: '',
        telefono: '',
        email: '',
        direccion: '',
        localidad: null as number | null,
        organizacion: null as number | null
      },
      columns: [
        { key: 'id', label: 'ID', align: 'center' },
        { key: 'nombre_completo', label: 'Nombre Completo' },
        { key: 'email', label: 'Email' },
        { key: 'telefono', label: 'Teléfono' },
        { key: 'fecha_nacimiento', label: 'Fecha de Nacimiento' },
        { key: 'localidad', label: 'Ubicación' },
        { key: 'organizacion', label: 'Organización' },
      ] as TableColumn[],
      exportFormatters: {
        nombre_completo: (item: Delegado) => `${item.apellido}, ${item.nombre}`,
        localidad: (item: Delegado) => {
          if (!item.localidad) return ''
          const localidadId = typeof item.localidad === 'object' ? item.localidad.id : item.localidad;
          return this.getCompleteLocationFromId(localidadId || 0);
        },
        organizacion: (item: Delegado) => {
          if (!item.organizacion) return ''
          const organizacionId = typeof item.organizacion === 'object' ? item.organizacion.id : item.organizacion;
          return this.getOrganizacionName(organizacionId || 0);
        }
      }
    }
  },
  mounted() {
    this.fetchDelegados()
    this.loadLookups()
  },
  methods: {
    async loadLookups() {
      try {
        const [locRes, orgRes, depRes, provRes, paisRes] = await Promise.all([
          ubicacionAPI.getLocalidades(),
          organizacionAPI.getAll(),
          ubicacionAPI.getDepartamentos(),
          ubicacionAPI.getProvincias(),
          ubicacionAPI.getPaises()
        ])

        // Build complete location hierarchy
        const paises = paisRes.data
        const provincias = provRes.data
        const departamentos = depRes.data
        const localidades = locRes.data

        // Add hierarchy to localidades
        this.localidades = localidades.map((localidad: any) => {
          const departamento = departamentos.find((d: any) => d.id === localidad.departamento)
          if (departamento) {
            const provincia = provincias.find((p: any) => p.id === departamento.provincia)
            if (provincia) {
              const pais = paises.find((pa: any) => pa.id === provincia.pais)
              departamento.provincia = { ...provincia, pais }
            }
            localidad.departamento = departamento
          }
          return localidad
        })

        this.organizaciones = orgRes.data
      } catch (err) {
        // non-blocking
        // eslint-disable-next-line no-console
        console.warn('No se pudieron cargar localidades/organizaciones para mapeo de nombres')
      }
    },
    async fetchDelegados() {
      this.loading = true
      this.error = null
      try {
        const response = await personaAPI.getDelegados()
        this.delegados = response.data
        this.filteredDelegados = [...this.delegados]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar delegados'
        console.error('Error al cargar delegados:', err)
      } finally {
        this.loading = false
      }
    },

    filterDelegados() {
      let filtered = [...this.delegados]

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(d =>
          d.nombre.toLowerCase().includes(query) ||
          d.apellido.toLowerCase().includes(query)
        )
      }

      if (this.dniSearchQuery) {
        const dniQuery = this.dniSearchQuery.toLowerCase()
        filtered = filtered.filter(d =>
          d.dni && d.dni.toLowerCase().includes(dniQuery)
        )
      }

      if (this.emailSearchQuery) {
        const emailQuery = this.emailSearchQuery.toLowerCase()
        filtered = filtered.filter(d =>
          d.email && d.email.toLowerCase().includes(emailQuery)
        )
      }

      this.filteredDelegados = filtered
    },

    clearFilters() {
      this.searchQuery = ''
      this.dniSearchQuery = ''
      this.emailSearchQuery = ''
      this.filteredDelegados = [...this.delegados]
    },

    editDelegado(delegado: Delegado) {
      this.formData = {
        id: delegado.id,
        nombre: delegado.nombre,
        apellido: delegado.apellido,
        dni: delegado.dni || '',
        fecha_nacimiento: delegado.fecha_nacimiento || '',
        telefono: delegado.telefono || '',
        email: delegado.email || '',
        direccion: delegado.direccion || '',
        localidad: typeof delegado.localidad === 'object' && delegado.localidad ? delegado.localidad.id : delegado.localidad,
        organizacion: typeof delegado.organizacion === 'object' && delegado.organizacion ? delegado.organizacion.id : delegado.organizacion,
      }
      this.showEditModal = true
    },

    async saveDelegado(delegadoData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && delegadoData.id) {
          await personaAPI.updateDelegado(delegadoData.id, delegadoData)
        } else {
          await personaAPI.createDelegado(delegadoData)
        }

        this.closeModal()
        await this.fetchDelegados()

        if (callback) callback(true)
      } catch (err: any) {
        console.error('Save error:', err)
        const errorMsg = err.response?.data?.detail
          || err.response?.data?.nombre?.[0]
          || err.response?.data?.apellido?.[0]
          || err.response?.data?.dni?.[0]
          || err.response?.data?.telefono?.[0]
          || err.response?.data?.email?.[0]
          || err.response?.data?.direccion?.[0]
          || err.response?.data?.localidad?.[0]
          || err.response?.data?.organizacion?.[0]
          || err.response?.data?.error
          || err.message
          || 'Error al guardar delegado'

        if (callback) callback(false, errorMsg)
        else alert(errorMsg)
      }
    },

    confirmDelete(delegado: Delegado) {
      this.delegadoToDelete = delegado
      this.showDeleteModal = true
    },

    cancelDelete() {
      this.showDeleteModal = false
      this.delegadoToDelete = null
    },

    async deleteDelegado() {
      if (!this.delegadoToDelete) return

      this.deleting = true
      try {
        await personaAPI.deleteDelegado(this.delegadoToDelete.id)
        await this.fetchDelegados()
        this.showDeleteModal = false
        this.delegadoToDelete = null
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar delegado')
        console.error('Error deleting delegado:', err)
      } finally {
        this.deleting = false
      }
    },

    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.formData = {
        id: null,
        nombre: '',
        apellido: '',
        dni: '',
        fecha_nacimiento: '',
        telefono: '',
        email: '',
        direccion: '',
        localidad: null,
        organizacion: null
      }
    },

    formatDate(dateString: string): string {
      try { return formatDateShort(dateString) } catch { return dateString }
    },

    getLocalidadName(localidadId: number): string {
      const loc = this.localidades.find(l => l.id === localidadId)
      return loc ? loc.nombre : `ID ${localidadId}`
    },
    getOrganizacionName(organizacionId: number): string {
      const org = this.organizaciones.find(o => o.id === organizacionId)
      return org ? org.nombre : `ID ${organizacionId}`
    },

    viewDelegadoDetails(delegado: Delegado) {
      this.selectedDelegado = delegado
      this.showDetailModal = true
    },

    closeDetailModal() {
      this.showDetailModal = false
      this.selectedDelegado = null
    },

    editFromDetail(delegado: Delegado) {
      this.editDelegado(delegado)
      this.showDetailModal = false
    },

    getCompleteLocationFromObject(localidad: any): string {
      if (!localidad) return 'No especificada'

      const parts = [localidad.nombre]

      if (localidad.departamento) {
        parts.push(localidad.departamento.nombre)

        if (localidad.departamento.provincia) {
          parts.push(localidad.departamento.provincia.nombre)

          if (localidad.departamento.provincia.pais) {
            parts.push(localidad.departamento.provincia.pais.nombre)
          }
        }
      }

      return parts.join(', ')
    },

    getCompleteLocationFromId(localidadId: number): string {
      const loc = this.localidades?.find?.((l: Localidad) => l.id === localidadId)
      if (loc) {
        return this.getCompleteLocationFromObject(loc)
      }
      return `ID ${localidadId}`
    }
  }
})
</script>

<style scoped>
.avatar { width: 36px; height: 36px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.875rem; }
</style>
