<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/DelegadoDetailModal.vue -->
<template>
  <div class="modal fade show d-block align-items-center justify-content-center" tabindex="-1" v-if="show" @click.self="close" style="display: flex; min-height: 100vh;">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-person-badge me-2"></i>
            Detalles del Delegado
          </h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        
        <div class="modal-body" v-if="delegado">
          <!-- Header with name and avatar -->
          <div class="row mb-4">
            <div class="col-12">
              <div class="d-flex align-items-center p-3 bg-light rounded">
                <div class="avatar-large rounded-circle bg-success text-white me-3 d-flex align-items-center justify-content-center">
                  <i class="bi bi-person-badge" style="font-size: 2rem;"></i>
                </div>
                <div>
                  <h4 class="mb-1">{{ delegado.apellido }}, {{ delegado.nombre }}</h4>
                  <p class="text-muted mb-0" v-if="delegado.dni">DNI: {{ delegado.dni }}</p>
                  <span class="badge bg-success mt-1">
                    <i class="bi bi-person-badge me-1"></i>Delegado
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Information sections -->
          <div class="row">
            <!-- Personal Information -->
            <div class="col-md-6 mb-4">
              <div class="card h-100">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-person me-2"></i>Información Personal</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label class="form-label text-muted small">Fecha de Nacimiento</label>
                    <p class="mb-0">{{ delegado.fecha_nacimiento ? formatDate(delegado.fecha_nacimiento) : 'No especificada' }}</p>
                  </div>
                  <div class="mb-3">
                    <label class="form-label text-muted small">Dirección</label>
                    <p class="mb-0">{{ delegado.direccion || 'No especificada' }}</p>
                  </div>
                  <div class="mb-0">
                    <label class="form-label text-muted small">Ubicación</label>
                    <p class="mb-0">
                      <span class="badge bg-info">
                        <i class="bi bi-geo-alt me-1"></i>{{ getCompleteLocation(delegado.localidad) }}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Contact Information -->
            <div class="col-md-6 mb-4">
              <div class="card h-100">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-telephone me-2"></i>Información de Contacto</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label class="form-label text-muted small">Email</label>
                    <p class="mb-0">
                      <span v-if="delegado.email">
                        <i class="bi bi-envelope me-2"></i>
                        <a :href="`mailto:${delegado.email}`" class="text-decoration-none">{{ delegado.email }}</a>
                      </span>
                      <span v-else class="text-muted">No especificado</span>
                    </p>
                  </div>
                  <div class="mb-0">
                    <label class="form-label text-muted small">Teléfono</label>
                    <p class="mb-0">
                      <span v-if="delegado.telefono">
                        <i class="bi bi-telephone me-2"></i>
                        <a :href="`tel:${delegado.telefono}`" class="text-decoration-none">{{ delegado.telefono }}</a>
                      </span>
                      <span v-else class="text-muted">No especificado</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Organization Information -->
          <div class="row">
            <div class="col-12 mb-4">
              <div class="card">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-building me-2"></i>Información de Organización</h6>
                </div>
                <div class="card-body">
                  <label class="form-label text-muted small">Organización</label>
                  <p class="mb-0">
                    <span v-if="delegado.organizacion && typeof delegado.organizacion === 'object'" class="badge bg-secondary">
                      <i class="bi bi-building me-1"></i>{{ delegado.organizacion.nombre }}
                    </span>
                    <span v-else-if="delegado.organizacion" class="badge bg-secondary">
                      <i class="bi bi-building me-1"></i>{{ getOrganizacionName(delegado.organizacion) }}
                    </span>
                    <span v-else class="text-muted">No especificada</span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button type="button" class="btn btn-outline-primary" @click="$emit('edit', delegado)">
            <i class="bi bi-pencil me-2"></i>Editar
          </button>
          <button type="button" class="btn btn-secondary" @click="close">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" v-if="show"></div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

interface Localidad { 
  id: number; 
  nombre: string;
  departamento?: { 
    id: number; 
    nombre: string; 
    provincia?: { 
      id: number; 
      nombre: string; 
      pais?: { 
        id: number; 
        nombre: string; 
      }
    }
  }
}

interface Organizacion { id: number; nombre: string }

interface Delegado {
  id: number
  nombre: string
  apellido: string
  dni: string | null
  fecha_nacimiento: string | null
  telefono: string | null
  email: string | null
  direccion: string | null
  localidad: number | Localidad | null
  organizacion: number | Organizacion | null
}

export default defineComponent({
  name: 'DelegadoDetailModal',
  props: {
    show: { type: Boolean, required: true },
    delegado: { type: Object as PropType<Delegado | null>, default: null },
    localidades: { type: Array as PropType<Localidad[]>, default: () => [] },
    organizaciones: { type: Array as PropType<Organizacion[]>, default: () => [] }
  },
  emits: ['close', 'edit'],
  methods: {
    close() {
      this.$emit('close')
    },
    formatDate(dateString: string): string {
      try {
        return new Date(dateString).toLocaleDateString('es-ES', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      } catch {
        return dateString
      }
    },
    getCompleteLocation(localidad: number | Localidad | null): string {
      if (!localidad) return 'No especificada'
      
      // If it's just an ID, try to find the localidad in the list
      if (typeof localidad === 'number') {
        const loc = this.localidades?.find?.((l: Localidad) => l.id === localidad)
        if (loc) {
          return this.buildLocationString(loc)
        }
        return `ID ${localidad}`
      }
      
      // If it's an object, build the location string
      if (typeof localidad === 'object') {
        return this.buildLocationString(localidad)
      }
      
      return 'No especificada'
    },
    buildLocationString(localidad: Localidad): string {
      const parts = [localidad.nombre]
      
      if (localidad.departamento) {
        parts.push(localidad.departamento.nombre)
        
        if (localidad.departamento.provincia) {
          parts.push(localidad.departamento.provincia.nombre)
          
          if (localidad.departamento.provincia.pais) {
            parts.push(localidad.departamento.provincia.pais.nombre)
          }
        }
      }
      
      return parts.join(', ')
    },
    getOrganizacionName(organizacionId: number): string {
      const org = this.organizaciones?.find?.((o: Organizacion) => o.id === organizacionId)
      return org ? org.nombre : `ID ${organizacionId}`
    }
  }
})
</script>

<style scoped>
.modal { background: rgba(0, 0, 0, 0.5); }

.avatar-large {
  width: 80px;
  height: 80px;
}

.card {
  border: 1px solid #e9ecef;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding: 0.75rem 1rem;
}

.card-header h6 {
  color: #495057;
  font-weight: 600;
}

.form-label.small {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}
</style>