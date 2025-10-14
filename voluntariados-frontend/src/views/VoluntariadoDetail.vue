<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent } from 'vue'
import AppNavBar from '@/components/Navbar.vue'
import VoluntariadoCard from '@/components/landing/VoluntariadoCard.vue'
import CTASection from '@/components/landing/CTASection.vue'
import JoinConfirmationModal from '@/components/landing/JoinConfirmationModal.vue'
import { voluntariadoAPI, turnoAPI, organizacionAPI } from '@/services/api'
import authService from '@/services/authService'

interface Turno {
  id: number
  fecha: string
  hora_inicio: string
  hora_fin: string
  cupo: number
  lugar?: string
}

interface Voluntariado {
  id: number
  nombre: string
  descripcion?: any
  estado: string
  fecha_inicio?: string
  fecha_fin?: string
  turno?: number
  gestionadores?: number
}

interface Organizacion {
  id: number
  nombre: string
  descripcion?: string
  contacto_email?: string
  localidad?: number
  voluntariado?: number
}

export default defineComponent({
  name: 'VoluntariadoDetail',
  components: {
    AppNavBar,
    VoluntariadoCard,
    CTASection,
    JoinConfirmationModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      voluntariadoId: 0,
      
      voluntariado: {
        title: '',
        organization: '',
        organizationId: 0,
        organizationLogo: 'https://via.placeholder.com/150',
        image: 'https://via.placeholder.com/600x400',
        tags: [] as string[],
        description: '',
        schedule: [] as Array<{ day: string; time: string }>
      },
      
      voluntariadoData: null as Voluntariado | null,

      turnos: [] as Turno[],
      allTurnos: [] as Turno[],
      
      organizacionVoluntariados: [] as any[],
      allOrgVoluntariados: [] as any[],
      
      similarVoluntariados: [] as any[],
      allSimilarVoluntariados: [] as any[],
      
      showAllTurnos: false,
      showAllOrgVoluntariados: false,
      showAllSimilar: false,
      
      isAuthenticated: false,

      // Modal state
      showJoinModal: false,
      joinLoading: false,
      joinSuccess: false,
      selectedTurnoId: null as number | null
    }
  },
  
  computed: {
    displayedTurnos(): Turno[] {
      return this.showAllTurnos ? this.allTurnos : this.allTurnos.slice(0, 2)
    },
    displayedOrgVoluntariados(): any[] {
      return this.showAllOrgVoluntariados ? this.allOrgVoluntariados : this.allOrgVoluntariados.slice(0, 2)
    },
    displayedSimilarVoluntariados(): any[] {
      return this.showAllSimilar ? this.allSimilarVoluntariados : this.allSimilarVoluntariados.slice(0, 3)
    }
  },
  
  async created() {
    this.voluntariadoId = parseInt(this.$route.params.id as string)
    this.isAuthenticated = authService.isAuthenticated()
    await this.loadVoluntariado()
  },
  
  methods: {
    async loadVoluntariado() {
      this.loading = true
      this.error = null
      
      try {
        // Load voluntariado details
        const volRes = await voluntariadoAPI.getById(this.voluntariadoId)
        const volData: Voluntariado = volRes.data
        this.voluntariadoData = volData
        
        // Load all data in parallel
        const [turnosRes, organizacionesRes, allVoluntariadosRes] = await Promise.all([
          turnoAPI.getAll(),
          organizacionAPI.getAll(),
          voluntariadoAPI.getAll()
        ])
        
        // Process voluntariado data
        this.voluntariado.title = volData.nombre
        this.voluntariado.description = this.getDescriptionText(volData.descripcion)
        this.voluntariado.tags = this.generateTags(volData)
        this.voluntariado.schedule = this.generateSchedule(volData)
        
        // Find organization that has this voluntariado
        const org = organizacionesRes.data.find((o: Organizacion) => o.voluntariado === this.voluntariadoId)
        if (org) {
          this.voluntariado.organization = org.nombre
          this.voluntariado.organizationId = org.id
          
          // Load other voluntariados from same organization
          await this.loadOrganizationVoluntariados(org.id, allVoluntariadosRes.data, organizacionesRes.data)
        } else {
          this.voluntariado.organization = 'Organización'
          this.voluntariado.organizationId = 0
        }
        
        // Load turnos
        this.allTurnos = turnosRes.data.filter((t: Turno) => {
          // Filter turnos that might be related to this voluntariado
          // Since Turno doesn't have a direct FK to Voluntariado in the model,
          // we'll show all available turnos for now
          return true
        })
        
        // Load similar voluntariados
        this.loadSimilarVoluntariados(allVoluntariadosRes.data)
        
      } catch (err: any) {
        console.error('Error loading voluntariado:', err)
        this.error = err.response?.data?.detail || 'Error al cargar el voluntariado'
        this.setFallbackData()
      } finally {
        this.loading = false
      }
    },
    
    async loadOrganizationVoluntariados(orgId: number, allVoluntariados: Voluntariado[], allOrganizaciones: Organizacion[]) {
      // Find all voluntariados from this organization
      const orgVoluntariados = allOrganizaciones
        .filter(o => o.id !== orgId) // Exclude current org to avoid duplicates
        .map(o => {
          const vol = allVoluntariados.find(v => v.id === o.voluntariado)
          return vol ? { ...vol, organizacion: o } : null
        })
        .filter(v => v !== null)
        .slice(0, 4)
      
      this.allOrgVoluntariados = orgVoluntariados.map(v => ({
        id: v!.id,
        title: v!.nombre,
        description: this.getDescriptionText(v!.descripcion) || 'Sin descripción',
        isFree: true,
        tags: ['Tag 1', 'Tag 2', 'Tag 3']
      }))
    },
    
    loadSimilarVoluntariados(allVoluntariados: Voluntariado[]) {
      // Get similar voluntariados (same estado, excluding current)
      this.allSimilarVoluntariados = allVoluntariados
        .filter(v => v.id !== this.voluntariadoId && v.estado === 'ACTIVE')
        .slice(0, 6)
        .map(v => ({
          id: v.id,
          title: v.nombre,
          description: this.getDescriptionText(v.descripcion) || 'Sin descripción',
          isFree: true,
          tags: this.generateTags(v)
        }))
    },
    
    getDescriptionText(descripcion: any): string {
      if (!descripcion) return 'Sin descripción disponible'
      if (typeof descripcion === 'string') return descripcion
      if (typeof descripcion === 'object' && descripcion.descripcion) {
        return descripcion.descripcion
      }
      if (typeof descripcion === 'object' && descripcion.resumen) {
        return descripcion.resumen
      }
      return 'Sin descripción disponible'
    },
    
    generateTags(voluntariado: Voluntariado): string[] {
      const tags = []
      if (voluntariado.estado) tags.push(voluntariado.estado)
      if (voluntariado.fecha_inicio) tags.push('Próximamente')
      tags.push('Tag ' + (voluntariado.id % 5 + 1))
      return tags.slice(0, 5)
    },
    
    generateSchedule(voluntariado: Voluntariado): Array<{ day: string; time: string }> {
      const schedule = [
        { day: 'Lunes - Viernes', time: '08:00 - 23:00' },
        { day: 'Sábado - Domingo', time: '15:00 - 20:00' }
      ]
      
      if (voluntariado.fecha_inicio && voluntariado.fecha_fin) {
        schedule.push({
          day: 'Período',
          time: `${this.formatDate(voluntariado.fecha_inicio)} - ${this.formatDate(voluntariado.fecha_fin)}`
        })
      }
      
      return schedule
    },
    
    formatDate(dateString: string): string {
      const date = new Date(dateString)
      return date.toLocaleDateString('es-AR', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      })
    },
    
    formatTime(timeString: string): string {
      return timeString.substring(0, 5) // HH:MM
    },
    
    formatTurnoDate(turno: Turno): string {
      const date = new Date(turno.fecha)
      const dayName = date.toLocaleDateString('es-AR', { weekday: 'long' })
      return dayName.charAt(0).toUpperCase() + dayName.slice(1)
    },
    
    formatTurnoFullDate(turno: Turno): string {
      const date = new Date(turno.fecha)
      return date.toLocaleDateString('es-AR', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      })
    },
    
    inscribirse() {
      if (!this.isAuthenticated) {
        this.$router.push({
          path: '/signup',
          query: { redirect: this.$route.fullPath }
        })
        return
      }
      this.selectedTurnoId = null;
      this.showJoinModal = true;
    },
    
    enrollInTurno(turnoId: number) {
      if (!this.isAuthenticated) {
        this.$router.push({
          path: '/signup',
          query: { redirect: this.$route.fullPath }
        });
        return;
      }
      this.selectedTurnoId = turnoId;
      this.showJoinModal = true;
    },
    
    handleJoinCancel() {
      this.showJoinModal = false;
      this.joinLoading = false;
      this.joinSuccess = false;
      this.selectedTurnoId = null;
    },

    async handleJoinConfirm() {
      this.joinLoading = true;
      this.error = null;

      const turnoIdToEnroll = this.selectedTurnoId || (this.voluntariadoData ? this.voluntariadoData.turno : null);

      if (!turnoIdToEnroll) {
        this.error = "No se ha especificado un turno para la inscripción.";
        this.joinLoading = false;
        alert(this.error);
        this.handleJoinCancel();
        return;
      }

      try {
        await turnoAPI.inscribirse(turnoIdToEnroll);
        this.joinSuccess = true;
        
        setTimeout(() => {
          this.handleJoinCancel();
          this.loadVoluntariado();
        }, 3000);
      } catch (err: any) {
        console.error('Error enrolling in turno:', err);
        this.error = err.response?.data?.detail || 'Error al inscribirse en el turno.';
        this.joinLoading = false;
        alert(this.error);
        this.handleJoinCancel();
      }
    },
    
    viewOrganization() {
      if (this.voluntariado.organizationId) {
        this.$router.push(`/organizaciones/${this.voluntariado.organizationId}`)
      }
    },
    
    viewVoluntariado(id: number) {
      this.$router.push(`/voluntariados/${id}`)
      window.scrollTo(0, 0)
      // Reload data for new voluntariado
      this.voluntariadoId = id
      this.loadVoluntariado()
    },
    
    setFallbackData() {
      this.voluntariado = {
        title: 'Voluntariado',
        organization: 'Nombre Organización',
        organizationId: 1,
        organizationLogo: 'https://via.placeholder.com/150',
        image: 'https://via.placeholder.com/600x400',
        tags: ['Tag 1', 'Tag 2', 'Tag 3'],
        description: 'Descripción del voluntariado no disponible.',
        schedule: [
          { day: 'Lunes - Viernes', time: '08:00 - 23:00' },
          { day: 'Sábado - Domingo', time: '15:00 - 20:00' }
        ]
      }
    }
  }
})
</script>

