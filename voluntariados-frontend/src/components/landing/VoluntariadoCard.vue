<!-- src/components/landing/VoluntariadoCard.vue -->
<template>
  <div class="voluntariado-card">
    <div class="card-image">
      <img 
        :src="imageUrl || 'https://via.placeholder.com/400x250'" 
        :alt="title"
        class="img-fluid"
      >
      <div class="card-badge" v-if="badge">
        <span class="badge" :class="badgeClass">{{ badge }}</span>
      </div>
    </div>
    <div class="card-body">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-description">{{ description }}</p>
      
      <div class="card-meta">
        <div class="meta-item" v-if="category">
          <i class="bi bi-tag me-1"></i>
          <span>{{ category }}</span>
        </div>
        <div class="meta-item" v-if="location">
          <i class="bi bi-geo-alt me-1"></i>
          <span>{{ location }}</span>
        </div>
        <div class="meta-item" v-if="date">
          <i class="bi bi-calendar me-1"></i>
          <span>{{ date }}</span>
        </div>
      </div>
      
      <div class="card-footer-actions">
        <slot name="actions">
          <button class="btn btn-primary btn-sm" @click="$emit('view')">
            Ver más <i class="bi bi-arrow-right ms-1"></i>
          </button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'VoluntariadoCard',
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    imageUrl: {
      type: String,
      default: ''
    },
    category: {
      type: String,
      default: ''
    },
    location: {
      type: String,
      default: ''
    },
    date: {
      type: String,
      default: ''
    },
    badge: {
      type: String,
      default: ''
    },
    badgeClass: {
      type: String,
      default: 'bg-success'
    }
  },
  emits: ['view']
})
</script>

<style scoped>
.voluntariado-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.voluntariado-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(139, 0, 0, 0.15);
}

.card-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.voluntariado-card:hover .card-image img {
  transform: scale(1.1);
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 1;
}

.card-badge .badge {
  padding: 0.5rem 1rem;
  font-weight: 600;
  border-radius: 20px;
}

.card-body {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.card-description {
  color: #6c757d;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem 0;
  border-top: 1px solid #e9ecef;
  border-bottom: 1px solid #e9ecef;
  margin-bottom: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #6c757d;
}

.meta-item i {
  color: #8B0000;
}

.card-footer-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-primary {
  background: linear-gradient(135deg, #8B0000, #DC143C);
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 15px rgba(139, 0, 0, 0.3);
}
</style>