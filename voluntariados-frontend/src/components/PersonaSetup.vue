<!-- PersonaSetup.vue -->
<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow">
          <div class="card-header bg-primary text-white text-center">
            <h3 class="mb-0">Completar Información Personal</h3>
            <p class="mb-0 mt-2">
              Completa tu información personal para continuar usando el sistema
            </p>
          </div>
          <div class="card-body">
            <form @submit.prevent="submitForm">
              <!-- Nombre -->
              <div class="mb-3">
                <label for="nombre" class="form-label">Nombre *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="nombre"
                  v-model="formData.nombre"
                  :class="{ 'is-invalid': errors.nombre }"
                  required
                >
                <div v-if="errors.nombre" class="invalid-feedback">
                  {{ errors.nombre }}
                </div>
              </div>

              <!-- Apellido -->
              <div class="mb-3">
                <label for="apellido" class="form-label">Apellido *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="apellido"
                  v-model="formData.apellido"
                  :class="{ 'is-invalid': errors.apellido }"
                  required
                >
                <div v-if="errors.apellido" class="invalid-feedback">
                  {{ errors.apellido }}
                </div>
              </div>

              <!-- DNI -->
              <div class="mb-3">
                <label for="dni" class="form-label">DNI *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="dni"
                  v-model="formData.dni"
                  :class="{ 'is-invalid': errors.dni }"
                  required
                >
                <div v-if="errors.dni" class="invalid-feedback">
                  {{ errors.dni }}
                </div>
              </div>

              <!-- Fecha de Nacimiento -->
              <div class="mb-3">
                <label for="fecha_nacimiento" class="form-label">Fecha de Nacimiento *</label>
                <input 
                  type="date" 
                  class="form-control" 
                  id="fecha_nacimiento"
                  v-model="formData.fecha_nacimiento"
                  :class="{ 'is-invalid': errors.fecha_nacimiento }"
                  required
                >
                <div v-if="errors.fecha_nacimiento" class="invalid-feedback">
                  {{ errors.fecha_nacimiento }}
                </div>
              </div>

              <!-- Teléfono -->
              <div class="mb-3">
                <label for="telefono" class="form-label">Teléfono *</label>
                <input 
                  type="tel" 
                  class="form-control" 
                  id="telefono"
                  v-model="formData.telefono"
                  :class="{ 'is-invalid': errors.telefono }"
                  required
                >
                <div v-if="errors.telefono" class="invalid-feedback">
                  {{ errors.telefono }}
                </div>
              </div>

              <!-- Email (pre-filled from user) -->
              <div class="mb-3">
                <label for="email" class="form-label">Email *</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="email"
                  v-model="formData.email"
                  :class="{ 'is-invalid': errors.email }"
                  required
                >
                <div v-if="errors.email" class="invalid-feedback">
                  {{ errors.email }}
                </div>
              </div>

              <!-- Dirección -->
              <div class="mb-3">
                <label for="direccion" class="form-label">Dirección *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="direccion"
                  v-model="formData.direccion"
                  :class="{ 'is-invalid': errors.direccion }"
                  required
                >
                <div v-if="errors.direccion" class="invalid-feedback">
                  {{ errors.direccion }}
                </div>
              </div>

              <!-- Localidad -->
              <div class="mb-3">
                <label for="localidad" class="form-label">Localidad *</label>
                <select 
                  class="form-select" 
                  id="localidad"
                  v-model="formData.localidad"
                  :class="{ 'is-invalid': errors.localidad }"
                >
                  <option value="">Selecciona una localidad</option>
                  <option 
                    v-for="localidad in localidades" 
                    :key="localidad.id" 
                    :value="localidad.id"
                  >
                    {{ getCompleteLocationName(localidad) }}
                  </option>
                </select>
                <div v-if="errors.localidad" class="invalid-feedback">
                  {{ errors.localidad }}
                </div>
              </div>

              <!-- Role-specific fields -->
              <div v-if="userRole === 'VOL'">
                <!-- Voluntario specific fields -->
                <div class="mb-3">
                  <label for="carrera" class="form-label">Carrera</label>
                  <select 
                    class="form-select" 
                    id="carrera"
                    v-model="formData.carrera"
                    :class="{ 'is-invalid': errors.carrera }"
                  >
                    <option value="">Selecciona una carrera (opcional)</option>
                    <option v-for="carrera in carreras" :key="carrera.id" :value="carrera.id">
                      {{ carrera.nombre }}
                    </option>
                  </select>
                  <div v-if="errors.carrera" class="invalid-feedback">
                    {{ errors.carrera }}
                  </div>
                </div>

                <div class="mb-3">
                  <div class="form-check">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      id="interno"
                      v-model="formData.interno"
                    >
                    <label class="form-check-label" for="interno">
                      Voluntario interno de la facultad
                    </label>
                  </div>
                </div>
              </div>

              <div v-if="userRole === 'DELEG'">
                <!-- Delegado specific fields -->
                <div class="mb-3">
                  <label for="organizacion" class="form-label">Organización</label>
                  <select 
                    class="form-select" 
                    id="organizacion"
                    v-model="formData.organizacion"
                    :class="{ 'is-invalid': errors.organizacion }"
                  >
                    <option value="">Selecciona una organización (opcional)</option>
                    <option v-for="org in organizaciones" :key="org.id" :value="org.id">
                    {{ org.nombre }}
                    </option>
                  </select>
                  <div v-if="errors.organizacion" class="invalid-feedback">
                    {{ errors.organizacion }}
                  </div>
                </div>
              </div>

              <!-- General error message -->
              <div v-if="generalError" class="alert alert-danger mb-3">
                {{ generalError }}
              </div>

              <!-- Submit button -->
              <div class="d-grid">
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  :disabled="submitting"
                >
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                  {{ submitting ? 'Guardando...' : 'Completar Configuración' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { userAPI, ubicacionAPI, facultadAPI } from '@/services/api'

interface Localidad {
  id: number
  nombre: string
  departamento?: {
    id: number
    nombre: string
    provincia?: {
      id: number
      nombre: string
      pais?: { id: number; nombre: string }
    }
  }
}

export default defineComponent({
  name: 'PersonaSetup',
  props: {
    userRole: {
      type: String,
      required: true,
      validator: (value: string) => ['VOL', 'ADMIN', 'DELEG'].includes(value)
    },
    userEmail: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      submitting: false,
      generalError: '',
      localidades: [] as Localidad[],
      carreras: [] as Array<{ id: number; nombre: string }>,
      organizaciones: [] as Array<{ id: number; nombre: string }>,
      formData: {
        nombre: '',
        apellido: '',
        dni: '',
        fecha_nacimiento: '',
        telefono: '',
        email: this.userEmail,
        direccion: '',
        localidad: null as number | null,
        // Voluntario specific
        carrera: null as number | null,
        interno: false,
        // Delegado specific
        organizacion: null as number | null
      },
      errors: {} as Record<string, string>
    }
  },
  async mounted() {
    await this.loadLocalidades()
    await this.loadCarreras()
    await this.loadOrganizaciones()
  },
  methods: {
    async loadLocalidades() {
      try {
        const [locRes, depRes, provRes, paisRes] = await Promise.all([
          ubicacionAPI.getLocalidades(),
          ubicacionAPI.getDepartamentos(),
          ubicacionAPI.getProvincias(),
          ubicacionAPI.getPaises()
        ])

        const paises = paisRes.data
        const provincias = provRes.data
        const departamentos = depRes.data
        const localidades = locRes.data

        this.localidades = localidades.map((localidad: any) => {
          const departamento = departamentos.find((d: any) => d.id === localidad.departamento)
          if (departamento) {
            const provincia = provincias.find((p: any) => p.id === departamento.provincia)
            if (provincia) {
              const pais = paises.find((pa: any) => pa.id === provincia.pais)
              departamento.provincia = { ...provincia, pais }
            }
            localidad.departamento = departamento
          }
          return localidad
        })
      } catch (error) {
        console.error('Error loading localidades:', error)
      }
    },

    async loadCarreras() {
      try {
        const res = await facultadAPI.getCarreras()
        this.carreras = res.data
      } catch (error) {
        console.error('Error loading carreras:', error)
      }
    },

    async loadOrganizaciones() {
        try {
            const { organizacionAPI } = await import('@/services/api')
            const res = await organizacionAPI.getAll()
            this.organizaciones = res.data
        } catch (error) {
            console.error('Error loading organizaciones:', error)
        }
    },

    getCompleteLocationName(localidad: Localidad): string {
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

    async submitForm() {
      this.submitting = true
      this.generalError = ''
      this.errors = {}

      try {
        // Prepare data based on user role
        const dataToSubmit: any = {
          nombre: this.formData.nombre,
          apellido: this.formData.apellido,
          dni: this.formData.dni,
          fecha_nacimiento: this.formData.fecha_nacimiento,
          telefono: this.formData.telefono,
          email: this.formData.email,
          direccion: this.formData.direccion,
          localidad: this.formData.localidad
        }

        // Add role-specific fields
        if (this.userRole === 'VOL') {
          dataToSubmit.carrera = this.formData.carrera
          dataToSubmit.interno = this.formData.interno
        } else if (this.userRole === 'DELEG') {
          dataToSubmit.organizacion = this.formData.organizacion
        }

        await userAPI.setupPersona(dataToSubmit)
        
        // Emit success event
        this.$emit('setup-complete')
        
      } catch (error: any) {
        console.error('Error setting up persona:', error)
        
        if (error.response?.data) {
          const errorData = error.response.data
          
          // Handle field-specific errors
          if (typeof errorData === 'object' && !errorData.detail) {
            this.errors = {}
            Object.keys(errorData).forEach(field => {
              if (Array.isArray(errorData[field])) {
                this.errors[field] = errorData[field][0]
              }
            })
          } else {
            this.generalError = errorData.detail || 'Error al completar la configuración'
          }
        } else {
          this.generalError = 'Error al completar la configuración'
        }
      } finally {
        this.submitting = false
      }
    }
  }
})
</script>

<style scoped>
.card {
  border: none;
  border-radius: 10px;
}

.card-header {
  border-radius: 10px 10px 0 0;
}

.form-label {
  font-weight: 600;
  color: #495057;
}

.btn-primary {
  background: linear-gradient(45deg, #007bff, #0056b3);
  border: none;
  border-radius: 5px;
  padding: 12px;
  font-weight: 600;
}

.btn-primary:hover {
  background: linear-gradient(45deg, #0056b3, #004085);
}
</style>