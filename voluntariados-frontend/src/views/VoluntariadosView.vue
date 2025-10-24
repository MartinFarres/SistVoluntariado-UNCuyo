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
  etapa?: string;
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
      selectedLocation: "",
      selectedDate: "",

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
    window.addEventListener('resize', this.updateItemsPerSlide);
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.updateItemsPerSlide);
  },

  methods: {
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
          etapa: 'Convocatoria',
          etapaLabel: 'Convocatoria',
          etapaDescription: 'Período de postulación abierto para inscribirse al voluntariado',
          badgeClass: 'bg-primary',
          voluntariados: [],
        },
        {
          etapa: 'Preparación',
          etapaLabel: 'Preparación',
          etapaDescription: 'Convocatoria cerrada. Organizándose el cursado y actividades',
          badgeClass: 'bg-warning text-dark',
          voluntariados: [],
        },
        {
          etapa: 'Activo',
          etapaLabel: 'Activo',
          etapaDescription: 'El voluntariado está en curso y se realizan actividades',
          badgeClass: 'bg-success',
          voluntariados: [],
        },
        {
          etapa: 'Proximamente',
          etapaLabel: 'Próximamente',
          etapaDescription: 'Antes del inicio de la convocatoria',
          badgeClass: 'bg-secondary',
          voluntariados: [],
        },
        {
          etapa: 'Finalizado',
          etapaLabel: 'Finalizado',
          etapaDescription: 'El voluntariado ya finalizó',
          badgeClass: 'bg-dark',
          voluntariados: [],
        },
      ];

      // Group voluntariados by etapa
      this.allVoluntariados.forEach((v) => {
        const voluntariadoDisplay = this.mapVoluntariadoToDisplay(v);
        const etapa = voluntariadoDisplay.etapa || 'Proximamente';
        
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
      const etapa = (v as any).etapa || 'Proximamente';

      return {
        id: v.id,
        title: v.nombre,
        description: this.getDescriptionText(v.descripcion) || "Sin descripción disponible",
        category: categories[v.id % categories.length],
        location: locations[v.id % locations.length],
        date: v.fecha_inicio ? this.formatDate(v.fecha_inicio) : undefined,
        etapa: etapa,
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

        const matchesLocation =
          !this.selectedLocation ||
          this.selectedLocation === "Todas" ||
          v.location === this.selectedLocation;

        return matchesSearch && matchesLocation;
      });
    },

    clearFilters() {
      this.searchQuery = "";
      this.selectedLocation = "";
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
          etapa: 'Convocatoria',
          etapaLabel: 'Convocatoria',
          etapaDescription: 'Período de postulación abierto para inscribirse al voluntariado',
          badgeClass: 'bg-primary',
          voluntariados: [
            {
              id: 1,
              title: "Sed ut perspiciatis",
              description:
                "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
              category: "Educación",
              location: "Mendoza",
              date: "15 Nov 2025",
              etapa: 'Convocatoria',
            },
            {
              id: 2,
              title: "Voluntariado de ejemplo",
              description: "Descripción de ejemplo",
              category: "Salud",
              location: "Mendoza",
              etapa: 'Convocatoria',
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

            <div class="col-md-4">
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
          </div>
        </div>
      </section>

      <!-- Voluntariados by Etapa with Carousels -->
      <section class="voluntariados-by-etapa py-5">
        <div class="container">
          <h2 class="section-title mb-5 text-center">Voluntariados Disponibles</h2>

          <div v-if="filteredVoluntariadosByEtapa.length > 0">
            <div
              v-for="(etapaGroup, index) in filteredVoluntariadosByEtapa"
              :key="index"
              class="etapa-section mb-5"
            >
              <!-- Etapa Header -->
              <div class="etapa-header mb-4">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h3 class="etapa-title mb-2">
                      <span :class="['badge', etapaGroup.badgeClass, 'me-2']">
                        {{ etapaGroup.etapaLabel }}
                      </span>
                      <span class="etapa-count text-muted">
                        ({{ etapaGroup.voluntariados.length }} {{ etapaGroup.voluntariados.length === 1 ? 'voluntariado' : 'voluntariados' }})
                      </span>
                    </h3>
                    <p class="etapa-description text-muted mb-0">{{ etapaGroup.etapaDescription }}</p>
                  </div>
                  
                  <!-- Navigation hint for carousel -->
                  <div v-if="etapaGroup.voluntariados.length > itemsPerSlide" class="carousel-hint text-muted">
                    <i class="bi bi-arrow-left-circle me-1"></i>
                    <i class="bi bi-arrow-right-circle"></i>
                  </div>
                </div>
              </div>

              <!-- Carousel for this etapa (or grid if items fit in one view) -->
              <div v-if="etapaGroup.voluntariados.length <= itemsPerSlide" class="row g-4 justify-content-center">
                <div
                  v-for="voluntariado in etapaGroup.voluntariados"
                  :key="voluntariado.id"
                  :class="['col-12', itemsPerSlide >= 2 ? 'col-md-6' : '', itemsPerSlide >= 3 ? 'col-lg-4' : '']"
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

              <div v-else :id="`carousel-${index}`" class="carousel slide" data-bs-ride="false">
                <div class="carousel-inner">
                  <!-- Each slide moves one item at a time showing itemsPerSlide items -->
                  <div
                    v-for="(slide, slideIndex) in getCarouselSlides(etapaGroup.voluntariados)"
                    :key="slideIndex"
                    :class="['carousel-item', { active: slideIndex === 0 }]"
                  >
                    <div class="row g-4 justify-content-center">
                      <div
                        v-for="voluntariado in slide"
                        :key="voluntariado.id"
                        :class="['col-12', itemsPerSlide >= 2 ? 'col-md-6' : '', itemsPerSlide >= 3 ? 'col-lg-4' : '']"
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
