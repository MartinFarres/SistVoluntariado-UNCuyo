<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import VoluntariadoCard from "@/components/landing/VoluntariadoCard.vue";
import CTASection from "@/components/landing/CTASection.vue";
import { voluntariadoAPI, organizacionAPI } from "@/services/api";

interface Voluntariado {
  id: number;
  nombre: string;
  descripcion?: any;
  estado: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  turno?: any;
}

interface VoluntariadoDisplay {
  id: number;
  title: string;
  description: string;
  category: string;
  location: string;
  date?: string;
  imageUrl?: string;
  badge?: string;
  badgeClass?: string;
  featured?: boolean;
  organizationId?: number;
  organizationName?: string;
}

interface OrganizacionVoluntariados {
  organizationId: number;
  organizationName: string;
  organizationLogo: string;
  voluntariados: VoluntariadoDisplay[];
}

export default defineComponent({
  name: "VoluntariadosView",
  components: {
    AppNavBar,
    VoluntariadoCard,
    CTASection,
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      searchQuery: "",
      selectedCategory: "",
      selectedLocation: "",
      selectedDate: "",

      categories: [
        "Todas",
        "Educación",
        "Medio Ambiente",
        "Salud",
        "Cultura",
        "Deportes",
        "Tecnología",
        "Derechos Humanos",
        "Desarrollo Social",
      ],

      locations: [
        "Todas",
        "Mendoza",
        "Godoy Cruz",
        "Luján de Cuyo",
        "Las Heras",
        "Maipú",
        "Guaymallén",
      ],

      // Data from backend
      allVoluntariados: [] as Voluntariado[],
      organizaciones: [] as any[],

      // Featured voluntariados
      featuredVoluntariados: [] as VoluntariadoDisplay[],

      // Voluntariados grouped by organization
      voluntariadosByOrganization: [] as OrganizacionVoluntariados[],
    };
  },

  computed: {
    filteredFeaturedVoluntariados(): VoluntariadoDisplay[] {
      return this.filterVoluntariados(this.featuredVoluntariados);
    },

    filteredVoluntariadosByOrganization(): OrganizacionVoluntariados[] {
      return this.voluntariadosByOrganization
        .map((org) => ({
          ...org,
          voluntariados: this.filterVoluntariados(org.voluntariados),
        }))
        .filter((org) => org.voluntariados.length > 0);
    },
  },

  async mounted() {
    await this.loadData();
  },

  methods: {
    async loadData() {
      this.loading = true;
      this.error = null;

      try {
        // Load voluntariados and organizations
        const [voluntariadosRes, organizacionesRes] = await Promise.all([
          voluntariadoAPI.getAllUpcoming(),
          organizacionAPI.getAll(),
        ]);

        this.allVoluntariados = voluntariadosRes.data;
        this.organizaciones = organizacionesRes.data;

        // Process featured voluntariados (ACTIVE and DRAFT with more recent dates)
        this.processFeaturedVoluntariados();

        // Group voluntariados by organization
        this.processVoluntariadosByOrganization();
      } catch (err: any) {
        console.error("Error loading voluntariados:", err);
        this.error = err.response?.data?.detail || "Error al cargar los voluntariados";
        this.setFallbackData();
      } finally {
        this.loading = false;
      }
    },

    processFeaturedVoluntariados() {
      // Get ACTIVE voluntariados and sort by date
      const activeVoluntariados = this.allVoluntariados
        .filter((v) => v.estado === "ACTIVE")
        .sort((a, b) => {
          const dateA = a.fecha_inicio ? new Date(a.fecha_inicio).getTime() : 0;
          const dateB = b.fecha_inicio ? new Date(b.fecha_inicio).getTime() : 0;
          return dateB - dateA;
        })
        .slice(0, 3);

      const badges = ["Destacado", "Nuevo", "Popular"];
      const badgeClasses = ["bg-warning", "bg-success", "bg-primary"];

      this.featuredVoluntariados = activeVoluntariados.map((v, index) =>
        this.mapVoluntariadoToDisplay(v, {
          badge: badges[index],
          badgeClass: badgeClasses[index],
          featured: true,
        })
      );
    },

    processVoluntariadosByOrganization() {
      // Create a map of organization ID to voluntariados
      const orgMap = new Map<number, Voluntariado[]>();

      // Group voluntariados by organization (using voluntariado relationship)
      this.allVoluntariados.forEach((v) => {
        // In your model, Organizacion has a FK to Voluntariado
        // We need to find which organization this voluntariado belongs to
        const org = this.organizaciones.find((o) => o.voluntariado === v.id);
        if (org) {
          if (!orgMap.has(org.id)) {
            orgMap.set(org.id, []);
          }
          orgMap.get(org.id)!.push(v);
        }
      });

      // Convert map to array
      this.voluntariadosByOrganization = [];
      orgMap.forEach((voluntariados, orgId) => {
        const org = this.organizaciones.find((o) => o.id === orgId);
        if (org && voluntariados.length > 0) {
          this.voluntariadosByOrganization.push({
            organizationId: org.id,
            organizationName: org.nombre,
            organizationLogo: "https://via.placeholder.com/60",
            voluntariados: voluntariados.map((v) =>
              this.mapVoluntariadoToDisplay(v, {
                organizationId: org.id,
                organizationName: org.nombre,
              })
            ),
          });
        }
      });

      // If no organizations have voluntariados, show all voluntariados under "General"
      if (this.voluntariadosByOrganization.length === 0 && this.allVoluntariados.length > 0) {
        this.voluntariadosByOrganization.push({
          organizationId: 0,
          organizationName: "Voluntariados Disponibles",
          organizationLogo: "https://via.placeholder.com/60",
          voluntariados: this.allVoluntariados
            .filter((v) => !this.featuredVoluntariados.find((fv) => fv.id === v.id))
            .map((v) => this.mapVoluntariadoToDisplay(v)),
        });
      }
    },

    mapVoluntariadoToDisplay(v: Voluntariado, extra: any = {}): VoluntariadoDisplay {
      const categories = [
        "Educación",
        "Medio Ambiente",
        "Salud",
        "Cultura",
        "Deportes",
        "Tecnología",
      ];
      const locations = [
        "Mendoza",
        "Godoy Cruz",
        "Luján de Cuyo",
        "Las Heras",
        "Maipú",
        "Guaymallén",
      ];

      return {
        id: v.id,
        title: v.nombre,
        description: this.getDescriptionText(v.descripcion) || "Sin descripción disponible",
        category: categories[v.id % categories.length],
        location: locations[v.id % locations.length],
        date: v.fecha_inicio ? this.formatDate(v.fecha_inicio) : undefined,
        ...extra,
      };
    },

    getDescriptionText(descripcion: any): string {
      if (!descripcion) return "";
      if (typeof descripcion === "string") return descripcion;
      if (typeof descripcion === "object" && descripcion.descripcion) {
        return descripcion.descripcion;
      }
      if (typeof descripcion === "object" && descripcion.resumen) {
        return descripcion.resumen;
      }
      return "";
    },

    formatDate(dateString: string): string {
      const date = new Date(dateString);
      const months = [
        "Ene",
        "Feb",
        "Mar",
        "Abr",
        "May",
        "Jun",
        "Jul",
        "Ago",
        "Sep",
        "Oct",
        "Nov",
        "Dic",
      ];
      return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
    },

    filterVoluntariados(voluntariados: VoluntariadoDisplay[]): VoluntariadoDisplay[] {
      return voluntariados.filter((v) => {
        const matchesSearch =
          !this.searchQuery ||
          v.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          v.description.toLowerCase().includes(this.searchQuery.toLowerCase());

        const matchesCategory =
          !this.selectedCategory ||
          this.selectedCategory === "Todas" ||
          v.category === this.selectedCategory;

        const matchesLocation =
          !this.selectedLocation ||
          this.selectedLocation === "Todas" ||
          v.location === this.selectedLocation;

        return matchesSearch && matchesCategory && matchesLocation;
      });
    },

    clearFilters() {
      this.searchQuery = "";
      this.selectedCategory = "";
      this.selectedLocation = "";
      this.selectedDate = "";
    },

    viewVoluntariado(id: number) {
      this.$router.push(`/voluntariados/${id}`);
    },

    setFallbackData() {
      this.featuredVoluntariados = [
        {
          id: 1,
          title: "Sed ut perspiciatis",
          description:
            "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
          category: "Educación",
          location: "Mendoza",
          date: "15 Nov 2025",
          badge: "Destacado",
          badgeClass: "bg-warning",
          featured: true,
        },
      ];

      this.voluntariadosByOrganization = [
        {
          organizationId: 1,
          organizationName: "Organización de Ejemplo",
          organizationLogo: "https://via.placeholder.com/60",
          voluntariados: [
            {
              id: 2,
              title: "Voluntariado de ejemplo",
              description: "Descripción de ejemplo",
              category: "Salud",
              location: "Mendoza",
            },
          ],
        },
      ];
    },
  },
});
</script>

