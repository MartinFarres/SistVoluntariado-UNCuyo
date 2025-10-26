<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import VoluntariadoCard from "@/components/landing/VoluntariadoCard.vue";
import CTASection from "@/components/landing/CTASection.vue";
import { organizacionAPI, voluntariadoAPI } from "@/services/api";

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
}

interface ProximoVoluntariado {
  id: number;
  title: string;
  description: string;
  category: string;
  location: string;
  date?: string;
  imageUrl?: string;
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
      finalizadosVoluntariados: [] as ProximoVoluntariado[],
    };
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
        // Fetch convocatoria, upcoming and finished in parallel and map each to the UI model.
        try {
          const results = await Promise.allSettled([
            voluntariadoAPI.getByOrganization(this.organizationId, "convocatoria"),
            voluntariadoAPI.getByOrganization(this.organizationId, "upcoming"),
            voluntariadoAPI.getByOrganization(this.organizationId, "finished"),
          ]);

          // convocatoria
          if (results[0].status === "fulfilled") {
            const conv: any = results[0].value;
            const convList: Voluntariado[] = conv.data || [];
            this.convocatoriaVoluntariados = convList.map((v) => this.mapVoluntariadoToDisplay(v));
          } else {
            this.convocatoriaVoluntariados = [];
            console.warn("convocatoria fetch failed:", (results[0] as any).reason || results[0]);
          }

          // upcoming
          if (results[1].status === "fulfilled") {
            const up: any = results[1].value;
            const upList: Voluntariado[] = up.data || [];
            this.proximosVoluntariados = upList.map((v) => this.mapVoluntariadoToDisplay(v));
          } else {
            this.proximosVoluntariados = [];
            console.warn("upcoming fetch failed:", (results[1] as any).reason || results[1]);
          }

          // finished
          if (results[2].status === "fulfilled") {
            const fin: any = results[2].value;
            const finList: Voluntariado[] = fin.data || [];
            this.finalizadosVoluntariados = finList.map((v) => this.mapVoluntariadoToDisplay(v));
          } else {
            this.finalizadosVoluntariados = [];
            console.warn("finished fetch failed:", (results[2] as any).reason || results[2]);
          }
        } catch (volErr) {
          console.warn("Error loading organization voluntariados via dedicated endpoint:", volErr);
          this.convocatoriaVoluntariados = [];
          this.proximosVoluntariados = [];
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
      const categories = ["Educación", "Medio Ambiente", "Salud", "Cultura", "Deportes"];
      const locations = ["Mendoza", "Godoy Cruz", "Luján de Cuyo", "Las Heras", "Maipú"];

      return {
        id: v.id,
        title: v.nombre,
        description: this.getDescriptionText(v.descripcion) || "Sin descripción disponible",
        category: categories[v.id % categories.length] || "",
        location: locations[v.id % locations.length] || "",
        date: v.fecha_inicio ? this.formatDate(v.fecha_inicio) : undefined,
        // Image is stored in the nested descripcion object (portada preferred, then logo)
        imageUrl:
          v.descripcion && typeof v.descripcion === "object"
            ? (v.descripcion.portada as string) || (v.descripcion.logo as string) || undefined
            : undefined,
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
      // Clear organization view model and upcoming voluntariados when loading fails
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
            class="voluntariado-section mb-5 p-4 bg-white rounded shadow-sm border-start border-5 border-success"
          >
            <div class="d-flex align-items-center mb-4">
              <div class="section-icon me-3 bg-success bg-opacity-10 rounded-circle p-3">
                <i class="bi bi-megaphone-fill text-success" style="font-size: 1.75rem"></i>
              </div>
              <div>
                <h2 class="section-title mb-1 text-success">Convocatoria</h2>
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
                  :category="voluntariado.category"
                  :location="voluntariado.location"
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
            class="voluntariado-section mb-5 p-4 bg-white rounded shadow-sm border-start border-5 border-primary"
          >
            <div class="d-flex align-items-center mb-4">
              <div class="section-icon me-3 bg-primary bg-opacity-10 rounded-circle p-3">
                <i class="bi bi-clock-history text-primary" style="font-size: 1.75rem"></i>
              </div>
              <div>
                <h2 class="section-title mb-1 text-primary">Próximamente</h2>
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
                  :category="voluntariado.category"
                  :location="voluntariado.location"
                  :date="voluntariado.date"
                  :image-url="voluntariado.imageUrl"
                  @view="viewVoluntariado(voluntariado.id)"
                />
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="bi bi-hourglass-split text-muted mb-2" style="font-size: 2rem"></i>
              <p class="text-muted mb-0">No hay voluntariados próximamente</p>
            </div>
          </div>

          <!-- Finalizados Section -->
          <div
            class="voluntariado-section mb-4 p-4 bg-white rounded shadow-sm border-start border-5 border-secondary"
          >
            <div class="d-flex align-items-center mb-4">
              <div class="section-icon me-3 bg-secondary bg-opacity-10 rounded-circle p-3">
                <i class="bi bi-check-circle-fill text-secondary" style="font-size: 1.75rem"></i>
              </div>
              <div>
                <h2 class="section-title mb-1 text-secondary">Finalizados</h2>
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
                  :category="voluntariado.category"
                  :location="voluntariado.location"
                  :date="voluntariado.date"
                  :image-url="voluntariado.imageUrl"
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
        secondary-link="/contact"
      />
    </template>
  </div>
</template>

<style scoped src="./../styles/organizationDetail.css"></style>
