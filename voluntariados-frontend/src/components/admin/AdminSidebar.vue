<template>
  <div class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <div class="sidebar-header">
      <div class="sidebar-brand">
        <i class="bi bi-heart-fill text-danger"></i>
        <span v-if="!isCollapsed" class="brand-text">UniVolunteer</span>
      </div>
      <button class="btn btn-link text-white d-none d-md-block" @click="$emit('toggle')">
        <i class="bi" :class="isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
      </button>
    </div>

    <hr class="my-3 border-secondary">

    <nav class="sidebar-nav">
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link to="/admin/dashboard" class="nav-link">
            <i class="bi bi-speedometer2"></i>
            <span v-if="!isCollapsed">Dashboard</span>
          </router-link>
        </li>
        
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="collapse" href="#opportunitiesMenu" role="button">
            <i class="bi bi-briefcase"></i>
            <span v-if="!isCollapsed">Opportunities</span>
            <i v-if="!isCollapsed" class="bi bi-chevron-down ms-auto"></i>
          </a>
          <div class="collapse" id="opportunitiesMenu">
            <ul class="nav flex-column ms-3">
              <li class="nav-item">
                <router-link to="/admin/opportunities" class="nav-link">
                  <i class="bi bi-list"></i>
                  <span v-if="!isCollapsed">All Opportunities</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/opportunities/create" class="nav-link">
                  <i class="bi bi-plus-circle"></i>
                  <span v-if="!isCollapsed">Create New</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/categories" class="nav-link">
                  <i class="bi bi-tags"></i>
                  <span v-if="!isCollapsed">Categories</span>
                </router-link>
              </li>
            </ul>
          </div>
        </li>

        <li class="nav-item">
          <router-link to="/admin/applications" class="nav-link">
            <i class="bi bi-file-earmark-text"></i>
            <span v-if="!isCollapsed">Applications</span>
            <span v-if="!isCollapsed" class="badge bg-danger ms-auto">12</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/volunteers" class="nav-link">
            <i class="bi bi-people"></i>
            <span v-if="!isCollapsed">Volunteers</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/reports" class="nav-link">
            <i class="bi bi-bar-chart"></i>
            <span v-if="!isCollapsed">Reports</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/calendar" class="nav-link">
            <i class="bi bi-calendar-event"></i>
            <span v-if="!isCollapsed">Calendar</span>
          </router-link>
        </li>

        <li class="nav-item mt-4">
          <h6 v-if="!isCollapsed" class="nav-heading text-muted px-3">Settings</h6>
        </li>

        <li class="nav-item">
          <router-link to="/admin/settings" class="nav-link">
            <i class="bi bi-gear"></i>
            <span v-if="!isCollapsed">Settings</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/users" class="nav-link">
            <i class="bi bi-person-badge"></i>
            <span v-if="!isCollapsed">Admin Users</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/" class="nav-link">
        <i class="bi bi-box-arrow-left"></i>
        <span v-if="!isCollapsed">Back to Site</span>
      </router-link>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'AdminSidebar',
  props: {
    isCollapsed: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 250px;
  background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
  color: #fff;
  transition: width 0.3s ease;
  z-index: 1050;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  box-shadow: 0 0 2rem 0 rgba(136, 152, 170, 0.15);
}

.sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 1.5rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  font-size: 1.25rem;
  font-weight: 600;
  white-space: nowrap;
}

.sidebar-brand i {
  font-size: 1.5rem;
  margin-right: 0.5rem;
}

.brand-text {
  transition: opacity 0.3s ease;
}

.collapsed .brand-text {
  opacity: 0;
  width: 0;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 0 1rem;
}

.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.nav-heading {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 0.5rem 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  border-radius: 0.375rem;
  transition: all 0.15s ease;
  text-decoration: none;
  position: relative;
  white-space: nowrap;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  transform: translateX(3px);
}

.nav-link i:first-child {
  font-size: 1rem;
  width: 20px;
  margin-right: 0.75rem;
}

.nav-link.router-link-active {
  background-color: rgba(94, 114, 228, 0.2);
  color: #fff;
}

.nav-link.router-link-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background-color: #5e72e4;
  border-radius: 0 4px 4px 0;
}

.collapsed .nav-link span {
  opacity: 0;
  width: 0;
}

.badge {
  font-size: 0.65rem;
  padding: 0.25rem 0.5rem;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Collapse menu styling */
.collapse .nav-link {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar.show {
    transform: translateX(0);
  }
}
</style>