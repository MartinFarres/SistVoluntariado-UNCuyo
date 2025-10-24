<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Voluntariados.vue -->
<template>
  <AdminLayout
    page-title="Administración de voluntariados"
    :breadcrumbs="[{ label: 'Voluntariados' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="openCreateModal">
        <i class="bi bi-plus"></i> Nuevo Voluntariado
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Voluntariados"
          :columns="columns"
          :items="filteredVoluntariados"
          :loading="loading"
          :error="error || undefined"
          :footer-text="`Mostrando ${filteredVoluntariados.length} de ${voluntariados.length} voluntariados`"
          create-button-text="Nuevo Voluntariado"
          empty-text="No se encontraron voluntariados. ¡Crea el primero!"
          @create="openCreateModal"
          @edit="editVoluntariado"
          @delete="confirmDelete"
          @retry="fetchVoluntariados"
        >
          <!-- Slot de filtros -->
          <template #filters>
            <div class="col-md-4">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por nombre..."
                v-model="searchQuery"
                @input="filterVoluntariados"
              >
            </div>
            <div class="col-md-3">
              <select class="form-control form-control-sm" v-model="estadoFilter" @change="filterVoluntariados">
                <option value="">Todos los estados</option>
                <option value="DRAFT">Borrador</option>
                <option value="ACTIVE">Activo</option>
                <option value="CLOSED">Cerrado</option>
              </select>
            </div>
          </template>

          <!-- Templates de celdas personalizadas -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="icon-wrapper me-3">
                <i class="bi bi-heart-fill text-danger fs-5"></i>
              </div>
              <div>
                <span class="fw-bold">{{ item.nombre }}</span>
                <small v-if="item.turnos_count === 0" class="text-warning d-block mt-1">
                  <i class="bi bi-exclamation-triangle-fill me-1"></i>
                  No tiene turnos relacionados
                </small>
              </div>
            </div>
          </template>

          <template #cell-estado="{ item }">
            <span class="badge" :class="getEstadoBadgeClass(item.estado)">
              {{ getEstadoDisplay(item.estado) }}
            </span>
          </template>

          <template #cell-organizacion="{ item }">
            <span v-if="item.organizacion">{{ item.organizacion.nombre }}</span>
            <span v-else class="text-muted">Sin organización</span>
          </template>

          <template #cell-turnos_count="{ value }">
            <span class="badge" :class="value > 0 ? 'bg-primary' : 'bg-secondary'">{{ value || 0 }}</span>
          </template>

          <template #actions="{ item }">
            <button
              class="btn btn-sm btn-outline-secondary me-1"
              @click.stop="goToTurnos(item)"
              title="Gestionar turnos"
            >
              <i class="bi bi-calendar-week"></i>
            </button>
            <button
              class="btn btn-sm btn-outline-primary me-1"
              @click.stop="editVoluntariado(item)"
              title="Editar"
            >
              <i class="bi bi-pencil"></i>
            </button>
            <button
              class="btn btn-sm btn-outline-danger"
              @click.stop="confirmDelete(item)"
              title="Eliminar"
            >
              <i class="bi bi-trash"></i>
            </button>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Modals -->
    <VoluntariadoModal
      v-if="showVoluntariadoModal"
      :show="showVoluntariadoModal"
      :is-edit="isEditMode"
      :voluntariado-data="formData"
      :organizaciones-list="organizacionesList"
      @close="closeModal"
      @save="saveVoluntariado"
      @open-descripcion-modal="showDescripcionModal = true"
    />

    <DescripcionModal
      v-if="showDescripcionModal"
      :show="showDescripcionModal"
      @close="showDescripcionModal = false"
      @save="handleSaveDescripcion"
    />

    <!-- Confirmation Modal for delete -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar voluntariado"
      :message="deleteVoluntariadoMessage()"
      :processing="deleteProcessing"
      processing-text="Eliminando..."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      @confirm="confirmDeleteVoluntariado"
      @cancel="cancelDeleteVoluntariado"
    />

  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AdminLayout from '@/components/admin/AdminLayout.vue';
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue';
import VoluntariadoModal from '@/components/admin/VoluntariadoModal.vue';
// Turnos se gestionan en otra vista
import DescripcionModal from '@/components/admin/DescripcionModal.vue';
import ConfirmationModal from '@/components/admin/ConfirmationModal.vue';
import { voluntariadoAPI, organizacionAPI, descripcionAPI } from '@/services/api';

const createInitialFormData = () => ({
  id: null,
  nombre: '',
  turnos: [] as any[],  // cambiar de 'turno' a 'turnos'
  descripcion: null,
  organizacion: null,
  estado: 'DRAFT'
});


