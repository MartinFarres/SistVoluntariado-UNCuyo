<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Voluntarios.vue -->
<template>
  <AdminLayout 
    page-title="Administración de voluntarios" 
    :breadcrumbs="[{ label: 'Voluntarios' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nuevo Voluntario
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Todos los Voluntarios"
          :columns="columns"
          :items="filteredVoluntarios"
          :loading="loading"
          :error="error || undefined"
          :footer-text="`Mostrando ${filteredVoluntarios.length} de ${voluntarios.length} voluntarios`"
          :clickable-rows="true"
          @create="showCreateModal = true"
          @edit="editVoluntario"
          @delete="confirmDelete"
          @retry="fetchVoluntarios"
          @row-click="viewVoluntarioDetails"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por nombre o apellido..."
                v-model="searchQuery"
                @input="filterVoluntarios"
              >
            </div>
            <div class="col-md-3">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por DNI..."
                v-model="dniSearchQuery"
                @input="filterVoluntarios"
              >
            </div>
            <div class="col-md-3">
              <input 
                type="email" 
                class="form-control form-control-sm" 
                placeholder="Buscar por email..."
                v-model="emailSearchQuery"
                @input="filterVoluntarios"
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
              <div class="avatar rounded-circle bg-primary text-white me-3 d-flex align-items-center justify-content-center">
                <i class="bi bi-person-heart" style="font-size: 1rem;"></i>
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

          <template #cell-carrera="{ item }">
            <span v-if="item.carrera && typeof item.carrera === 'object'" class="badge bg-success">
              {{ item.carrera.nombre }}
            </span>
            <span v-else-if="item.carrera" class="badge bg-success">
              {{ getCarreraName(item.carrera) }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>

          <template #cell-interno="{ value }">
            <span v-if="value" class="badge bg-primary">
              <i class="bi bi-check-circle me-1"></i>Interno
            </span>
            <span v-else class="badge bg-outline-secondary">
              <i class="bi bi-x-circle me-1"></i>Externo
            </span>
          </template>

        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Voluntario Modal -->
    <VoluntariosModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :voluntario-data="formData"
      @close="closeModal"
      @save="saveVoluntario"
    />

    <!-- Voluntario Detail Modal -->
    <VoluntarioDetailModal
      :show="showDetailModal"
      :voluntario="selectedVoluntario"
      :localidades="localidades"
      :carreras="carreras"
      @close="closeDetailModal"
      @edit="editFromDetail"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar Voluntario"
      :message="`¿Estás seguro de que quieres eliminar a ${voluntarioToDelete?.apellido}, ${voluntarioToDelete?.nombre}?`"
      description="Esta acción no se puede deshacer. El voluntario será eliminado permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deleteVoluntario"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import VoluntariosModal from '@/components/admin/VoluntariosModal.vue'
import VoluntarioDetailModal from '@/components/admin/VoluntarioDetailModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { personaAPI, facultadAPI, ubicacionAPI } from '@/services/api'

interface Localidad {
  id: number
  nombre: string
  departamento?: {
    id: number
    nombre: string
    provincia?: {
      id: number
      nombre: string
      pais?: {
        id: number
        nombre: string
      }
    }
  }
}

interface Carrera { id: number; nombre: string }

interface Voluntario {
  id: number
  nombre: string
  apellido: string
  dni: string | null
  fecha_nacimiento: string | null
  telefono: string | null
  email: string | null
  direccion: string | null
  localidad: number | Localidad | null
  interno: boolean
  observaciones: string | null
  carrera: number | { id: number; nombre: string } | null
}

export default defineComponent({
  name: 'AdminVoluntarios',
  components: {
    AdminLayout,
    AdminTable,
    VoluntariosModal,
    VoluntarioDetailModal,
    ConfirmationModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      voluntarios: [] as Voluntario[],
      filteredVoluntarios: [] as Voluntario[],
      localidades: [] as Localidad[],
      carreras: [] as Carrera[],
      searchQuery: '',
      dniSearchQuery: '',
      emailSearchQuery: '',
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      showDetailModal: false,
      deleting: false,
      voluntarioToDelete: null as Voluntario | null,
      selectedVoluntario: null as Voluntario | null,
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
        interno: false,
        observaciones: '',
        carrera: null as number | null
      },
      columns: [
        { key: 'id', label: 'ID', align: 'center' },
        { key: 'nombre_completo', label: 'Nombre Completo' },
        { key: 'email', label: 'Email' },
        { key: 'telefono', label: 'Teléfono' },
        { key: 'localidad', label: 'Ubicación' },
        { key: 'carrera', label: 'Carrera' },
        { key: 'interno', label: 'Interno', align: 'center' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchVoluntarios()
    this.loadLookups()
  },
  methods: {
    async loadLookups() {
      try {
        const [locRes, carRes, depRes, provRes, paisRes] = await Promise.all([
          ubicacionAPI.getLocalidades(),
          facultadAPI.getCarreras(),
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
        
        this.carreras = carRes.data
      } catch (err) {/* ignore */}
    },
    async fetchVoluntarios() {
      this.loading = true
      this.error = null
      try {
        const response = await personaAPI.getVoluntarios()
        this.voluntarios = response.data
        this.filteredVoluntarios = [...this.voluntarios]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar voluntarios'
        console.error('Error al cargar voluntarios:', err)
      } finally {
        this.loading = false
      }
    },

    filterVoluntarios() {
      let filtered = [...this.voluntarios]

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(voluntario =>
          voluntario.nombre.toLowerCase().includes(query) ||
          voluntario.apellido.toLowerCase().includes(query)
        )
      }

      if (this.dniSearchQuery) {
        const dniQuery = this.dniSearchQuery.toLowerCase()
        filtered = filtered.filter(persona => 
          persona.dni && persona.dni.toLowerCase().includes(dniQuery)
        )
      }

      if (this.emailSearchQuery) {
        const emailQuery = this.emailSearchQuery.toLowerCase()
        filtered = filtered.filter(persona => 
          persona.email && persona.email.toLowerCase().includes(emailQuery)
        )
      }

      this.filteredVoluntarios = filtered
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.dniSearchQuery = ''
      this.emailSearchQuery = ''
      this.filteredVoluntarios = [...this.voluntarios]
    },

    editVoluntario(voluntario: Voluntario) {
      this.formData = {
        id: voluntario.id,
        nombre: voluntario.nombre,
        apellido: voluntario.apellido,
        dni: voluntario.dni || '',
        fecha_nacimiento: voluntario.fecha_nacimiento || '',
        telefono: voluntario.telefono || '',
        email: voluntario.email || '',
        direccion: voluntario.direccion || '',
        localidad: typeof voluntario.localidad === 'object' && voluntario.localidad ? voluntario.localidad.id : voluntario.localidad,
        interno: !!voluntario.interno,
        observaciones: voluntario.observaciones || '',
        carrera: typeof voluntario.carrera === 'object' && voluntario.carrera ? voluntario.carrera.id : voluntario.carrera
      }
      this.showEditModal = true
    },

    async saveVoluntario(voluntarioData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && voluntarioData.id) {
          await personaAPI.updateVoluntario(voluntarioData.id, voluntarioData)
        } else {
          await personaAPI.createVoluntario(voluntarioData)
        }
        
        this.closeModal()
        await this.fetchVoluntarios()
        
        if (callback) {
          callback(true)
        }
      } catch (err: any) {
        console.error('Save error:', err)
        
        // Build detailed error message with field information
        let errorMsg = ''
        const data = err.response?.data || {}
        
        // Check for field-specific errors
        const fieldErrors: string[] = []
        const fieldNames: Record<string, string> = {
          nombre: 'Nombre',
          apellido: 'Apellido', 
          dni: 'DNI',
          telefono: 'Teléfono',
          email: 'Email',
          direccion: 'Dirección',
          localidad: 'Localidad',
          fecha_nacimiento: 'Fecha de nacimiento',
          carrera: 'Carrera',
          observaciones: 'Observaciones',
          interno: 'Interno'
        }
        
        Object.keys(fieldNames).forEach(field => {
          if (data[field] && Array.isArray(data[field])) {
            fieldErrors.push(`${fieldNames[field]}: ${data[field][0]}`)
          }
        })
        
        if (fieldErrors.length > 0) {
          errorMsg = fieldErrors[0] || '';
        } else {
          // Fall back to general error messages
          errorMsg = data.detail 
            || data.error
            || err.message 
            || 'Error al guardar voluntario'
        }

        if (callback) {
          callback(false, errorMsg)
        } else {
          alert(errorMsg)
        }
      }
    },
        
    confirmDelete(voluntario: Voluntario) {
      this.voluntarioToDelete = voluntario
      this.showDeleteModal = true
    },
    
    cancelDelete() {
      this.showDeleteModal = false
      this.voluntarioToDelete = null
    },

    async deleteVoluntario() {
      if (!this.voluntarioToDelete) return

      this.deleting = true
      try {
        await personaAPI.deleteVoluntario(this.voluntarioToDelete.id)
        await this.fetchVoluntarios()
        this.showDeleteModal = false
        this.voluntarioToDelete = null
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar voluntario')
        console.error('Error eliminando voluntario:', err)
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
        interno: false,
        observaciones: '',
        carrera: null
      }
    },

    formatDate(dateString: string): string {
      try {
        return new Date(dateString).toLocaleDateString('es-ES')
      } catch {
        return dateString
      }
    },

    getLocalidadName(localidadId: number): string {
      const loc = this.localidades?.find?.((l: Localidad) => l.id === localidadId)
      return loc ? loc.nombre : `ID ${localidadId}`
    },
    getCarreraName(carreraId: number): string {
      const car = this.carreras?.find?.((c: { id: number; nombre: string }) => c.id === carreraId)
      return car ? car.nombre : `ID ${carreraId}`
    },

    viewVoluntarioDetails(voluntario: Voluntario) {
      this.selectedVoluntario = voluntario
      this.showDetailModal = true
    },

    closeDetailModal() {
      this.showDetailModal = false
      this.selectedVoluntario = null
    },

    editFromDetail(voluntario: Voluntario) {
      this.editVoluntario(voluntario)
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