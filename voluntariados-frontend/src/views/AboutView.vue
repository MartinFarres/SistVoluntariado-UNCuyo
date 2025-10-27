<!-- src/views/AboutView.vue -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import CTASection from "@/components/landing/CTASection.vue";
import { useLandingConfig } from "@/composables/useLandingConfig";

export default defineComponent({
  name: "AboutView",
  components: {
    AppNavBar,
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
      values: [
        {
          icon: "bi-heart",
          title: "Compromiso",
          description:
            "Estamos comprometidos con el desarrollo de una comunidad universitaria más solidaria y participativa.",
        },
        {
          icon: "bi-people",
          title: "Inclusión",
          description:
            "Creemos en la diversidad y en crear espacios donde todos los estudiantes puedan contribuir y crecer.",
        },
        {
          icon: "bi-lightbulb",
          title: "Innovación",
          description:
            "Buscamos nuevas formas de conectar el talento estudiantil con las necesidades de la comunidad.",
        },
        {
          icon: "bi-trophy",
          title: "Excelencia",
          description:
            "Nos esforzamos por ofrecer experiencias de voluntariado de alta calidad que beneficien a todos.",
        },
      ],

      stats: [
        { number: "500+", label: "Voluntarios Activos" },
        { number: "50+", label: "Organizaciones Aliadas" },
        { number: "100+", label: "Proyectos Realizados" },
        { number: "10k+", label: "Horas de Voluntariado" },
      ],

      team: [
        {
          name: "Dr. Juan Pérez",
          role: "Director del Programa",
          description:
            "Más de 15 años de experiencia en desarrollo comunitario y educación universitaria.",
          avatar: "https://via.placeholder.com/150",
        },
        {
          name: "Lic. María González",
          role: "Coordinadora General",
          description:
            "Especialista en gestión de voluntariado y responsabilidad social universitaria.",
          avatar: "https://via.placeholder.com/150",
        },
        {
          name: "Ing. Carlos Rodríguez",
          role: "Coordinador de Tecnología",
          description:
            "Desarrolla las plataformas digitales para facilitar la participación estudiantil.",
          avatar: "https://via.placeholder.com/150",
        },
        {
          name: "Lic. Ana Martínez",
          role: "Coordinadora de Alianzas",
          description:
            "Establece vínculos con organizaciones sociales y gestiona proyectos colaborativos.",
          avatar: "https://via.placeholder.com/150",
        },
      ],

      milestones: [
        {
          year: "2018",
          title: "Fundación del Programa",
          description:
            "Nace el programa de voluntariado universitario con la misión de conectar estudiantes con su comunidad.",
        },
        {
          year: "2019",
          title: "Primeras Alianzas",
          description: "Establecemos colaboraciones con 10 organizaciones sociales locales.",
        },
        {
          year: "2021",
          title: "Expansión Regional",
          description: "El programa se expande a toda la provincia de Mendoza.",
        },
        {
          year: "2023",
          title: "Reconocimiento Nacional",
          description:
            "Recibimos el premio a la mejor iniciativa de voluntariado universitario del país.",
        },
        {
          year: "2025",
          title: "Plataforma Digital",
          description:
            "Lanzamiento de nuestra plataforma digital para facilitar la inscripción y gestión de voluntariados.",
        },
      ],
    };
  },

  mounted() {
    this.fetchLandingConfig();
  },
});
</script>

