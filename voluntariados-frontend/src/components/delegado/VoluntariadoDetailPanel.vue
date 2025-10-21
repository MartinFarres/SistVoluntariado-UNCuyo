<!-- src/components/delegado/VoluntariadoDetailPanel.vue -->
<template>
  <div class="voluntariado-detail-panel" v-if="voluntariado">
    <div class="card border-primary">
      <div class="card-body">
        <div class="row">
          <!-- Left: Basic Info -->
          <div class="col-md-6">
            <h5 class="card-title text-primary mb-3">
              <i class="bi bi-info-circle me-2"></i>
              Información del Voluntariado
            </h5>
            <div class="info-section">
              <div class="info-item">
                <span class="info-label">Nombre:</span>
                <span class="info-value">{{ voluntariado.nombre }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Fecha de Inicio:</span>
                <span class="info-value">{{ formatDate(voluntariado.fecha_inicio) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Fecha de Fin:</span>
                <span class="info-value">{{ formatDate(voluntariado.fecha_fin) }}</span>
              </div>
              <div class="info-item" v-if="voluntariado.organizacion">
                <span class="info-label">Organización:</span>
                <span class="info-value">{{ getOrganizacionName(voluntariado.organizacion) }}</span>
              </div>
            </div>
          </div>

          <!-- Right: Actions -->
          <div class="col-md-6">
            <h5 class="card-title text-primary mb-3">
              <i class="bi bi-gear me-2"></i>
              Acciones Rápidas
            </h5>
            <div class="d-grid gap-2">
              <button 
                class="btn btn-outline-primary text-start"
                @click="$emit('view-detail')"
              >
                <i class="bi bi-eye me-2"></i>
                Ver Detalles Completos
              </button>
              <button 
                class="btn btn-outline-info text-start"
                @click="$emit('manage-turnos')"
              >
                <i class="bi bi-calendar-check me-2"></i>
                Gestionar Turnos
              </button>
              <button 
                class="btn btn-outline-success text-start"
                @click="$emit('view-inscripciones')"
              >
                <i class="bi bi-people me-2"></i>
                Ver Inscripciones
              </button>
              <button 
                class="btn btn-outline-warning text-start"
                @click="$emit('edit-voluntariado')"
              >
                <i class="bi bi-pencil me-2"></i>
                Editar Voluntariado
              </button>
            </div>
          </div>
        </div>

        <!-- Close Button -->
        <div class="text-end mt-3">
          <button class="btn btn-sm btn-outline-secondary" @click="$emit('close')">
            <i class="bi bi-x-circle me-1"></i>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

interface Voluntariado {
  id: number
  nombre: string
  fecha_inicio?: string | null
  fecha_fin?: string | null
  organizacion?: any
  estado: string
}

export default defineComponent({
  name: 'VoluntariadoDetailPanel',
  props: {
    voluntariado: {
      type: Object as PropType<Voluntariado | null>,
      default: null
    }
  },
  emits: ['close', 'view-detail', 'manage-turnos', 'view-inscripciones', 'edit-voluntariado'],
  methods: {
    formatDate(date?: string | null): string {
      if (!date) return '-'
      try {
        const d = new Date(date)
        return d.toLocaleDateString('es-AR', { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        })
      } catch {
        return String(date)
      }
    },
    getOrganizacionName(org: any): string {
      if (typeof org === 'string') return org
      if (org && org.nombre) return org.nombre
      return 'No especificada'
    }
  }
})
</script>

<style scoped>
.voluntariado-detail-panel {
  margin-top: 1rem;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  border-width: 2px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.875rem;
  color: #6c757d;
  font-weight: 500;
}

.info-value {
  font-size: 1rem;
  color: #212529;
  font-weight: 400;
}

.btn-outline-primary:hover,
.btn-outline-info:hover,
.btn-outline-success:hover,
.btn-outline-warning:hover {
  transform: translateX(5px);
  transition: transform 0.2s ease;
}
</style>
