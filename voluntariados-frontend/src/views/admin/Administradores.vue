<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Administradores.vue -->
<template>
  <AdminLayout 
    page-title="Administración de administradores" 
    :breadcrumbs="[{ label: 'Administradores' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nuevo Administrador
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title=""
          :columns="columns"
          :items="filteredAdministradores"
          :show-create-button="false"
          :loading="loading"
          :error="error || undefined"
          :footer-text="`Mostrando ${filteredAdministradores.length} de ${administradores.length} administradores`"
          :clickable-rows="true"
          @create="showCreateModal = true"
          @edit="editAdministrador"
          @delete="confirmDelete"
          @retry="fetchAdministradores"
          @row-click="viewAdministradorDetails"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por nombre o apellido..."
                v-model="searchQuery"
                @input="filterAdministradores"
              >
            </div>
            <div class="col-md-3">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por DNI..."
                v-model="dniSearchQuery"
                @input="filterAdministradores"
              >
            </div>
            <div class="col-md-3">
              <input 
                type="email" 
                class="form-control form-control-sm" 
                placeholder="Buscar por email..."
                v-model="emailSearchQuery"
                @input="filterAdministradores"
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
            <div class="avatar rounded-circle bg-danger text-white me-3 d-flex align-items-center justify-content-center">
                <i class="bi bi-shield-check" style="font-size: 1rem;"></i>
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
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Administrador Modal -->
    <AdministradorModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :administrador-data="formData"
      @close="closeModal"
      @save="saveAdministrador"
    />

    <!-- Administrador Detail Modal -->
    <AdministradorDetailModal
      :show="showDetailModal"
      :administrador="selectedAdministrador"
      :localidades="localidades"
      @close="closeDetailModal"
      @edit="editFromDetail"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar Administrador"
      :message="`¿Estás seguro de que quieres eliminar a ${administradorToDelete?.apellido}, ${administradorToDelete?.nombre}?`"
      description="Esta acción no se puede deshacer. El administrador y su usuario serán eliminados permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deleteAdministrador"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import AdministradorModal from '@/components/admin/AdministradorModal.vue'
import AdministradorDetailModal from '@/components/admin/AdministradorDetailModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { personaAPI, ubicacionAPI } from '@/services/api'
import { formatDateShort } from '@/utils/dateUtils'

interface Localidad {
  id: number
  nombre: string
  departamento?: {
    id: number
    nombre: string
    provincia?: {
      id: number
      nombre: string
      pais?: { id: number; nombre: string }
    }
  }
}

interface Administrador {
  id: number
  nombre: string
  apellido: string
  dni: string | null
  fecha_nacimiento: string | null
  telefono: string | null
  email: string | null
  direccion: string | null
  localidad: number | Localidad | null
}

