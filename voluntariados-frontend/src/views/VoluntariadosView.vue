<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import VoluntariadoCard from "@/components/landing/VoluntariadoCard.vue";
import CTASection from "@/components/landing/CTASection.vue";
import { voluntariadoAPI, organizacionAPI } from "@/services/api";
import { formatDateCustom } from "@/utils/dateUtils";

interface Voluntariado {
  id: number;
  nombre: string;
  descripcion?: any;
  estado: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  turno?: any;
  inscriptos_count?: number;
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
  etapa?: string;
  inscriptos?: number;
}

interface EtapaGroup {
  etapa: string;
  etapaLabel: string;
  etapaDescription: string;
  badgeClass: string;
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
      selectedDate: "",

      // Data from backend
      allVoluntariados: [] as Voluntariado[],
      organizaciones: [] as any[],

      // Voluntariados grouped by etapa
      voluntariadosByEtapa: [] as EtapaGroup[],

      // Carousel responsive settings
      itemsPerSlide: 3,
    };
  },

  computed: {
    filteredVoluntariadosByEtapa(): EtapaGroup[] {
      return this.voluntariadosByEtapa
        .map((etapaGroup) => ({
          ...etapaGroup,
          voluntariados: this.filterVoluntariados(etapaGroup.voluntariados),
        }))
        .filter((etapaGroup) => etapaGroup.voluntariados.length > 0);
    },
  },

  async mounted() {
    await this.loadData();
    this.updateItemsPerSlide();
    window.addEventListener("resize", this.updateItemsPerSlide);
  },

  beforeUnmount() {
    window.removeEventListener("resize", this.updateItemsPerSlide);
  },

  methods: {
    /**
     * Get the CSS class for the etapa icon based on stage
     */
    getEtapaIconClass(etapa: string): string {
      const classMap: Record<string, string> = {
        Convocatoria: "convocatoria",
        Preparación: "preparacion",
        Activo: "activo",
        Proximamente: "proximamente",
        Finalizado: "finalizado",
      };
      return classMap[etapa] || "proximamente";
    },

    /**
     * Get the icon for each etapa stage
     */
    getEtapaIcon(etapa: string): string {
      const iconMap: Record<string, string> = {
        Convocatoria: "bi bi-megaphone-fill",
        Preparación: "bi bi-hourglass-split",
        Activo: "bi bi-lightning-charge-fill",
        Proximamente: "bi bi-calendar-event",
        Finalizado: "bi bi-check-circle-fill",
      };
      return iconMap[etapa] || "bi bi-calendar-event";
    },

    /**
     * Get the badge icon for each etapa
     */
    getEtapaBadgeIcon(etapa: string): string {
      const iconMap: Record<string, string> = {
        Convocatoria: "bi bi-broadcast",
        Preparación: "bi bi-clock-history",
        Activo: "bi bi-play-circle-fill",
        Proximamente: "bi bi-hourglass",
        Finalizado: "bi bi-flag-fill",
      };
      return iconMap[etapa] || "bi bi-circle-fill";
    },

    /**
     * Get status text for each etapa badge
     */
    getEtapaStatusText(etapa: string): string {
      const statusMap: Record<string, string> = {
        Convocatoria: "Inscripciones Abiertas",
        Preparación: "En Organización",
        Activo: "En Curso",
        Proximamente: "Próximamente",
        Finalizado: "Completado",
      };
      return statusMap[etapa] || "Estado";
    },
    updateItemsPerSlide() {
      const width = window.innerWidth;
      if (width < 768) {
        this.itemsPerSlide = 1; // Mobile: 1 item
      } else if (width < 992) {
        this.itemsPerSlide = 2; // Tablet: 2 items
      } else {
        this.itemsPerSlide = 3; // Desktop: 3 items
      }
    },
    async loadData() {
      this.loading = true;
      this.error = null;

      try {
        // Load voluntariados and organizations
        const [voluntariadosRes, organizacionesRes] = await Promise.all([
          voluntariadoAPI.getAllValid(),
          organizacionAPI.getAll(),
        ]);

        this.allVoluntariados = voluntariadosRes.data;
        this.organizaciones = organizacionesRes.data;

        // Process voluntariados by etapa
        this.processVoluntariadosByEtapa();
      } catch (err: any) {
        console.error("Error loading voluntariados:", err);
        this.error = err.response?.data?.detail || "Error al cargar los voluntariados";
        this.setFallbackData();
      } finally {
        this.loading = false;
      }
    },

    processVoluntariadosByEtapa() {
      // Define etapa groups with proper colors matching VoluntariadoDetail
      const etapaGroups: EtapaGroup[] = [
        {
          etapa: "Convocatoria",
          etapaLabel: "Convocatoria",
          etapaDescription: "Período de postulación abierto para inscribirse al voluntariado",
          badgeClass: "bg-primary",
          voluntariados: [],
        },
        {
          etapa: "Preparación",
          etapaLabel: "Preparación",
          etapaDescription: "Convocatoria cerrada. Organizándose el cursado y actividades",
          badgeClass: "bg-warning text-dark",
          voluntariados: [],
        },
        {
          etapa: "Activo",
          etapaLabel: "Activo",
          etapaDescription: "El voluntariado está en curso y se realizan actividades",
          badgeClass: "bg-success",
          voluntariados: [],
        },
        {
          etapa: "Proximamente",
          etapaLabel: "Próximamente",
          etapaDescription: "Antes del inicio de la convocatoria",
          badgeClass: "bg-secondary",
          voluntariados: [],
        },
        {
          etapa: "Finalizado",
          etapaLabel: "Finalizado",
          etapaDescription: "El voluntariado ya finalizó",
          badgeClass: "bg-dark",
          voluntariados: [],
        },
      ];

      // Group voluntariados by etapa
      this.allVoluntariados.forEach((v) => {
        const voluntariadoDisplay = this.mapVoluntariadoToDisplay(v);
        const etapa = voluntariadoDisplay.etapa || "Proximamente";

        const group = etapaGroups.find((g) => g.etapa === etapa);
        if (group) {
          group.voluntariados.push(voluntariadoDisplay);
        }
      });

      // Only include groups with voluntariados
      this.voluntariadosByEtapa = etapaGroups.filter((g) => g.voluntariados.length > 0);
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

      // Extract etapa from the voluntariado data if available
      const etapa = (v as any).etapa || "Proximamente";

      // Determine image URL from nested descripcion (portada preferred, then logo)
      let imageUrl: string | undefined = undefined;
      if (v.descripcion && typeof v.descripcion === "object") {
        imageUrl = (v.descripcion.portada as string) || (v.descripcion.logo as string) || undefined;
      }

      return {
        id: v.id,
        title: v.nombre,
        description: this.getDescriptionText(v.descripcion) || "Sin descripción disponible",
        category: categories[v.id % categories.length],
        location: locations[v.id % locations.length],
        date: v.fecha_inicio ? this.formatDate(v.fecha_inicio) : undefined,
        imageUrl: imageUrl,
        etapa: etapa,
        inscriptos: (v as any).inscriptos_count ?? undefined,
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
      return formatDateCustom(dateString);
    },

    filterVoluntariados(voluntariados: VoluntariadoDisplay[]): VoluntariadoDisplay[] {
      return voluntariados.filter((v) => {
        const matchesSearch =
          !this.searchQuery ||
          v.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          v.description.toLowerCase().includes(this.searchQuery.toLowerCase());

        return matchesSearch;
      });
    },

    clearFilters() {
      this.searchQuery = "";
      this.selectedDate = "";
    },

    viewVoluntariado(id: number) {
      this.$router.push(`/voluntariados/${id}`);
    },

    chunkArray(array: any[], size: number): any[][] {
      const chunks: any[][] = [];
      for (let i = 0; i < array.length; i += size) {
        chunks.push(array.slice(i, i + size));
      }
      return chunks;
    },

    getCarouselSlides(voluntariados: VoluntariadoDisplay[]): VoluntariadoDisplay[][] {
      const slides: VoluntariadoDisplay[][] = [];
      // Generate slides that move one item at a time
      // Stop when we reach the last full set of items
      const maxSlides = voluntariados.length - this.itemsPerSlide + 1;
      for (let i = 0; i < maxSlides; i++) {
        const slide = voluntariados.slice(i, i + this.itemsPerSlide);
        slides.push(slide);
      }
      return slides;
    },

    setFallbackData() {
      this.voluntariadosByEtapa = [
        {
          etapa: "Convocatoria",
          etapaLabel: "Convocatoria",
          etapaDescription: "Período de postulación abierto para inscribirse al voluntariado",
          badgeClass: "bg-primary",
          voluntariados: [
            {
              id: 1,
              title: "Sed ut perspiciatis",
              description:
                "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
              category: "Educación",
              location: "Mendoza",
              date: "15 Nov 2025",
              etapa: "Convocatoria",
            },
            {
              id: 2,
              title: "Voluntariado de ejemplo",
              description: "Descripción de ejemplo",
              category: "Salud",
              location: "Mendoza",
              etapa: "Convocatoria",
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
  <section class="page-header shared-hero">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto text-center">
            <h1 class="page-title mb-3">Voluntariados Destacados</h1>
            <p class="page-subtitle">
              A continuación, encontrarás una selección de voluntariados destacados que ofrecen
              oportunidades únicas para contribuir y hacer una diferencia en la comunidad.
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

      <!-- Search and Filters -->
      <section class="filters-section py-2 bg-light">
        <div class="container">
          <div class="row g-2">
            <div class="col-12 col-md-6 col-lg-4">
              <div class="filter-group">
                <label for="searchInput" class="form-label visually-hidden">Buscar Voluntariados</label>
                <div class="input-group">
                  <span class="input-group-text" id="search-icon"
                    ><i class="bi bi-search"></i
                  ></span>
                  <input
                    type="text"
                    id="searchInput"
                    class="form-control"
                    placeholder="Buscar voluntariados..."
                    v-model="searchQuery"
                    aria-label="Buscar voluntariados"
                    aria-describedby="search-icon"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Voluntariados by Etapa with Carousels -->
      <section class="voluntariados-by-etapa py-5">
        <div class="container">
          <div v-if="filteredVoluntariadosByEtapa.length > 0">
            <div
              v-for="(etapaGroup, index) in filteredVoluntariadosByEtapa"
              :key="index"
              class="etapa-section mb-5"
            >
              <!-- Enhanced Etapa Header with Clear Structure -->
              <div class="etapa-header" :data-etapa="etapaGroup.etapa">
                <!-- Title Row with Icon, Title, Badge and Count -->
                <div class="etapa-title-row">
                  <!-- Stage Icon -->
                  <div class="etapa-icon" :class="getEtapaIconClass(etapaGroup.etapa)">
                    <i :class="getEtapaIcon(etapaGroup.etapa)"></i>
                  </div>

                  <!-- Title -->
                  <h3 class="etapa-title">
                    {{ etapaGroup.etapaLabel }}
                  </h3>

                  <!-- Badges Container -->
                  <div class="etapa-badge-container">
                    <!-- Status Badge -->
                    <span :class="['badge', etapaGroup.badgeClass]">
                      <i :class="getEtapaBadgeIcon(etapaGroup.etapa)"></i>
                      {{ getEtapaStatusText(etapaGroup.etapa) }}
                    </span>

                    <!-- Count Badge -->
                    <span class="etapa-count">
                      <i class="bi bi-list-check me-1"></i>
                      {{ etapaGroup.voluntariados.length }}
                      {{ etapaGroup.voluntariados.length === 1 ? "voluntariado" : "voluntariados" }}
                    </span>
                  </div>
                </div>

                <!-- Description Row with Icon -->
                <div class="etapa-description-row">
                  <div class="etapa-description-icon">
                    <i class="bi bi-info-circle-fill"></i>
                  </div>
                  <p class="etapa-description">
                    <strong>{{ etapaGroup.etapaLabel }}:</strong>
                    {{ etapaGroup.etapaDescription }}
                  </p>
                </div>
              </div>

              <!-- Carousel or Grid for this etapa -->
              <div
                v-if="etapaGroup.voluntariados.length <= itemsPerSlide"
                class="row g-4 justify-content-center"
              >
                <!-- Grid layout for few items -->
                <div
                  v-for="voluntariado in etapaGroup.voluntariados"
                  :key="voluntariado.id"
                  :class="[
                    'col-12',
                    itemsPerSlide >= 2 ? 'col-md-6' : '',
                    itemsPerSlide >= 3 ? 'col-lg-4' : '',
                  ]"
                >
                  <VoluntariadoCard
                    :title="voluntariado.title"
                    :description="voluntariado.description"
                    :category="voluntariado.category"
                    :location="voluntariado.location"
                    :date="voluntariado.date"
                    :image-url="voluntariado.imageUrl"
                    :inscriptos="voluntariado.inscriptos"
                    @view="viewVoluntariado(voluntariado.id)"
                  />
                </div>
              </div>

              <div v-else :id="`carousel-${index}`" class="carousel slide" data-bs-ride="false">
                <!-- Carousel for many items -->
                <div class="carousel-inner">
                  <div
                    v-for="(slide, slideIndex) in getCarouselSlides(etapaGroup.voluntariados)"
                    :key="slideIndex"
                    :class="['carousel-item', { active: slideIndex === 0 }]"
                  >
                    <div class="row g-4 justify-content-center">
                      <div
                        v-for="voluntariado in slide"
                        :key="voluntariado.id"
                        :class="[
                          'col-12',
                          itemsPerSlide >= 2 ? 'col-md-6' : '',
                          itemsPerSlide >= 3 ? 'col-lg-4' : '',
                        ]"
                      >
                        <VoluntariadoCard
                          :title="voluntariado.title"
                          :description="voluntariado.description"
                          :category="voluntariado.category"
                          :location="voluntariado.location"
                          :date="voluntariado.date"
                          :image-url="voluntariado.imageUrl"
                          :inscriptos="voluntariado.inscriptos"
                          @view="viewVoluntariado(voluntariado.id)"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Carousel Controls -->
                <button
                  class="carousel-control-prev"
                  type="button"
                  :data-bs-target="`#carousel-${index}`"
                  data-bs-slide="prev"
                >
                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Anterior</span>
                </button>
                <button
                  class="carousel-control-next"
                  type="button"
                  :data-bs-target="`#carousel-${index}`"
                  data-bs-slide="next"
                >
                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Siguiente</span>
                </button>

                <!-- Indicators -->
                <div class="carousel-indicators">
                  <button
                    v-for="(slide, indicatorIndex) in getCarouselSlides(etapaGroup.voluntariados)"
                    :key="indicatorIndex"
                    type="button"
                    :data-bs-target="`#carousel-${index}`"
                    :data-bs-slide-to="indicatorIndex"
                    :class="{ active: indicatorIndex === 0 }"
                    :aria-current="indicatorIndex === 0"
                    :aria-label="`Slide ${indicatorIndex + 1}`"
                  ></button>
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
        primary-link="/about#contact"
        primary-icon="bi-envelope me-2"
        secondary-text="Ver organizaciones"
        secondary-link="/organizaciones"
        secondary-icon="bi-building me-2"
      />
    </template>
  </div>
</template>

<!-- Local view styles + shared header CSS -->
<style scoped src="./../styles/voluntariadosView.css"></style>
<style src="./../styles/sharedHeaders.css"></style>