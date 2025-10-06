<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/admin/UsersRefactored.vue -->
<template>
  <AdminLayout 
    page-title="Users Management" 
    :breadcrumbs="[{ label: 'Users' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="showCreateModal = true">
        <i class="bi bi-plus"></i> New User
      </button>
    </template>

    <div class="row">
      <div class="col">
        <AdminTable
          title="All Users"
          :columns="columns"
          :items="filteredUsers"
          :loading="loading"
          :error="error"
          :footer-text="`Showing ${filteredUsers.length} of ${users.length} users`"
          @create="showCreateModal = true"
          @edit="editUser"
          @delete="confirmDelete"
          @retry="fetchUsers"
        >
          <!-- Filters Slot -->
          <template #filters>
            <div class="col-md-3">
              <input 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Search by email..."
                v-model="searchQuery"
                @input="filterUsers"
              >
            </div>
            <div class="col-md-2">
              <select class="form-control form-control-sm" v-model="roleFilter" @change="filterUsers">
                <option value="">All Roles</option>
                <option value="ADMIN">Administrativo</option>
                <option value="DELEG">Delegado</option>
                <option value="VOL">Voluntario</option>
              </select>
            </div>
            <div class="col-md-2">
              <select class="form-control form-control-sm" v-model="statusFilter" @change="filterUsers">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div class="col-md-2">
              <select class="form-control form-control-sm" v-model="staffFilter" @change="filterUsers">
                <option value="">All Types</option>
                <option value="staff">Staff Only</option>
                <option value="non-staff">Non-Staff</option>
              </select>
            </div>
            <div class="col-md-3 text-end">
              <button class="btn btn-sm btn-outline-primary" @click="clearFilters">
                <i class="bi bi-x-circle"></i> Clear Filters
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

          <template #cell-is_active="{ item }">
            <span class="badge" :class="item.is_active ? 'bg-success' : 'bg-secondary'">
              {{ item.is_active ? 'Active' : 'Inactive' }}
            </span>
          </template>

          <template #cell-is_staff="{ item }">
            <i 
              class="bi" 
              :class="item.is_staff ? 'bi-check-circle-fill text-success' : 'bi-x-circle text-muted'"
            ></i>
          </template>

          <template #cell-date_joined="{ value }">
            {{ formatDate(value) }}
          </template>

          <template #cell-last_login="{ value }">
            {{ value ? formatDate(value) : 'Never' }}
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
  is_active: boolean
  is_staff: boolean
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
      statusFilter: '',
      staffFilter: '',
      showCreateModal: false,
      showEditModal: false,
      formData: {
        id: null as number | null,
        email: '',
        password: '',
        role: 'VOL' as 'ADMIN' | 'DELEG' | 'VOL',
        is_active: true,
        is_staff: false,
        persona: null as number | null
      },
      columns: [
        { key: 'id', label: 'ID' },
        { key: 'email', label: 'Email' },
        { key: 'role', label: 'Role' },
        { key: 'is_active', label: 'Status' },
        { key: 'is_staff', label: 'Staff' },
        { key: 'date_joined', label: 'Date Joined' },
        { key: 'last_login', label: 'Last Login' }
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
      
      if (this.statusFilter === 'active') {
        filtered = filtered.filter(user => user.is_active)
      } else if (this.statusFilter === 'inactive') {
        filtered = filtered.filter(user => !user.is_active)
      }
      
      if (this.staffFilter === 'staff') {
        filtered = filtered.filter(user => user.is_staff)
      } else if (this.staffFilter === 'non-staff') {
        filtered = filtered.filter(user => !user.is_staff)
      }
      
      this.filteredUsers = filtered
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.roleFilter = ''
      this.statusFilter = ''
      this.staffFilter = ''
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
      return date.toLocaleDateString('en-US', {
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
        is_active: user.is_active,
        is_staff: user.is_staff,
        persona: user.persona
      }
      this.showEditModal = true
    },
    
    async saveUser(userData: any) {
      try {
        if (this.showEditModal && userData.id) {
          const updateData: any = {
            email: userData.email,
            role: userData.role,
            is_active: userData.is_active,
            is_staff: userData.is_staff
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
        
        this.closeModal()
        await this.fetchUsers()
      } catch (err: any) {
        throw new Error(err.response?.data?.detail || 'Failed to save user')
      }
    },
    
    confirmDelete(user: User) {
      if (confirm(`Are you sure you want to delete user ${user.email}?`)) {
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
        is_active: true,
        is_staff: false,
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