<!-- src/components/landing/TestimonialsSection.vue -->
<template>
  <section class="testimonials-section py-5">
    <div class="container">
      <h2 class="section-title text-center mb-5">
        {{ title }}
      </h2>
      
      <div class="row g-4">
        <div 
          v-for="(testimonial, index) in testimonials" 
          :key="index"
          class="col-md-4"
        >
          <div class="testimonial-card">
            <div class="testimonial-avatar">
              <img 
                :src="testimonial.avatar || 'https://via.placeholder.com/80'" 
                :alt="testimonial.name"
              >
            </div>
            <div class="testimonial-content">
              <div class="quote-icon">
                <i class="bi bi-quote"></i>
              </div>
              <p class="testimonial-text">{{ testimonial.text }}</p>
              <div class="testimonial-author">
                <h4 class="author-name">{{ testimonial.name }}</h4>
                <p class="author-role">{{ testimonial.role }}</p>
              </div>
              <a 
                v-if="testimonial.link" 
                :href="testimonial.link" 
                class="testimonial-link"
              >
                Leer más <i class="bi bi-arrow-right ms-1"></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

interface Testimonial {
  name: string
  role: string
  text: string
  avatar?: string
  link?: string
}

export default defineComponent({
  name: 'TestimonialsSection',
  props: {
    title: {
      type: String,
      default: 'Testimonios De Nuestro Voluntarios'
    },
    testimonials: {
      type: Array as PropType<Testimonial[]>,
      required: true
    }
  }
})
</script>

<style scoped>
.testimonials-section {
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

.testimonial-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 2rem;
  height: 100%;
  transition: all 0.3s ease;
  position: relative;
  border: 1px solid #e9ecef;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(139, 0, 0, 0.15);
  background: white;
}

.testimonial-avatar {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.testimonial-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.quote-icon {
  color: #8B0000;
  font-size: 2rem;
  opacity: 0.3;
  margin-bottom: 1rem;
}

.testimonial-text {
  color: #495057;
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.testimonial-author {
  margin-bottom: 1rem;
}

.author-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.author-role {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0;
}

.testimonial-link {
  color: #8B0000;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
}

.testimonial-link:hover {
  color: #DC143C;
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
}
</style>