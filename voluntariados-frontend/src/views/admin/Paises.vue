<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Countries.vue -->
<template>
  <AdminLayout 
    page-title="Administración de Paises" 
    :breadcrumbs="[{ label: 'Países' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nuevo país
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Todos los países"
          :columns="columns"
          :items="filteredCountries"
          :loading="loading"
          :error="error"
          :footer-text="`Mostrando ${filteredCountries.length} de ${countries.length} países`"
          @create="showCreateModal = true"
          @edit="editCountry"
          @delete="confirmDelete"
          @retry="fetchCountries"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-6">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Buscar por nombre..."
                v-model="searchQuery"
                @input="filterCountries"
              >
            </div>
            <div class="col-md-6 text-end">
              <button class="btn btn-sm btn-outline-primary" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Borrar filtros
              </button>
            </div>
          </template>

          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="avatar rounded-circle bg-primary text-white me-3">
                <i class="bi bi-globe"></i>
              </div>
              <span>{{ item.nombre }}</span>
            </div>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Country Modal -->
    <PaisModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :country-data="formData"
      @close="closeModal"
      @save="saveCountry"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar País"
      :message="`¿Estás seguro de que quieres eliminar el país ${countryToDelete?.nombre}?`"
      description="Esta acción no se puede deshacer. El país será eliminado permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deleteCountry"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import PaisModal from '@/components/admin/PaisModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { ubicacionAPI } from '@/services/api'

interface Country {
  id: number
  nombre: string
}

export default defineComponent({
  name: 'AdminCountries',
  components: {
    AdminLayout,
    AdminTable,
    PaisModal,
    ConfirmationModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      countries: [] as Country[],
      filteredCountries: [] as Country[],
      searchQuery: '',
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      deleting: false,
      countryToDelete: null as Country | null,
      formData: {
        id: null as number | null,
        nombre: ''
      },
      columns: [
        { key: 'id', label: 'ID', align: 'center' },
        { key: 'nombre', label: 'Nombre' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchCountries()
  },
  methods: {
    async fetchCountries() {
      this.loading = true
      this.error = null
      try {
        const response = await ubicacionAPI.getPaises()
        this.countries = response.data
        this.filteredCountries = [...this.countries]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar países'
        console.error('Error al cargar países:', err)
      } finally {
        this.loading = false
      }
    },
    
    filterCountries() {
      let filtered = [...this.countries]
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(country => 
          country.nombre.toLowerCase().includes(query)
        )
      }
      
      this.filteredCountries = filtered
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.filteredCountries = [...this.countries]
    },
    
    editCountry(country: Country) {
      this.formData = {
        id: country.id,
        nombre: country.nombre
      }
      this.showEditModal = true
    },
    
    async saveCountry(countryData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && countryData.id) {
          await ubicacionAPI.updatePais(countryData.id, {
            nombre: countryData.nombre
          })
        } else {
          await ubicacionAPI.createPais({
            nombre: countryData.nombre
          })
        }
        
        if (callback) callback(true)
        this.closeModal()
        await this.fetchCountries()
      } catch (err: any) {
        console.error('Save error:', err)
        const errorMsg = err.response?.data?.detail 
          || err.response?.data?.nombre?.[0]
          || err.response?.data?.error
          || err.message 
          || 'Error al guardar país'
        
        if (callback) {
          callback(false, errorMsg)
        } else {
          alert(errorMsg)
        }
      }
    },
    
    confirmDelete(country: Country) {
      this.countryToDelete = country
      this.showDeleteModal = true
    },
    
    cancelDelete() {
      this.showDeleteModal = false
      this.countryToDelete = null
    },
    
    async deleteCountry() {
      if (!this.countryToDelete) return
      
      this.deleting = true
      try {
        await ubicacionAPI.deletePais(this.countryToDelete.id)
        await this.fetchCountries()
        this.showDeleteModal = false
        this.countryToDelete = null
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar país')
        console.error('Error deleting country:', err)
      } finally {
        this.deleting = false
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.formData = {
        id: null,
        nombre: ''
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
</style>``