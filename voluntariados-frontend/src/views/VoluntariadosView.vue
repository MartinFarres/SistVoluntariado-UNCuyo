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
  badge?: string
  badgeClass?: string
  featured?: boolean
}

export default defineComponent({
  name: 'VoluntariadosView',
  components: {
    AppNavBar,
    VoluntariadoCard,
    CTASection
  },
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      selectedLocation: '',
      selectedDate: '',
      
      categories: [
        'Todas',
        'Educación',
        'Medio Ambiente',
        'Salud',
        'Cultura',
        'Deportes',
        'Tecnología',
        'Derechos Humanos',
        'Desarrollo Social'
      ],
      
      locations: [
        'Todas',
        'Mendoza',
        'Godoy Cruz',
        'Luján de Cuyo',
        'Las Heras',
        'Maipú',
        'Guaymallén'
      ],
      
      // Featured voluntariados
      featuredVoluntariados: [
        {
          id: 1,
          title: 'Sed ut perspiciatis',
          description: 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.',
          category: 'Educación',
          location: 'Mendoza',
          date: '15 Nov 2025',
          badge: 'Destacado',
          badgeClass: 'bg-warning',
          featured: true
        },
        {
          id: 2,
          title: 'Lorem ipsum dolor',
          description: 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam.',
          category: 'Medio Ambiente',
          location: 'Godoy Cruz',
          date: '20 Nov 2025',
          badge: 'Nuevo',
          badgeClass: 'bg-success',
          featured: true
        },
        {
          id: 3,
          title: 'Nemo enim ipsam',
          description: 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti.',
          category: 'Salud',
          location: 'Luján de Cuyo',
          date: '25 Nov 2025',
          badge: 'Popular',
          badgeClass: 'bg-primary',
          featured: true
        }
      ],
      
      // All voluntariados by organization
      voluntariadosByOrganization: [
        {
          organizationName: 'Cruz Roja Argentina',
          organizationLogo: 'https://via.placeholder.com/60',
          voluntariados: [
            {
              id: 4,
              title: 'Sed ut perspiciatis unde omnis',
              description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit.',
              category: 'Salud',
              location: 'Mendoza',
              date: '1 Dic 2025'
            },
            {
              id: 5,
              title: 'Lorem ipsum dolor sit',
              description: 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium totam rem.',
              category: 'Educación',
              location: 'Godoy Cruz',
              date: '5 Dic 2025'
            }
          ]
        },
        {
          organizationName: 'Fundación Naturaleza',
          organizationLogo: 'https://via.placeholder.com/60',
          voluntariados: [
            {
              id: 6,
              title: 'Nemo enim ipsam voluptatem',
              description: 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti.',
              category: 'Medio Ambiente',
              location: 'Las Heras',
              date: '10 Dic 2025'
            },
            {
              id: 7,
              title: 'Quis autem vel eum',
              description: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid.',
              category: 'Medio Ambiente',
              location: 'Maipú',
              date: '15 Dic 2025'
            },
            {
              id: 8,
              title: 'Temporibus autem quibusdam',
              description: 'Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi.',
              category: 'Educación',
              location: 'Guaymallén',
              date: '20 Dic 2025'
            }
          ]
        },
        {
          organizationName: 'Techo Mendoza',
          organizationLogo: 'https://via.placeholder.com/60',
          voluntariados: [
            {
              id: 9,
              title: 'Itaque earum rerum',
              description: 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.',
              category: 'Desarrollo Social',
              location: 'Mendoza',
              date: '22 Dic 2025'
            }
          ]
        }
      ]
    }
  },
  computed: {
    filteredFeaturedVoluntariados(): Voluntariado[] {
      return this.filterVoluntariados(this.featuredVoluntariados)
    },
    
    filteredVoluntariadosByOrganization() {
      return this.voluntariadosByOrganization.map(org => ({
        ...org,
        voluntariados: this.filterVoluntariados(org.voluntariados)
      })).filter(org => org.voluntariados.length > 0)
    }
  },
  methods: {
    filterVoluntariados(voluntariados: Voluntariado[]): Voluntariado[] {
      return voluntariados.filter(v => {
        const matchesSearch = !this.searchQuery || 
          v.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          v.description.toLowerCase().includes(this.searchQuery.toLowerCase())
        
        const matchesCategory = !this.selectedCategory || 
          this.selectedCategory === 'Todas' || 
          v.category === this.selectedCategory
        
        const matchesLocation = !this.selectedLocation || 
          this.selectedLocation === 'Todas' || 
          v.location === this.selectedLocation
        
        return matchesSearch && matchesCategory && matchesLocation
      })
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.selectedCategory = ''
      this.selectedLocation = ''
      this.selectedDate = ''
    },
    
    viewVoluntariado(id: number) {
      // Navigate to detail page
      this.$router.push(`/voluntariados/${id}`)
    }
  }
})
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
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
              tempor incididunt ut labore et dolore magna aliqua
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Filters Section -->
    <section class="filters-section py-4 bg-light">
      <div class="container">
        <div class="row g-3">
          <div class="col-md-4">
            <div class="filter-group">
              <label class="filter-label">
                <i class="bi bi-search me-2"></i>Buscar
              </label>
              <input 
                v-model="searchQuery"
                type="text" 
                class="form-control" 
                placeholder="Buscar voluntariados..."
              >
            </div>
          </div>
          
          <div class="col-md-3">
            <div class="filter-group">
              <label class="filter-label">
                <i class="bi bi-tag me-2"></i>Categoría
              </label>
              <select v-model="selectedCategory" class="form-select">
                <option value="">Todas las categorías</option>
                <option v-for="cat in categories.slice(1)" :key="cat" :value="cat">
                  {{ cat }}
                </option>
              </select>
            </div>
          </div>
          
          <div class="col-md-3">
            <div class="filter-group">
              <label class="filter-label">
                <i class="bi bi-geo-alt me-2"></i>Ubicación
              </label>
              <select v-model="selectedLocation" class="form-select">
                <option value="">Todas las ubicaciones</option>
                <option v-for="loc in locations.slice(1)" :key="loc" :value="loc">
                  {{ loc }}
                </option>
              </select>
            </div>
          </div>
          
          <div class="col-md-2 d-flex align-items-end">
            <button 
              @click="clearFilters" 
              class="btn btn-outline-secondary w-100"
            >
              <i class="bi bi-x-circle me-2"></i>Limpiar
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Voluntariados -->
    <section class="featured-voluntariados py-5">
      <div class="container">
        <h2 class="section-title mb-4">Voluntariados Destacados</h2>
        
        <div v-if="filteredFeaturedVoluntariados.length > 0" class="row g-4">
          <div 
            v-for="voluntariado in filteredFeaturedVoluntariados" 
            :key="voluntariado.id"
            class="col-md-6 col-lg-4"
          >
            <VoluntariadoCard 
              :title="voluntariado.title"
              :description="voluntariado.description"
              :category="voluntariado.category"
              :location="voluntariado.location"
              :date="voluntariado.date"
              :badge="voluntariado.badge"
              :badge-class="voluntariado.badgeClass"
              :image-url="voluntariado.imageUrl"
              @view="viewVoluntariado(voluntariado.id)"
            />
          </div>
        </div>
        
        <div v-else class="text-center py-5">
          <i class="bi bi-search display-1 text-muted mb-3"></i>
          <p class="text-muted">No se encontraron voluntariados con los filtros seleccionados</p>
        </div>
      </div>
    </section>

    <!-- Voluntariados by Organization -->
    <section class="voluntariados-by-org py-5 bg-light">
      <div class="container">
        <h2 class="section-title mb-4">Voluntariados por Organización</h2>
        
        <div v-if="filteredVoluntariadosByOrganization.length > 0">
          <div 
            v-for="(org, index) in filteredVoluntariadosByOrganization" 
            :key="index"
            class="organization-section mb-5"
          >
            <!-- Organization Header -->
            <div class="organization-header mb-4">
              <div class="org-logo">
                <img :src="org.organizationLogo" :alt="org.organizationName">
              </div>
              <h3 class="org-name">{{ org.organizationName }}</h3>
            </div>
            
            <!-- Organization's Voluntariados -->
            <div class="row g-4">
              <div 
                v-for="voluntariado in org.voluntariados" 
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
  </div>
