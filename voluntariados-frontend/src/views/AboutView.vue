<!-- src/views/AboutView.vue -->
<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import CTASection from '@/components/landing/CTASection.vue'
import { useLandingConfig } from '@/composables/useLandingConfig'

export default defineComponent({
  name: 'AboutView',
  components: {
    AppNavBar,
    CTASection
  },
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig()
    return {
      landingConfig,
      fetchLandingConfig
    }
  },
  data() {
    return {
      values: [
        {
          icon: 'bi-heart',
          title: 'Compromiso',
          description: 'Estamos comprometidos con el desarrollo de una comunidad universitaria más solidaria y participativa.'
        },
        {
          icon: 'bi-people',
          title: 'Inclusión',
          description: 'Creemos en la diversidad y en crear espacios donde todos los estudiantes puedan contribuir y crecer.'
        },
        {
          icon: 'bi-lightbulb',
          title: 'Innovación',
          description: 'Buscamos nuevas formas de conectar el talento estudiantil con las necesidades de la comunidad.'
        },
        {
          icon: 'bi-trophy',
          title: 'Excelencia',
          description: 'Nos esforzamos por ofrecer experiencias de voluntariado de alta calidad que beneficien a todos.'
        }
      ],
      
      stats: [
        { number: '500+', label: 'Voluntarios Activos' },
        { number: '50+', label: 'Organizaciones Aliadas' },
        { number: '100+', label: 'Proyectos Realizados' },
        { number: '10k+', label: 'Horas de Voluntariado' }
      ],
      
      team: [
        {
          name: 'Dr. Juan Pérez',
          role: 'Director del Programa',
          description: 'Más de 15 años de experiencia en desarrollo comunitario y educación universitaria.',
          avatar: 'https://via.placeholder.com/150'
        },
        {
          name: 'Lic. María González',
          role: 'Coordinadora General',
          description: 'Especialista en gestión de voluntariado y responsabilidad social universitaria.',
          avatar: 'https://via.placeholder.com/150'
        },
        {
          name: 'Ing. Carlos Rodríguez',
          role: 'Coordinador de Tecnología',
          description: 'Desarrolla las plataformas digitales para facilitar la participación estudiantil.',
          avatar: 'https://via.placeholder.com/150'
        },
        {
          name: 'Lic. Ana Martínez',
          role: 'Coordinadora de Alianzas',
          description: 'Establece vínculos con organizaciones sociales y gestiona proyectos colaborativos.',
          avatar: 'https://via.placeholder.com/150'
        }
      ],
      
      milestones: [
        {
          year: '2018',
          title: 'Fundación del Programa',
          description: 'Nace el programa de voluntariado universitario con la misión de conectar estudiantes con su comunidad.'
        },
        {
          year: '2019',
          title: 'Primeras Alianzas',
          description: 'Establecemos colaboraciones con 10 organizaciones sociales locales.'
        },
        {
          year: '2021',
          title: 'Expansión Regional',
          description: 'El programa se expande a toda la provincia de Mendoza.'
        },
        {
          year: '2023',
          title: 'Reconocimiento Nacional',
          description: 'Recibimos el premio a la mejor iniciativa de voluntariado universitario del país.'
        },
        {
          year: '2025',
          title: 'Plataforma Digital',
          description: 'Lanzamiento de nuestra plataforma digital para facilitar la inscripción y gestión de voluntariados.'
        }
      ]
    }
  },
  
  mounted() {
    this.fetchLandingConfig()
  }
})
</script>

<template>
  <div class="about-page">
    <AppNavBar />
    
    <!-- Hero Section -->
    <section class="about-hero">
      <div class="hero-overlay"></div>
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto text-center">
            <h1 class="hero-title mb-4">Sobre Nosotros</h1>
            <p class="hero-subtitle">
              Conectamos el talento y la pasión de estudiantes universitarios con 
              las necesidades de nuestra comunidad, creando un impacto positivo y duradero.
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
                Promover la participación activa de estudiantes universitarios en proyectos 
                de voluntariado que generen un impacto positivo en la sociedad, fomentando 
                valores de solidaridad, compromiso social y desarrollo personal.
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
                Ser la plataforma líder en América Latina que conecta estudiantes universitarios 
                con oportunidades de voluntariado, transformando comunidades y formando 
                profesionales comprometidos con el bienestar social.
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
          <div 
            v-for="(stat, index) in stats" 
            :key="index"
            class="col-6 col-md-3"
          >
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
          <div 
            v-for="(value, index) in values" 
            :key="index"
            class="col-md-6 col-lg-3"
          >
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
          <p class="section-subtitle">
            Los hitos que marcaron nuestro camino
          </p>
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
          <p class="section-subtitle">
            Profesionales dedicados a hacer la diferencia
          </p>
        </div>
        
        <div class="row g-4">
          <div 
            v-for="(member, index) in team" 
            :key="index"
            class="col-md-6 col-lg-3"
          >
            <div class="team-member-card">
              <div class="member-avatar">
                <img :src="member.avatar" :alt="member.name">
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
          <p class="section-subtitle">
            Beneficios para estudiantes y organizaciones
          </p>
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
    <section class="contact-info-section py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <div class="contact-info-box text-center">
              <i class="bi bi-envelope-heart display-4 text-primary mb-4"></i>
              <h2 class="mb-3">¿Tenés Preguntas?</h2>
              <p class="mb-4">
                Nuestro equipo está disponible para ayudarte. No dudes en contactarnos 
                para obtener más información sobre nuestros programas de voluntariado.
              </p>
              <div class="contact-methods">
                <div class="contact-method">
                  <i class="bi bi-envelope me-2"></i>
                  <a href="mailto:info@voluntariado.edu.ar">info@voluntariado.edu.ar</a>
                </div>
                <div class="contact-method">
                  <i class="bi bi-telephone me-2"></i>
                  <a href="tel:+542614234567">+54 261 423 4567</a>
                </div>
                <div class="contact-method">
                  <i class="bi bi-geo-alt me-2"></i>
                  <span>Mendoza, Argentina</span>
                </div>
              </div>
              <router-link to="/contact" class="btn btn-primary btn-lg mt-4">
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

