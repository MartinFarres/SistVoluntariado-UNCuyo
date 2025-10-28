<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import VoluntariadoCard from "@/components/landing/VoluntariadoCard.vue";
import CTASection from "@/components/landing/CTASection.vue";
import { organizacionAPI, voluntariadoAPI } from "@/services/api";
import authService from "@/services/authService";

interface Organizacion {
  id: number;
  nombre: string;
  descripcion?: string;
  contacto_email?: string;
  localidad?: number;
  localidad_data?: any;
  voluntariado?: number;
  activo?: boolean;
  logo?: string | null;
  banner?: string | null;
}

interface Voluntariado {
  id: number;
  nombre: string;
  descripcion?: any;
  estado: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  requiere_convocatoria?: boolean;
  etapa?: string;
}

interface ProximoVoluntariado {
  id: number;
  title: string;
  description: string;
  date?: string;
  imageUrl?: string;
  canJoin?: boolean;
  latitud?: number | null;
  longitud?: number | null;
}

export default defineComponent({
  name: "OrganizationDetail",
  components: {
    AppNavBar,
    VoluntariadoCard,
    CTASection,
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      organizationId: 0,

      // Organization view model (initially empty; populated from backend)
      organization: {
        name: "",
        slogan: "",
        logo: null as string | null,
        banner: null as string | null,
        description: "",
        tags: [] as string[],
        contact: {
          email: "",
          phone: "",
          website: "",
        },
        stats: [] as { label: string; value: string }[],
      },

      proximosVoluntariados: [] as ProximoVoluntariado[],
      convocatoriaVoluntariados: [] as ProximoVoluntariado[],
      activosVoluntariados: [] as ProximoVoluntariado[],
      finalizadosVoluntariados: [] as ProximoVoluntariado[],
    };
  },

  computed: {
    isVoluntarioUser(): boolean {
      return authService.hasRole("VOL");
    },
  },

  async created() {
    this.organizationId = parseInt(this.$route.params.id as string);
    await this.loadOrganization();
  },

  methods: {
    async loadOrganization() {
      this.loading = true;
      this.error = null;

      try {
        // Load organization details
        const orgRes = await organizacionAPI.getById(this.organizationId);
        const orgData: Organizacion = orgRes.data;

        // Populate organization view model from backend data
        this.organization.name = orgData.nombre || "";
        this.organization.description = orgData.descripcion || "";
        this.organization.logo = orgData.logo || null;
        this.organization.banner = orgData.banner || null;
        this.organization.contact.email = orgData.contacto_email || "";
        this.organization.slogan = (orgData as any).slogan || "";
        this.organization.contact.website = (orgData as any).url || "";

        // Generate tags based on organization data
        this.organization.tags = this.generateTags(orgData);

        // If localidad_data present, append location info to website/contact as appropriate
        if (orgData.localidad_data) {
          this.organization.contact.website = this.organization.contact.website
            ? this.organization.contact.website
            : `${orgData.localidad_data.nombre}, ${orgData.localidad_data.provincia || ""}`;
        }

        // Load voluntariados that belong to this organization using the dedicated endpoint
        // Fetch convocatoria, upcoming, active and finished in parallel and map each to the UI model.
        try {
          const results = await Promise.allSettled([
            voluntariadoAPI.getByOrganization(this.organizationId, "convocatoria"),
            voluntariadoAPI.getByOrganization(this.organizationId, "upcoming"),
            voluntariadoAPI.getByOrganization(this.organizationId, "active"),
            voluntariadoAPI.getByOrganization(this.organizationId, "finished"),
          ]);

          const extractList = (resp: any): Voluntariado[] => {
            if (!resp) return [];
            const d = resp.data;
            if (Array.isArray(d)) return d;
            if (d && Array.isArray(d.results)) return d.results;
            // Some endpoints may return an object with keys -> try to be defensive
            return [];
          };

          // convocatoria
          if (results[0].status === "fulfilled") {
            const convList = extractList((results[0] as any).value);
            this.convocatoriaVoluntariados = convList.map((v) => this.mapVoluntariadoToDisplay(v));
          } else {
            this.convocatoriaVoluntariados = [];
            console.warn("convocatoria fetch failed:", (results[0] as any).reason || results[0]);
          }

          // upcoming
          if (results[1].status === "fulfilled") {
            const upList = extractList((results[1] as any).value);
            this.proximosVoluntariados = upList.map((v) => this.mapVoluntariadoToDisplay(v));
          } else {
            this.proximosVoluntariados = [];
            console.warn("upcoming fetch failed:", (results[1] as any).reason || results[1]);
          }

          // active
          if (results[2].status === "fulfilled") {
            const actList = extractList((results[2] as any).value);
            this.activosVoluntariados = actList.map((v) => this.mapVoluntariadoToDisplay(v));
          } else {
            this.activosVoluntariados = [];
            console.warn("active fetch failed:", (results[2] as any).reason || results[2]);
          }

          // finished
          if (results[3].status === "fulfilled") {
            const finList = extractList((results[3] as any).value);
            this.finalizadosVoluntariados = finList.map((v) => this.mapVoluntariadoToDisplay(v));
          } else {
            this.finalizadosVoluntariados = [];
            console.warn("finished fetch failed:", (results[3] as any).reason || results[3]);
          }
        } catch (volErr) {
          console.warn("Error loading organization voluntariados via dedicated endpoint:", volErr);
          this.convocatoriaVoluntariados = [];
          this.proximosVoluntariados = [];
          this.activosVoluntariados = [];
          this.finalizadosVoluntariados = [];
        }

        // If no voluntariados found, leave the list empty (no hardcoded samples)
        // this.proximosVoluntariados remains as the mapped array (possibly empty)
      } catch (err: any) {
        console.error("Error loading organization:", err);
        this.error = err.response?.data?.detail || "Error al cargar la organización";
        this.setFallbackData();
      } finally {
        this.loading = false;
      }
    },

    mapVoluntariadoToDisplay(v: Voluntariado): ProximoVoluntariado {
      // Determine etapa from the voluntariado data
      const etapa = (v as any).etapa || "Proximamente";

      // Determine if user can join this voluntariado
      // User can join if:
      // 1. User is a volunteer (VOL role)
      // 2. AND one of the following:
      //    - Voluntariado is in "Convocatoria" stage
      //    - Voluntariado is in "Activo" stage AND doesn't require convocatoria
      const canJoin =
        this.isVoluntarioUser &&
        (etapa === "Convocatoria" || (etapa === "Activo" && v.requiere_convocatoria === false));

      // Prefer resumen for card description
      let resumen = "";
      if (v.descripcion && typeof v.descripcion === "object" && v.descripcion.resumen) {
        resumen = v.descripcion.resumen;
      } else if (v.descripcion && typeof v.descripcion === "object" && v.descripcion.descripcion) {
        resumen = v.descripcion.descripcion;
      } else if (typeof v.descripcion === "string") {
        resumen = v.descripcion;
      }
      return {
        id: v.id,
        title: v.nombre,
        description: resumen || "Sin descripción disponible",
        latitud: (v as any).latitud ?? null,
        longitud: (v as any).longitud ?? null,
        date: v.fecha_inicio ? this.formatDate(v.fecha_inicio) : undefined,
        // Image is stored in the nested descripcion object (portada preferred, then logo)
        imageUrl:
          v.descripcion && typeof v.descripcion === "object"
            ? (v.descripcion.portada as string) || (v.descripcion.logo as string) || undefined
            : undefined,
        canJoin: canJoin,
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

    generateTags(org: Organizacion): string[] {
      const tags = ["Organización"];

      if (org.activo) tags.push("Activa");
      if (org.voluntariado) tags.push("Con Voluntariado");
      if (org.contacto_email) tags.push("Contacto Email");
      if (org.localidad) tags.push("Con Ubicación");

      return tags.slice(0, 5);
    },

    // No hardcoded sample voluntariados: data comes from the backend

    viewVoluntariado(id: number) {
      this.$router.push(`/voluntariados/${id}`);
    },

    contactOrganization() {
      if (this.organization.contact.email && this.organization.contact.email !== "No disponible") {
        window.location.href = `mailto:${this.organization.contact.email}`;
      } else {
        alert("No hay información de contacto disponible");
      }
    },

    callPhone(phone?: string) {
      if (!phone) return;
      window.location.href = `tel:${phone}`;
    },

    followOrganization() {
      // TODO: Implement follow logic with backend
      alert("Funcionalidad de seguir organización próximamente");
    },

    setFallbackData() {
      // Clear organization view model and voluntariados when loading fails
      this.organization = {
        name: "",
        slogan: "",
        logo: null,
        banner: null,
        description: "",
        tags: [],
        contact: { email: "", phone: "", website: "" },
        stats: [],
      };

      this.proximosVoluntariados = [];
      this.convocatoriaVoluntariados = [];
      this.activosVoluntariados = [];
      this.finalizadosVoluntariados = [];
    },
  },
});
</script>

<template>
  <div class="organization-detail">
    <AppNavBar />

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
      <!-- Hero Section with Organization Info -->
      <section
        class="organization-hero position-relative"
        :style="
          organization.banner
            ? {
                backgroundImage: `url(${organization.banner})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
              }
            : {}
        "
      >
        <div class="hero-overlay"></div>
        <!-- Banner indicator when no banner is present -->
        <div class="position-absolute top-0 end-0 m-3">
          <span v-if="!organization.banner" class="badge bg-secondary">Sin portada</span>
        </div>
        <div class="container">
          <div class="row">
            <div class="col-lg-10 mx-auto">
              <!-- Slogan -->
              <div class="text-center mb-4">
                <h2 class="organization-slogan">{{ organization.slogan }}</h2>
              </div>

              <!-- Main Info Card -->
              <div class="organization-card">
                <div class="row align-items-center">
                  <!-- Logo -->
                  <div class="col-md-3">
                    <div class="organization-logo text-center">
                      <img
                        v-if="organization.logo"
                        :src="organization.logo"
                        :alt="organization.name"
                        class="img-fluid rounded"
                        style="max-width: 140px; max-height: 140px; object-fit: contain"
                      />
                      <div v-else class="placeholder-logo">
                        <i class="bi bi-building" style="font-size: 48px; color: #6c757d"></i>
                        <div class="text-muted small mt-2">Sin logo</div>
                      </div>
                    </div>
                  </div>

                  <!-- Info -->
                  <div class="col-md-9">
                    <div class="organization-info">
                      <div class="d-flex justify-content-between align-items-start mb-3">
                        <h1 class="organization-name">{{ organization.name }}</h1>
                        <button class="btn btn-outline-primary btn-sm" @click="followOrganization">
                          <i class="bi bi-star me-1"></i>
                          Seguir
                        </button>
                      </div>

                      <!-- Tags -->
                      <div class="organization-tags mb-3">
                        <span
                          v-for="(tag, index) in organization.tags"
                          :key="index"
                          class="badge bg-secondary me-2 mb-2"
                        >
                          {{ tag }}
                        </span>
                      </div>

                      <!-- Description -->
                      <p class="organization-description">
                        {{ organization.description }}
                      </p>

                      <!-- Contact Buttons -->
                      <div class="contact-buttons">
                        <button
                          v-if="organization.contact.email"
                          class="btn btn-sm btn-outline-secondary me-2 mb-2"
                          @click="contactOrganization"
                        >
                          <i class="bi bi-envelope me-1"></i>
                          {{ organization.contact.email }}
                        </button>

                        <button
                          v-if="organization.contact.phone"
                          class="btn btn-sm btn-outline-secondary me-2 mb-2"
                          @click="callPhone(organization.contact.phone)"
                        >
                          <i class="bi bi-telephone me-1"></i>
                          {{ organization.contact.phone }}
                        </button>

                        <a
                          v-if="organization.contact.website"
                          :href="
                            organization.contact.website.startsWith('http')
                              ? organization.contact.website
                              : 'https://' + organization.contact.website
                          "
                          target="_blank"
                          rel="noopener noreferrer"
                          class="btn btn-sm btn-outline-secondary mb-2"
                        >
                          <i class="bi bi-globe me-1"></i>
                          {{ organization.contact.website }}
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Voluntariados Sections -->
      <section class="voluntariados-sections py-5 bg-light">
        <div class="container">
          <!-- Convocatoria Section -->
          <div
            class="voluntariado-section mb-5 p-4 bg-white rounded shadow-sm border-start border-5 stage-border-convocatoria"
          >
            <div class="d-flex align-items-center mb-4">
              <div class="section-icon me-3 stage-bg-convocatoria rounded-circle p-3">
                <i class="bi bi-megaphone-fill text-white" style="font-size: 1.75rem"></i>
              </div>
              <div>
                <h2 class="section-title mb-1 stage-text-convocatoria">Convocatoria</h2>
                <p class="text-muted mb-0 small">Voluntariados en período de inscripción</p>
              </div>
            </div>
            <div v-if="convocatoriaVoluntariados.length > 0" class="row g-4">
              <div
                v-for="voluntariado in convocatoriaVoluntariados"
                :key="`conv-${voluntariado.id}`"
                class="col-md-6 col-lg-4"
              >
                <VoluntariadoCard
                  :title="voluntariado.title"
                  :description="voluntariado.description"
                  :latitud="voluntariado.latitud ?? undefined"
                  :longitud="voluntariado.longitud ?? undefined"
                  :date="voluntariado.date"
                  :image-url="voluntariado.imageUrl"
                  @view="viewVoluntariado(voluntariado.id)"
                />
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-calendar-x text-muted mb-2" style="font-size: 2rem"></i>
              <p class="text-muted mb-0">No hay voluntariados en convocatoria</p>
            </div>
          </div>

          <!-- Próximamente Section -->
          <div
            class="voluntariado-section mb-5 p-4 bg-white rounded shadow-sm border-start border-5 stage-border-proximamente"
          >
            <div class="d-flex align-items-center mb-4">
              <div class="section-icon me-3 stage-bg-proximamente rounded-circle p-3">
                <i class="bi bi-clock-history text-white" style="font-size: 1.75rem"></i>
              </div>
              <div>
                <h2 class="section-title mb-1 stage-text-proximamente">Próximamente</h2>
                <p class="text-muted mb-0 small">Voluntariados que comenzarán pronto</p>
              </div>
            </div>
            <div v-if="proximosVoluntariados.length > 0" class="row g-4">
              <div
                v-for="voluntariado in proximosVoluntariados"
                :key="`up-${voluntariado.id}`"
                class="col-md-6 col-lg-4"
              >
                <VoluntariadoCard
                  :title="voluntariado.title"
                  :description="voluntariado.description"
                  :latitud="voluntariado.latitud ?? undefined"
                  :longitud="voluntariado.longitud ?? undefined"
                  :date="voluntariado.date"
                  :image-url="voluntariado.imageUrl"
                  :can-join="voluntariado.canJoin"
                  @view="viewVoluntariado(voluntariado.id)"
                />
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-hourglass-split text-muted mb-2" style="font-size: 2rem"></i>
              <p class="text-muted mb-0">No hay voluntariados próximamente</p>
            </div>
          </div>

          <!-- Activos Section -->
          <div
            class="voluntariado-section mb-5 p-4 bg-white rounded shadow-sm border-start border-5 stage-border-activo"
          >
            <div class="d-flex align-items-center mb-4">
              <div class="section-icon me-3 stage-bg-activo rounded-circle p-3">
                <i class="bi bi-play-circle-fill text-white" style="font-size: 1.75rem"></i>
              </div>
              <div>
                <h2 class="section-title mb-1 stage-text-activo">Activos</h2>
                <p class="text-muted mb-0 small">Voluntariados en curso</p>
              </div>
            </div>
            <div v-if="activosVoluntariados.length > 0" class="row g-4">
              <div
                v-for="voluntariado in activosVoluntariados"
                :key="`act-${voluntariado.id}`"
                class="col-md-6 col-lg-4"
              >
                <VoluntariadoCard
                  :title="voluntariado.title"
                  :description="voluntariado.description"
                  :latitud="voluntariado.latitud ?? undefined"
                  :longitud="voluntariado.longitud ?? undefined"
                  :date="voluntariado.date"
                  :image-url="voluntariado.imageUrl"
                  :can-join="voluntariado.canJoin"
                  @view="viewVoluntariado(voluntariado.id)"
                />
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-pause-circle text-muted mb-2" style="font-size: 2rem"></i>
              <p class="text-muted mb-0">No hay voluntariados activos</p>
            </div>
          </div>

          <!-- Finalizados Section -->
          <div
            class="voluntariado-section mb-4 p-4 bg-white rounded shadow-sm border-start border-5 stage-border-finalizado"
          >
            <div class="d-flex align-items-center mb-4">
              <div class="section-icon me-3 stage-bg-finalizado rounded-circle p-3">
                <i class="bi bi-check-circle-fill text-white" style="font-size: 1.75rem"></i>
              </div>
              <div>
                <h2 class="section-title mb-1 stage-text-finalizado">Finalizados</h2>
                <p class="text-muted mb-0 small">Voluntariados completados</p>
              </div>
            </div>
            <div v-if="finalizadosVoluntariados.length > 0" class="row g-4">
              <div
                v-for="voluntariado in finalizadosVoluntariados"
                :key="`fin-${voluntariado.id}`"
                class="col-md-6 col-lg-4"
              >
                <VoluntariadoCard
                  :title="voluntariado.title"
                  :description="voluntariado.description"
                  :latitud="voluntariado.latitud ?? undefined"
                  :longitud="voluntariado.longitud ?? undefined"
                  :date="voluntariado.date"
                  :image-url="voluntariado.imageUrl"
                  :can-join="voluntariado.canJoin"
                  @view="viewVoluntariado(voluntariado.id)"
                />
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-archive text-muted mb-2" style="font-size: 2rem"></i>
              <p class="text-muted mb-0">No hay voluntariados finalizados</p>
            </div>
          </div>

          <!-- View All Link -->
          <div class="text-center mt-5">
            <router-link to="/voluntariados" class="btn btn-outline-secondary btn-lg">
              Ver Todos los Voluntariados
              <i class="bi bi-arrow-right ms-2"></i>
            </router-link>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <CTASection
        title="¡Inscríbete hoy y marca la diferencia!"
        primary-text="Registrarme como voluntario"
        primary-link="/signup"
        secondary-text="Soy Organización, quiero colaborar"
        secondary-link="/about#contact"
      />
    </template>
  </div>
</template>

<style scoped src="./../styles/organizationDetail.css"></style>
<style scoped>
@import "./../styles/VoluntariadoStageColors.css";

/* Stage-specific styling using CSS variables */
.stage-border-convocatoria {
  border-color: var(--stage-convocatoria-bg) !important;
}

.stage-bg-convocatoria {
  background-color: var(--stage-convocatoria-bg);
  opacity: 1;
}

.stage-text-convocatoria {
  color: var(--stage-convocatoria-bg);
}

.stage-border-proximamente {
  border-color: var(--stage-proximamente-bg) !important;
}

.stage-bg-proximamente {
  background-color: var(--stage-proximamente-bg);
  opacity: 1;
}

.stage-text-proximamente {
  color: var(--stage-proximamente-bg);
}

.stage-border-activo {
  border-color: var(--stage-activo-bg) !important;
}

.stage-bg-activo {
  background-color: var(--stage-activo-bg);
  opacity: 1;
}

.stage-text-activo {
  color: var(--stage-activo-bg);
}

.stage-border-finalizado {
  border-color: var(--stage-finalizado-bg) !important;
}

.stage-bg-finalizado {
  background-color: var(--stage-finalizado-bg);
  opacity: 1;
}

.stage-text-finalizado {
  color: var(--stage-finalizado-bg);
}
</style>
