<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/AdministradorDetailModal.vue -->
<template>
  <div class="modal fade show d-block align-items-center justify-content-center" tabindex="-1" v-if="show" @click.self="close" style="display: flex; min-height: 100vh;">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-shield-check me-2"></i>
            Detalles del Administrador
          </h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        
        <div class="modal-body" v-if="administrador">
          <!-- Header with name and avatar -->
          <div class="row mb-4">
            <div class="col-12">
              <div class="d-flex align-items-center p-3 bg-light rounded">
                <div class="avatar-large rounded-circle bg-danger text-white me-3 d-flex align-items-center justify-content-center">
                  <i class="bi bi-shield-check" style="font-size: 2rem;"></i>
                </div>
                <div>
                  <h4 class="mb-1">{{ administrador.apellido }}, {{ administrador.nombre }}</h4>
                  <p class="text-muted mb-0" v-if="administrador.dni">DNI: {{ administrador.dni }}</p>
                  <span class="badge bg-danger mt-1">
                    <i class="bi bi-shield-check me-1"></i>Administrador
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
                    <p class="mb-0">{{ administrador.fecha_nacimiento ? formatDate(administrador.fecha_nacimiento) : 'No especificada' }}</p>
                  </div>
                  <div class="mb-3">
                    <label class="form-label text-muted small">Dirección</label>
                    <p class="mb-0">{{ administrador.direccion || 'No especificada' }}</p>
                  </div>
                  <div class="mb-0">
                    <label class="form-label text-muted small">Ubicación</label>
                    <p class="mb-0">
                      <span class="badge bg-info">
                        <i class="bi bi-geo-alt me-1"></i>{{ getCompleteLocation(administrador.localidad) }}
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
                      <span v-if="administrador.email">
                        <i class="bi bi-envelope me-2"></i>
                        <a :href="`mailto:${administrador.email}`" class="text-decoration-none">{{ administrador.email }}</a>
                      </span>
                      <span v-else class="text-muted">No especificado</span>
                    </p>
                  </div>
                  <div class="mb-0">
                    <label class="form-label text-muted small">Teléfono</label>
                    <p class="mb-0">
                      <span v-if="administrador.telefono">
                        <i class="bi bi-telephone me-2"></i>
                        <a :href="`tel:${administrador.telefono}`" class="text-decoration-none">{{ administrador.telefono }}</a>
                      </span>
                      <span v-else class="text-muted">No especificado</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Administrative Information -->
          <div class="row">
            <div class="col-12 mb-4">
              <div class="card">
                <div class="card-header">
                  <h6 class="mb-0"><i class="bi bi-gear me-2"></i>Información Administrativa</h6>
                </div>
                <div class="card-body">
                  <div class="d-flex align-items-center">
                    <div class="me-3">
                      <i class="bi bi-shield-check text-danger" style="font-size: 1.5rem;"></i>
                    </div>
                    <div>
                      <p class="mb-1 fw-bold">Privilegios de Administrador</p>
                      <p class="mb-0 text-muted small">
                        Este usuario tiene acceso completo al sistema de administración, 
                        incluyendo la gestión de usuarios, delegados, voluntarios y configuración del sistema.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button type="button" class="btn btn-outline-primary" @click="$emit('edit', administrador)">
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

interface Administrador {
  id: number
  nombre: string
  apellido: string
  dni: string | null
  fecha_nacimiento: string | null
  telefono: string | null
  email: string | null
  direccion: string | null
  localidad: number | Localidad | null
}

export default defineComponent({
  name: 'AdministradorDetailModal',
  props: {
    show: { type: Boolean, required: true },
    administrador: { type: Object as PropType<Administrador | null>, default: null },
    localidades: { type: Array as PropType<Localidad[]>, default: () => [] }
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