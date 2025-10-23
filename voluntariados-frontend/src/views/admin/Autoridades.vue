<template>
  <AdminLayout
    page-title="Administración de autoridades"
    :breadcrumbs="[{ label: 'Autoridades' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="openCreateModal">
        <i class="bi bi-plus"></i> Nueva Autoridad
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Autoridades"
          :columns="columns"
          :items="filteredAutoridades"
          :loading="loading"
          :error="error"
          :footer-text="`Mostrando ${filteredAutoridades.length} de ${autoridades.length} autoridades`"
          create-button-text="Nueva Autoridad"
          empty-text="No se encontraron autoridades. ¡Crea la primera!"
          @create="openCreateModal"
          @edit="editAutoridad"
          @delete="confirmDelete"
          @retry="fetchAutoridades"
        >
          <!-- Filtros -->
          <template #filters>
            <div class="col-md-4">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por nombre o cargo..."
                v-model="searchQuery"
                @input="filterAutoridades"
              />
            </div>
          </template>

          <!-- Celda de Nombre -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="icon-wrapper me-3">
                <i class="bi bi-person-badge fs-5 text-primary"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }} {{ item.apellido }}</span>
              </div>
            </div>
          </template>

          <template #cell-firma="{ item }">
            <div v-if="item.firma">
              <img :src="item.firma" alt="Firma" style="height: 40px; object-fit: contain;">
            </div>
            <div v-else>
              <span class="text-muted">Sin firma</span>
            </div>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Modal -->
    <AutoridadModal
      v-if="showAutoridadModal"
      :show="showAutoridadModal"
      :is-edit="isEditMode"
      :autoridad-data="formData"
      @close="closeModal"
      @save="saveAutoridad"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AdminLayout from '@/components/admin/AdminLayout.vue';
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue';
import AutoridadModal from '@/components/admin/AutoridadModal.vue';
import { autoridadAPI } from '@/services/api';

const createInitialFormData = () => ({
  id: null,
  nombre: '',
  apellido: '',
  cargo: '',
  entidad_encargada: '',
  firma: null as File | null
});

export default defineComponent({
  name: 'AdminAutoridades',
  components: {
    AdminLayout,
    AdminTable,
    AutoridadModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      autoridades: [] as any[],
      filteredAutoridades: [] as any[],
      searchQuery: '',
      showAutoridadModal: false,
      isEditMode: false,
      formData: createInitialFormData(),
      columns: [
        { key: 'nombre', label: 'Nombre' },
        { key: 'cargo', label: 'Cargo' },
        { key: 'entidad_encargada', label: 'Entidad Encargada' },
        { key: 'firma', label: 'Firma' }
      ] as TableColumn[]
    };
  },
  mounted() {
    this.fetchAutoridades();
  },
  methods: {
    async fetchAutoridades() {
      this.loading = true;
      this.error = null;
      try {
        const response = await autoridadAPI.getAll();
        this.autoridades = response.data;
        this.filteredAutoridades = [...this.autoridades];
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar autoridades';
      } finally {
        this.loading = false;
      }
    },
    filterAutoridades() {
      const q = this.searchQuery.toLowerCase();
      this.filteredAutoridades = this.autoridades.filter(a =>
        a.nombre.toLowerCase().includes(q) ||
        a.apellido.toLowerCase().includes(q) ||
        a.cargo.toLowerCase().includes(q)
      );
    },
    openCreateModal() {
      this.formData = createInitialFormData();
      this.isEditMode = false;
      this.showAutoridadModal = true;
    },
    editAutoridad(autoridad: any) {
      this.formData = { ...autoridad };
      console.log(this.formData)
      this.isEditMode = true;
      this.showAutoridadModal = true;
    },
    async saveAutoridad(data: any) {
      try {
        const form = new FormData();
        form.append('nombre', data.nombre);
        form.append('apellido', data.apellido);
        form.append('cargo', data.cargo);
        form.append('entidad_encargada', data.entidad_encargada);
        if (data.firma instanceof File) {
          form.append('firma', data.firma);
        }

        if (this.isEditMode && data.id) {
          await autoridadAPI.update(data.id, form);
        } else {
          await autoridadAPI.create(form);
        }

        this.closeModal();
        await this.fetchAutoridades();
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al guardar la autoridad');
      }
    },
    confirmDelete(autoridad: any) {
      if (confirm(`¿Estás seguro de que quieres eliminar a "${autoridad.nombre} ${autoridad.apellido}"?`)) {
        this.deleteAutoridad(autoridad.id);
      }
    },
    async deleteAutoridad(id: number) {
      try {
        await autoridadAPI.delete(id);
        await this.fetchAutoridades();
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar la autoridad');
      }
    },
    closeModal() {
      this.showAutoridadModal = false;
      this.isEditMode = false;
    }
  }
});
</script>

<style scoped>
.icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(13, 110, 253, 0.1);
  border-radius: 0.5rem;
}
</style>
