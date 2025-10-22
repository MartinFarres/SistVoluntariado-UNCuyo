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
          :error="error"
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
              </div>
            </div>
          </template>

          <template #cell-estado="{ item }">
            <span class="badge" :class="getEstadoBadgeClass(item.estado)">
              {{ getEstadoDisplay(item.estado) }}
            </span>
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
      :gestionadores-list="gestionadoresList"
      @close="closeModal"
      @save="saveVoluntariado"
      @open-turno-modal="showTurnoModal = true"
      @open-descripcion-modal="showDescripcionModal = true"
    />

    <TurnoModal
      v-if="showTurnoModal"
      :show="showTurnoModal"
      :fecha="formData.fecha_inicio"
      @close="showTurnoModal = false"
      @save="handleSaveTurno"
    />

    <DescripcionModal
      v-if="showDescripcionModal"
      :show="showDescripcionModal"
      @close="showDescripcionModal = false"
      @save="handleSaveDescripcion"
    />

  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AdminLayout from '@/components/admin/AdminLayout.vue';
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue';
import VoluntariadoModal from '@/components/admin/VoluntariadoModal.vue';
import TurnoModal from '@/components/admin/TurnoModal.vue';
import DescripcionModal from '@/components/admin/DescripcionModal.vue';
import { voluntariadoAPI, personaAPI, turnoAPI, descripcionAPI } from '@/services/api';

const createInitialFormData = () => ({
  id: null,
  nombre: '',
  turnos: [] as any[],  // cambiar de 'turno' a 'turnos'
  descripcion: null,
  fecha_inicio: null,
  fecha_fin: null,
  gestionadores: null,
  estado: 'DRAFT'
});


export default defineComponent({
  name: 'AdminVoluntariados',
  components: {
    AdminLayout,
    AdminTable,
    VoluntariadoModal,
    TurnoModal,
    DescripcionModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      voluntariados: [] as any[],
      filteredVoluntariados: [] as any[],
      gestionadoresList: [] as any[],
      searchQuery: '',
      estadoFilter: '',
      showVoluntariadoModal: false,
      isEditMode: false,
      showTurnoModal: false,
      showDescripcionModal: false,
      formData: createInitialFormData(),
      columns: [
        { key: 'nombre', label: 'Nombre' },
        { key: 'estado', label: 'Estado' },
      ] as TableColumn[]
    };
  },
  mounted() {
    this.fetchVoluntariados();
    this.fetchGestionadores();
  },
  methods: {
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
    async fetchGestionadores() {
      try {
        const response = await personaAPI.getGestionadores();
        this.gestionadoresList = response.data;
      } catch (err) {
        console.error("Error fetching gestionadores:", err);
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

      // Asegurar que el select de Manager quede preseleccionado con el id
      this.formData.gestionadores = voluntariado.gestionador?.id ?? null;

      // Traer los turnos del voluntariado
      try {
        const response = await voluntariadoAPI.getTurnos(voluntariado.id);
        this.formData.turnos = response.data; // asumiendo que devuelve un array
      } catch (err) {
        console.error('Error al cargar turnos:', err);
        this.formData.turnos = [];
      }

      this.showVoluntariadoModal = true;
    },
    async saveVoluntariado(data: any) {
      try {
        const payload = {
          nombre: data.nombre,
          descripcion_id: data.descripcion?.id,
          fecha_inicio: data.fecha_inicio,
          fecha_fin: data.fecha_fin,
          // En el modal, 'gestionadores' es un número (id). Para compatibilidad si llega objeto, tomar su id.
          gestionadores_id: (typeof data.gestionadores === 'number') ? data.gestionadores : data.gestionadores?.id,
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
    async handleSaveTurno(turnoData: any) {
  try {
    if (!this.formData.id) {
      alert("Primero guarda el voluntariado antes de agregar turnos.");
      return;
    }

    const payload = {
      ...turnoData,
      voluntariado_id: this.formData.id  // clave nueva: relación FK
    };

    await turnoAPI.create(payload);
    this.showTurnoModal = false;


    const response = await voluntariadoAPI.getTurnos(this.formData.id);
    this.formData.turnos.push(response.data);


  } catch (error) {
    console.error("Error al crear el turno:", error);
    alert("Error al crear el turno.");
  }
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
      if (confirm(`¿Estás seguro de que quieres eliminar "${voluntariado.nombre}"?`)) {
        this.deleteVoluntariado(voluntariado.id);
      }
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
