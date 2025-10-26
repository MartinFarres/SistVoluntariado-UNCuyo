<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/Organizaciones.vue -->
<template>
  <AdminLayout
    page-title="Administración de organizaciones"
    :breadcrumbs="[{ label: 'Organizaciones' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nueva Organización
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Todas las Organizaciones"
          :columns="columns"
          :items="filteredOrganizaciones"
          :loading="loading"
          :error="error || undefined"
          :footer-text="`Mostrando ${filteredOrganizaciones.length} de ${organizaciones.length} organizaciones`"
          @create="showCreateModal = true"
          @edit="editOrganizacion"
          @delete="confirmDelete"
          @retry="fetchOrganizaciones"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-8">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por nombre..."
                v-model="searchQuery"
                @input="filterOrganizaciones"
              />
            </div>
            <div class="col-md-2">
              <select
                class="form-select form-select-sm"
                v-model="statusFilter"
                @change="filterOrganizaciones"
              >
                <option value="">Todos</option>
                <option value="true">Activos</option>
                <option value="false">Inactivos</option>
              </select>
            </div>
            <div class="col-md-2 text-end">
              <button class="btn btn-sm btn-outline-primary" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Limpiar
              </button>
            </div>
          </template>

          <!-- Custom Cell Templates -->
          <template #cell-nombre="{ item }">
            <div class="d-flex align-items-center">
              <div class="me-3">
                <img
                  v-if="item && item.logo"
                  :src="item.logo"
                  alt="logo"
                  class="rounded-circle"
                  style="width: 36px; height: 36px; object-fit: cover"
                />
                <div
                  v-else
                  class="avatar rounded-circle bg-info text-white d-inline-flex align-items-center justify-content-center"
                  style="width: 36px; height: 36px"
                >
                  <i class="bi bi-building"></i>
                </div>
              </div>
              <div>
                <div class="fw-bold">{{ item.nombre }}</div>
                <div v-if="item.slogan" class="text-muted small">{{ item.slogan }}</div>
              </div>
            </div>
          </template>

          <template #cell-activo="{ value }">
            <span :class="value ? 'badge bg-success' : 'badge bg-secondary'">
              {{ value ? "Activo" : "Inactivo" }}
            </span>
          </template>

          <template #cell-contacto_email="{ value }">
            <span v-if="value">
              <i class="bi bi-envelope me-1"></i>
              {{ value }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>

          <template #cell-localidad="{ item }">
            <span v-if="item.localidad && typeof item.localidad === 'object'" class="badge bg-info">
              {{ item.localidad.nombre }}
            </span>
            <span v-else-if="item.localidad" class="badge bg-info">
              Localidad {{ item.localidad }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit Organization Modal -->
    <OrganizacionModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :organization-data="formData"
      @close="closeModal"
      @save="saveOrganizacion"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar Organización"
      :message="`¿Estás seguro de que quieres eliminar la organización ${organizacionToDelete?.nombre}?`"
      description="Esta acción no se puede deshacer. La organización será eliminada permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deleteOrganizacion"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminLayout from "@/components/admin/AdminLayout.vue";
import AdminTable, { type TableColumn } from "@/components/admin/AdminTable.vue";
import OrganizacionModal from "@/components/admin/OrganizacionModal.vue";
import ConfirmationModal from "@/components/admin/ConfirmationModal.vue";
import { organizacionAPI } from "@/services/api";

interface Localidad {
  id: number;
  nombre: string;
}

interface Organizacion {
  id: number;
  nombre: string;
  activo: boolean;
  descripcion?: string;
  contacto_email?: string;
  localidad?: number | Localidad | null;
  direccion?: string | null;
  logo?: string | null;
  banner?: string | null;
  slogan?: string | null;
  url?: string | null;
}

export default defineComponent({
  name: "AdminOrganizaciones",
  components: {
    AdminLayout,
    AdminTable,
    OrganizacionModal,
    ConfirmationModal,
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      organizaciones: [] as Organizacion[],
      filteredOrganizaciones: [] as Organizacion[],
      searchQuery: "",
      statusFilter: "",
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      deleting: false,
      organizacionToDelete: null as Organizacion | null,
      formData: {
        id: null as number | null,
        nombre: "",
        activo: true,
        descripcion: "",
        contacto_email: "",
        localidad: null as number | null,
        direccion: "",
        logo: null as string | null,
        banner: null as string | null,
        slogan: null as string | null,
        url: null as string | null,
      },
      columns: [
        { key: "id", label: "ID", align: "center" },
        { key: "nombre", label: "Nombre" },
        { key: "slogan", label: "Slogan" },
        { key: "activo", label: "Estado" },
        { key: "contacto_email", label: "Email" },
        { key: "localidad", label: "Localidad" },
      ] as TableColumn[],
    };
  },
  mounted() {
    this.fetchOrganizaciones();
  },
  methods: {
    async fetchOrganizaciones() {
      this.loading = true;
      this.error = null;
      try {
        const response = await organizacionAPI.getAll();
        this.organizaciones = response.data;
        this.filteredOrganizaciones = [...this.organizaciones];
      } catch (err: any) {
        this.error = err.response?.data?.detail || "Error al cargar organizaciones";
        console.error("Error al cargar organizaciones:", err);
      } finally {
        this.loading = false;
      }
    },

    filterOrganizaciones() {
      let filtered = [...this.organizaciones];

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter((org) => org.nombre.toLowerCase().includes(query));
      }

      if (this.statusFilter !== "") {
        const isActive = this.statusFilter === "true";
        filtered = filtered.filter((org) => org.activo === isActive);
      }

      this.filteredOrganizaciones = filtered;
    },

    clearFilters() {
      this.searchQuery = "";
      this.statusFilter = "";
      this.filteredOrganizaciones = [...this.organizaciones];
    },

    editOrganizacion(organizacion: Organizacion) {
      this.formData = {
        id: organizacion.id,
        nombre: organizacion.nombre,
        activo: organizacion.activo,
        descripcion: organizacion.descripcion || "",
        contacto_email: organizacion.contacto_email || "",
        localidad:
          typeof organizacion.localidad === "object" && organizacion.localidad
            ? organizacion.localidad.id
            : organizacion.localidad || null,
        direccion: (organizacion as any).direccion || "",
        logo: (organizacion as any).logo || null,
        banner: (organizacion as any).banner || null,
        slogan: (organizacion as any).slogan || null,
        url: (organizacion as any).url || null,
      };
      this.showEditModal = true;
    },

    async saveOrganizacion(
      organizacionData: any,
      callback?: (success: boolean, error?: string) => void
    ) {
      try {
        // If the modal sent a FormData (files present), organizacionData will be FormData
        if (organizacionData instanceof FormData) {
          if (this.showEditModal && this.formData.id) {
            await organizacionAPI.update(this.formData.id, organizacionData);
          } else {
            await organizacionAPI.create(organizacionData);
          }
        } else {
          if (this.showEditModal && organizacionData.id) {
            await organizacionAPI.update(organizacionData.id, organizacionData);
          } else {
            await organizacionAPI.create(organizacionData);
          }
        }

        this.closeModal();
        await this.fetchOrganizaciones();

        if (callback) {
          callback(true);
        }
      } catch (err: any) {
        console.error("Save error:", err);
        const errorMsg =
          err.response?.data?.detail ||
          err.response?.data?.nombre?.[0] ||
          err.response?.data?.activo?.[0] ||
          err.response?.data?.descripcion?.[0] ||
          err.response?.data?.contacto_email?.[0] ||
          err.response?.data?.localidad?.[0] ||
          err.response?.data?.direccion?.[0] ||
          err.response?.data?.error ||
          err.message ||
          "Error al guardar la organizacion";

        if (callback) {
          callback(false, errorMsg);
        } else {
          alert(errorMsg);
        }
      }
    },

    confirmDelete(organizacion: Organizacion) {
      this.organizacionToDelete = organizacion;
      this.showDeleteModal = true;
    },

    cancelDelete() {
      this.showDeleteModal = false;
      this.organizacionToDelete = null;
    },

    async deleteOrganizacion() {
      if (!this.organizacionToDelete) return;

      this.deleting = true;
      try {
        await organizacionAPI.delete(this.organizacionToDelete.id);
        await this.fetchOrganizaciones();
        this.showDeleteModal = false;
        this.organizacionToDelete = null;
      } catch (err: any) {
        alert(err.response?.data?.detail || "Error al eliminar organización");
        console.error("Error deleting organizacion:", err);
      } finally {
        this.deleting = false;
      }
    },

    closeModal() {
      this.showCreateModal = false;
      this.showEditModal = false;
      this.formData = {
        id: null,
        nombre: "",
        activo: true,
        descripcion: "",
        contacto_email: "",
        localidad: null,
        direccion: "",
        logo: null,
        banner: null,
        slogan: null,
        url: null,
      };
    },
  },
});
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
