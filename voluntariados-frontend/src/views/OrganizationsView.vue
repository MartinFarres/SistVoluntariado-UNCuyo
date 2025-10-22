<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <div class="organizations-view">
    <AppNavBar />

    <!-- Hero Section -->
    <section class="organizations-hero">
      <div class="hero-overlay"></div>
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto text-center">
            <h1 class="hero-title mb-4">Organizaciones Aliadas</h1>
            <p class="hero-subtitle">
              Conocé las organizaciones con las que trabajamos para generar un impacto positivo en
              nuestra comunidad.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Search and Filters -->
    <section class="filters-section py-4 bg-light">
      <div class="container">
        <div class="row g-3">
          <div class="col-md-8 mx-auto">
            <div class="filter-group">
              <label class="filter-label">
                <i class="bi bi-search me-2"></i>Buscar Organización
              </label>
              <div class="input-group">
                <input
                  v-model="searchTerm"
                  @input="currentPage = 1"
                  type="search"
                  class="form-control"
                  placeholder="Buscar por nombre..."
                  aria-label="Buscar organizaciones"
                />
                <button
                  class="btn btn-outline-secondary"
                  type="button"
                  @click="searchTerm = ''"
                  v-if="searchTerm"
                >
                  <i class="bi bi-x-lg"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mt-4">
      <div class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
      </div>
    </div>

    <!-- Organizations Grid -->
    <section v-else class="organizations-section py-5">
      <div class="container">
        <div v-if="filteredOrgs.length === 0" class="text-center py-5">
          <i class="bi bi-search display-1 text-muted mb-3"></i>
          <h5 class="text-muted">No se encontraron organizaciones</h5>
          <p class="text-muted">Intenta con otro término de búsqueda</p>
        </div>

        <div v-else>
          <div class="row g-4 mb-4">
            <div v-for="org in pagedOrgs" :key="org.id" class="col-12 col-md-6 col-lg-4">
              <div class="organization-card" @click="viewOrganization(org.id)">
                <div class="card-header-org">
                  <div class="org-icon">
                    <i class="bi bi-building"></i>
                  </div>
                  <div class="org-header-content">
                    <h5 class="org-title">{{ org.nombre }}</h5>
                  </div>
                </div>
                <div class="card-body-org">
                  <p class="org-description">
                    {{ getDescriptionText(org.descripcion) }}
                  </p>
                  <div class="org-footer">
                    <small class="text-muted">ID: {{ org.id }}</small>
                    <button
                      class="btn btn-sm btn-outline-primary"
                      @click.stop="viewOrganization(org.id)"
                    >
                      Ver más
                      <i class="bi bi-arrow-right ms-1"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <nav v-if="totalPages > 1" aria-label="Navegación de organizaciones" class="mt-5">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button
                  class="page-link"
                  @click="changePage(currentPage - 1)"
                  aria-label="Anterior"
                  :disabled="currentPage === 1"
                >
                  <i class="bi bi-chevron-left"></i>
                </button>
              </li>
              <li
                v-for="p in totalPages"
                :key="p"
                class="page-item"
                :class="{ active: p === currentPage }"
              >
                <button class="page-link" @click="changePage(p)">{{ p }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button
                  class="page-link"
                  @click="changePage(currentPage + 1)"
                  aria-label="Siguiente"
                  :disabled="currentPage === totalPages"
                >
                  <i class="bi bi-chevron-right"></i>
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <CTASection
      title="¿Representás una organización?"
      subtitle="Contactanos para colaborar y ser parte de nuestra red de organizaciones aliadas"
      primary-text="Contactanos"
      primary-link="/contact"
      primary-icon="bi-envelope me-2"
      secondary-text="Ver Voluntariados"
      secondary-link="/voluntariados"
      secondary-icon="bi-search me-2"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import CTASection from "@/components/landing/CTASection.vue";
import { organizacionAPI } from "@/services/api";

export default defineComponent({
  name: "OrganizationsView",
  components: {
    AppNavBar,
    CTASection,
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      organizations: [] as any[],
      searchTerm: "",
      currentPage: 1,
      perPage: 9,
    };
  },
  computed: {
    filteredOrgs(): any[] {
      const q = (this.searchTerm || "").trim().toLowerCase();
      if (!q) return this.organizations;
      return this.organizations.filter((o: any) => (o.nombre || "").toLowerCase().includes(q));
    },
    totalPages(): number {
      return Math.max(1, Math.ceil(this.filteredOrgs.length / this.perPage));
    },
    pagedOrgs(): any[] {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredOrgs.slice(start, start + this.perPage);
    },
  },
  async created() {
    await this.loadOrganizations();
  },
  methods: {
    async loadOrganizations() {
      this.loading = true;
      this.error = null;
      try {
        const res = await organizacionAPI.getAll();
        this.organizations = res.data || [];
        this.organizations = this.organizations.map((o: any) => ({
          ...o,
          id: Number(o.id),
          nombre: o.nombre || o.name || "Sin nombre",
        }));
      } catch (err: any) {
        console.error("Error loading organizaciones:", err);
        this.error = err?.response?.data?.detail || "Error al cargar organizaciones";
      } finally {
        this.loading = false;
      }
    },
    changePage(page: number) {
      if (page < 1) page = 1;
      if (page > this.totalPages) page = this.totalPages;
      this.currentPage = page;
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    viewOrganization(id: number) {
      this.$router.push(`/organizaciones/${id}`);
    },
    getDescriptionText(descripcion: any): string {
      if (!descripcion)
        return "Conocé más sobre esta organización y descubrí cómo podés colaborar.";
      if (typeof descripcion === "string") {
        const text = descripcion.slice(0, 150);
        return text.length < descripcion.length ? text + "..." : text;
      }
      if (typeof descripcion === "object" && descripcion.descripcion) {
        const text = String(descripcion.descripcion).slice(0, 150);
        return text.length < String(descripcion.descripcion).length ? text + "..." : text;
      }
      if (typeof descripcion === "object" && descripcion.resumen) {
        const text = String(descripcion.resumen).slice(0, 150);
        return text.length < String(descripcion.resumen).length ? text + "..." : text;
      }
      return "Conocé más sobre esta organización y descubrí cómo podés colaborar.";
    },
  },
});
</script>
<style scoped src="./../styles/organizationsView.css"></style>
