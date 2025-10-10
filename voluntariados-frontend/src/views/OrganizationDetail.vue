<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import VoluntariadoCard from '@/components/landing/VoluntariadoCard.vue'
import CTASection from '@/components/landing/CTASection.vue'

interface Voluntariado {
  id: number
  title: string
  description: string
  category: string
  location: string
  date?: string
  imageUrl?: string
}

export default defineComponent({
  name: 'OrganizationDetail',
  components: {
    AppNavBar,
    VoluntariadoCard,
    CTASection
  },
  data() {
    return {
      organizationId: 0,
      organization: {
        name: 'Nombre Organización',
        slogan: 'Frase / Slogan Org.',
        logo: 'https://via.placeholder.com/150',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore',
        tags: ['Tag 1', 'Tag 2', 'Tag 3', 'Tag 4', 'Tag 5'],
        contact: {
          email: 'contacto@organizacion.com',
          phone: '+54 261 123-4567',
          website: 'www.organizacion.com'
        },
        stats: [
          { label: 'Voluntarios Activos', value: '150+' },
          { label: 'Proyectos Completados', value: '45' },
          { label: 'Horas de Voluntariado', value: '5000+' }
        ]
      },
      proximosVoluntariados: [
        {
          id: 1,
          title: 'Sed ut perspiciatis',
          description: 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia.',
          category: 'Educación',
          location: 'Mendoza',
          date: '15 Nov 2025'
        },
        {
          id: 2,
          title: 'Lorem ipsum dolor',
          description: 'Amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.',
          category: 'Medio Ambiente',
          location: 'Godoy Cruz',
          date: '20 Nov 2025'
        },
        {
          id: 3,
          title: 'Nemo enim ipsam',
          description: 'Consectetur magni dolores eos qui ratione voluptatem sequi nesciunt.',
          category: 'Salud',
          location: 'Las Heras',
          date: '25 Nov 2025'
        }
      ]
    }
  },
  created() {
    this.organizationId = parseInt(this.$route.params.id as string)
    this.loadOrganization()
  },
  methods: {
    async loadOrganization() {
      // TODO: Fetch organization data from API
      console.log('Loading organization:', this.organizationId)
    },
    viewVoluntariado(id: number) {
      this.$router.push(`/voluntariados/${id}`)
    },
    contactOrganization() {
      // TODO: Implement contact logic
      console.log('Contact organization')
    },
    followOrganization() {
      // TODO: Implement follow logic
      console.log('Follow organization')
    }
  }
})
</script>

<template>
  <div class="organization-detail">
    <AppNavBar />
    
    <!-- Hero Section with Organization Info -->
    <section class="organization-hero">
      <div class="hero-overlay"></div>
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
                  <div class="organization-logo">
                    <img :src="organization.logo" :alt="organization.name">
                  </div>
                </div>
                
                <!-- Info -->
                <div class="col-md-9">
                  <div class="organization-info">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                      <h1 class="organization-name">{{ organization.name }}</h1>
                      <button 
                        class="btn btn-outline-primary btn-sm"
                        @click="followOrganization"
                      >
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
                      <button class="btn btn-sm btn-outline-secondary me-2 mb-2">
                        <i class="bi bi-envelope me-1"></i>
                        {{ organization.contact.email }}
                      </button>
                      <button class="btn btn-sm btn-outline-secondary me-2 mb-2">
                        <i class="bi bi-telephone me-1"></i>
                        {{ organization.contact.phone }}
                      </button>
                      <button class="btn btn-sm btn-outline-secondary mb-2">
                        <i class="bi bi-globe me-1"></i>
                        {{ organization.contact.website }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Proximos Voluntariados Section -->
    <section class="proximos-voluntariados py-5">
      <div class="container">
        <h2 class="section-title mb-4">Próximos Voluntariados</h2>
        
        <div class="row g-4 mb-4">
          <div 
            v-for="voluntariado in proximosVoluntariados" 
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
        
        <div class="text-center">
            <router-link
            to="/voluntariados"
            class="btn btn-outline-secondary btn-lg"
            >
                Ver Voluntariados
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
  </div>
</template>

<style scoped>
.organization-detail {
  min-height: 100vh;
  background: #f8f9fa;
}

/* Hero Section */
.organization-hero {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  padding: 3rem 0 4rem;
  position: relative;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.5);
  z-index: 1;
}

.organization-hero .container {
  position: relative;
  z-index: 2;
}

.organization-slogan {
  font-size: 1.8rem;
  font-weight: 300;
  color: #495057;
  margin-bottom: 2rem;
}

/* Organization Card */
.organization-card {
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
}

.organization-logo {
  width: 100%;
  max-width: 150px;
  height: 150px;
  margin: 0 auto;
  border: 3px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
}

.organization-logo img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.organization-name {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.organization-tags .badge {
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.organization-description {
  color: #6c757d;
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.contact-buttons .btn {
  border-radius: 20px;
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
}

.contact-buttons .btn:hover {
  background: #8B0000;
  color: white;
  border-color: #8B0000;
  transform: translateY(-2px);
}

/* Section Title */
.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  position: relative;
  padding-bottom: 1rem;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #8B0000, #DC143C);
  border-radius: 2px;
}

/* Proximos Voluntariados */
.proximos-voluntariados {
  background: white;
}

.btn-outline-secondary {
  border: 2px solid #6c757d;
  color: #6c757d;
  border-radius: 50px;
  padding: 0.75rem 2rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline-secondary:hover {
  background: #6c757d;
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(108, 117, 125, 0.3);
}

.btn-outline-primary {
  border: 2px solid #8B0000;
  color: #8B0000;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: #8B0000;
  border-color: #8B0000;
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .organization-slogan {
    font-size: 1.4rem;
  }
  
  .organization-name {
    font-size: 1.5rem;
  }
  
  .organization-card {
    padding: 1.5rem;
  }
  
  .organization-logo {
    max-width: 120px;
    height: 120px;
    margin-bottom: 1.5rem;
  }
  
  .contact-buttons .btn {
    width: 100%;
    margin-right: 0 !important;
  }
}
</style>