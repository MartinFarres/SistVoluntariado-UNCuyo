<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Localidades.vue -->
<template>
  <AdminLayout 
    page-title="Administración de Localidades" 
    :breadcrumbs="[{ label: 'Localidades' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nueva Localidad
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Todas las localidades"
          :columns="columns"
          :items="filteredLocalidades"
          :loading="loading"
          :error="error"
          :footer-text="`Mostrando ${filteredLocalidades.length} de ${localidades.length} localidades`"
          @create="showCreateModal = true"
          @edit="editLocalidad"
          @delete="confirmDelete"
          @retry="fetchLocalidades"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por nombre..."
                v-model="searchQuery"
                @input="filterLocalidades"
              >
            </div>
            <div class="col-md-3">
              <select class="form-control form-control-sm" v-model="departamentoFilter" @change="filterLocalidades">
                <option value="">Todos los departamentos</option>
                <option v-for="departamento in departamentos" :key="departamento.id" :value="departamento.id">
                  {{ departamento.nombre }}
                </option>
              </select>
            </div>
            <div class="col-md-5 text-end">
              <button class="btn btn-sm btn-outline-primary" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Borrar filtros
              </button>
            </div>
          </template>

          <!-- Custom Cell Templates -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="avatar rounded-circle bg-warning text-white me-3">
                <i class="bi bi-pin-map"></i>
              </div>
              <span>{{ item.nombre }}</span>
            </div>
          </template>

          <template #cell-codigo_postal="{ item }">
            <span class="badge bg-secondary">
              {{ item.codigo_postal }}
            </span>
          </template>

          <template #cell-departamento="{ item }">
            <span class="badge bg-info">
              {{ getDepartamentoName(item.departamento) }}
            </span>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Localidad Modal -->
    <LocalidadModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :localidad-data="formData"
      :departamentos="departamentos"
      @close="closeModal"
      @save="saveLocalidad"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar Localidad"
      :message="`¿Estás seguro de que quieres eliminar la localidad ${localidadToDelete?.nombre}?`"
      description="Esta acción no se puede deshacer. La localidad será eliminada permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deleteLocalidad"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import LocalidadModal from '@/components/admin/LocalidadModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { ubicacionAPI } from '@/services/api'

interface Departamento {
  id: number
  nombre: string
}

interface Localidad {
  id: number
  nombre: string
  codigo_postal: string
  departamento: number | { id: number; nombre: string }
}

export default defineComponent({
  name: 'AdminLocalidades',
  components: {
    AdminLayout,
    AdminTable,
    LocalidadModal,
    ConfirmationModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      localidades: [] as Localidad[],
      filteredLocalidades: [] as Localidad[],
      departamentos: [] as Departamento[],
      searchQuery: '',
      departamentoFilter: '',
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      deleting: false,
      localidadToDelete: null as Localidad | null,
      formData: {
        id: null as number | null,
        nombre: '',
        codigo_postal: '',
        departamento: null as number | null
      },
      columns: [
        { key: 'id', label: 'ID', align: 'center' },
        { key: 'nombre', label: 'Nombre' },
        { key: 'codigo_postal', label: 'Código Postal' },
        { key: 'departamento', label: 'Departamento' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchDepartamentos()
    this.fetchLocalidades()
  },
  methods: {
    async fetchDepartamentos() {
      try {
        const response = await ubicacionAPI.getDepartamentos()
        this.departamentos = response.data
      } catch (err: any) {
        console.error('Error fetching departamentos:', err)
      }
    },

    async fetchLocalidades() {
      this.loading = true
      this.error = null
      try {
        const response = await ubicacionAPI.getLocalidades()
        this.localidades = response.data
        this.filteredLocalidades = [...this.localidades]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar localidades'
        console.error('Error al cargar localidades:', err)
      } finally {
        this.loading = false
      }
    },
    
    filterLocalidades() {
      let filtered = [...this.localidades]
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(localidad => 
          localidad.nombre.toLowerCase().includes(query) ||
          localidad.codigo_postal.toLowerCase().includes(query)
        )
      }

      if (this.departamentoFilter) {
        filtered = filtered.filter(localidad => {
          const departamentoId = typeof localidad.departamento === 'object' ? localidad.departamento.id : localidad.departamento
          return departamentoId === Number(this.departamentoFilter)
        })
      }
      
      this.filteredLocalidades = filtered
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.departamentoFilter = ''
      this.filteredLocalidades = [...this.localidades]
    },

    getDepartamentoName(departamentoId: number | { id: number; nombre: string }): string {
      // Handle both number and object formats
      if (typeof departamentoId === 'object' && departamentoId !== null) {
        return departamentoId.nombre
      }
      const departamento = this.departamentos.find(d => d.id === departamentoId)
      return departamento ? departamento.nombre : 'N/A'
    },
    
    editLocalidad(localidad: Localidad) {
      this.formData = {
        id: localidad.id,
        nombre: localidad.nombre,
        codigo_postal: localidad.codigo_postal,
        departamento: typeof localidad.departamento === 'object' ? (localidad.departamento as any)?.id : localidad.departamento
      }
      this.showEditModal = true
    },
    
    async saveLocalidad(localidadData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && localidadData.id) {
          await ubicacionAPI.updateLocalidad(localidadData.id, {
            nombre: localidadData.nombre,
            codigo_postal: localidadData.codigo_postal,
            departamento_id: localidadData.departamento
          })
        } else {
          await ubicacionAPI.createLocalidad({
            nombre: localidadData.nombre,
            codigo_postal: localidadData.codigo_postal,
            departamento_id: localidadData.departamento
          })
        }
        
        if (callback) callback(true)
        this.closeModal()
        await this.fetchLocalidades()
      } catch (err: any) {
        console.error('Save error:', err)
        const errorMsg = err.response?.data?.detail 
          || err.response?.data?.nombre?.[0]
          || err.response?.data?.codigo_postal?.[0]
          || err.response?.data?.departamento_id?.[0]
          || err.message 
          || 'Failed to save localidad'
        
        if (callback) {
          callback(false, errorMsg)
        } else {
          alert(errorMsg)
        }
      }
    },
    
    confirmDelete(localidad: Localidad) {
      this.localidadToDelete = localidad
      this.showDeleteModal = true
    },
    
    cancelDelete() {
      this.showDeleteModal = false
      this.localidadToDelete = null
    },
    
    async deleteLocalidad() {
      if (!this.localidadToDelete) return
      
      this.deleting = true
      try {
        await ubicacionAPI.deleteLocalidad(this.localidadToDelete.id)
        await this.fetchLocalidades()
        this.showDeleteModal = false
        this.localidadToDelete = null
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar localidad')
        console.error('Error deleting localidad:', err)
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
        codigo_postal: '',
        departamento: null
      }
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