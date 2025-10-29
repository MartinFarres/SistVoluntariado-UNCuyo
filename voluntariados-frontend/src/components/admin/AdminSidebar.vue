<template>
  <div class="sidebar" :class="{ collapsed: isCollapsed, show: isSidebarVisible }">
    <nav class="sidebar-nav">
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link to="/admin/dashboard" class="nav-link">
            <i class="bi bi-speedometer2"></i>
            <span v-if="!isCollapsed">Dashboard</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/users" class="nav-link">
            <i class="bi bi-person-badge"></i>
            <span v-if="!isCollapsed">Usuarios</span>
          </router-link>
        </li>

        <a class="nav-link" @click="togglePersonasMenu" role="button">
          <i class="bi bi-briefcase"></i>
          <span v-if="!isCollapsed">Personas</span>
          <i
            v-if="!isCollapsed"
            class="bi bi-chevron-down ms-auto chevron"
            :class="{ rotated: personasMenuOpen }"
          ></i>
        </a>
        <transition @enter="expand" @after-enter="afterExpand" @leave="collapse">
          <div v-show="personasMenuOpen" class="submenu" data-menu="personas">
            <ul class="nav flex-column ms-3">
              <li class="nav-item">
                <router-link to="/admin/personas" class="nav-link">
                  <i class="bi bi-person"></i>
                  <span v-if="!isCollapsed">Todas las personas</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/delegados" class="nav-link">
                  <i class="bi bi-person-badge"></i>
                  <span v-if="!isCollapsed">Delegados</span>
                </router-link>
              </li>

              <li class="nav-item">
                <router-link to="/admin/voluntarios" class="nav-link">
                  <i class="bi bi-person-heart"></i>
                  <span v-if="!isCollapsed">Voluntarios</span>
                </router-link>
              </li>

              <li class="nav-item">
                <router-link to="/admin/administradores" class="nav-link">
                  <i class="bi bi-shield-check"></i>
                  <span v-if="!isCollapsed">Administradores</span>
                </router-link>
              </li>
            </ul>
          </div>
        </transition>

        <li class="nav-item">
          <router-link to="/admin/voluntariados" class="nav-link">
            <i class="bi bi-people"></i>
            <span v-if="!isCollapsed">Voluntariados</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/organizaciones" class="nav-link">
            <i class="bi bi-building"></i>
            <span v-if="!isCollapsed">Organizaciones</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/facultades" class="nav-link">
            <i class="bi bi-mortarboard"></i>
            <span v-if="!isCollapsed">Facultades</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/admin/carreras" class="nav-link">
            <i class="bi bi-eyeglasses"></i>
            <span v-if="!isCollapsed">Carreras</span>
          </router-link>
        </li>

        <a class="nav-link" @click="toggleUbicacionMenu" role="button">
          <i class="bi bi-briefcase"></i>
          <span v-if="!isCollapsed">Ubicación</span>
          <i
            v-if="!isCollapsed"
            class="bi bi-chevron-down ms-auto chevron"
            :class="{ rotated: ubicacionMenuOpen }"
          ></i>
        </a>
        <transition @enter="expand" @after-enter="afterExpand" @leave="collapse">
          <div v-show="ubicacionMenuOpen" class="submenu" data-menu="ubicacion">
            <ul class="nav flex-column ms-3">
              <li class="nav-item">
                <router-link to="/admin/paises" class="nav-link">
                  <i class="bi bi-globe"></i>
                  <span v-if="!isCollapsed">Paises</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/provincias" class="nav-link">
                  <i class="bi bi-map"></i>
                  <span v-if="!isCollapsed">Provincias</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/departamentos" class="nav-link">
                  <i class="bi bi-geo-alt"></i>
                  <span v-if="!isCollapsed">Departamentos</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/localidades" class="nav-link">
                  <i class="bi bi-pin-map"></i>
                  <span v-if="!isCollapsed">Localidades</span>
                </router-link>
              </li>
            </ul>
          </div>
        </transition>

        <li class="nav-item">
          <router-link to="/admin/landing-config" class="nav-link">
            <i class="bi bi-house-gear"></i>
            <span v-if="!isCollapsed">Configuración del Sitio</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/about-config" class="nav-link">
            <i class="bi bi-file-earmark-text"></i>
            <span v-if="!isCollapsed">Configuración - About</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/powerbi" class="nav-link">
            <i class="bi bi-bar-chart-line"></i>
            <span v-if="!isCollapsed">Power BI</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/admin/certificados" class="nav-link">
            <i class="bi bi-award"></i>
            <span v-if="!isCollapsed">Certificados</span>
          </router-link>
        </li>

      </ul>
    </nav>

    <div class="sidebar-footer">
      <button
        class="collapse-btn"
        @click="$emit('toggle')"
        :aria-expanded="!isCollapsed"
        aria-label="Contraer/Expandir"
        title="Contraer/Expandir"
      >
        <i class="bi" :class="isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
        <span v-if="!isCollapsed" class="collapse-label">colapsar</span>
      </button>

      <router-link to="/" class="nav-link">
        <i class="bi bi-box-arrow-left"></i>
        <span v-if="!isCollapsed">Volver al sitio</span>
      </router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { useLandingConfig } from "@/composables/useLandingConfig";

