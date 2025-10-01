<!-- src/views/admin/Users.vue -->
<template>
  <div class="admin-dashboard">
    <!-- Sidebar -->
    <AdminSidebar :isCollapsed="sidebarCollapsed" @toggle="toggleSidebar" />

    <!-- Main Content -->
    <div class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <!-- Top Navbar -->
      <nav class="navbar navbar-top navbar-expand navbar-dark bg-gradient-primary">
        <div class="container-fluid">
          <button class="btn btn-link text-white d-md-none" @click="toggleSidebar">
            <i class="bi bi-list fs-4"></i>
          </button>
          <div class="collapse navbar-collapse">
            <ul class="navbar-nav align-items-center ms-auto">
              <li class="nav-item">
                <a class="nav-link text-white" href="#">
                  <i class="bi bi-bell fs-5"></i>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link text-white" href="#">
                  <i class="bi bi-person"></i>
                  <span class="ms-2">Admin User</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <!-- Header -->
      <div class="header bg-gradient-primary pb-6 pt-5 pt-md-7">
        <div class="container-fluid">
          <div class="header-body">
            <div class="row align-items-center py-4">
              <div class="col-lg-6 col-7">
                <h6 class="h2 text-white d-inline-block mb-0">Users Management</h6>
                <nav aria-label="breadcrumb" class="d-none d-md-inline-block ml-md-4">
                  <ol class="breadcrumb breadcrumb-links breadcrumb-dark">
                    <li class="breadcrumb-item">
                      <router-link to="/admin/dashboard" class="text-white">
                        <i class="bi bi-house"></i>
                      </router-link>
                    </li>
                    <li class="breadcrumb-item active text-white" aria-current="page">Users</li>
                  </ol>
                </nav>
              </div>
              <div class="col-lg-6 col-5 text-end">
                <button class="btn btn-light" @click="showCreateModal = true">
                  <i class="bi bi-plus"></i> New User
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Page Content -->
      <div class="container-fluid mt--6">
        <div class="row">
          <div class="col">
            <div class="card shadow">
              <!-- Card header -->
              <div class="card-header border-0">
                <div class="row align-items-center">
                  <div class="col">
                    <h3 class="mb-0">All Users</h3>
                  </div>
                </div>
                
                <!-- Filters -->
                <div class="row mt-3">
                  <div class="col-md-3">
                    <div class="form-group mb-0">
                      <input 
                        type="text" 
                        class="form-control form-control-sm" 
                        placeholder="Search by email..."
                        v-model="searchQuery"
                        @input="filterUsers"
                      >
                    </div>
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
                </div>
              </div>

              <!-- Loading State -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger m-4">
                <i class="bi bi-exclamation-triangle"></i> {{ error }}
              </div>

              <!-- Users Table -->
              <div v-else class="table-responsive">
                <table class="table align-items-center table-flush">
                  <thead class="thead-light">
                    <tr>
                      <th>ID</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Status</th>
                      <th>Staff</th>
                      <th>Date Joined</th>
                      <th>Last Login</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="user in filteredUsers" :key="user.id">
                      <td>{{ user.id }}</td>
                      <td>
                        <div class="d-flex align-items-center">
                          <div class="avatar rounded-circle bg-primary text-white me-3">
                            <i class="bi bi-person"></i>
                          </div>
                          <span>{{ user.email }}</span>
                        </div>
                      </td>
                      <td>
                        <span 
                          class="badge" 
                          :class="getRoleBadgeClass(user.role)"
                        >
                          {{ getRoleDisplay(user.role) }}
                        </span>
                      </td>
                      <td>
                        <span 
                          class="badge" 
                          :class="user.is_active ? 'bg-success' : 'bg-secondary'"
                        >
                          {{ user.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                      <td>
                        <i 
                          class="bi" 
                          :class="user.is_staff ? 'bi-check-circle-fill text-success' : 'bi-x-circle text-muted'"
                        ></i>
                      </td>
                      <td>{{ formatDate(user.date_joined) }}</td>
                      <td>{{ user.last_login ? formatDate(user.last_login) : 'Never' }}</td>
                      <td>
                        <button 
                          class="btn btn-sm btn-outline-primary me-1" 
                          @click="editUser(user)"
                          title="Edit"
                        >
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button 
                          class="btn btn-sm btn-outline-danger" 
                          @click="confirmDelete(user)"
                          title="Delete"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                    <tr v-if="filteredUsers.length === 0">
                      <td colspan="8" class="text-center py-4 text-muted">
                        <i class="bi bi-inbox fs-3 d-block mb-2"></i>
                        No users found
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Pagination -->
              <div class="card-footer py-4">
                <nav>
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <small class="text-muted">
                        Showing {{ filteredUsers.length }} of {{ users.length }} users
                      </small>
                    </div>
                  </div>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <div 
      class="modal fade" 
      :class="{ show: showCreateModal || showEditModal, 'd-block': showCreateModal || showEditModal }" 
      tabindex="-1"
      v-if="showCreateModal || showEditModal"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ showEditModal ? 'Edit User' : 'Create New User' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveUser">
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input 
                  type="email" 
                  class="form-control" 
                  v-model="formData.email" 
                  required
                >
              </div>
              <div class="mb-3" v-if="!showEditModal">
                <label class="form-label">Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  v-model="formData.password" 
                  :required="!showEditModal"
                  minlength="8"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Role</label>
                <select class="form-control" v-model="formData.role" required>
                  <option value="VOL">Voluntario</option>
                  <option value="DELEG">Delegado</option>
                  <option value="ADMIN">Administrativo</option>
                </select>
              </div>
              <div class="mb-3 form-check">
                <input 
                  type="checkbox" 
                  class="form-check-input" 
                  id="isActive"
                  v-model="formData.is_active"
                >
                <label class="form-check-label" for="isActive">
                  Active
                </label>
              </div>
              <div class="mb-3 form-check">
                <input 
                  type="checkbox" 
                  class="form-check-input" 
                  id="isStaff"
                  v-model="formData.is_staff"
                >
                <label class="form-check-label" for="isStaff">
                  Staff Member
                </label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="saveUser">
              {{ showEditModal ? 'Update' : 'Create' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showCreateModal || showEditModal"></div>
  </div>
</template>

<script lang="ts">
import AdminSidebar from '@/components/admin/AdminSidebar.vue'
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

export default {
  name: 'AdminUsers',
  components: {
    AdminSidebar
  },
  data() {
    return {
      sidebarCollapsed: false,
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
      }
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    
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
      
      // Search by email
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(user => 
          user.email.toLowerCase().includes(query)
        )
      }
      
      // Filter by role
      if (this.roleFilter) {
        filtered = filtered.filter(user => user.role === this.roleFilter)
      }
      
      // Filter by status
      if (this.statusFilter === 'active') {
        filtered = filtered.filter(user => user.is_active)
      } else if (this.statusFilter === 'inactive') {
        filtered = filtered.filter(user => !user.is_active)
      }
      
      // Filter by staff
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
    
    async saveUser() {
      try {
        if (this.showEditModal && this.formData.id) {
          // Update existing user
          const updateData: any = {
            email: this.formData.email,
            role: this.formData.role,
            is_active: this.formData.is_active,
            is_staff: this.formData.is_staff
          }
          if (this.formData.password) {
            updateData.password = this.formData.password
          }
          await userAPI.updateUser(this.formData.id, updateData)
        } else {
          // Create new user
          await userAPI.createUser({
            email: this.formData.email,
            password: this.formData.password,
            role: this.formData.role,
            persona: this.formData.persona
          })
        }
        
        this.closeModal()
        await this.fetchUsers()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Failed to save user')
        console.error('Error saving user:', err)
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
}
</script>

<style scoped>
/* Same styles as Dashboard.vue */
.admin-dashboard {
  display: flex;
  min-height: 100vh;
  background-color: #f7fafc;
}

.main-content {
  flex: 1;
  margin-left: 250px;
  transition: margin-left 0.3s ease;
}

.main-content.sidebar-collapsed {
  margin-left: 80px;
}

.bg-gradient-primary {
  background: linear-gradient(87deg, #5e72e4 0, #825ee4 100%);
}

.header {
  position: relative;
}

.navbar-top {
  position: sticky;
  top: 0;
  z-index: 1000;
}

.card {
  border: 0;
  box-shadow: 0 0 2rem 0 rgba(136, 152, 170, 0.15);
}

.table thead th {
  padding: 0.75rem 1rem;
  text-transform: uppercase;
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 1px;
  border-bottom: 1px solid #e9ecef;
}

.avatar {
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}

.modal.show {
  background: rgba(0, 0, 0, 0.5);
}

.breadcrumb-dark .breadcrumb-item + .breadcrumb-item::before {
  color: rgba(255, 255, 255, 0.6);
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
}
</style>