<template>
  <div class="about-page">
    <AppNavBar />

    <!-- Hero Section -->
    <section class="page-header shared-hero">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto text-center">
            <h1 class="page-title mb-3">Sobre Nosotros</h1>
            <p class="page-subtitle">
              Conectamos el talento y la pasión de estudiantes universitarios con las necesidades de
              nuestra comunidad, creando un impacto positivo y duradero.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Mission & Vision -->
    <section class="mission-section py-5">
      <div class="container">
        <div class="row g-4">
          <div class="col-md-6">
            <div class="info-box">
              <div class="info-icon">
                <i class="bi bi-flag"></i>
              </div>
              <h2 class="info-title">Nuestra Misión</h2>
              <p class="info-text">
                Promover la participación activa de estudiantes universitarios en proyectos de
                voluntariado que generen un impacto positivo en la sociedad, fomentando valores de
                solidaridad, compromiso social y desarrollo personal.
              </p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="info-box">
              <div class="info-icon">
                <i class="bi bi-eye"></i>
              </div>
              <h2 class="info-title">Nuestra Visión</h2>
              <p class="info-text">
                Ser la plataforma líder en América Latina que conecta estudiantes universitarios con
                oportunidades de voluntariado, transformando comunidades y formando profesionales
                comprometidos con el bienestar social.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section py-5">
      <div class="container">
        <div class="row g-4">
          <div v-for="(stat, index) in stats" :key="index" class="col-6 col-md-3">
            <div class="stat-card text-center">
              <div class="stat-number">{{ stat.number }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Values Section -->
    <section class="values-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">Nuestros Valores</h2>
          <p class="section-subtitle">
            Los principios que guían nuestro trabajo y definen nuestra cultura
          </p>
        </div>

        <div class="row g-4">
          <div v-for="(value, index) in values" :key="index" class="col-md-6 col-lg-3">
            <div class="value-card text-center">
              <div class="value-icon">
                <i class="bi" :class="value.icon"></i>
              </div>
              <h3 class="value-title">{{ value.title }}</h3>
              <p class="value-description">{{ value.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Timeline Section -->
    <section class="timeline-section py-5 bg-light">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">Nuestra Historia</h2>
          <p class="section-subtitle">Los hitos que marcaron nuestro camino</p>
        </div>

        <div class="timeline">
          <div
            v-for="(milestone, index) in milestones"
            :key="index"
            class="timeline-item"
            :class="{ 'timeline-item-right': index % 2 !== 0 }"
          >
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <div class="timeline-year">{{ milestone.year }}</div>
              <h3 class="timeline-title">{{ milestone.title }}</h3>
              <p class="timeline-description">{{ milestone.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="team-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">Nuestro Equipo</h2>
          <p class="section-subtitle">Profesionales dedicados a hacer la diferencia</p>
        </div>

        <div class="row g-4">
          <div v-for="(member, index) in team" :key="index" class="col-md-6 col-lg-3">
            <div class="team-member-card">
              <div class="member-avatar">
                <img :src="member.avatar" :alt="member.name" />
              </div>
              <div class="member-info">
                <h3 class="member-name">{{ member.name }}</h3>
                <p class="member-role">{{ member.role }}</p>
                <p class="member-description">{{ member.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- What We Offer Section -->
    <section class="offer-section py-5 bg-light">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">¿Qué Ofrecemos?</h2>
          <p class="section-subtitle">Beneficios para estudiantes y organizaciones</p>
        </div>

        <div class="row g-4">
          <div class="col-md-6">
            <div class="offer-card">
              <h3 class="offer-card-title">
                <i class="bi bi-mortarboard me-2"></i>
                Para Estudiantes
              </h3>
              <ul class="offer-list">
                <li>Desarrollo de habilidades blandas y técnicas</li>
                <li>Certificados de participación y reconocimiento</li>
                <li>Networking con profesionales y organizaciones</li>
                <li>Experiencia práctica en tu campo de estudio</li>
                <li>Acceso a capacitaciones y talleres</li>
                <li>Construcción de un portafolio social</li>
              </ul>
            </div>
          </div>
          <div class="col-md-6">
            <div class="offer-card">
              <h3 class="offer-card-title">
                <i class="bi bi-building me-2"></i>
                Para Organizaciones
              </h3>
              <ul class="offer-list">
                <li>Acceso a talento universitario comprometido</li>
                <li>Apoyo en proyectos sociales y comunitarios</li>
                <li>Visibilidad en la comunidad universitaria</li>
                <li>Alianzas estratégicas con la universidad</li>
                <li>Gestión simplificada de voluntarios</li>
                <li>Impacto social medible y sostenible</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Info Section -->
    <section id="contact" class="contact-info-section py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <div class="contact-info-box text-center">
              <i class="bi bi-envelope-heart display-4 text-primary mb-4"></i>
              <h2 class="mb-3">¿Tenés Preguntas?</h2>
              <p class="mb-4">
                Nuestro equipo está disponible para ayudarte. No dudes en contactarnos para obtener
                más información sobre nuestros programas de voluntariado.
              </p>
              <div class="contact-methods">
                <div v-if="landingConfig.contact_email" class="contact-method">
                  <i class="bi bi-envelope me-2"></i>
                  <a :href="`mailto:${landingConfig.contact_email}`">{{
                    landingConfig.contact_email
                  }}</a>
                </div>
                <div v-if="landingConfig.phone_number" class="contact-method">
                  <i class="bi bi-telephone me-2"></i>
                  <a :href="`tel:${landingConfig.phone_number}`">{{
                    landingConfig.phone_number
                  }}</a>
                </div>
                <div
                  v-if="landingConfig.instagram_handle && landingConfig.instagram_url"
                  class="contact-method"
                >
                  <i class="bi bi-instagram me-2"></i>
                  <a :href="landingConfig.instagram_url" target="_blank" rel="noopener noreferrer"
                    >@{{ landingConfig.instagram_handle }}</a
                  >
                </div>
              </div>
              <a
                v-if="landingConfig.contact_email"
                :href="`mailto:${landingConfig.contact_email}`"
                class="btn btn-primary btn-lg mt-4"
              >
                <i class="bi bi-chat-dots me-2"></i>
                Contactanos
              </a>
              <router-link v-else to="/contact" class="btn btn-primary btn-lg mt-4">
                <i class="bi bi-chat-dots me-2"></i>
                Contactanos
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <CTASection
      title="¡Sumate a Nuestra Comunidad!"
      subtitle="Comenzá hoy tu camino como voluntario y sé parte del cambio"
      primary-text="Registrarme"
      primary-link="/signup"
      secondary-text="Ver Voluntariados"
      secondary-link="/voluntariados"
      secondary-icon="bi-search me-2"
    />
  </div>
</template>

<style scoped src="./../styles/about.css"></style>
<style src="./../styles/sharedHeaders.css"></style>