<style scoped>
.about-page {
  min-height: 100vh;
  background: white;
}

.about-hero {
  background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
  padding: 6rem 0 4rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.about-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120"><path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" fill="%23fff"/></svg>') no-repeat bottom;
  background-size: cover;
  opacity: 0.1;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.about-hero .container {
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  text-shadow: 2px 4px 8px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.3rem;
  opacity: 0.95;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.7;
}

.mission-section {
  background: #f8f9fa;
}

.info-box {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  height: 100%;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.info-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(139, 0, 0, 0.15);
  border-color: #8B0000;
}

.info-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #8B0000, #DC143C);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
}

.info-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.info-text {
  color: #6c757d;
  line-height: 1.8;
  font-size: 1rem;
}

.stats-section {
  background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
  color: white;
}

.stat-card {
  padding: 2rem 1rem;
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.stat-label {
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 500;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  position: relative;
  padding-bottom: 1rem;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #8B0000, #DC143C);
  border-radius: 2px;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #6c757d;
  max-width: 700px;
  margin: 0 auto;
}

.value-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  height: 100%;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.value-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(139, 0, 0, 0.15);
}

.value-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #8B0000, #DC143C);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2.5rem;
  margin: 0 auto 1.5rem;
}

.value-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.value-description {
  color: #6c757d;
  line-height: 1.7;
  font-size: 0.95rem;
}

.timeline {
  position: relative;
  padding: 2rem 0;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #8B0000, #DC143C);
  transform: translateX(-50%);
}

.timeline-item {
  position: relative;
  margin-bottom: 3rem;
  width: 50%;
  padding-right: 3rem;
}

.timeline-item-right {
  margin-left: 50%;
  padding-right: 0;
  padding-left: 3rem;
}

.timeline-marker {
  position: absolute;
  right: -14px;
  top: 0;
  width: 24px;
  height: 24px;
  background: white;
  border: 4px solid #8B0000;
  border-radius: 50%;
  z-index: 2;
}

.timeline-item-right .timeline-marker {
  right: auto;
  left: -14px;
}

.timeline-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

.timeline-year {
  display: inline-block;
  background: linear-gradient(135deg, #8B0000, #DC143C);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.timeline-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.75rem;
}

.timeline-description {
  color: #6c757d;
  line-height: 1.7;
  margin: 0;
}

.team-member-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  height: 100%;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.team-member-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(139, 0, 0, 0.15);
}

.member-avatar {
  width: 120px;
  height: 120px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #8B0000;
  box-shadow: 0 4px 15px rgba(139, 0, 0, 0.2);
}

.member-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.member-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.member-role {
  font-size: 0.95rem;
  color: #8B0000;
  font-weight: 600;
  margin-bottom: 1rem;
}

.member-description {
  font-size: 0.9rem;
  color: #6c757d;
  line-height: 1.6;
  margin: 0;
}

.offer-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  height: 100%;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.offer-card:hover {
  border-color: #8B0000;
  transform: translateY(-5px);
}

.offer-card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.offer-card-title i {
  color: #8B0000;
}

.offer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.offer-list li {
  padding: 0.75rem 0;
  padding-left: 2rem;
  color: #495057;
  line-height: 1.6;
  position: relative;
}

.offer-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #8B0000;
  font-weight: 700;
  font-size: 1.2rem;
}

.contact-info-box {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 2px solid #e9ecef;
}

.contact-methods {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.contact-method {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: #495057;
}

.contact-method i {
  color: #8B0000;
  font-size: 1.3rem;
}

.contact-method a {
  color: #495057;
  text-decoration: none;
  transition: color 0.3s ease;
}

.contact-method a:hover {
  color: #8B0000;
}

.btn-primary {
  background: linear-gradient(135deg, #8B0000, #DC143C);
  border: none;
  padding: 1rem 2.5rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(139, 0, 0, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(139, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
  
  .timeline::before {
    left: 20px;
  }
  
  .timeline-item,
  .timeline-item-right {
    width: 100%;
    padding-left: 3rem;
    padding-right: 0;
    margin-left: 0;
  }
  
  .timeline-marker,
  .timeline-item-right .timeline-marker {
    left: 8px;
    right: auto;
  }
  
  .contact-info-box {
    padding: 2rem;
  }
}
</style>