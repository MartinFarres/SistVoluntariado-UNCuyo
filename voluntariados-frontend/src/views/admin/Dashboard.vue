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
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <form class="navbar-search navbar-search-light form-inline me-auto d-none d-md-flex">
              <div class="form-group mb-0">
                <div class="input-group input-group-alternative">
                  <div class="input-group-prepend">
                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                  </div>
                  <input class="form-control" placeholder="Search" type="text">
                </div>
              </div>
            </form>
            <ul class="navbar-nav align-items-center ms-auto">
              <li class="nav-item dropdown">
                <a class="nav-link" href="#" role="button" data-bs-toggle="dropdown">
                  <i class="bi bi-bell text-white fs-5"></i>
                  <span class="badge badge-pill bg-danger">3</span>
                </a>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link pe-0" href="#" role="button" data-bs-toggle="dropdown">
                  <div class="media align-items-center">
                    <span class="avatar avatar-sm rounded-circle bg-white text-primary">
                      <i class="bi bi-person"></i>
                    </span>
                    <div class="media-body ms-2 d-none d-lg-block">
                      <span class="mb-0 text-sm text-white fw-bold">Admin User</span>
                    </div>
                  </div>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <!-- Header with Stats -->
      <div class="header bg-gradient-primary pb-6 pt-5 pt-md-7">
        <div class="container-fluid">
          <div class="header-body">
            <div class="row">
              <div class="col-xl-3 col-lg-6">
                <StatsCard
                  title="Total Opportunities"
                  value="45"
                  icon="bi-briefcase"
                  iconColor="bg-danger"
                  percentage="+12%"
                  percentageColor="text-success"
                  description="Since last month"
                />
              </div>
              <div class="col-xl-3 col-lg-6">
                <StatsCard
                  title="Active Volunteers"
                  value="238"
                  icon="bi-people"
                  iconColor="bg-warning"
                  percentage="+8%"
                  percentageColor="text-success"
                  description="Since last week"
                />
              </div>
              <div class="col-xl-3 col-lg-6">
                <StatsCard
                  title="Applications"
                  value="124"
                  icon="bi-file-earmark-text"
                  iconColor="bg-info"
                  percentage="+3%"
                  percentageColor="text-success"
                  description="Since yesterday"
                />
              </div>
              <div class="col-xl-3 col-lg-6">
                <StatsCard
                  title="Hours Logged"
                  value="1,843"
                  icon="bi-clock"
                  iconColor="bg-success"
                  percentage="+15%"
                  percentageColor="text-success"
                  description="Since last month"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Page Content -->
      <div class="container-fluid mt--6">
        <div class="row">
          <!-- Recent Opportunities Table -->
          <div class="col-xl-8">
            <div class="card shadow">
              <div class="card-header border-0">
                <div class="row align-items-center">
                  <div class="col">
                    <h3 class="mb-0">Recent Opportunities</h3>
                  </div>
                  <div class="col text-end">
                    <button class="btn btn-sm btn-primary">
                      <i class="bi bi-plus"></i> Add New
                    </button>
                  </div>
                </div>
              </div>
              <div class="table-responsive">
                <table class="table align-items-center table-flush">
                  <thead class="thead-light">
                    <tr>
                      <th>Title</th>
                      <th>Category</th>
                      <th>Applications</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>After-School Tutoring</td>
                      <td>
                        <span class="badge bg-primary">Education</span>
                      </td>
                      <td>23</td>
                      <td>
                        <span class="badge bg-success">Active</span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary me-1">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                    <tr>
                      <td>Campus Sustainability</td>
                      <td>
                        <span class="badge bg-success">Environment</span>
                      </td>
                      <td>18</td>
                      <td>
                        <span class="badge bg-success">Active</span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary me-1">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                    <tr>
                      <td>Food Bank Coordinator</td>
                      <td>
                        <span class="badge bg-info">Community</span>
                      </td>
                      <td>31</td>
                      <td>
                        <span class="badge bg-warning">Pending</span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary me-1">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Quick Actions & Activity -->
          <div class="col-xl-4">
            <!-- Quick Actions Card -->
            <div class="card shadow mb-4">
              <div class="card-header border-0">
                <h3 class="mb-0">Quick Actions</h3>
              </div>
              <div class="card-body">
                <div class="list-group list-group-flush">
                  <a href="#" class="list-group-item list-group-item-action">
                    <div class="d-flex align-items-center">
                      <div class="icon icon-shape bg-gradient-primary text-white rounded-circle me-3">
                        <i class="bi bi-plus"></i>
                      </div>
                      <div>
                        <h4 class="mb-0">Create Opportunity</h4>
                        <small class="text-muted">Add new volunteering position</small>
                      </div>
                    </div>
                  </a>
                  <a href="#" class="list-group-item list-group-item-action">
                    <div class="d-flex align-items-center">
                      <div class="icon icon-shape bg-gradient-info text-white rounded-circle me-3">
                        <i class="bi bi-people"></i>
                      </div>
                      <div>
                        <h4 class="mb-0">Manage Volunteers</h4>
                        <small class="text-muted">View and manage users</small>
                      </div>
                    </div>
                  </a>
                  <a href="#" class="list-group-item list-group-item-action">
                    <div class="d-flex align-items-center">
                      <div class="icon icon-shape bg-gradient-success text-white rounded-circle me-3">
                        <i class="bi bi-file-earmark-check"></i>
                      </div>
                      <div>
                        <h4 class="mb-0">Review Applications</h4>
                        <small class="text-muted">Pending: 12 applications</small>
                      </div>
                    </div>
                  </a>
                </div>
              </div>
            </div>

            <!-- Recent Activity Card -->
            <div class="card shadow">
              <div class="card-header border-0">
                <h3 class="mb-0">Recent Activity</h3>
              </div>
              <div class="card-body p-0">
                <div class="list-group list-group-flush">
                  <div class="list-group-item">
                    <div class="d-flex align-items-center">
                      <div class="avatar-sm bg-primary text-white rounded-circle me-3 d-flex align-items-center justify-content-center">
                        <i class="bi bi-person-plus"></i>
                      </div>
                      <div class="flex-grow-1">
                        <h5 class="mb-0">New volunteer registered</h5>
                        <small class="text-muted">2 hours ago</small>
                      </div>
                    </div>
                  </div>
                  <div class="list-group-item">
                    <div class="d-flex align-items-center">
                      <div class="avatar-sm bg-success text-white rounded-circle me-3 d-flex align-items-center justify-content-center">
                        <i class="bi bi-check-circle"></i>
                      </div>
                      <div class="flex-grow-1">
                        <h5 class="mb-0">Application approved</h5>
                        <small class="text-muted">5 hours ago</small>
                      </div>
                    </div>
                  </div>
                  <div class="list-group-item">
                    <div class="d-flex align-items-center">
                      <div class="avatar-sm bg-warning text-white rounded-circle me-3 d-flex align-items-center justify-content-center">
                        <i class="bi bi-star"></i>
                      </div>
                      <div class="flex-grow-1">
                        <h5 class="mb-0">New review posted</h5>
                        <small class="text-muted">1 day ago</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import AdminSidebar from '@/components/admin/AdminSidebar.vue'