export default defineComponent({
  name: 'AdminAdministradores',
  components: {
    AdminLayout,
    AdminTable,
    AdministradorModal,
    AdministradorDetailModal,
    ConfirmationModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      administradores: [] as Administrador[],
      filteredAdministradores: [] as Administrador[],
      localidades: [] as Localidad[],
      searchQuery: '',
      dniSearchQuery: '',
      emailSearchQuery: '',
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      showDetailModal: false,
      deleting: false,
      administradorToDelete: null as Administrador | null,
      selectedAdministrador: null as Administrador | null,
      formData: {
        id: null as number | null,
        nombre: '',
        apellido: '',
        dni: '',
        fecha_nacimiento: '',
        telefono: '',
        email: '',
        direccion: '',
        localidad: null as number | null
      },
      columns: [
        { key: 'id', label: 'ID', align: 'center' },
        { key: 'nombre_completo', label: 'Nombre Completo' },
        { key: 'email', label: 'Email' },
        { key: 'telefono', label: 'Teléfono' },
        { key: 'fecha_nacimiento', label: 'Fecha de Nacimiento' },
        { key: 'localidad', label: 'Ubicación' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchAdministradores()
    this.loadLookups()
  },
  methods: {
    async loadLookups() {
      try {
        const [locRes, depRes, provRes, paisRes] = await Promise.all([
          ubicacionAPI.getLocalidades(),
          ubicacionAPI.getDepartamentos(),
          ubicacionAPI.getProvincias(),
          ubicacionAPI.getPaises()
        ])

        const paises = paisRes.data
        const provincias = provRes.data
        const departamentos = depRes.data
        const localidades = locRes.data

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
      } catch (err) {/* ignore */}
    },

    async fetchAdministradores() {
      this.loading = true
      this.error = null
      try {
        const response = await personaAPI.getAdministradores()
        this.administradores = response.data
        this.filteredAdministradores = [...this.administradores]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar administradores'
        console.error('Error al cargar administradores:', err)
      } finally {
        this.loading = false
      }
    },

    filterAdministradores() {
      let filtered = [...this.administradores]

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(admin =>
          admin.nombre.toLowerCase().includes(query) ||
          admin.apellido.toLowerCase().includes(query)
        )
      }

      if (this.dniSearchQuery) {
        const dniQuery = this.dniSearchQuery.toLowerCase()
        filtered = filtered.filter(admin => 
          admin.dni && admin.dni.toLowerCase().includes(dniQuery)
        )
      }

      if (this.emailSearchQuery) {
        const emailQuery = this.emailSearchQuery.toLowerCase()
        filtered = filtered.filter(admin => 
          admin.email && admin.email.toLowerCase().includes(emailQuery)
        )
      }

      this.filteredAdministradores = filtered
    },

    clearFilters() {
      this.searchQuery = ''
      this.dniSearchQuery = ''
      this.emailSearchQuery = ''
      this.filteredAdministradores = [...this.administradores]
    },

    editAdministrador(administrador: Administrador) {
      this.formData = {
        id: administrador.id,
        nombre: administrador.nombre,
        apellido: administrador.apellido,
        dni: administrador.dni || '',
        fecha_nacimiento: administrador.fecha_nacimiento || '',
        telefono: administrador.telefono || '',
        email: administrador.email || '',
        direccion: administrador.direccion || '',
        localidad: typeof administrador.localidad === 'object' && administrador.localidad ? administrador.localidad.id : administrador.localidad
      }
      this.showEditModal = true
    },

    async saveAdministrador(administradorData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && administradorData.id) {
          await personaAPI.updateAdministrador(administradorData.id, administradorData)
        } else {
          await personaAPI.createAdministrador(administradorData)
        }

        this.closeModal()
        await this.fetchAdministradores()

        if (callback) {
          callback(true)
        }
      } catch (err: any) {
        console.error('Save error:', err)

        let errorMsg = ''
        const data = err.response?.data || {}

        const fieldErrors: string[] = []
        const fieldNames: Record<string, string> = {
          nombre: 'Nombre',
          apellido: 'Apellido', 
          dni: 'DNI',
          telefono: 'Teléfono',
          email: 'Email',
          direccion: 'Dirección',
          localidad: 'Localidad',
          fecha_nacimiento: 'Fecha de nacimiento'
        }

        Object.keys(fieldNames).forEach(field => {
          if (data[field] && Array.isArray(data[field])) {
            fieldErrors.push(`${fieldNames[field]}: ${data[field][0]}`)
          }
        })

        if (fieldErrors.length > 0) {
          errorMsg = fieldErrors.join('; ')
        } else {
          errorMsg = data.detail 
            || data.error
            || err.message 
            || 'Error al guardar administrador'
        }

        if (callback) {
          callback(false, errorMsg)
        } else {
          alert(errorMsg)
        }
      }
    },

    confirmDelete(administrador: Administrador) {
      this.administradorToDelete = administrador
      this.showDeleteModal = true
    },

    cancelDelete() {
      this.showDeleteModal = false
      this.administradorToDelete = null
    },

    async deleteAdministrador() {
      if (!this.administradorToDelete) return

      this.deleting = true
      try {
        await personaAPI.deleteAdministrador(this.administradorToDelete.id)
        await this.fetchAdministradores()
        this.showDeleteModal = false
        this.administradorToDelete = null
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar administrador')
        console.error('Error eliminando administrador:', err)
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
        localidad: null
      }
    },

    formatDate(dateString: string): string {
      try {
        if (!dateString) return '-'
        return formatDateShort(dateString)
      } catch {
        return dateString
      }
    },

    getLocalidadName(localidadId: number): string {
      const loc = this.localidades?.find?.((l: Localidad) => l.id === localidadId)
      return loc ? loc.nombre : `ID ${localidadId}`
    },

    viewAdministradorDetails(administrador: Administrador) {
      this.selectedAdministrador = administrador
      this.showDetailModal = true
    },

    closeDetailModal() {
      this.showDetailModal = false
      this.selectedAdministrador = null
    },

    editFromDetail(administrador: Administrador) {
      this.editAdministrador(administrador)
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
.avatar {
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}
</style>