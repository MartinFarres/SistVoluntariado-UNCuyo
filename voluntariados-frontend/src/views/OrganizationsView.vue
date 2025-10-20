<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <div class="organizations-view">
    <AppNavBar />

    <section class="hero py-5">
      <div class="container">
        <div class="text-center mb-4">
          <h1 class="mb-2">Organizaciones</h1>
          <p class="text-muted">Explorá las organizaciones y conectá con las que te interesen.</p>
        </div>

        <div class="row mb-4">
          <div class="col-md-8 mx-auto">
            <div class="input-group">
              <input
                v-model="searchTerm"
                @input="currentPage = 1"
                type="search"
                class="form-control"
                placeholder="Buscar organización por nombre..."
                aria-label="Buscar organizaciones"
              />
              <button class="btn btn-outline-secondary" @click="searchTerm = ''">Limpiar</button>
            </div>
          </div>
        </div>

        <div v-if="loading" class="d-flex justify-content-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
        </div>

        <div v-else-if="error" class="container">
          <div class="alert alert-warning">{{ error }}</div>
        </div>

        <div v-else>
          <div v-if="filteredOrgs.length === 0" class="text-center py-5 text-muted">
            No se encontraron organizaciones.
          </div>

          <div class="row g-4">
            <div v-for="org in pagedOrgs" :key="org.id" class="col-12 col-md-6 col-lg-4">
              <div
                class="org-card p-3 h-100"
                @click="viewOrganization(org.id)"
                style="cursor: pointer"
              >
                <div class="d-flex align-items-start gap-3">
                  <div
                    class="avatar bg-light rounded-3 d-flex align-items-center justify-content-center"
                  >
                    <i class="bi bi-building fs-3 text-secondary"></i>
                  </div>
                  <div class="flex-grow-1">
                    <h5 class="mb-1">{{ org.nombre }}</h5>
                    <p class="mb-2 text-muted small">
                      {{ getDescriptionText(org.descripcion) }}
                    </p>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-muted">ID {{ org.id }}</small>
                      <button
                        class="btn btn-sm btn-outline-primary"
                        @click.stop="viewOrganization(org.id)"
                      >
                        Ver
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Paginación simple -->
          <div class="d-flex justify-content-center mt-4" v-if="totalPages > 1">
            <nav aria-label="Page navigation">
              <ul class="pagination">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <button
                    class="page-link"
                    @click="changePage(currentPage - 1)"
                    aria-label="Anterior"
                  >
                    &laquo;
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
                  >
                    &raquo;
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </section>

    <CTASection
      title="¿Representás una organización?"
      primary-text="Contactanos"
      primary-link="/contact"
      secondary-text=""
      secondary-link=""
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
        // normalizar nombre de campo si hace falta
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
      if (!descripcion) return "Sin descripción";
      if (typeof descripcion === "string") return descripcion.slice(0, 120);
      if (typeof descripcion === "object" && descripcion.descripcion)
        return String(descripcion.descripcion).slice(0, 120);
      if (typeof descripcion === "object" && descripcion.resumen)
        return String(descripcion.resumen).slice(0, 120);
      return "Sin descripción";
    },
  },
});
</script>

<style scoped>
/* Estilos mínimos para la vista */
.org-card {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.org-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}
.avatar {
  width: 64px;
  height: 64px;
}
.hero {
  background: linear-gradient(135deg, #f8f9fa 0, #fff 100%);
}
</style>
