<!-- src/components/landing/VoluntariadoCard.vue -->
<template>
  <div class="voluntariado-card" @click="$emit('view')">
    <!-- Card Header with Image Background (like org header) -->
    <div
      class="card-header-vol"
      :style="
        imageUrl && imageUrl !== 'https://via.placeholder.com/400x250'
          ? {
              backgroundImage: `url(${imageUrl})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
            }
          : {}
      "
    >
      <!-- Gradient overlay for better text visibility -->
      <div class="header-overlay"></div>
      
      <!-- Can join badge in top-left -->
      <div class="card-badge-left" v-if="canJoin">
        <span class="badge bg-success">
          <i class="bi bi-check-circle-fill me-1"></i>
          Podés inscribirte
        </span>
      </div>

      <!-- Top-right badge, if provided -->
      <div class="card-badge-right" v-if="badge">
        <span class="badge" :class="badgeClass">{{ badge }}</span>
      </div>

      <!-- Header content -->
      <div class="vol-header-content">
        <h3 class="vol-title">{{ title }}</h3>
        
        <!-- Date badge -->
        <div class="vol-badges-row" v-if="date">
          <span class="badge vol-badge-date">
            <i class="bi bi-calendar2-event-fill me-1"></i>
            {{ date }}
          </span>
        </div>
      </div>
    </div>

    <!-- Card Body -->
    <div class="card-body-vol">
      <p class="vol-description">{{ description }}</p>

      <!-- Voluntariado Details -->
      <div class="vol-details">
        <div v-if="location" class="detail-item">
          <i class="bi bi-geo-alt-fill"></i>
          <small class="ms-2">{{ location }}</small>
        </div>
        <div v-if="inscriptos != null" class="detail-item">
          <i class="bi bi-people-fill"></i>
          <small class="ms-2"><strong>{{ inscriptos }}</strong> inscriptos</small>
        </div>
      </div>
    </div>

    <!-- Card Footer -->
    <div class="card-footer-vol">
      <small class="text-muted"></small>
      <span class="view-more-indicator">
        <slot name="actions">
          <span class="view-action">
            Ver más <i class="bi bi-arrow-right"></i>
          </span>
        </slot>
      </span>
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
    },
    canJoin: {
      type: Boolean,
      default: false
    }
  },
  emits: ['view']
})
</script>

<style scoped>
/* Main Card Container - matching organization card */
.voluntariado-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  transition: all 0.4s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 2px solid #e9ecef;
  position: relative;
}

/* Top border animation on hover */
.voluntariado-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--brand-start), var(--brand-end));
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 2;
}

.voluntariado-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 35px rgba(0, 128, 128, 0.15);
  border-color: rgba(0, 128, 128, 0.3);
}

.voluntariado-card:hover::before {
  opacity: 1;
}

/* Card Header with gradient background (like org card) */
.card-header-vol {
  padding: 1.5rem;
  background: linear-gradient(135deg, var(--brand-start) 0%, var(--brand-end) 100%);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 160px;
  position: relative;
  overflow: hidden;
}

/* Decorative gradient overlay */
.header-overlay {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.1) 100%);
  z-index: 0;
}

.card-header-vol::after {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 150%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* Badge positioning */
.card-badge-left {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 2;
  animation: pulse 2s ease-in-out infinite;
}

.card-badge-left .badge {
  padding: 0.5rem 1rem;
  font-weight: 600;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.card-badge-right {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 2;
}

.card-badge-right .badge {
  padding: 0.5rem 1rem;
  font-weight: 600;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* Header content */
.vol-header-content {
  position: relative;
  z-index: 1;
}

.vol-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  line-height: 1.3;
  word-wrap: break-word;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  color: white;
}

.vol-badges-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.vol-badge-date {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  font-size: 0.75rem;
  padding: 0.4rem 0.8rem;
  font-weight: 600;
  color: white;
}

/* Card Body */
.card-body-vol {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.vol-description {
  color: #495057;
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 1.25rem;
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: calc(1.7 * 1rem * 3);
  flex-grow: 1;
}

/* Details section */
.vol-details {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid #f1f1f1;
}

.detail-item {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #6c757d;
  padding: 0.5rem 0;
  transition: color 0.3s ease;
}

.voluntariado-card:hover .detail-item {
  color: #495057;
}

.detail-item i {
  width: 20px;
  text-align: center;
  flex-shrink: 0;
  color: var(--brand-accent);
  font-size: 1rem;
}

/* Card Footer */
.card-footer-vol {
  background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
  padding: 1rem 1.5rem;
  border-top: 2px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.view-more-indicator {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--brand-accent);
  opacity: 0;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: auto;
}

.view-action {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.view-more-indicator i {
  transition: transform 0.3s ease;
}

.voluntariado-card:hover .view-more-indicator {
  opacity: 1;
}

.voluntariado-card:hover .view-more-indicator i {
  transform: translateX(5px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .card-header-vol {
    min-height: 140px;
    padding: 1.25rem;
  }

  .vol-title {
    font-size: 1.1rem;
  }

  .vol-description {
    font-size: 0.95rem;
  }
}
</style>
