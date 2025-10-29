<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Provincias.vue -->
<template>
  <AdminLayout
    page-title="Administración de Provincias"
    :breadcrumbs="[{ label: 'Provincias' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nueva Provincia
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Provincias"
          :columns="columns"
          :items="filteredProvincias"
          :export-formatters="exportFormatters"
          :loading="loading"
          :error="error"
          :footer-text="`Mostrando ${filteredProvincias.length} de ${provincias.length} provincias`"
          @create="showCreateModal = true"
          @edit="editProvincia"
          @delete="confirmDelete"
          @retry="fetchProvincias"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por nombre..."
                v-model="searchQuery"
                @input="filterProvincias"
              >
            </div>
            <div class="col-md-3">
              <select class="form-control form-control-sm" v-model="paisFilter" @change="filterProvincias">
                <option value="">Todos los países</option>
                <option v-for="pais in paises" :key="pais.id" :value="pais.id">
                  {{ pais.nombre }}
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
              <div class="avatar rounded-circle bg-primary text-white me-3">
                <i class="bi bi-geo-alt"></i>
              </div>
              <span>{{ item.nombre }}</span>
            </div>
          </template>

          <template #cell-pais="{ item }">
            <span class="badge bg-info">
              {{ getPaisName(item.pais) }}
            </span>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Provincia Modal -->
    <ProvinciaModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :provincia-data="formData"
      :paises="paises"
      @close="closeModal"
      @save="saveProvincia"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar Provincia"
      :message="`¿Estás seguro de que quieres eliminar la provincia ${provinciaToDelete?.nombre}?`"
      description="Esta acción no se puede deshacer. La provincia será eliminada permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deleteProvincia"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import ProvinciaModal from '@/components/admin/ProvinciaModal.vue'
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue'
import { ubicacionAPI } from '@/services/api'

interface Pais {
  id: number
  nombre: string
}

interface Provincia {
  id: number
  nombre: string
  pais: number | { id: number; nombre: string }
}

export default defineComponent({
  name: 'AdminProvincias',
  components: {
    AdminLayout,
    AdminTable,
    ProvinciaModal,
    ConfirmationModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      provincias: [] as Provincia[],
      filteredProvincias: [] as Provincia[],
      paises: [] as Pais[],
      searchQuery: '',
      paisFilter: '',
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      deleting: false,
      provinciaToDelete: null as Provincia | null,
      formData: {
        id: null as number | null,
        nombre: '',
        pais: null as number | null
      },
      columns: [
        { key: 'id', label: 'ID', align: 'center' },
        { key: 'nombre', label: 'Nombre' },
        { key: 'pais', label: 'País' }
      ] as TableColumn[],
      exportFormatters: {
        pais: (item: Provincia) => this.getPaisName(item.pais)
      }
    }
  },
  mounted() {
    this.fetchPaises()
    this.fetchProvincias()
  },
  methods: {
    async fetchPaises() {
      try {
        const response = await ubicacionAPI.getPaises()
        this.paises = response.data
      } catch (err: any) {
        console.error('Error fetching paises:', err)
      }
    },

    async fetchProvincias() {
      this.loading = true
      this.error = null
      try {
        const response = await ubicacionAPI.getProvincias()
        this.provincias = response.data
        this.filteredProvincias = [...this.provincias]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar provincias'
        console.error('Error al cargar provincias:', err)
      } finally {
        this.loading = false
      }
    },

    filterProvincias() {
      let filtered = [...this.provincias]

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(provincia =>
          provincia.nombre.toLowerCase().includes(query)
        )
      }

      if (this.paisFilter) {
        filtered = filtered.filter(provincia => {
          const paisId = typeof provincia.pais === 'object' ? provincia.pais.id : provincia.pais
          return paisId === Number(this.paisFilter)
        })
      }

      this.filteredProvincias = filtered
    },

    clearFilters() {
      this.searchQuery = ''
      this.paisFilter = ''
      this.filteredProvincias = [...this.provincias]
    },

    getPaisName(paisId: number | { id: number; nombre: string }): string {
      // Handle both number and object formats
      if (typeof paisId === 'object' && paisId !== null) {
        return paisId.nombre
      }
      const pais = this.paises.find(p => p.id === paisId)
      return pais ? pais.nombre : 'N/A'
    },

    editProvincia(provincia: Provincia) {
      this.formData = {
        id: provincia.id,
        nombre: provincia.nombre,
        pais: typeof provincia.pais === 'object' ? (provincia.pais as any)?.id : provincia.pais
      }
      this.showEditModal = true
    },

    async saveProvincia(provinciaData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && provinciaData.id) {
          await ubicacionAPI.updateProvincia(provinciaData.id, {
            nombre: provinciaData.nombre,
            pais_id: provinciaData.pais
          })
        } else {
          await ubicacionAPI.createProvincia({
            nombre: provinciaData.nombre,
            pais_id: provinciaData.pais
          })
        }

        if (callback) callback(true)
        this.closeModal()
        await this.fetchProvincias()
      } catch (err: any) {
        console.error('Save error:', err)
        const errorMsg = err.response?.data?.detail
          || err.response?.data?.nombre?.[0]
          || err.response?.data?.pais_id?.[0]
          || err.message
          || 'Failed to save provincia'

        if (callback) {
          callback(false, errorMsg)
        } else {
          alert(errorMsg)
        }
      }
    },

    confirmDelete(provincia: Provincia) {
      this.provinciaToDelete = provincia
      this.showDeleteModal = true
    },

    cancelDelete() {
      this.showDeleteModal = false
      this.provinciaToDelete = null
    },

    async deleteProvincia() {
      if (!this.provinciaToDelete) return

      this.deleting = true
      try {
        await ubicacionAPI.deleteProvincia(this.provinciaToDelete.id)
        await this.fetchProvincias()
        this.showDeleteModal = false
        this.provinciaToDelete = null
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar provincia')
        console.error('Error deleting provincia:', err)
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
        pais: null
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