<template>
  <div class="voluntariado-detail">
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
      <!-- Hero Section -->
      <section class="voluntariado-hero">
        <div class="hero-overlay"></div>
        <div class="container">
          <div class="row">
            <div class="col-lg-10 mx-auto">
              <div class="text-center mb-4">
                <h2 
                  class="organization-name-hero" 
                  @click="viewOrganization" 
                  style="cursor: pointer;"
                >
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
                          {{ isAuthenticated ? 'Unirme' : 'Registrarse para Unirme' }}
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
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Turnos Section -->
      <section class="org-voluntariados-section py-5 bg-light" v-if="allTurnos.length > 0">
        <div class="container">
          <div class="section-header mb-4">
            <h2 class="section-title">Turnos Disponibles</h2>
            <p class="section-subtitle">
              Seleccioná el turno que mejor se adapte a tu disponibilidad
            </p>
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
                    <div class="turno-day">{{ formatTurnoDate(turno) }}</div>
                    <div class="turno-label">{{ turno.lugar || 'Ubicación' }}</div>
                  </div>
                  <button 
                    class="btn btn-sm btn-dark" 
                    @click="enrollInTurno(turno.id)"
                  >
                    {{ isAuthenticated ? 'Inscribirse' : 'Registrarse' }}
                  </button>
                </div>
                <div class="turno-details">
                  <p class="turno-text">
                    {{ formatTurnoFullDate(turno) }} 
                    {{ formatTime(turno.hora_inicio) }} - {{ formatTime(turno.hora_fin) }}
                  </p>
                  <p class="turno-text">
                    <i class="bi bi-people me-2"></i>
                    {{ turno.cupo }} cupos disponibles
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="text-center" v-if="!showAllTurnos && allTurnos.length > 2">
            <button 
              class="btn btn-outline-secondary"
              @click="showAllTurnos = true"
            >
              Ver más turnos
            </button>
          </div>
        </div>
      </section>

      <!-- Organization Voluntariados -->
      <section class="org-voluntariados-section py-5" v-if="allOrgVoluntariados.length > 0">
        <div class="container">
          <h2 class="section-title mb-4">Más de {{ voluntariado.organization }}</h2>
          
          <div class="row g-4 mb-4">
            <div 
              v-for="vol in displayedOrgVoluntariados" 
              :key="vol.id"
              class="col-md-6"
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
                </div>
              </div>
            </div>
          </div>
          
          <div class="text-center" v-if="!showAllOrgVoluntariados && allOrgVoluntariados.length > 2">
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
      <section class="similar-voluntariados-section py-5 bg-light" v-if="allSimilarVoluntariados.length > 0">
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
          
          <div class="text-center" v-if="!showAllSimilar && allSimilarVoluntariados.length > 3">
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
      
      <JoinConfirmationModal
        :show="showJoinModal"
        :voluntariado-title="voluntariado.title"
        :organization-name="voluntariado.organization"
        :loading="joinLoading"
        :show-success="joinSuccess"
        @confirm="handleJoinConfirm"
        @cancel="handleJoinCancel"
      />
    </template>
  </div>
</template>

<style scoped>
.voluntariado-detail {
  min-height: 100vh;
  background: #f8f9fa;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

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
  margin: 0.5rem 0;
}

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

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.btn-dark:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

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
