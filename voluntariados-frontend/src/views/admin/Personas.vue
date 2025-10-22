<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Personas.vue -->
<template>
  <AdminLayout 
    page-title="Administración de personas" 
    :breadcrumbs="[{ label: 'Personas' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nueva Persona
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title=""
          :columns="columns"
          :items="filteredPersonas"
          :show-create-button="false"
          :loading="loading"
          :error="error || undefined"
          :footer-text="`Mostrando ${filteredPersonas.length} de ${personas.length} personas`"
          @create="showCreateModal = true"
          @edit="editPersona"
          @delete="confirmDelete"
          @retry="fetchPersonas"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por nombre o apellido..."
                v-model="searchQuery"
                @input="filterPersonas"
              >
            </div>
            <div class="col-md-3">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por DNI..."
                v-model="dniSearchQuery"
                @input="filterPersonas"
              >
            </div>
            <div class="col-md-3">
              <input 
                type="email" 
                class="form-control form-control-sm" 
                placeholder="Buscar por email..."
                v-model="emailSearchQuery"
                @input="filterPersonas"
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
              <div class="avatar rounded-circle bg-primary text-white me-3">
                <i class="bi bi-person"></i>
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
              {{ item.localidad.nombre }}
            </span>
            <span v-else-if="item.localidad" class="badge bg-info">
              {{ getLocalidadName(item.localidad) }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Persona Modal -->
    <PersonaModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :persona-data="formData"
      @close="closeModal"
      @save="savePersona"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar Persona"
      :message="`¿Estás seguro de que quieres eliminar a ${personaToDelete?.apellido}, ${personaToDelete?.nombre}?`"
      description="Esta acción no se puede deshacer. La persona y su usuario serán eliminados permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deletePersona"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import PersonaModal from '@/components/admin/PersonaModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { personaAPI, ubicacionAPI } from '@/services/api'

interface Localidad {
  id: number
  nombre: string
}

interface Persona {
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
  name: 'AdminPersonas',
  components: {
    AdminLayout,
    AdminTable,
    PersonaModal,
    ConfirmationModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      personas: [] as Persona[],
      filteredPersonas: [] as Persona[],
      localidades: [] as Localidad[],
      searchQuery: '',
      dniSearchQuery: '',
      emailSearchQuery: '',
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      deleting: false,
      personaToDelete: null as Persona | null,
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
        { key: 'localidad', label: 'Localidad' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchPersonas()
    this.loadLookups()
  },
  methods: {
    async loadLookups() {
      try {
        const locRes = await ubicacionAPI.getLocalidades()
        this.localidades = locRes.data
      } catch (err) {/* ignore */}
    },
    async fetchPersonas() {
      this.loading = true
      this.error = null
      try {
        const response = await personaAPI.getAll()
        this.personas = response.data
        this.filteredPersonas = [...this.personas]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar personas'
        console.error('Error al cargar personas:', err)
      } finally {
        this.loading = false
      }
    },
    
    filterPersonas() {
      let filtered = [...this.personas]
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(persona => 
          persona.nombre.toLowerCase().includes(query) ||
          persona.apellido.toLowerCase().includes(query)
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
      
      this.filteredPersonas = filtered
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.dniSearchQuery = ''
      this.emailSearchQuery = ''
      this.filteredPersonas = [...this.personas]
    },
    
    editPersona(persona: Persona) {
      this.formData = {
        id: persona.id,
        nombre: persona.nombre,
        apellido: persona.apellido,
        dni: persona.dni || '',
        fecha_nacimiento: persona.fecha_nacimiento || '',
        telefono: persona.telefono || '',
        email: persona.email || '',
        direccion: persona.direccion || '',
        localidad: typeof persona.localidad === 'object' && persona.localidad ? persona.localidad.id : persona.localidad
      }
      this.showEditModal = true
    },
    
    async savePersona(personaData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && personaData.id) {
          await personaAPI.update(personaData.id, personaData)
        } else {
          await personaAPI.create(personaData)
        }
        
        this.closeModal()
        await this.fetchPersonas()
        
        if (callback) {
          callback(true)
        }
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
          || err.response?.data?.error
          || err.message 
          || 'Error al guardar persona'
        
        if (callback) {
          callback(false, errorMsg)
        } else {
          alert(errorMsg)
        }
      }
    },
        
    confirmDelete(persona: Persona) {
      this.personaToDelete = persona
      this.showDeleteModal = true
    },
    
    cancelDelete() {
      this.showDeleteModal = false
      this.personaToDelete = null
    },
    
    async deletePersona() {
      if (!this.personaToDelete) return
      
      this.deleting = true
      try {
        await personaAPI.delete(this.personaToDelete.id)
        await this.fetchPersonas()
        this.showDeleteModal = false
        this.personaToDelete = null
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar persona')
        console.error('Error deleting persona:', err)
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
        return new Date(dateString).toLocaleDateString('es-ES')
      } catch {
        return dateString
      }
    },

    getLocalidadName(localidadId: number): string {
      const loc = this.localidades?.find?.((l: Localidad) => l.id === localidadId)
      return loc ? loc.nombre : `ID ${localidadId}`
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