import StatsCard from '@/components/admin/StatsCard.vue'

export default {
  name: 'AdminDashboard',
  components: {
    AdminSidebar,
    StatsCard
  },
  data() {
    return {
      sidebarCollapsed: false
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    }
  }
}
</script>

<style scoped>
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

/* Header Gradient */
.bg-gradient-primary {
  background: linear-gradient(87deg, #5e72e4 0, #825ee4 100%);
}

.header {
  position: relative;
}

/* Navbar */
.navbar-top {
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-search .form-control {
  background-color: rgba(255, 255, 255, 0.1);
  border: 0;
  color: #fff;
}

.navbar-search .form-control::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.navbar-search .input-group-text {
  background-color: rgba(255, 255, 255, 0.1);
  border: 0;
  color: rgba(255, 255, 255, 0.7);
}

/* Avatar */
.avatar {
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.avatar-sm {
  width: 36px;
  height: 36px;
}

/* Icons */
.icon-shape {
  width: 48px;
  height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.bg-gradient-info {
  background: linear-gradient(87deg, #11cdef 0, #1171ef 100%);
}

.bg-gradient-success {
  background: linear-gradient(87deg, #2dce89 0, #2dcecc 100%);
}

/* Cards */
.card {
  border: 0;
}

.card-header {
  background-color: transparent;
}

/* Table */
.table thead th {
  padding: 0.75rem 1rem;
  text-transform: uppercase;
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 1px;
  border-bottom: 1px solid #e9ecef;
}

.table-flush tbody tr:first-child td {
  border-top: 0;
}

/* List Group */
.list-group-item {
  border-left: 0;
  border-right: 0;
}

.list-group-item:first-child {
  border-top: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
}
</style>