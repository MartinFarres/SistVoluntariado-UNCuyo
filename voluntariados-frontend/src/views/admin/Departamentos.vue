<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Departamentos.vue -->
<template>
  <AdminLayout 
    page-title="Administración de Departamentos" 
    :breadcrumbs="[{ label: 'Departamentos' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nuevo Departamento
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Todos los departamentos"
          :columns="columns"
          :items="filteredDepartamentos"
          :loading="loading"
          :error="error"
          :footer-text="`Mostrando ${filteredDepartamentos.length} de ${departamentos.length} departamentos`"
          @create="showCreateModal = true"
          @edit="editDepartamento"
          @delete="confirmDelete"
          @retry="fetchDepartamentos"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por nombre..."
                v-model="searchQuery"
                @input="filterDepartamentos"
              >
            </div>
            <div class="col-md-3">
              <select class="form-control form-control-sm" v-model="provinciaFilter" @change="filterDepartamentos">
                <option value="">Todas las provincias</option>
                <option v-for="provincia in provincias" :key="provincia.id" :value="provincia.id">
                  {{ provincia.nombre }}
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
              <div class="avatar rounded-circle bg-success text-white me-3">
                <i class="bi bi-building"></i>
              </div>
              <span>{{ item.nombre }}</span>
            </div>
          </template>

          <template #cell-provincia="{ item }">
            <span class="badge bg-info">
              {{ getProvinciaName(item.provincia) }}
            </span>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Departamento Modal -->
    <DepartamentoModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :departamento-data="formData"
      :provincias="provincias"
      @close="closeModal"
      @save="saveDepartamento"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import DepartamentoModal from '@/components/admin/DepartamentoModal.vue'
import { ubicacionAPI } from '@/services/api'

interface Provincia {
  id: number
  nombre: string
}

interface Departamento {
  id: number
  nombre: string
  provincia: number | { id: number; nombre: string }
}

export default defineComponent({
  name: 'AdminDepartamentos',
  components: {
    AdminLayout,
    AdminTable,
    DepartamentoModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      departamentos: [] as Departamento[],
      filteredDepartamentos: [] as Departamento[],
      provincias: [] as Provincia[],
      searchQuery: '',
      provinciaFilter: '',
      showCreateModal: false,
      showEditModal: false,
      formData: {
        id: null as number | null,
        nombre: '',
        provincia: null as number | null
      },
      columns: [
        { key: 'id', label: 'ID' },
        { key: 'nombre', label: 'Nombre' },
        { key: 'provincia', label: 'Provincia' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchProvincias()
    this.fetchDepartamentos()
  },
  methods: {
    async fetchProvincias() {
      try {
        const response = await ubicacionAPI.getProvincias()
        this.provincias = response.data
      } catch (err: any) {
        console.error('Error fetching provincias:', err)
      }
    },

    async fetchDepartamentos() {
      this.loading = true
      this.error = null
      try {
        const response = await ubicacionAPI.getDepartamentos()
        this.departamentos = response.data
        this.filteredDepartamentos = [...this.departamentos]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to fetch departamentos'
        console.error('Error fetching departamentos:', err)
      } finally {
        this.loading = false
      }
    },
    
    filterDepartamentos() {
      let filtered = [...this.departamentos]
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(departamento => 
          departamento.nombre.toLowerCase().includes(query)
        )
      }

      if (this.provinciaFilter) {
        filtered = filtered.filter(departamento => {
          const provinciaId = typeof departamento.provincia === 'object' ? departamento.provincia.id : departamento.provincia
          return provinciaId === Number(this.provinciaFilter)
        })
      }
      
      this.filteredDepartamentos = filtered
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.provinciaFilter = ''
      this.filteredDepartamentos = [...this.departamentos]
    },

    getProvinciaName(provinciaId: number | { id: number; nombre: string }): string {
      // Handle both number and object formats
      if (typeof provinciaId === 'object' && provinciaId !== null) {
        return provinciaId.nombre
      }
      const provincia = this.provincias.find(p => p.id === provinciaId)
      return provincia ? provincia.nombre : 'N/A'
    },
    
    editDepartamento(departamento: Departamento) {
      this.formData = {
        id: departamento.id,
        nombre: departamento.nombre,
        provincia: typeof departamento.provincia === 'object' ? (departamento.provincia as any)?.id : departamento.provincia
      }
      this.showEditModal = true
    },
    
    async saveDepartamento(departamentoData: any) {
      try {
        if (this.showEditModal && departamentoData.id) {
          await ubicacionAPI.updateDepartamento(departamentoData.id, {
            nombre: departamentoData.nombre,
            provincia_id: departamentoData.provincia
          })
        } else {
          await ubicacionAPI.createDepartamento({
            nombre: departamentoData.nombre,
            provincia_id: departamentoData.provincia
          })
        }
        
        this.closeModal()
        await this.fetchDepartamentos()
      } catch (err: any) {
        console.error('Save error:', err)
        const errorMsg = err.response?.data?.detail 
          || err.response?.data?.nombre?.[0]
          || err.response?.data?.provincia_id?.[0]
          || err.message 
          || 'Failed to save departamento'
        alert(errorMsg)
        throw new Error(errorMsg)
      }
    },
    
    confirmDelete(departamento: Departamento) {
      if (confirm(`¿Estás seguro de que quieres eliminar el departamento "${departamento.nombre}"?`)) {
        this.deleteDepartamento(departamento.id)
      }
    },
    
    async deleteDepartamento(id: number) {
      try {
        await ubicacionAPI.deleteDepartamento(id)
        await this.fetchDepartamentos()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Failed to delete departamento')
        console.error('Error deleting departamento:', err)
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.formData = {
        id: null,
        nombre: '',
        provincia: null
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