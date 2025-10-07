<!-- src/components/landing/HowItWorksSection.vue -->
<template>
  <section class="how-it-works-section py-5">
    <div class="container">
      <h2 class="section-title text-center mb-5">
        {{ title }}
      </h2>
      
      <div class="row g-4">
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          class="col-md-6"
        >
          <div class="step-card" :class="step.highlight ? 'highlight' : ''">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-content">
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-description">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

interface Step {
  title: string
  description: string
  highlight?: boolean
}

export default defineComponent({
  name: 'HowItWorksSection',
  props: {
    title: {
      type: String,
      default: '¿Cómo Funciona?'
    },
    steps: {
      type: Array as PropType<Step[]>,
      required: true
    }
  }
})
</script>

<style scoped>
.how-it-works-section {
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

.step-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  gap: 1.5rem;
  height: 100%;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.step-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(139, 0, 0, 0.15);
  border-color: #8B0000;
  background: white;
}

.step-card.highlight {
  background: linear-gradient(135deg, rgba(139, 0, 0, 0.05), rgba(220, 20, 60, 0.05));
  border-color: #8B0000;
}

.step-number {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #8B0000, #DC143C);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: 0 4px 15px rgba(139, 0, 0, 0.3);
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.75rem;
}

.step-description {
  color: #6c757d;
  line-height: 1.7;
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
  
  .step-card {
    flex-direction: column;
    text-align: center;
  }
  
  .step-number {
    margin: 0 auto;
  }
}
</style>