export default {
  name: "AdminSidebar",
  props: {
    isCollapsed: {
      type: Boolean,
      default: false,
    },
    isSidebarVisible: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      ubicacionMenuOpen: false,
      personasMenuOpen: false,
      suppressNextPersonasAnim: false,
      suppressNextUbicacionAnim: false,
      certificadosMenuOpen: false,
    };
  },
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig();
    return {
      landingConfig,
      fetchLandingConfig,
    };
  },
  mounted() {
    // Check if we're on a ubicacion route and open the menu
    this.checkUbicacionRoute();
    // Check personas route too
    this.checkPersonasRoute();
    // Fetch landing config (will use cached version if already loaded)
    this.fetchLandingConfig();
  },
  watch: {
    $route() {
      // Keep menu open when navigating within ubicacion routes
      this.checkUbicacionRoute();
      this.checkPersonasRoute();
    },
  },
  methods: {
    // Transition hooks for smooth height animation
    expand(el: Element, done: () => void) {
      const node = el as HTMLElement;
      // Check if we should suppress animation for route-driven open
      const menu = node.dataset.menu;
      if (
        (menu === "personas" && this.suppressNextPersonasAnim) ||
        (menu === "ubicacion" && this.suppressNextUbicacionAnim)
      ) {
        this.afterExpand(el);
        if (menu === "personas") this.suppressNextPersonasAnim = false;
        if (menu === "ubicacion") this.suppressNextUbicacionAnim = false;
        return done();
      }
      node.style.height = "0px";
      node.style.overflow = "hidden";
      const target = node.scrollHeight;
      requestAnimationFrame(() => {
        node.style.transition = "height 200ms ease";
        node.style.height = target + "px";
        const cleanup = () => {
          node.removeEventListener("transitionend", cleanup);
          done();
        };
        node.addEventListener("transitionend", cleanup);
      });
    },
    afterExpand(el: Element) {
      const node = el as HTMLElement;
      node.style.height = "auto";
      node.style.overflow = "visible";
      node.style.transition = "";
    },
    collapse(el: Element, done: () => void) {
      const node = el as HTMLElement;
      node.style.overflow = "hidden";
      const current = node.scrollHeight;
      node.style.height = current + "px";
      // Force a reflow so the starting height is applied before shrinking
      void node.offsetHeight;
      node.style.transition = "height 200ms ease";
      node.style.height = "0px";
      const cleanup = () => {
        node.removeEventListener("transitionend", cleanup);
        done();
      };
      node.addEventListener("transitionend", cleanup);
    },
    toggleUbicacionMenu() {
      this.ubicacionMenuOpen = !this.ubicacionMenuOpen;
    },
    toggleCertificadosMenu() {
      this.certificadosMenuOpen = !this.certificadosMenuOpen;
    },
    togglePersonasMenu() {
      this.personasMenuOpen = !this.personasMenuOpen;
    },
    checkUbicacionRoute() {
      const ubicacionRoutes = [
        "/admin/paises",
        "/admin/provincias",
        "/admin/departamentos",
        "/admin/localidades",
      ];
      if (ubicacionRoutes.includes(this.$route.path)) {
        // Open due to route without animation replay
        if (!this.ubicacionMenuOpen) {
          this.suppressNextUbicacionAnim = true;
          this.ubicacionMenuOpen = true;
        }
      }
    },
    checkPersonasRoute() {
      const personasRoutes = [
        "/admin/personas",
        "/admin/delegados",
        "/admin/voluntarios",
        "/admin/administradores",
      ];
      if (personasRoutes.includes(this.$route.path)) {
        // Open due to route without animation replay
        if (!this.personasMenuOpen) {
          this.suppressNextPersonasAnim = true;
          this.personasMenuOpen = true;
        }
      }
    },
  },
};
</script>