</template>

<style scoped>
.voluntariados-page {
  min-height: 100vh;
  background: #f8f9fa;
}

/* Page Header */
.page-header {
  background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
  padding: 4rem 0 3rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.page-header .container {
  position: relative;
  z-index: 2;
}

.page-title {
  font-size: 3rem;
  font-weight: 800;
  text-shadow: 2px 4px 8px rgba(0, 0, 0, 0.3);
  margin-bottom: 1rem;
}

.page-subtitle {
  font-size: 1.2rem;
  opacity: 0.95;
  max-width: 700px;
  margin: 0 auto;
}

/* Filters Section */
.filters-section {
  border-bottom: 2px solid #dee2e6;
  background: white !important;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.filter-label i {
  color: #8B0000;
}

.form-control,
.form-select {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
  border-color: #8B0000;
  box-shadow: 0 0 0 0.2rem rgba(139, 0, 0, 0.1);
}

.btn-outline-secondary {
  border: 2px solid #6c757d;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline-secondary:hover {
  background: #6c757d;
  border-color: #6c757d;
  transform: translateY(-2px);
}

/* Section Titles */
.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  position: relative;
  padding-bottom: 1rem;
  margin-bottom: 2rem;
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

/* Featured Voluntariados */
.featured-voluntariados {
  background: white;
}

/* Organization Section */
.organization-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
}

.organization-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e9ecef;
}

.org-logo {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #e9ecef;
  flex-shrink: 0;
}

.org-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 0.5rem;
}

.org-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

/* Empty State */
.bi-search.display-1 {
  font-size: 4rem;
}

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .organization-header {
    flex-direction: column;
    text-align: center;
  }
}
</style>