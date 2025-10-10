<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Voluntariados.vue -->
<template>
  <AdminLayout 
    page-title="Administración de voluntariados" 
    :breadcrumbs="[{ label: 'Voluntariados' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> New Voluntariado
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Voluntariados"
          :columns="columns"
          :items="filteredVoluntariados"
          :loading="loading"
          :error="error"
          :footer-text="`Showing ${filteredVoluntariados.length} of ${voluntariados.length} voluntariados`"
          create-button-text="New Voluntariado"
          empty-text="No voluntariados found. Create your first one!"
          @create="showCreateModal = true"
          @edit="editVoluntariado"
          @delete="confirmDelete"
          @retry="fetchVoluntariados"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-4">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Search by name..."
                v-model="searchQuery"
                @input="filterVoluntariados"
              >
            </div>
            <div class="col-md-3">
              <select class="form-control form-control-sm" v-model="estadoFilter" @change="filterVoluntariados">
                <option value="">All Status</option>
                <option value="DRAFT">Draft</option>
                <option value="ACTIVE">Active</option>
                <option value="CLOSED">Closed</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-sm btn-outline-primary w-100" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Clear
              </button>
            </div>
          </template>

          <!-- Custom Cell Templates -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="icon-wrapper me-3">
                <i class="bi bi-heart-fill text-danger fs-5"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }}</span>
              </div>
            </div>
          </template>

          <template #cell-estado="{ item }">
            <span class="badge" :class="getEstadoBadgeClass(item.estado)">
              {{ getEstadoDisplay(item.estado) }}
            </span>
          </template>

          <template #cell-fecha_inicio="{ value }">
            {{ value ? formatDate(value) : 'N/A' }}
          </template>

          <template #cell-fecha_fin="{ value }">
            {{ value ? formatDate(value) : 'N/A' }}
          </template>

          <!-- Custom Actions -->
          <template #actions="{ item }">
            <button 
              class="btn btn-sm btn-outline-info me-1" 
              @click="viewDetails(item)"
              title="View Details"
            >
              <i class="bi bi-eye"></i>
            </button>
            <button 
              class="btn btn-sm btn-outline-primary me-1" 
              @click="editVoluntariado(item)"
              title="Edit"
            >
              <i class="bi bi-pencil"></i>
            </button>
            <button 
              class="btn btn-sm btn-outline-danger" 
              @click="confirmDelete(item)"
              title="Delete"
            >
              <i class="bi bi-trash"></i>
            </button>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Voluntariado Modal -->
    <VoluntariadoModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :voluntariado-data="formData"
      @close="closeModal"
      @save="saveVoluntariado"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import VoluntariadoModal from '@/components/admin/VoluntariadoModal.vue'
import { voluntariadoAPI } from '@/services/api'

interface Voluntariado {
  id: number
  nombre: string
  turno: number | null
  descripcion: number | null
  fecha_inicio: string | null
  fecha_fin: string | null
  gestionadores: number | null
  estado: 'DRAFT' | 'ACTIVE' | 'CLOSED'
}

