<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Facultades.vue -->
<template>
  <AdminLayout
    page-title="Facultades Management"
    :breadcrumbs="[{ label: 'Facultades' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nueva Facultad
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Todas las Facultades"
          :columns="columns"
          :items="filteredFacultades"
          :loading="loading"
          :error="error"
          :footer-text="`Mostrando ${filteredFacultades.length} de ${facultades.length} facultades`"
          @create="showCreateModal = true"
          @edit="editFacultad"
          @delete="confirmDelete"
          @retry="fetchFacultades"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por nombre..."
                v-model="searchQuery"
                @input="filterFacultades"
              >
            </div>
            <div class="col-md-2">
              <select class="form-control form-control-sm" v-model="statusFilter" @change="filterFacultades">
                <option value="">Todos los estados</option>
                <option value="active">Activas</option>
                <option value="inactive">Inactivas</option>
              </select>
            </div>
            <div class="col-md-3 text-end ms-auto">
              <button class="btn btn-sm btn-outline-primary" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Limpiar Filtros
              </button>
            </div>
          </template>

          <!-- Custom Cell Templates -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="avatar rounded-circle bg-primary text-white me-3">
                <i class="bi bi-building"></i>
              </div>
              <div>
                <div class="fw-semibold">{{ item.nombre }}</div>
              </div>
            </div>
          </template>

          <template #cell-activa="{ item }">
            <span class="badge" :class="item.activa ? 'bg-success' : 'bg-secondary'">
              {{ item.activa ? 'Activa' : 'Inactiva' }}
            </span>
          </template>

          <template #cell-carreras="{ item }">
            <span class="badge bg-info">
              {{ Array.isArray(item.carreras) ? item.carreras.length : 0 }} carrera(s)
            </span>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Facultad Modal -->
    <FacultadModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :facultad-data="formData"
      @close="closeModal"
      @save="saveFacultad"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import FacultadModal from '@/components/admin/FacultadModal.vue'
import { facultadAPI } from '@/services/api'

interface Facultad {
  id: number
  nombre: string
  activa: boolean
  carreras: string[]
}

export default defineComponent({
  name: 'AdminFacultades',
  components: {
    AdminLayout,
    AdminTable,
    FacultadModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      facultades: [] as Facultad[],
      filteredFacultades: [] as Facultad[],
      searchQuery: '',
      statusFilter: '',
      showCreateModal: false,
      showEditModal: false,
      formData: {
        id: null as number | null,
        nombre: '',
        activa: true
      },
      columns: [
        { key: 'id', label: 'ID' },
        { key: 'nombre', label: 'Facultad' },
        { key: 'activa', label: 'Estado' },
        { key: 'carreras', label: 'Carreras' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchFacultades()
  },
  methods: {
    async fetchFacultades() {
      this.loading = true
      this.error = null
      try {
        const response = await facultadAPI.getFacultades()
        this.facultades = response.data
        this.filteredFacultades = [...this.facultades]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar facultades'
        console.error('Error fetching facultades:', err)
      } finally {
        this.loading = false
      }
    },

    filterFacultades() {
      let filtered = [...this.facultades]

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(facultad =>
          facultad.nombre.toLowerCase().includes(query)
        )
      }

      if (this.statusFilter === 'active') {
        filtered = filtered.filter(facultad => facultad.activa)
      } else if (this.statusFilter === 'inactive') {
        filtered = filtered.filter(facultad => !facultad.activa)
      }

      this.filteredFacultades = filtered
    },

    clearFilters() {
      this.searchQuery = ''
      this.statusFilter = ''
      this.filteredFacultades = [...this.facultades]
    },

    editFacultad(facultad: Facultad) {
      this.formData = {
        id: facultad.id,
        nombre: facultad.nombre,
        activa: facultad.activa
      }
      this.showEditModal = true
    },

    async saveFacultad(facultadData: any) {
      try {
        if (this.showEditModal && facultadData.id) {
          await facultadAPI.updateFacultad(facultadData.id, {
            nombre: facultadData.nombre,
            activa: facultadData.activa
          })
        } else {
          await facultadAPI.createFacultad({
            nombre: facultadData.nombre,
            activa: facultadData.activa
          })
        }

        this.closeModal()
        await this.fetchFacultades()
      } catch (err: any) {
        throw new Error(err.response?.data?.detail || 'Error al guardar facultad')
      }
    },

    confirmDelete(facultad: Facultad) {
      if (confirm(`¿Está seguro que desea eliminar la facultad "${facultad.nombre}"?`)) {
        this.deleteFacultad(facultad.id)
      }
    },

    async deleteFacultad(id: number) {
      try {
        await facultadAPI.deleteFacultad(id)
        await this.fetchFacultades()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar facultad')
        console.error('Error deleting facultad:', err)
      }
    },

    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.formData = {
        id: null,
        nombre: '',
        activa: true
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
