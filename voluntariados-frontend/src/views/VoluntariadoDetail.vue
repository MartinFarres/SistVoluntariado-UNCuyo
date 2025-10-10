<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import VoluntariadoCard from '@/components/landing/VoluntariadoCard.vue'
import CTASection from '@/components/landing/CTASection.vue'

interface Turno {
  id: number
  day: string
  date: string
  time: string
  spots: number
  location: string
}

interface SimilarVoluntariado {
  id: number
  title: string
  description: string
  imageUrl?: string
  isFree?: boolean
  tags: string[]
}

export default defineComponent({
  name: 'VoluntariadoDetail',
  components: {
    AppNavBar,
    VoluntariadoCard,
    CTASection
  },
  data() {
    return {
      voluntariadoId: 0,
      voluntariado: {
        title: 'Voluntariado',
        organization: 'Nombre Organización',
        organizationId: 1,
        organizationLogo: 'https://via.placeholder.com/150',
        image: 'https://via.placeholder.com/600x400',
        tags: ['Tag 1', 'Tag 2', 'Tag 3', 'Tag 4', 'Tag 5'],
        description: `Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.

Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.

Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.`,
        schedule: [
          { day: 'Lunes - Viernes', time: '08:00 - 23:00' },
          { day: 'Sábado - Domingo', time: '15:00 - 20:00' }
        ]
      },
      turnos: [
        { id: 1, day: 'Lunes', date: 'Nov 15, 2025', time: '9:00 AM - 12:00 PM', spots: 5, location: 'Mendoza' },
        { id: 2, day: 'Martes', date: 'Nov 16, 2025', time: '2:00 PM - 5:00 PM', spots: 3, location: 'Godoy Cruz' },
        { id: 3, day: 'Miércoles', date: 'Nov 17, 2025', time: '10:00 AM - 1:00 PM', spots: 8, location: 'Las Heras' },
        { id: 4, day: 'Jueves', date: 'Nov 18, 2025', time: '3:00 PM - 6:00 PM', spots: 4, location: 'Luján' },
        { id: 5, day: 'Viernes', date: 'Nov 19, 2025', time: '9:00 AM - 12:00 PM', spots: 6, location: 'Maipú' },
        { id: 6, day: 'Sábado', date: 'Nov 20, 2025', time: '11:00 AM - 2:00 PM', spots: 2, location: 'Mendoza' }
      ],
      organizacionVoluntariados: [
        {
          id: 101,
          title: 'Sed ut perspiciatis unde omnis',
          description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
          isFree: true,
          tags: ['Educación', 'Niños', 'Mendoza']
        },
        {
          id: 102,
          title: 'Lorem ipsum dolor sit',
          description: 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores.',
          isFree: false,
          tags: ['Salud', 'Adultos', 'Godoy Cruz']
        }
      ],
      similarVoluntariados: [
        {
          id: 201,
          title: 'Sed ut perspiciatis',
          description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
          isFree: true,
          tags: ['Educación', 'Cultura', 'Arte']
        },
        {
          id: 202,
          title: 'Lorem ipsum dolor',
          description: 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos.',
          isFree: true,
          tags: ['Medio Ambiente', 'Naturaleza', 'Sustentabilidad']
        },
        {
          id: 203,
          title: 'Nemo enim ipsam',
          description: 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque.',
          isFree: true,
          tags: ['Salud', 'Bienestar', 'Comunidad']
        },
        {
          id: 204,
          title: 'Sed ut perspiciatis',
          description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
          isFree: true,
          tags: ['Tecnología', 'Innovación', 'Digital']
        },
        {
          id: 205,
          title: 'Lorem ipsum dolor',
          description: 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos.',
          isFree: true,
          tags: ['Deportes', 'Juventud', 'Recreación']
        },
        {
          id: 206,
          title: 'Nemo enim ipsam',
          description: 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque.',
          isFree: true,
          tags: ['Arte', 'Expresión', 'Cultura']
        }
      ],
      showAllTurnos: false,
      showAllOrgVoluntariados: false,
      showAllSimilar: false
    }
  },
  computed: {
    displayedTurnos(): Turno[] {
      return this.showAllTurnos ? this.turnos : this.turnos.slice(0, 2)
    },
    displayedOrgVoluntariados(): SimilarVoluntariado[] {
      return this.showAllOrgVoluntariados ? this.organizacionVoluntariados : this.organizacionVoluntariados.slice(0, 2)
    },
    displayedSimilarVoluntariados(): SimilarVoluntariado[] {
      return this.showAllSimilar ? this.similarVoluntariados : this.similarVoluntariados.slice(0, 3)
    }
  },
  created() {
    this.voluntariadoId = parseInt(this.$route.params.id as string)
    this.loadVoluntariado()
  },
  methods: {
    async loadVoluntariado() {
      // TODO: Fetch voluntariado data from API
      console.log('Loading voluntariado:', this.voluntariadoId)
    },
    inscribirse() {
      // TODO: Implement enrollment logic
      this.$router.push(`/voluntariados/${this.voluntariadoId}/inscripcion`)
    },
    enrollInTurno(turnoId: number) {
      // TODO: Implement turno enrollment
      console.log('Enrolling in turno:', turnoId)
    },
    viewOrganization() {
      this.$router.push(`/organizaciones/${this.voluntariado.organizationId}`)
    },
    viewVoluntariado(id: number) {
      this.$router.push(`/voluntariados/${id}`)
      window.scrollTo(0, 0)
    }
  }
})
</script>

