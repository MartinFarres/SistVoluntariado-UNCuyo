<template>
  <AdminLayout
    page-title="Carreras Management"
    :breadcrumbs="[{ label: 'Carreras' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nueva Carrera
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Todas las Carreras"
          :columns="columns"
          :items="filteredCarreras"
          :loading="loading"
          :footer-text="`Mostrando ${filteredCarreras.length} de ${carreras.length} carreras`"
          @create="showCreateModal = true"
          @edit="editCarrera"
          @delete="confirmDelete"
          @retry="fetchCarreras"
        >
          <template #filters>
            <div class="col-md-4">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por nombre..."
                v-model="searchQuery"
                @input="filterCarreras"
              >
            </div>
            <div class="col-md-3">
              <select
                class="form-select form-select-sm"
                v-model="selectedFacultad"
                @change="filterCarreras"
              >
                <option :value="null">Todas las facultades</option>
                <option
                  v-for="facultad in facultades"
                  :key="facultad.id"
                  :value="facultad.id"
                >
                  {{ facultad.nombre }}
                </option>
              </select>
            </div>
            <div class="col-md-2 text-end ms-auto">
              <button class="btn btn-sm btn-outline-primary" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Limpiar Filtros
              </button>
            </div>
          </template>
          <template #cell-facultad="{ item }">
            <span>{{ item.facultad_data?.nombre || '-' }}</span>
          </template>
        </AdminTable>
      </div>
    </div>

    <CarreraModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :carrera-data="formData"
      :facultades="facultades"
      :saving="saving"
      @close="closeModal"
      @save="saveCarrera"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import CarreraModal from '@/components/admin/CarreraModal.vue'
import { facultadAPI } from '@/services/api'

interface Carrera {
  id: number
  nombre: string
  facultad: number | null
  facultad_data?: { nombre: string }
}

interface Facultad {
  id: number
  nombre: string
  activa: boolean
}

interface CarreraFormData {
  id: number | null
  nombre: string
  facultad: number | null
}

export default defineComponent({
  name: 'AdminCarreras',
  components: { AdminLayout, AdminTable, CarreraModal },
  data() {
    return {
      loading: false,
      saving: false,
      error: null as string | null,
      carreras: [] as Carrera[],
      filteredCarreras: [] as Carrera[],
      facultades: [] as Facultad[],
      searchQuery: '',
      selectedFacultad: null as number | null,
      showCreateModal: false,
      showEditModal: false,
      formData: {
        id: null,
        nombre: '',
        facultad: null
      } as CarreraFormData,
      columns: [
        { key: 'id', label: 'ID' },
        { key: 'nombre', label: 'Carrera' },
        { key: 'facultad', label: 'Facultad' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchCarreras()
    this.fetchFacultades()
  },
  methods: {
    async fetchCarreras() {
      this.loading = true
      this.error = null
      try {
        const response = await facultadAPI.getCarreras()
        this.carreras = response.data
        this.filterCarreras()
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar carreras'
      } finally {
        this.loading = false
      }
    },
    async fetchFacultades() {
      try {
        const response = await facultadAPI.getFacultades()
        this.facultades = response.data
      } catch (err: any) {
        console.error('Error al cargar facultades:', err)
      }
    },
    filterCarreras() {
      let filtered = [...this.carreras]

      // Filtrar por búsqueda de texto
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter((c: Carrera) =>
          c.nombre.toLowerCase().includes(query)
        )
      }

      // Filtrar por facultad seleccionada
      if (this.selectedFacultad !== null) {
        filtered = filtered.filter((c: Carrera) =>
          c.facultad === this.selectedFacultad
        )
      }

      this.filteredCarreras = filtered
    },
    clearFilters() {
      this.searchQuery = ''
      this.selectedFacultad = null
      this.filteredCarreras = [...this.carreras]
    },
    editCarrera(carrera: Carrera) {
      this.formData = {
        id: carrera.id,
        nombre: carrera.nombre,
        facultad: carrera.facultad
      }
      this.showEditModal = true
    },
    async saveCarrera(carreraData: CarreraFormData) {
      this.saving = true
      try {
        if (this.showEditModal && carreraData.id) {
          await facultadAPI.updateCarrera(carreraData.id, {
            nombre: carreraData.nombre,
            facultad: carreraData.facultad
          })
        } else {
          await facultadAPI.createCarrera({
            nombre: carreraData.nombre,
            facultad: carreraData.facultad
          })
        }
        this.closeModal()
        await this.fetchCarreras()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al guardar carrera')
      } finally {
        this.saving = false
      }
    },
    confirmDelete(carrera: Carrera) {
      if (confirm(`¿Está seguro que desea eliminar la carrera "${carrera.nombre}"?`)) {
        this.deleteCarrera(carrera.id)
      }
    },
    async deleteCarrera(id: number) {
      try {
        await facultadAPI.deleteCarrera(id)
        await this.fetchCarreras()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar carrera')
      }
    },
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.formData = { id: null, nombre: '', facultad: null }
    }
  }
})
</script>