export default defineComponent({
  name: 'AdminVoluntariados',
  components: {
    AdminLayout,
    AdminTable,
    VoluntariadoModal,
    DescripcionModal,
    ConfirmationModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      voluntariados: [] as any[],
      filteredVoluntariados: [] as any[],
      organizacionesList: [] as any[],
      searchQuery: '',
      estadoFilter: '',
      showVoluntariadoModal: false,
      isEditMode: false,
      showDescripcionModal: false,
      formData: createInitialFormData(),
      // Delete confirmation modal state
      showDeleteModal: false,
      deleteProcessing: false,
      deleteTargetVoluntariado: null as any | null,
      columns: [
        { key: 'nombre', label: 'Nombre' },
        { key: 'organizacion', label: 'Organización' },
        { key: 'estado', label: 'Estado' },
        { key: 'turnos_count', label: 'Turnos', align: 'center' },
      ] as TableColumn[]
    };
  },
  mounted() {
    this.fetchVoluntariados();
    this.fetchOrganizaciones();
  },
  methods: {
    deleteVoluntariadoMessage(): string {
      return this.deleteTargetVoluntariado
        ? `¿Estás seguro de que quieres eliminar "${this.deleteTargetVoluntariado.nombre}"?`
        : '¿Eliminar voluntariado?';
    },
    async fetchVoluntariados() {
      this.loading = true;
      this.error = null;
      try {
        const response = await voluntariadoAPI.getAll();
        this.voluntariados = response.data;
        this.filteredVoluntariados = [...this.voluntariados];
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar voluntariados';
      } finally {
        this.loading = false;
      }
    },
    async fetchOrganizaciones() {
      try {
        const response = await organizacionAPI.getAll();
        this.organizacionesList = response.data;
      } catch (err) {
        console.error("Error fetching organizaciones:", err);
      }
    },
    filterVoluntariados() {
      let filtered = [...this.voluntariados];
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(v => v.nombre.toLowerCase().includes(query));
      }
      if (this.estadoFilter) {
        filtered = filtered.filter(v => v.estado === this.estadoFilter);
      }
      this.filteredVoluntariados = filtered;
    },
    clearFilters() {
      this.searchQuery = '';
      this.estadoFilter = '';
      this.filteredVoluntariados = [...this.voluntariados];
    },
    getEstadoBadgeClass(estado: string) {
      const classes: Record<string, string> = {
        'DRAFT': 'bg-secondary',
        'ACTIVE': 'bg-success',
        'CLOSED': 'bg-danger'
      };
      return classes[estado] || 'bg-secondary';
    },
    getEstadoDisplay(estado: string) {
      const displays: Record<string, string> = {
        'DRAFT': 'Borrador',
        'ACTIVE': 'Activo',
        'CLOSED': 'Cerrado'
      };
      return displays[estado] || estado;
    },
    openCreateModal() {
      this.formData = createInitialFormData();
      this.isEditMode = false;
      this.showVoluntariadoModal = true;
    },
    async editVoluntariado(voluntariado: any) {
      // Primero asignar los datos básicos
      this.formData = { ...voluntariado };
      this.isEditMode = true;

      // Asegurar que el select de Organización quede preseleccionado con el id
      this.formData.organizacion = voluntariado.organizacion?.id ?? null;

      this.showVoluntariadoModal = true;
    },
    async saveVoluntariado(data: any) {
      try {
        const payload = {
          nombre: data.nombre,
          descripcion_id: data.descripcion?.id,
          // Handle organizacion: if it's a number use it, if it's an object take its id, otherwise null
          organizacion_id: (typeof data.organizacion === 'number') ? data.organizacion : (data.organizacion?.id || null),
          estado: data.estado
        };

        if (this.isEditMode && data.id) {
          await voluntariadoAPI.update(data.id, payload);
        } else {
          await voluntariadoAPI.create(payload);
        }

        this.closeModal();
        await this.fetchVoluntariados();
      } catch (err: any) {
        throw new Error(err.response?.data?.detail || 'Error al guardar el voluntariado');
      }
    },
    goToTurnos(voluntariado: any) {
      this.$router.push({ name: 'AdminVoluntariadoTurnos', params: { id: voluntariado.id } })
    },
    async handleSaveDescripcion(descripcionData: any) {
      try {
        const response = await descripcionAPI.create(descripcionData);
        this.formData.descripcion = response.data; // Actualiza el ID en el formulario principal
        this.showDescripcionModal = false;
      } catch (error) {
        console.error("Error al crear la descripción:", error);
        alert("Error al crear la descripción.");
      }
    },
    confirmDelete(voluntariado: any) {
      this.deleteTargetVoluntariado = voluntariado;
      this.showDeleteModal = true;
    },
    async confirmDeleteVoluntariado() {
      if (!this.deleteTargetVoluntariado) return;
      this.deleteProcessing = true;
      try {
        await this.deleteVoluntariado(this.deleteTargetVoluntariado.id);
        this.showDeleteModal = false;
        this.deleteTargetVoluntariado = null;
      } catch (err) {
        // deleteVoluntariado already alerts on error
      } finally {
        this.deleteProcessing = false;
      }
    },
    cancelDeleteVoluntariado() {
      this.showDeleteModal = false;
      this.deleteTargetVoluntariado = null;
      this.deleteProcessing = false;
    },
    async deleteVoluntariado(id: number) {
      try {
        await voluntariadoAPI.delete(id);
        await this.fetchVoluntariados();
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar el voluntariado');
      }
    },
    closeModal() {
      this.showVoluntariadoModal = false;
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
  background: rgba(220, 53, 69, 0.1);
  border-radius: 0.5rem;
}
</style>
