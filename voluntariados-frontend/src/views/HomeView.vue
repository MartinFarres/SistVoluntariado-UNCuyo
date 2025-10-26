<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import HeroSection from "@/components/landing/HeroSection.vue";
import InfoSection from "@/components/landing/InfoSection.vue";
import VoluntariadoCard from "@/components/landing/VoluntariadoCard.vue";
import TestimonialsSection from "@/components/landing/TestimonialsSection.vue";
import OrganizationsSection from "@/components/landing/OrganizationsSection.vue";
import HowItWorksSection from "@/components/landing/HowItWorksSection.vue";
import TeamSection from "@/components/landing/TeamSection.vue";
import CTASection from "@/components/landing/CTASection.vue";
import { voluntariadoAPI, organizacionAPI } from "@/services/api";
import { useLandingConfig } from "@/composables/useLandingConfig";
import authService from "@/services/authService";

interface Voluntariado {
  id: number;
  nombre: string;
  descripcion?: any;
  estado: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

interface Organizacion {
  id: number;
  nombre: string;
  descripcion?: string;
}

export default defineComponent({
  name: "HomeView",
  components: {
    AppNavBar,
    HeroSection,
    InfoSection,
    VoluntariadoCard,
    TestimonialsSection,
    OrganizationsSection,
    HowItWorksSection,
    TeamSection,
    CTASection,
  },
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig();
    return {
      landingConfig,
      fetchLandingConfig,
    };
  },
  data() {
    return {
      isAuthenticated: false,
      loading: false,
      error: null as string | null,

      // Info Section Data
      infoItems: [
        {
          icon: "bi-lightbulb",
          title: "Iniciativa",
          description:
            "Descubrí oportunidades únicas para generar un impacto positivo en tu comunidad universitaria y más allá. Cada voluntariado es una oportunidad para crecer.",
        },
        {
          icon: "bi-trophy",
          title: "Objetivos",
          description:
            "Alcanzá tus metas personales y profesionales mientras ayudás a otros. Desarrollá habilidades, expandí tu red de contactos y construí un currículum destacado.",
        },
        {
          icon: "bi-flag",
          title: "Misión",
          description:
            "Nuestra misión es conectar estudiantes comprometidos con organizaciones que necesitan su talento y energía para crear un mundo mejor.",
        },
        {
          icon: "bi-people",
          title: "Para los Estudiantes",
          description:
            "Accedé a una amplia variedad de oportunidades de voluntariado diseñadas especialmente para estudiantes universitarios que quieren marcar la diferencia.",
        },
      ],

      // Featured Voluntariados - will be populated from API
      featuredVoluntariados: [] as any[],

      // Testimonials
      testimonials: [
        {
          name: "Sed ut perspiciatis",
          role: "Estudiante de Medicina",
          text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        },
        {
          name: "Lorem ipsum dolor",
          role: "Estudiante de Ingeniería",
          text: "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.",
        },
        {
          name: "Nemo enim ipsam",
          role: "Estudiante de Derecho",
          text: "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. Quis autem vel eum iure reprehenderit.",
        },
      ],

      // Organizations - will be populated from API
      organizations: [] as any[],

      // How it Works Steps
      howItWorksSteps: [
        {
          title: "1. Registrate",
          description:
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
        },
        {
          title: "2. Explora Voluntariados",
          description:
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.",
        },
        {
          title: "3. Consulta los Detalles",
          description:
            "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.",
        },
        {
          title: "4. Participa",
          description:
            "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore.",
        },
        {
          title: "5. Inscribite en Capacitaciones",
          description:
            "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur.",
        },
        {
          title: "6. Recibi tu Certificado",
          description:
            "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas.",
        },
      ],

      // Team Members
      teamMembers: [
        { name: "Juan Pérez", role: "Director" },
        { name: "María González", role: "Coordinadora" },
        { name: "Carlos Rodríguez", role: "Voluntario Senior" },
        { name: "Ana Martínez", role: "Administradora" },
      ],
    };
  },

  async mounted() {
    this.isAuthenticated = authService.isAuthenticated();
    // Ensure landing config is loaded before loading other data
    await this.fetchLandingConfig();
    await this.loadData();
  },

  methods: {
    async loadData() {
      this.loading = true;
      this.error = null;

      try {
        // Load voluntariados and organizations in parallel
        const [voluntariadosRes, organizacionesRes] = await Promise.all([
          voluntariadoAPI.getAllUpcoming(),
          organizacionAPI.getAll(),
        ]);

        // Process voluntariados
        const allVoluntariados: Voluntariado[] = voluntariadosRes.data;

        // Filter only active voluntariados and take first 3
        const activeVoluntariados = allVoluntariados
          .filter((v) => v.estado === "ACTIVE")
          .slice(0, 3);

        // Map to featured format
        this.featuredVoluntariados = activeVoluntariados.map((v, index) => {
          const badges = ["Nuevo", "Destacado", "Popular"];
          const badgeClasses = ["bg-success", "bg-warning", "bg-primary"];
          const categories = ["Educación", "Medio Ambiente", "Salud"];
          const locations = ["Mendoza", "Godoy Cruz", "Luján de Cuyo"];

          return {
            id: v.id,
            title: v.nombre,
            description: this.getDescriptionText(v.descripcion) || "Sin descripción disponible",
            category: categories[index % categories.length],
            location: locations[index % locations.length],
            badge: badges[index % badges.length],
            badgeClass: badgeClasses[index % badgeClasses.length],
            // Image comes from nested descripcion: prefer portada, then logo
            imageUrl:
              v.descripcion && typeof v.descripcion === "object"
                ? (v.descripcion.portada as string) || (v.descripcion.logo as string) || undefined
                : undefined,
          };
        });

        // Process organizations - take first 8
        const allOrganizations: Organizacion[] = organizacionesRes.data;
        this.organizations = allOrganizations.slice(0, 8).map((org) => ({
          name: org.nombre,
        }));
      } catch (err: any) {
        console.error("Error loading home data:", err);
        this.error = err.response?.data?.detail || "Error al cargar los datos";

        // Use fallback data on error
        this.setFallbackData();
      } finally {
        this.loading = false;
      }
    },

    getDescriptionText(descripcion: any): string {
      if (!descripcion) return "";
      if (typeof descripcion === "string") return descripcion;
      if (typeof descripcion === "object" && descripcion.descripcion) {
        return descripcion.descripcion;
      }
      return "";
    },

    setFallbackData() {
      this.featuredVoluntariados = [
        {
          title: "Sed ut perspiciatis",
          description:
            "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione.",
          category: "Educación",
          location: "Mendoza",
          badge: "Nuevo",
          badgeClass: "bg-success",
        },
        {
          title: "Lorem ipsum dolor",
          description:
            "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium totam rem aperiam.",
          category: "Medio Ambiente",
          location: "Godoy Cruz",
          badge: "Destacado",
          badgeClass: "bg-warning",
        },
        {
          title: "Nemo enim ipsam",
          description:
            "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti.",
          category: "Salud",
          location: "Luján de Cuyo",
          badge: "Popular",
          badgeClass: "bg-primary",
        },
      ];

      this.organizations = [
        { name: "Cruz Roja" },
        { name: "Cáritas" },
        { name: "UNICEF" },
        { name: "Fundación SI" },
        { name: "Techo" },
        { name: "Greenpeace" },
        { name: "Banco de Alimentos" },
        { name: "Fundación Huésped" },
      ];
    },
  },
});
</script>

