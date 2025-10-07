<!-- src/components/landing/OrganizationsSection.vue -->
<template>
  <section class="organizations-section py-5">
    <div class="container">
      <h2 class="section-title text-center mb-3">
        {{ title }}
      </h2>
      <p class="section-subtitle text-center mb-5">
        {{ subtitle }}
      </p>
      
      <div class="organizations-grid">
        <div 
          v-for="(org, index) in organizations" 
          :key="index"
          class="organization-item"
        >
          <div class="organization-logo">
            <img 
              :src="org.logo || 'https://via.placeholder.com/150x80'" 
              :alt="org.name"
            >
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

interface Organization {
  name: string
  logo?: string
}

export default defineComponent({
  name: 'OrganizationsSection',
  props: {
    title: {
      type: String,
      default: 'Organizaciones Aliadas'
    },
    subtitle: {
      type: String,
      default: ''
    },
    organizations: {
      type: Array as PropType<Organization[]>,
      required: true
    }
  }
})
</script>

<style scoped>
.organizations-section {
  background: #f8f9fa;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #6c757d;
  max-width: 700px;
  margin: 0 auto;
}

.organizations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  align-items: center;
  justify-items: center;
}

.organization-item {
  width: 100%;
  max-width: 200px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.organization-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(139, 0, 0, 0.1);
}

.organization-logo {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.organization-logo img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  filter: grayscale(100%);
  opacity: 0.7;
  transition: all 0.3s ease;
}

.organization-item:hover .organization-logo img {
  filter: grayscale(0%);
  opacity: 1;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
  
  .organizations-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem;
  }
}
</style>