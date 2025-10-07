<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <AdminLayout 
    page-title="Administración de usuarios" 
    :breadcrumbs="[{ label: 'Usuarios' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> Nuevo Usuario
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="Todos los Usuarios"
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
              >
            </div>
            <div class="col-md-4">
              <select class="form-control form-control-sm" v-model="roleFilter" @change="filterUsers">
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

          <template #cell-date_joined="{ value }">
            {{ formatDate(value) }}
          </template>

          <template #cell-last_login="{ value }">
            {{ value ? formatDate(value) : 'Nunca' }}
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
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import UserModal from '@/components/admin/UserModal.vue'
import { userAPI } from '@/services/api'

interface User {
  id: number
  email: string
  role: 'ADMIN' | 'DELEG' | 'VOL'
  date_joined: string
  last_login: string | null
  persona: number | null
}

export default defineComponent({
  name: 'AdminUsers',
  components: {
    AdminLayout,
    AdminTable,
    UserModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      users: [] as User[],
      filteredUsers: [] as User[],
      searchQuery: '',
      roleFilter: '',
      showCreateModal: false,
      showEditModal: false,
      formData: {
        id: null as number | null,
        email: '',
        password: '',
        role: 'VOL' as 'ADMIN' | 'DELEG' | 'VOL',
        persona: null as number | null
      },
      columns: [
        { key: 'id', label: 'ID' },
        { key: 'email', label: 'Email' },
        { key: 'role', label: 'Rol' },
        { key: 'date_joined', label: 'Fecha de Registro' },
        { key: 'last_login', label: 'Último Acceso' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.loading = true
      this.error = null
      try {
        const response = await userAPI.getAllUsers()
        this.users = response.data
        this.filteredUsers = [...this.users]
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to fetch users'
        console.error('Error fetching users:', err)
      } finally {
        this.loading = false
      }
    },
    
    filterUsers() {
      let filtered = [...this.users]
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(user => 
          user.email.toLowerCase().includes(query)
        )
      }
      
      if (this.roleFilter) {
        filtered = filtered.filter(user => user.role === this.roleFilter)
      }
      
      this.filteredUsers = filtered
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.roleFilter = ''
      this.filteredUsers = [...this.users]
    },
    
    getRoleBadgeClass(role: string) {
      const classes: Record<string, string> = {
        'ADMIN': 'bg-danger',
        'DELEG': 'bg-warning',
        'VOL': 'bg-info'
      }
      return classes[role] || 'bg-secondary'
    },
    
    getRoleDisplay(role: string) {
      const displays: Record<string, string> = {
        'ADMIN': 'Administrativo',
        'DELEG': 'Delegado',
        'VOL': 'Voluntario'
      }
      return displays[role] || role
    },
    
    formatDate(dateString: string) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('es-AR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    
    editUser(user: User) {
      this.formData = {
        id: user.id,
        email: user.email,
        password: '',
        role: user.role,
        persona: user.persona
      }
      this.showEditModal = true
    },
    
    async saveUser(userData: any, callback?: (success: boolean, error?: string) => void) {
      try {
        if (this.showEditModal && userData.id) {
          const updateData: any = {
            email: userData.email,
            role: userData.role
          }
          if (userData.password) {
            updateData.password = userData.password
          }
          await userAPI.updateUser(userData.id, updateData)
        } else {
          await userAPI.createUser({
            email: userData.email,
            password: userData.password,
            role: userData.role,
            persona: userData.persona
          })
        }
        
        if (callback) callback(true)
        this.closeModal()
        await this.fetchUsers()
      } catch (err: any) {
        // Extract error message from backend
        const errorMsg = err.response?.data?.detail 
          || err.response?.data?.email?.[0]
          || err.response?.data?.password?.[0]
          || err.response?.data?.role?.[0]
          || err.message 
          || 'Failed to save user'
        
        if (callback) {
          callback(false, errorMsg)
        } else {
          alert(errorMsg)
        }
      }
    },
        
    confirmDelete(user: User) {
      if (confirm(`¿Estás seguro de que quieres eliminar el usuario ${user.email}?`)) {
        this.deleteUser(user.id)
      }
    },
    
    async deleteUser(id: number) {
      try {
        await userAPI.deleteUser(id)
        await this.fetchUsers()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Failed to delete user')
        console.error('Error deleting user:', err)
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.formData = {
        id: null,
        email: '',
        password: '',
        role: 'VOL',
        persona: null
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