<template>
  <div class="voluntariados-page">
    <AppNavBar />

    <!-- Page Header -->
    <section class="page-header">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto text-center">
            <h1 class="page-title mb-3">Voluntariados Destacados</h1>
            <p class="page-subtitle">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
              incididunt ut labore et dolore magna aliqua
            </p>
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

    <!-- Error Alert -->
    <div v-else-if="error" class="container mt-4">
      <div class="alert alert-warning" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
      </div>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Filters Section -->
      <section class="filters-section py-4 bg-light">
        <div class="container">
          <div class="row g-3">
            <div class="col-md-4">
              <div class="filter-group">
                <label class="filter-label"> <i class="bi bi-search me-2"></i>Buscar </label>
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control"
                  placeholder="Buscar voluntariados..."
                />
              </div>
            </div>

            <div class="col-md-3">
              <div class="filter-group">
                <label class="filter-label"> <i class="bi bi-tag me-2"></i>Categoría </label>
                <select v-model="selectedCategory" class="form-select">
                  <option value="">Todas las categorías</option>
                  <option v-for="cat in categories.slice(1)" :key="cat" :value="cat">
                    {{ cat }}
                  </option>
                </select>
              </div>
            </div>

            <div class="col-md-3">
              <div class="filter-group">
                <label class="filter-label"> <i class="bi bi-geo-alt me-2"></i>Ubicación </label>
                <select v-model="selectedLocation" class="form-select">
                  <option value="">Todas las ubicaciones</option>
                  <option v-for="loc in locations.slice(1)" :key="loc" :value="loc">
                    {{ loc }}
                  </option>
                </select>
              </div>
            </div>

            <div class="col-md-2 d-flex align-items-end">
              <button @click="clearFilters" class="btn btn-outline-secondary w-100">
                <i class="bi bi-x-circle me-2"></i>Limpiar
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Featured Voluntariados -->
      <section class="featured-voluntariados py-5">
        <div class="container">
          <h2 class="section-title mb-4">Voluntariados Destacados</h2>

          <div v-if="filteredFeaturedVoluntariados.length > 0" class="row g-4">
            <div
              v-for="voluntariado in filteredFeaturedVoluntariados"
              :key="voluntariado.id"
              class="col-md-6 col-lg-4"
            >
              <VoluntariadoCard
                :title="voluntariado.title"
                :description="voluntariado.description"
                :category="voluntariado.category"
                :location="voluntariado.location"
                :date="voluntariado.date"
                :badge="voluntariado.badge"
                :badge-class="voluntariado.badgeClass"
                :image-url="voluntariado.imageUrl"
                @view="viewVoluntariado(voluntariado.id)"
              />
            </div>
          </div>

          <div v-else class="text-center py-5">
            <i class="bi bi-search display-1 text-muted mb-3"></i>
            <p class="text-muted">No se encontraron voluntariados con los filtros seleccionados</p>
          </div>
        </div>
      </section>

      <!-- Voluntariados by Organization -->
      <section class="voluntariados-by-org py-5 bg-light">
        <div class="container">
          <h2 class="section-title mb-4">Voluntariados por Organización</h2>

          <div v-if="filteredVoluntariadosByOrganization.length > 0">
            <div
              v-for="(org, index) in filteredVoluntariadosByOrganization"
              :key="index"
              class="organization-section mb-5"
            >
              <!-- Organization Header -->
              <div class="organization-header mb-4">
                <div class="org-logo">
                  <img :src="org.organizationLogo" :alt="org.organizationName" />
                </div>
                <h3 class="org-name">{{ org.organizationName }}</h3>
              </div>

              <!-- Organization's Voluntariados -->
              <div class="row g-4">
                <div
                  v-for="voluntariado in org.voluntariados"
                  :key="voluntariado.id"
                  class="col-md-6 col-lg-4"
                >
                  <VoluntariadoCard
                    :title="voluntariado.title"
                    :description="voluntariado.description"
                    :category="voluntariado.category"
                    :location="voluntariado.location"
                    :date="voluntariado.date"
                    :image-url="voluntariado.imageUrl"
                    @view="viewVoluntariado(voluntariado.id)"
                  />
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-5">
            <i class="bi bi-search display-1 text-muted mb-3"></i>
            <p class="text-muted">No se encontraron voluntariados con los filtros seleccionados</p>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <CTASection
        title="¿No encontrás lo que buscás?"
        subtitle="Contactános y te ayudaremos a encontrar el voluntariado perfecto para vos"
        primary-text="Contactar"
        primary-link="/contact"
        primary-icon="bi-envelope me-2"
        secondary-text="Ver organizaciones"
        secondary-link="/organizaciones"
        secondary-icon="bi-building me-2"
      />
    </template>
  </div>
</template>

<style scoped src="./../styles/voluntariadosView.css"></style>
