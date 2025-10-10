<!-- src/components/landing/InfoSection.vue -->
<template>
  <section class="info-section py-5">
    <div class="container">
      <div class="row">
        <div class="col-lg-10 mx-auto">
          <h2 class="section-title text-center mb-5">
            {{ title }}
          </h2>
          
          <div class="row g-4">
            <div 
              v-for="(item, index) in items" 
              :key="index"
              class="col-md-6"
            >
              <div class="info-card h-100">
                <div class="info-icon mb-3">
                  <i class="bi" :class="item.icon"></i>
                </div>
                <h3 class="info-title">{{ item.title }}</h3>
                <p class="info-description">{{ item.description }}</p>
                <a 
                  v-if="item.link" 
                  :href="item.link" 
                  class="info-link"
                >
                  Leer más <i class="bi bi-arrow-right ms-1"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

interface InfoItem {
  icon: string
  title: string
  description: string
  link?: string
}

export default defineComponent({
  name: 'InfoSection',
  props: {
    title: {
      type: String,
      required: true
    },
    items: {
      type: Array as PropType<InfoItem[]>,
      required: true
    }
  }
})
</script>

<style scoped>
.info-section {
  background: #f8f9fa;
  padding: 5rem 0;
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

.info-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(139, 0, 0, 0.15);
  border-color: #8B0000;
}

.info-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #8B0000, #DC143C);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.8rem;
}

.info-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.info-description {
  color: #6c757d;
  line-height: 1.7;
  margin-bottom: 1rem;
}

.info-link {
  color: #8B0000;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
}

.info-link:hover {
  color: #DC143C;
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
  
  .info-section {
    padding: 3rem 0;
  }
}
</style>