<template>
  <div class="home">
    <AppNavBar />

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-warning m-4" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Hero Section -->
      <HeroSection :title="landingConfig.welcome_message" :subtitle="landingConfig.description" />

      <!-- What is University Volunteering -->
      <InfoSection title="¿Qué es el Voluntariado Universitario?" :items="infoItems" />

      <!-- Featured Voluntariados -->
      <section class="featured-section py-5">
        <div class="container">
          <h2 class="section-title text-center mb-3">Algunos de Nuestros Voluntariados</h2>
          <p class="section-subtitle text-center mb-5">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
            incididunt ut labore et dolore magna aliqua.
          </p>

          <div class="row g-4">
            <div
              v-for="(voluntariado, index) in featuredVoluntariados"
              :key="index"
              class="col-md-6 col-lg-4"
            >
              <VoluntariadoCard
                :title="voluntariado.title"
                :description="voluntariado.description"
                :image-url="voluntariado.imageUrl"
                :category="voluntariado.category"
                :location="voluntariado.location"
                :badge="voluntariado.badge"
                :badge-class="voluntariado.badgeClass"
                @view="() => $router.push(`/voluntariados/${voluntariado.id || ''}`)"
              />
            </div>
          </div>

          <div class="text-center mt-5">
            <router-link to="/voluntariados" class="btn btn-primary btn-lg">
              Ver todos los voluntariados
              <i class="bi bi-arrow-right ms-2"></i>
            </router-link>
          </div>
        </div>
      </section>

      <!-- Testimonials -->
      <TestimonialsSection :testimonials="testimonials" />

      <!-- Partner Organizations -->
      <OrganizationsSection
        title="Organizaciones Aliadas"
        subtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        :organizations="organizations"
      />

      <!-- How It Works -->
      <HowItWorksSection :steps="howItWorksSteps" />

      <!-- Team -->
      <TeamSection
        title="Nuestro Equipo"
        subtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        :team-members="teamMembers"
      />

      <!-- CTA Section -->
      <!-- v-if="!isAuthenticated" -->
      <CTASection
        title="¡Inscríbete hoy y marca la diferencia!"
        primary-text="Comenzar ahora"
        primary-link="/signup"
        secondary-text="Ver más información"
        secondary-link="/about"
      />
    </template>
  </div>
</template>

<style scoped src="./../styles/homeView.css"></style>
