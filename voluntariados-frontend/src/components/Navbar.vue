<template>
  <nav
    class="navbar navbar-expand-lg"
    :class="{
      'navbar-scrolled': isScrolled,
      'navbar-dark': isScrolled,
      'navbar-light': !isScrolled,
    }"
  >
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">
        <img
          src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.ecured.cu%2Fimages%2Fa%2Faa%2FUncuyo.png&f=1&nofb=1&ipt=723a2b6d05dff391eb91592a367230330b4975456d4a195c31127eaaaa7618f7"
          alt="UNCuyo Logo"
          class="logo"
        />
        <span>UNCuyo Voluntariado</span>
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item">
            <router-link class="nav-link" to="/voluntariados">Voluntariados</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/organizaciones">Organizaciones</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about">Sobre Nosotros</router-link>
          </li>
          <li v-if="!isAdmin && !isDelegado && isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/area-personal">Área Personal</router-link>
          </li>
          <li v-if="isAdmin" class="nav-item">
            <router-link class="nav-link" to="/admin/dashboard">Panel de Admin</router-link>
          </li>
          <li v-if="isDelegado || isAdmin" class="nav-item">
            <router-link class="nav-link" to="/area-personal/gestionador"
              >Gestion de Voluntariados</router-link
            >
          </li>
          <li v-if="isAuthenticated" class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="bi bi-person-circle user-icon"></i>
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
              <li><router-link class="dropdown-item" to="/profile">Mi Perfil</router-link></li>
              <li><hr class="dropdown-divider" /></li>
              <li>
                <a class="dropdown-item" href="#" @click.prevent="handleLogout">Cerrar Sesión</a>
              </li>
            </ul>
          </li>
          <li v-else class="nav-item d-flex align-items-center auth-buttons">
            <router-link to="/signin" class="btn btn-outline-primary sign-in-btn"
              >Iniciar Sesión</router-link
            >
            <router-link to="/signup" class="btn btn-primary sign-up-btn">Registrarse</router-link>
          </li>
        </ul>
      </div>
    </div>
    <ConfirmationModal
      :show="showLogoutModal"
      title="Confirmar Cierre de Sesión"
      message="¿Estás seguro de que quieres cerrar sesión?"
      confirmText="Cerrar Sesión"
      @confirm="handleLogoutConfirm"
      @cancel="handleLogoutCancel"
    />
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "vue-router";
import authService from "@/services/authService";
import ConfirmationModal from "@/components/admin/ConfirmationModal.vue";

export default defineComponent({
  name: "AppNavBar",
  components: {
    ConfirmationModal,
  },
  data() {
    return {
      isScrolled: false,
      isAuthenticated: false,
      isAdmin: false,
      userRole: "",
      showLogoutModal: false,
    };
  },
  computed: {
    isDelegado(): boolean {
      return this.userRole === "DELEG";
    },
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 10;
    },
    updateAuthStatus() {
      this.isAuthenticated = authService.isAuthenticated();
      this.isAdmin = authService.isAdmin();
      if (this.isAuthenticated) {
        const user = authService.getStoredUser();
        if (user) {
          this.userRole = user.role;
        }
      } else {
        this.isAdmin = false;
        this.userRole = "";
      }
    },
    handleLogout() {
      this.showLogoutModal = true;
    },
    handleLogoutConfirm() {
      authService.logout();
      this.updateAuthStatus();
      this.showLogoutModal = false;
      this.router.push("/signin");
    },
    handleLogoutCancel() {
      this.showLogoutModal = false;
    },
  },
  created() {
    window.addEventListener("scroll", this.handleScroll);
    this.updateAuthStatus();
    // Listen for login/logout events to update navbar
    window.addEventListener("auth-change", this.updateAuthStatus);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
    window.removeEventListener("auth-change", this.updateAuthStatus);
  },
  watch: {
    $route() {
      this.updateAuthStatus();
    },
  },
  setup() {
    const router = useRouter();
    return { router };
  },
});
</script>

<style scoped src="./../styles/navBar.css"></style>
