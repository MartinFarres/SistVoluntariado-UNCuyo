<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <AdminLayout page-title="Administración de usuarios" :breadcrumbs="[{ label: 'Usuarios' }]">
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nuevo Usuario
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title=""
          :columns="columns"
          :items="filteredUsers"
          :loading="loading"
          :error="error"
          :footer-text="`Mostrando ${filteredUsers.length} de ${users.length} usuarios`"
          @create="showCreateModal = true"
          @edit="editUser"
          @delete="confirmDelete"
          @retry="fetchUsers"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-5">
              <input
                type="text"
                class="form-control form-control-sm"
                placeholder="Buscar por email..."
                v-model="searchQuery"
                @input="filterUsers"
              />
            </div>
            <div class="col-md-4">
              <select
                class="form-control form-control-sm"
                v-model="roleFilter"
                @change="filterUsers"
              >
                <option value="">Todos los roles</option>
                <option value="ADMIN">Administrativo</option>
                <option value="DELEG">Delegado</option>
                <option value="VOL">Voluntario</option>
              </select>
            </div>
            <div class="col-md-3 text-end">
              <button class="btn btn-sm btn-outline-primary" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Limpiar
              </button>
            </div>
          </template>

          <!-- Custom Cell Templates -->
          <template #cell-email="{ item }">
            <div class="d-flex align-items-center">
              <div class="avatar rounded-circle bg-primary text-white me-3">
                <i class="bi bi-person"></i>
              </div>
              <span>{{ item.email }}</span>
            </div>
          </template>

          <template #cell-role="{ item }">
            <span class="badge" :class="getRoleBadgeClass(item.role)">
              {{ getRoleDisplay(item.role) }}
            </span>
          </template>

          <template #cell-signup_date="{ value }">
            {{ formatDate(value) }}
          </template>

          <template #cell-last_login="{ value }">
            {{ value ? formatDate(value) : "Nunca" }}
          </template>
        </AdminTable>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <UserModal
      :show="showCreateModal || showEditModal"
      :is-edit="showEditModal"
      :user-data="formData"
      @close="closeModal"
      @save="saveUser"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      title="Eliminar Usuario"
      :message="`¿Estás seguro de que quieres eliminar el usuario ${userToDelete?.email}?`"
      description="Esta acción no se puede deshacer. El usuario será eliminado permanentemente del sistema."
      confirm-text="Eliminar"
      cancel-text="Cancelar"
      type="danger"
      :processing="deleting"
      processing-text="Eliminando..."
      @confirm="deleteUser"
      @cancel="cancelDelete"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminLayout from "@/components/admin/AdminLayout.vue";
import AdminTable, { type TableColumn } from "@/components/admin/AdminTable.vue";
import UserModal from "@/components/admin/UserModal.vue";
import ConfirmationModal from "@/components/admin/ConfirmationModal.vue";
import { userAPI, authAPI, personaAPI } from "@/services/api";

interface User {
  id: number;
  email: string;
  role: "ADMIN" | "DELEG" | "VOL";
  signup_date: string;
  last_login: string | null;
  persona: number | null;
}

