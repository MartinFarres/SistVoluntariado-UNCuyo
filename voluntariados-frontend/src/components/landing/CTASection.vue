<!-- src/components/landing/CTASection.vue -->
<template>
  <section class="cta-section">
    <div class="cta-overlay"></div>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8 text-center">
          <h2 class="cta-title mb-4">{{ title }}</h2>
          <p class="cta-subtitle mb-5">{{ subtitle }}</p>
          <div class="cta-actions">
            <router-link 
              :to="primaryLink" 
              class="btn btn-light btn-lg me-3 mb-3"
            >
              <i class="bi" :class="primaryIcon"></i>
              {{ primaryText }}
            </router-link>
            <router-link 
              v-if="secondaryText"
              :to="secondaryLink" 
              class="btn btn-outline-light btn-lg mb-3"
            >
              <i class="bi" :class="secondaryIcon"></i>
              {{ secondaryText }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'CTASection',
  props: {
    title: {
      type: String,
      default: '¡Inscríbete hoy y marca la diferencia!'
    },
    subtitle: {
      type: String,
      default: ''
    },
    primaryText: {
      type: String,
      default: 'Comenzar ahora'
    },
    primaryLink: {
      type: String,
      default: '/signup'
    },
    primaryIcon: {
      type: String,
      default: 'bi-arrow-right-circle me-2'
    },
    secondaryText: {
      type: String,
      default: ''
    },
    secondaryLink: {
      type: String,
      default: '/contact'
    },
    secondaryIcon: {
      type: String,
      default: 'bi-envelope me-2'
    }
  }
})
</script>

<style scoped>
.cta-section {
  position: relative;
  padding: 6rem 0;
  background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120"><path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" fill="%23fff"/></svg>') no-repeat top;
  background-size: cover;
  opacity: 0.1;
}

.cta-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.container {
  position: relative;
  z-index: 2;
}

.cta-title {
  font-size: 2.8rem;
  font-weight: 800;
  color: white;
  text-shadow: 2px 4px 8px rgba(0, 0, 0, 0.3);
  margin-bottom: 1.5rem;
}

.cta-subtitle {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 300;
}

.btn-light {
  background: white;
  color: #8B0000;
  border: none;
  padding: 1rem 2.5rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-light:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  background: #f8f9fa;
  color: #8B0000;
}

.btn-outline-light {
  border: 2px solid white;
  color: white;
  padding: 1rem 2.5rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background: white;
  color: #8B0000;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .cta-title {
    font-size: 2rem;
  }
  
  .cta-subtitle {
    font-size: 1.1rem;
  }
  
  .btn-lg {
    padding: 0.875rem 2rem;
    font-size: 1rem;
  }
}
</style>