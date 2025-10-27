<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <div class="organizations-view">
    <AppNavBar />

    <!-- Hero Section -->
    <section class="page-header shared-hero">
      <div class="page-overlay"></div>
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
    <section class="filters-section py-2 bg-light">
      <div class="container">
        <div class="row g-2">
          <div class="col-12 col-md-6 col-lg-4">
            <div class="filter-group">
              <label for="searchInput" class="form-label visually-hidden"
                >Buscar Organizaciones</label
              >
              <div class="input-group">
                <span class="input-group-text" id="search-icon"><i class="bi bi-search"></i></span>
                <input
                  type="text"
                  id="searchInput"
                  class="form-control"
                  placeholder="Buscar organizaciones..."
                  v-model="searchTerm"
                  aria-label="Buscar organizaciones"
                  aria-describedby="search-icon"
                />
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
        <!-- Enhanced Section Header -->
        <div class="organizations-header">
          <!-- Title Row with Icon and Badge -->
          <div class="organizations-title-row">
            <!-- Icon -->
            <div class="organizations-icon">
              <i class="bi bi-buildings-fill"></i>
            </div>

            <!-- Title -->
            <h2 class="organizations-title">Organizaciones Colaboradoras</h2>

            <!-- Badge showing total count -->
            <span class="badge bg-primary organizations-badge">
              <i class="bi bi-building-check"></i>
              {{ filteredOrgs.length }}
              {{ filteredOrgs.length === 1 ? "organización" : "organizaciones" }}
            </span>
          </div>

          <!-- Description Row -->
          <div class="organizations-description-row">
            <div class="organizations-description-icon">
              <i class="bi bi-info-circle-fill"></i>
            </div>
            <p class="organizations-description">
              <strong>Nuestras Alianzas:</strong> Trabajamos con organizaciones comprometidas con el
              cambio social. Cada una ofrece oportunidades únicas para que puedas contribuir y hacer
              la diferencia en tu comunidad.
            </p>
          </div>
        </div>

        <!-- Organizations Grid or Empty State -->
        <div v-if="filteredOrgs.length === 0" class="text-center py-5">
          <i class="bi bi-search display-1 text-muted mb-3"></i>
          <h5 class="text-muted">No se encontraron organizaciones</h5>
          <p class="text-muted">Intenta con otro término de búsqueda</p>
        </div>

        <div v-else>
          <div class="row g-4 mb-4">
            <div
              v-for="org in pagedOrgs"
              :key="org.id"
              class="col-12 col-md-6 col-lg-4 d-flex align-items-stretch"
            >
              <div class="organization-card w-100" @click="viewOrganization(org.id)">
                <!-- Card Header with Gradient -->
                <div
                  class="card-header-org"
                  :style="
                    org.banner
                      ? {
                          backgroundImage: `url(${org.banner})`,
                          backgroundSize: 'cover',
                          backgroundPosition: 'center',
                        }
                      : {}
                  "
                >
                  <div class="org-icon">
                    <img
                      v-if="org.logo"
                      :src="org.logo"
                      alt="logo"
                      class="rounded-circle"
                      style="width: 48px; height: 48px; object-fit: cover"
                    />
                    <i v-else class="bi bi-building"></i>
                  </div>
                  <div class="org-header-content">
                    <h5 class="org-title">{{ org.nombre }}</h5>
                    <span
                      class="badge"
                      :class="
                        org.activo
                          ? 'bg-success-subtle text-success-emphasis'
                          : 'bg-secondary-subtle text-secondary-emphasis'
                      "
                    >
                      <i
                        class="bi me-1"
                        :class="org.activo ? 'bi-check-circle-fill' : 'bi-x-circle-fill'"
                      ></i>
                      {{ org.activo ? "Activa" : "Inactiva" }}
                    </span>
                  </div>
                </div>

                <!-- Card Body -->
                <div class="card-body-org">
                  <p class="org-description">
                    {{ getDescriptionText(org.descripcion) }}
                  </p>

                  <!-- Organization Details -->
                  <div class="org-details">
                    <div v-if="org.direccion" class="detail-item">
                      <i class="bi bi-geo-alt-fill"></i>
                      <small class="ms-2">{{ org.direccion }}</small>
                    </div>
                    <div v-if="org.localidad" class="detail-item">
                      <i class="bi bi-pin-map-fill"></i>
                      <small class="ms-2">{{ getLocalidadName(org.localidad) }}</small>
                    </div>
                    <div v-if="org.contacto_email" class="detail-item">
                      <i class="bi bi-envelope-fill"></i>
                      <small class="ms-2">{{ org.contacto_email }}</small>
                    </div>
                  </div>
                </div>

                <!-- Card Footer -->
                <div class="card-footer-org">
                  <small class="text-muted"></small>
                  <span class="view-more-indicator">
                    Ver más <i class="bi bi-arrow-right"></i>
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination (if needed) -->
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
      primary-link="/about#contact"
      primary-icon="bi-envelope me-2"
      secondary-text="Ver Voluntariados"
      secondary-link="/voluntariados"
      secondary-icon="bi-search me-2"
    />
  </div>
</template>

<!-- Include shared header styles so both pages share height and background -->
<style src="./../styles/sharedHeaders.css"></style>

<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import CTASection from "@/components/landing/CTASection.vue";
import { organizacionAPI, ubicacionAPI } from "@/services/api";

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
      localidades: [] as any[],
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
    await this.loadLocalidades();
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
    async loadLocalidades() {
      try {
        const res = await ubicacionAPI.getLocalidades();
        this.localidades = res.data || [];
      } catch (err) {
        console.error("Error loading localidades:", err);
      }
    },
    getLocalidadName(localidadId: number): string {
      if (!localidadId || !this.localidades.length) {
        return "Ubicación no especificada";
      }
      const localidad = this.localidades.find((l: any) => l.id === localidadId);
      return localidad ? localidad.nombre : `ID: ${localidadId}`;
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
      const fallback = "Conocé más sobre esta organización y descubrí cómo podés colaborar.";
      if (!descripcion) return fallback;

      let textToTruncate = "";
      if (typeof descripcion === "string") {
        textToTruncate = descripcion;
      } else if (
        typeof descripcion === "object" &&
        (descripcion.descripcion || descripcion.resumen)
      ) {
        textToTruncate = String(descripcion.descripcion || descripcion.resumen);
      }

      if (!textToTruncate) return fallback;

      const maxLength = 120;
      return textToTruncate.length > maxLength
        ? textToTruncate.slice(0, maxLength) + "..."
        : textToTruncate;
    },
  },
});
</script>
<style scoped src="./../styles/organizationsView.css"></style>
<style src="./../styles/sharedHeaders.css"></style>