export default defineComponent({
  name: "AdminUsers",
  components: {
    AdminLayout,
    AdminTable,
    UserModal,
    ConfirmationModal,
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      users: [] as User[],
      filteredUsers: [] as User[],
      searchQuery: "",
      roleFilter: "",
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      deleting: false,
      userToDelete: null as User | null,
      formData: {
        id: null as number | null,
        email: "",
        password: "",
        role: "VOL" as "ADMIN" | "DELEG" | "VOL",
        persona: null as number | null,
        delegado_organizacion: null as number | null,
      },
      columns: [
        { key: "id", label: "ID", align: "center" },
        { key: "email", label: "Email" },
        { key: "role", label: "Rol" },
        { key: "signup_date", label: "Fecha de Registro" },
        { key: "last_login", label: "Último Acceso" },
      ] as TableColumn[],
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.error = null;
      try {
        const response = await userAPI.getAllUsers();
        this.users = response.data;
        this.filteredUsers = [...this.users];
      } catch (err: any) {
        this.error = err.response?.data?.detail || "Error al cargar usuarios";
        console.error("Error al cargar usuarios:", err);
      } finally {
        this.loading = false;
      }
    },

    filterUsers() {
      let filtered = [...this.users];

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter((user) => user.email.toLowerCase().includes(query));
      }

      if (this.roleFilter) {
        filtered = filtered.filter((user) => user.role === this.roleFilter);
      }

      this.filteredUsers = filtered;
    },

    clearFilters() {
      this.searchQuery = "";
      this.roleFilter = "";
      this.filteredUsers = [...this.users];
    },

    getRoleBadgeClass(role: string) {
      const classes: Record<string, string> = {
        ADMIN: "bg-danger",
        DELEG: "bg-warning",
        VOL: "bg-info",
      };
      return classes[role] || "bg-secondary";
    },

    getRoleDisplay(role: string) {
      const displays: Record<string, string> = {
        ADMIN: "Administrativo",
        DELEG: "Delegado",
        VOL: "Voluntario",
      };
      return displays[role] || role;
    },

    formatDate(dateString: string) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return date.toLocaleDateString("es-AR", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },

    async editUser(user: User) {
      this.formData = {
        id: user.id,
        email: user.email,
        password: "",
        role: user.role,
        persona: user.persona,
        delegado_organizacion: null,
      };

      // If the user is a Delegado and has a persona id, fetch the persona to prefill organization
      if (user.role === "DELEG" && user.persona) {
        try {
          const resp = await personaAPI.getDelegadoById(user.persona);
          // resp.data.organizacion is expected to be an id
          this.formData.delegado_organizacion = resp.data.organizacion || null;
        } catch (e) {
          // log error and leave delegado_organizacion null
          console.error("Error fetching delegado persona:", e);
          this.formData.delegado_organizacion = null;
        }
      }

      this.showEditModal = true;
    },

    async saveUser(userData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && userData.id) {
          const updateData: any = {
            email: userData.email,
            role: userData.role,
          };
          if (userData.password) {
            updateData.password = userData.password;
          }
          await userAPI.updateUser(userData.id, updateData);
          // If editing a Delegado, update the persona organizacion as well
          if (userData.role === "DELEG" && userData.persona && userData.delegado_organizacion) {
            try {
              await personaAPI.updateDelegado(userData.persona, {
                organizacion: userData.delegado_organizacion,
              });
            } catch (e) {
              // Log but don't block; main user update completed
              console.error("Failed updating delegado persona:", e);
            }
          }
        } else {
          // Build payload for registration. Include delegado_organizacion if provided
          const payload: any = {
            email: userData.email,
            password: userData.password,
            role: userData.role,
          };
          if (userData.delegado_organizacion) {
            payload.delegado_organizacion = userData.delegado_organizacion;
          }
          await authAPI.register(payload);
        }

        if (callback) callback(true);
        this.closeModal();
        await this.fetchUsers();
      } catch (err: any) {
        // Extract error message from backend
        const errorMsg =
          err.response?.data?.detail ||
          err.response?.data?.email?.[0] ||
          err.response?.data?.password?.[0] ||
          err.response?.data?.role?.[0] ||
          err.message ||
          "Failed to save user";

        if (callback) {
          callback(false, errorMsg);
        } else {
          alert(errorMsg);
        }
      }
    },

    confirmDelete(user: User) {
      this.userToDelete = user;
      this.showDeleteModal = true;
    },

    cancelDelete() {
      this.showDeleteModal = false;
      this.userToDelete = null;
    },

    async deleteUser() {
      if (!this.userToDelete) return;

      this.deleting = true;
      try {
        await userAPI.deleteUser(this.userToDelete.id);
        await this.fetchUsers();
        this.showDeleteModal = false;
        this.userToDelete = null;
      } catch (err: any) {
        alert(err.response?.data?.detail || "Error al eliminar usuario");
        console.error("Error deleting user:", err);
      } finally {
        this.deleting = false;
      }
    },

    closeModal() {
      this.showCreateModal = false;
      this.showEditModal = false;
      this.formData = {
        id: null,
        email: "",
        password: "",
        role: "VOL",
        persona: null,
        delegado_organizacion: null,
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
