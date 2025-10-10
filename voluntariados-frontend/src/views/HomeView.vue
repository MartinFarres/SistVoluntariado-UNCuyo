<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import HeroSection from '@/components/landing/HeroSection.vue'
import InfoSection from '@/components/landing/InfoSection.vue'
import VoluntariadoCard from '@/components/landing/VoluntariadoCard.vue'
import TestimonialsSection from '@/components/landing/TestimonialsSection.vue'
import OrganizationsSection from '@/components/landing/OrganizationsSection.vue'
import HowItWorksSection from '@/components/landing/HowItWorksSection.vue'
import TeamSection from '@/components/landing/TeamSection.vue'
import CTASection from '@/components/landing/CTASection.vue'

export default defineComponent({
  name: 'HomeView',
  components: {
    AppNavBar,
    HeroSection,
    InfoSection,
    VoluntariadoCard,
    TestimonialsSection,
    OrganizationsSection,
    HowItWorksSection,
    TeamSection,
    CTASection
  },
  data() {
    return {
      // Info Section Data
      infoItems: [
        {
          icon: 'bi-lightbulb',
          title: 'Iniciativa',
          description: 'Descubrí oportunidades únicas para generar un impacto positivo en tu comunidad universitaria y más allá. Cada voluntariado es una oportunidad para crecer.'
        },
        {
          icon: 'bi-trophy',
          title: 'Objetivos',
          description: 'Alcanzá tus metas personales y profesionales mientras ayudás a otros. Desarrollá habilidades, expandí tu red de contactos y construí un currículum destacado.'
        },
        {
          icon: 'bi-flag',
          title: 'Misión',
          description: 'Nuestra misión es conectar estudiantes comprometidos con organizaciones que necesitan su talento y energía para crear un mundo mejor.'
        },
        {
          icon: 'bi-people',
          title: 'Para los Estudiantes',
          description: 'Accedé a una amplia variedad de oportunidades de voluntariado diseñadas especialmente para estudiantes universitarios que quieren marcar la diferencia.'
        }
      ],
      
      // Featured Voluntariados
      featuredVoluntariados: [
        {
          title: 'Sed ut perspiciatis',
          description: 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione.',
          category: 'Educación',
          location: 'Mendoza',
          badge: 'Nuevo',
          badgeClass: 'bg-success'
        },
        {
          title: 'Lorem ipsum dolor',
          description: 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium totam rem aperiam.',
          category: 'Medio Ambiente',
          location: 'Godoy Cruz',
          badge: 'Destacado',
          badgeClass: 'bg-warning'
        },
        {
          title: 'Nemo enim ipsam',
          description: 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti.',
          category: 'Salud',
          location: 'Luján de Cuyo',
          badge: 'Popular',
          badgeClass: 'bg-primary'
        }
      ],
      
      // Testimonials
      testimonials: [
        {
          name: 'Sed ut perspiciatis',
          role: 'Estudiante de Medicina',
          text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.'
        },
        {
          name: 'Lorem ipsum dolor',
          role: 'Estudiante de Ingeniería',
          text: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.'
        },
        {
          name: 'Nemo enim ipsam',
          role: 'Estudiante de Derecho',
          text: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. Quis autem vel eum iure reprehenderit.'
        }
      ],
      
      // Organizations
      organizations: [
        { name: 'Cruz Roja' },
        { name: 'Cáritas' },
        { name: 'UNICEF' },
        { name: 'Fundación SI' },
        { name: 'Techo' },
        { name: 'Greenpeace' },
        { name: 'Banco de Alimentos' },
        { name: 'Fundación Huésped' }
      ],
      
      // How it Works Steps
      howItWorksSteps: [
        {
          title: '1. Registrate',
          description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.'
        },
        {
          title: '2. Explora Voluntariados',
          description: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.'
        },
        {
          title: '3. Consulta los Detalles',
          description: 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.'
        },
        {
          title: '4. Participa',
          description: 'Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore.'
        },
        {
          title: '5. Inscribite en Capacitaciones',
          description: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur.'
        },
        {
          title: '6. Recibi tu Certificado',
          description: 'Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas.'
        }
      ],
      
      // Team Members
      teamMembers: [
        { name: 'Juan Pérez', role: 'Director' },
        { name: 'María González', role: 'Coordinadora' },
        { name: 'Carlos Rodríguez', role: 'Voluntario Senior' },
        { name: 'Ana Martínez', role: 'Administradora' }
      ]
    }
  }
})
</script>

<template>
  <div class="home">
    <AppNavBar />
    
    <!-- Hero Section -->
    <HeroSection 
      title="Convertite en el cambio que querés ver."
      subtitle="¡Sumáte a los voluntariados!"
    />
    
    <!-- What is University Volunteering -->
    <InfoSection 
      title="¿Qué es el Voluntariado Universitario?"
      :items="infoItems"
    />
    
    <!-- Featured Voluntariados -->
    <section class="featured-section py-5">
      <div class="container">
        <h2 class="section-title text-center mb-3">
          Algunos de Nuestros Voluntariados
        </h2>
        <p class="section-subtitle text-center mb-5">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
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
              :category="voluntariado.category"
              :location="voluntariado.location"
              :badge="voluntariado.badge"
              :badge-class="voluntariado.badgeClass"
              @view="() => $router.push('/voluntariados')"
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
    <CTASection 
      title="¡Inscríbete hoy y marca la diferencia!"
      primary-text="Comenzar ahora"
      primary-link="/signup"
      secondary-text="Ver más información"
      secondary-link="/about"
    />
  </div>
</template>

<style scoped>
.home {
  overflow-x: hidden;
}

.featured-section {
  background: white;
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
  max-width: 800px;
  margin: 0 auto;
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

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}
</style>