<template>
  <div class="voluntariado-detail">
    <AppNavBar />
    
    <!-- Hero Section -->
    <section class="voluntariado-hero">
      <div class="hero-overlay"></div>
      <div class="container">
        <div class="row">
          <div class="col-lg-10 mx-auto">
            <div class="text-center mb-4">
              <h2 class="organization-name-hero" @click="viewOrganization" style="cursor: pointer;">
                {{ voluntariado.organization }}
              </h2>
            </div>
            
            <!-- Main Card -->
            <div class="voluntariado-card">
              <div class="row">
                <!-- Image -->
                <div class="col-md-4">
                  <div class="voluntariado-image">
                    <img :src="voluntariado.image" :alt="voluntariado.title">
                  </div>
                </div>
                
                <!-- Info -->
                <div class="col-md-8">
                  <div class="voluntariado-info">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                      <h1 class="voluntariado-title">{{ voluntariado.title }}</h1>
                      <button 
                        class="btn btn-primary"
                        @click="inscribirse"
                      >
                        Unirme
                      </button>
                    </div>
                    
                    <!-- Tags -->
                    <div class="voluntariado-tags mb-3">
                      <span 
                        v-for="(tag, index) in voluntariado.tags" 
                        :key="index"
                        class="badge bg-secondary me-2 mb-2"
                      >
                        {{ tag }}
                      </span>
                    </div>
                    
                    <!-- Schedule -->
                    <div class="schedule-info">
                      <div 
                        v-for="(schedule, index) in voluntariado.schedule" 
                        :key="index"
                        class="schedule-item"
                      >
                        <strong>{{ schedule.day }}</strong>
                        <span>{{ schedule.time }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Description Section -->
    <section class="description-section py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <div class="description-content">
              <p v-for="(paragraph, index) in voluntariado.description.split('\n\n')" :key="index" class="mb-4">
                {{ paragraph }}
              </p>
              <div class="text-center mt-4">
                <button class="btn btn-outline-secondary">
                  Ver Más
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Voluntariados por Organización Section -->
    <section class="org-voluntariados-section py-5 bg-light">
      <div class="container">
        <div class="section-header mb-4">
          <h2 class="section-title">Voluntariados por Organización</h2>
          <p class="section-subtitle">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
          </p>
        </div>
        
        <div class="row g-4 mb-4">
          <div class="col-md-6">
            <div class="map-placeholder">
              <i class="bi bi-geo-alt-fill"></i>
              <p>Mapa de ubicación</p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="org-info-card">
              <h3 class="card-title">Sed ut perspiciatis unde omnis</h3>
              <p class="card-description">
                Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut 
                odit aut fugit, sed quia consequuntur magni dolores eos qui 
                ratione voluptatem sequi nesciunt. Neque porro quisquam est, 
                vel dolorem eum qui qua sit amet et urna.
              </p>
            </div>
          </div>
        </div>
        
        <!-- Turnos Grid -->
        <div class="row g-3 mb-4">
          <div 
            v-for="turno in displayedTurnos" 
            :key="turno.id"
            class="col-md-6 col-lg-4"
          >
            <div class="turno-card">
              <div class="turno-header">
                <div>
                  <div class="turno-day">{{ turno.day }}</div>
                  <div class="turno-label">Heart List</div>
                </div>
                <button class="btn btn-sm btn-dark" @click="enrollInTurno(turno.id)">
                  Apply
                </button>
              </div>
              <div class="turno-details">
                <p class="turno-text">{{ turno.date }} {{ turno.time }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Organization Voluntariados Cards -->
        <div class="row g-4 mb-4">
          <div 
            v-for="vol in displayedOrgVoluntariados" 
            :key="vol.id"
            class="col-md-6"
          >
            <div class="simple-card">
              <div class="card-image-placeholder">
                <i class="bi bi-image"></i>
              </div>
              <div class="card-content">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h4 class="card-title-small">{{ vol.title }}</h4>
                  <span v-if="vol.isFree" class="badge bg-success">FREE</span>
                </div>
                <p class="card-description-small">{{ vol.description }}</p>
                <div class="card-tags">
                  <span 
                    v-for="(tag, idx) in vol.tags" 
                    :key="idx"
                    class="tag-item"
                  >
                    <i class="bi bi-tag-fill me-1"></i>{{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="text-center" v-if="!showAllOrgVoluntariados && organizacionVoluntariados.length > 2">
          <button 
            class="btn btn-outline-secondary"
            @click="showAllOrgVoluntariados = true"
          >
            Ver más voluntariados de esta organización
          </button>
        </div>
      </div>
    </section>

    <!-- Voluntariados Similares Section -->
    <section class="similar-voluntariados-section py-5">
      <div class="container">
        <h2 class="section-title mb-4">Voluntariados Similares</h2>
        
        <div class="row g-4 mb-4">
          <div 
            v-for="vol in displayedSimilarVoluntariados" 
            :key="vol.id"
            class="col-md-6 col-lg-4"
          >
            <div class="simple-card" @click="viewVoluntariado(vol.id)" style="cursor: pointer;">
              <div class="card-image-placeholder">
                <i class="bi bi-image"></i>
              </div>
              <div class="card-content">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h4 class="card-title-small">{{ vol.title }}</h4>
                  <span v-if="vol.isFree" class="badge bg-success">FREE</span>
                </div>
                <p class="card-description-small">{{ vol.description }}</p>
                <div class="card-tags">
                  <span 
                    v-for="(tag, idx) in vol.tags" 
                    :key="idx"
                    class="tag-item"
                  >
                    <i class="bi bi-tag-fill me-1"></i>{{ tag }}
                  </span>
                </div>
                <button class="btn btn-sm btn-outline-primary mt-3 w-100">
                  Leer más
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="text-center" v-if="!showAllSimilar && similarVoluntariados.length > 3">
          <button 
            class="btn btn-outline-secondary"
            @click="showAllSimilar = true"
          >
            Ver más voluntariados similares
          </button>
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
.voluntariado-detail {
  min-height: 100vh;
  background: #f8f9fa;
}

/* Hero Section */
.voluntariado-hero {
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

.voluntariado-hero .container {
  position: relative;
  z-index: 2;
}

.organization-name-hero {
  font-size: 1.8rem;
  font-weight: 300;
  color: #495057;
  margin-bottom: 2rem;
  transition: color 0.3s ease;
}

.organization-name-hero:hover {
  color: #8B0000;
}

/* Voluntariado Card */
.voluntariado-card {
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
}

.voluntariado-image {
  width: 100%;
  height: 250px;
  border-radius: 8px;
  overflow: hidden;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
}

.voluntariado-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.voluntariado-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.voluntariado-tags .badge {
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.schedule-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.schedule-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 6px;
  font-size: 0.95rem;
}

.schedule-item strong {
  color: #2c3e50;
}

.schedule-item span {
  color: #6c757d;
}

/* Description Section */
.description-section {
  background: white;
}

.description-content {
  color: #495057;
  font-size: 1rem;
  line-height: 1.8;
}

.description-content p {
  text-align: justify;
}

/* Section Headers */
.section-header {
  text-align: center;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  color: #6c757d;
  font-size: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

/* Map and Info Card */
.map-placeholder {
  background: #e9ecef;
  border-radius: 12px;
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}

.map-placeholder i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.org-info-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  height: 100%;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
}

.org-info-card .card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.org-info-card .card-description {
  color: #6c757d;
  line-height: 1.7;
}

/* Turno Cards */
.turno-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.turno-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(139, 0, 0, 0.15);
}

.turno-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.turno-day {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
}

.turno-label {
  font-size: 0.85rem;
  color: #6c757d;
}

.turno-details {
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.turno-text {
  color: #495057;
  font-size: 0.9rem;
  margin: 0;
}

/* Simple Cards */
.simple-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.simple-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(139, 0, 0, 0.15);
}

.card-image-placeholder {
  width: 100%;
  height: 200px;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #adb5bd;
}

.card-image-placeholder i {
  font-size: 3rem;
}

.card-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title-small {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.card-description-small {
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.6;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  font-size: 0.75rem;
  color: #6c757d;
  padding: 0.25rem 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.tag-item i {
  font-size: 0.65rem;
}

/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #8B0000, #DC143C);
  border: none;
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(139, 0, 0, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(139, 0, 0, 0.3);
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

.btn-dark {
  background: #2c3e50;
  border: none;
  border-radius: 4px;
  font-weight: 600;
}

.btn-dark:hover {
  background: #1a252f;
}

/* Responsive */
@media (max-width: 768px) {
  .organization-name-hero {
    font-size: 1.4rem;
  }
  
  .voluntariado-title {
    font-size: 1.4rem;
  }
  
  .voluntariado-card {
    padding: 1.5rem;
  }
  
  .voluntariado-image {
    height: 200px;
    margin-bottom: 1.5rem;
  }
  
  .btn-primary {
    width: 100%;
    margin-top: 1rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
}
</style>