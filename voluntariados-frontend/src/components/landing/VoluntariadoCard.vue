<!-- src/components/landing/VoluntariadoCard.vue -->
<template>
  <div class="voluntariado-card">
    <!-- Image/Header -->
    <div class="card-image">
      <img
        :src="imageUrl || 'https://via.placeholder.com/400x250'"
        :alt="title"
        class="img-fluid"
      />
      <!-- Top-right badge, if provided -->
      <div class="card-badge" v-if="badge">
        <span class="badge" :class="badgeClass">{{ badge }}</span>
      </div>
    </div>

    <!-- Header row similar to turno header: left date, right category/badge fallback -->
    <div class="vc-header" v-if="date || category || badge">
      <div class="vc-date" v-if="date">
        <i class="bi bi-calendar2-event-fill me-2"></i>
        <span class="vc-date-text">{{ date }}</span>
      </div>
      <div class="vc-status-badge ms-auto">
        <!-- Prefer explicit badge if passed; else show inscriptos -->
        <span v-if="badge" class="badge" :class="badgeClass">{{ badge }}</span>
        <span v-else-if="inscriptos != null" class="badge bg-light text-dark border">
          <i class="bi bi-people-fill text-success me-1"></i>
          {{ inscriptos }} inscriptos
        </span>
      </div>
    </div>

    <!-- Body -->
    <div class="card-body">
      <h3 class="card-title">{{ title }}</h3>
      <div class="vc-info">
        <div class="vc-info-row" v-if="location">
          <i class="bi bi-geo-alt-fill text-primary"></i>
          <span>{{ location }}</span>
        </div>
        <div class="vc-info-row" v-if="inscriptos != null">
          <i class="bi bi-people-fill text-success"></i>
          <span><strong>{{ inscriptos }}</strong> inscriptos</span>
        </div>
      </div>
      <p class="card-description">{{ description }}</p>

      <!-- Footer -->
      <div class="vc-footer">
        <slot name="actions">
          <button class="btn w-100 btn-primary btn-sm" @click="$emit('view')">
            <i class="bi bi-eye-fill me-2"></i> Ver más
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
    inscriptos: {
      type: Number,
      default: null
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
  box-shadow: 0 12px 30px rgba(0, 128, 128, 0.15); /* Using RGB of --brand-accent */
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

/* Header similar to turno header */
.vc-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e9ecef;
}

.vc-date {
  display: flex;
  align-items: center;
  color: #2c3e50;
  font-weight: 600;
}

.vc-date i {
  color: var(--brand-mid);
}

.vc-status-badge .badge {
  padding: 0.4rem 0.8rem;
  border-radius: 10px;
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

/* Info rows like turno body */
.vc-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.vc-info-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #495057;
  font-size: 0.95rem;
}

.vc-info-row i {
  font-size: 1rem;
}

.card-description {
  color: #6c757d;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  flex: 1;
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Footer similar to turno */
.vc-footer {
  margin-top: auto;
}

.btn-primary {
  background: linear-gradient(135deg, var(--brand-start), var(--brand-end));
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(95, 158, 160, 0.3); /* Using RGB of --brand-start */
}
</style>