export default defineComponent({
  name: 'AdminVoluntariados',
  components: {
    AdminLayout,
    AdminTable,
    VoluntariadoModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      voluntariados: [] as Voluntariado[],
      filteredVoluntariados: [] as Voluntariado[],
      searchQuery: '',
      estadoFilter: '',
      showCreateModal: false,
      showEditModal: false,
      formData: {
        id: null as number | null,
        nombre: '',
        turno: null as number | null,
        descripcion: null as number | null,
        fecha_inicio: null as string | null,
        fecha_fin: null as string | null,
        gestionadores: null as number | null,
        estado: 'DRAFT' as 'DRAFT' | 'ACTIVE' | 'CLOSED'
      },
      columns: [
        { key: 'id', label: 'ID', align: 'center' },
        { key: 'nombre', label: 'Name' },
        { key: 'estado', label: 'Status' },
        { key: 'fecha_inicio', label: 'Start Date' },
        { key: 'fecha_fin', label: 'End Date' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchVoluntariados()
  },
  methods: {
    async fetchVoluntariados() {
      this.loading = true
      this.error = null
      try {
        const response = await voluntariadoAPI.getAll()
        this.voluntariados = response.data
        this.filteredVoluntariados = [...this.voluntariados]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar voluntariados'
        console.error('Error al cargar voluntariados:', err)
      } finally {
        this.loading = false
      }
    },
    
    filterVoluntariados() {
      let filtered = [...this.voluntariados]
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(v => 
          v.nombre.toLowerCase().includes(query)
        )
      }
      
      if (this.estadoFilter) {
        filtered = filtered.filter(v => v.estado === this.estadoFilter)
      }
      
      this.filteredVoluntariados = filtered
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.estadoFilter = ''
      this.filteredVoluntariados = [...this.voluntariados]
    },
    
    getEstadoBadgeClass(estado: string) {
      const classes: Record<string, string> = {
        'DRAFT': 'bg-secondary',
        'ACTIVE': 'bg-success',
        'CLOSED': 'bg-danger'
      }
      return classes[estado] || 'bg-secondary'
    },
    
    getEstadoDisplay(estado: string) {
      const displays: Record<string, string> = {
        'DRAFT': 'Borrador',
        'ACTIVE': 'Activo',
        'CLOSED': 'Cerrado'
      }
      return displays[estado] || estado
    },
    
    formatDate(dateString: string) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    
    viewDetails(voluntariado: Voluntariado) {
      this.$router.push(`/admin/voluntariados/${voluntariado.id}`)
    },
    
    editVoluntariado(voluntariado: Voluntariado) {
      this.formData = {
        id: voluntariado.id,
        nombre: voluntariado.nombre,
        turno: voluntariado.turno,
        descripcion: voluntariado.descripcion,
        fecha_inicio: voluntariado.fecha_inicio,
        fecha_fin: voluntariado.fecha_fin,
        gestionadores: voluntariado.gestionadores,
        estado: voluntariado.estado
      }
      this.showEditModal = true
    },
    
    async saveVoluntariado(data: any) {
      try {
        if (this.showEditModal && data.id) {
          const updateData = {
            nombre: data.nombre,
            turno: data.turno,
            descripcion: data.descripcion,
            fecha_inicio: data.fecha_inicio,
            fecha_fin: data.fecha_fin,
            gestionadores: data.gestionadores,
            estado: data.estado
          }
          await voluntariadoAPI.update(data.id, updateData)
        } else {
          await voluntariadoAPI.create({
            nombre: data.nombre,
            turno: data.turno,
            descripcion: data.descripcion,
            fecha_inicio: data.fecha_inicio,
            fecha_fin: data.fecha_fin,
            gestionadores: data.gestionadores,
            estado: data.estado
          })
        }
        
        this.closeModal()
        await this.fetchVoluntariados()
      } catch (err: any) {
        throw new Error(err.response?.data?.detail || 'Failed to save voluntariado')
      }
    },
    
    confirmDelete(voluntariado: Voluntariado) {
      if (confirm(`Are you sure you want to delete "${voluntariado.nombre}"?`)) {
        this.deleteVoluntariado(voluntariado.id)
      }
    },
    
    async deleteVoluntariado(id: number) {
      try {
        await voluntariadoAPI.delete(id)
        await this.fetchVoluntariados()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Failed to delete voluntariado')
        console.error('Error deleting voluntariado:', err)
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.formData = {
        id: null,
        nombre: '',
        turno: null,
        descripcion: null,
        fecha_inicio: null,
        fecha_fin: null,
        gestionadores: null,
        estado: 'DRAFT'
      }
    }
  }
})
</script>

<style scoped>
.icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 0.5rem;
}
</style>