<style scoped>
/* Match HomeView palette: text #2c3e50, accents var(--brand-start) -> var(--brand-end) */
.sidebar {
  position: fixed;
  top: var(--topbar-height, 0px);
  left: 0;
  height: calc(100vh - var(--topbar-height, 0px));
  width: 240px;
  background: #ffffff;
  color: #2c3e50;
  transition: width 0.3s ease, transform 0.3s ease;
  z-index: 1010; /* below modal(1055) and topbar(1020), above content */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* prevent page scroll from affecting sidebar */
  box-shadow: 0 0 2rem 0 rgba(44, 62, 80, 0.12);
}

.sidebar.collapsed {
  width: 80px;
}

/* Sidebar header with centered button */
.sidebar-header {
  padding: 0.75rem 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.15s ease;
}

.sidebar-header:hover {
  background-color: rgba(44, 62, 80, 0.06);
}

/* Collapse button: pill with text when expanded, compact circle when collapsed */
.collapse-btn {
  background: #f7fafc;
  border: none;
  color: #2c3e50;
  height: 36px; /* smaller height to fit thinner sidebar */
  width: auto;
  padding: 0 8px; /* tighter pill */
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 0.9rem; /* slightly smaller label */
  box-shadow: 0 1px 4px rgba(44, 62, 80, 0.07);
  transition: background 0.15s, box-shadow 0.15s;
  cursor: pointer;
}
.collapse-btn i {
  font-size: 1rem; /* smaller icon */
}
.collapse-label {
  font-weight: 500;
}
.collapsed .sidebar-footer .collapse-btn {
  width: 36px; /* match compact height */
  padding: 0;
  border-radius: 50%;
}
.collapse-btn:focus {
  outline: 2px solid var(--brand-end);
}
.collapse-btn:hover {
  background: #e9ecef;
  color: var(--brand-end);
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.12);
}
.collapse-btn:active {
  background: #f1f3f4;
  color: var(--brand-accent);
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto; /* scroll only the nav when needed */
  padding: 0.75rem; /* slightly tighter padding all around */
}

.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(95, 158, 160, 0.2); /* subtle brand tint */
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
  padding: 0.5rem 0.75rem; /* tighter */
  font-size: 0.95rem; /* slightly smaller text */
  color: rgba(44, 62, 80, 0.85);
  border-radius: 0.375rem;
  transition: all 0.15s ease;
  text-decoration: none;
  position: relative;
  white-space: nowrap;
}

.nav-link:hover {
  background-color: rgba(135, 206, 235, 0.08);
  color: var(--brand-accent);
  transform: translateX(2px);
}

.nav-link i:first-child {
  font-size: 0.95rem; /* smaller icon */
  width: 18px;
  margin-right: 0.5rem;
}

.nav-link.router-link-active {
  background-color: rgba(135, 206, 235, 0.12);
  color: var(--brand-accent);
}

.nav-link.router-link-active::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background: linear-gradient(180deg, var(--brand-start), var(--brand-end));
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
  padding: 0.75rem; /* slimmer footer */
  border-top: 1px solid rgba(44, 62, 80, 0.08);
}

/* Collapse menu styling */
.collapse .nav-link,
.submenu .nav-link {
  padding: 0.4rem 0.75rem; /* tighter submenu */
  font-size: 0.85rem;
}

/* Submenu container defaults for transition */
.submenu {
  overflow: hidden;
}

/* Chevron rotation animation */
.chevron {
  transition: transform 200ms ease;
}
.chevron.rotated {
  transform: rotate(180deg);
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
