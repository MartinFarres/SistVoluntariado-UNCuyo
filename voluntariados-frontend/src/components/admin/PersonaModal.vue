<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/PersonaModal.vue -->
<template>
  <div class="modal fade show d-block align-items-center justify-content-center" tabindex="-1" v-if="show" @click.self="close" style="display: flex; min-height: 100vh;">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-person me-2"></i>
            {{ isEdit ? 'Editar' : 'Crear' }} Persona
          </h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        
        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
              {{ errorMessage }}
              <button type="button" class="btn-close" @click="errorMessage = null"></button>
            </div>
            <div class="row">
              <!-- Nombre -->
              <div class="col-md-6 mb-3">
                <label for="nombre" class="form-label">
                  Nombre <span class="text-danger">*</span>
                </label>
                <input
                  type="text"
                  id="nombre"
                  class="form-control"
                  v-model="formData.nombre"
                  maxlength="100"
                  required
                >
              </div>
              
              <!-- Apellido -->
              <div class="col-md-6 mb-3">
                <label for="apellido" class="form-label">
                  Apellido <span class="text-danger">*</span>
                </label>
                <input
                  type="text"
                  id="apellido"
                  class="form-control"
                  v-model="formData.apellido"
                  maxlength="100"
                  required
                >
              </div>
            </div>

            <div class="row">
              <!-- DNI -->
              <div class="col-md-6 mb-3">
                <label for="dni" class="form-label">DNI <span class="text-danger">*</span></label>
                <input
                  type="text"
                  id="dni"
                  class="form-control"
                  v-model="formData.dni"
                  placeholder="Ej: 12345678"
                  maxlength="20"
                  required
                >
              </div>
              
              <!-- Fecha de Nacimiento -->
              <div class="col-md-6 mb-3">
                <label for="fecha_nacimiento" class="form-label">Fecha de Nacimiento <span class="text-danger">*</span></label>
                <input
                  type="date"
                  id="fecha_nacimiento"
                  class="form-control"
                  v-model="formData.fecha_nacimiento"
                  required
                >
              </div>
            </div>

            <div class="row">
              <!-- Email -->
              <div class="col-md-6 mb-3">
                <label for="email" class="form-label">Email <span class="text-danger">*</span></label>
                <input
                  type="email"
                  id="email"
                  class="form-control"
                  v-model="formData.email"
                  placeholder="persona@ejemplo.com"
                  maxlength="254"
                  required
                >
              </div>
              
              <!-- Teléfono -->
              <div class="col-md-6 mb-3">
                <label for="telefono" class="form-label">Teléfono <span class="text-danger">*</span></label>
                <input
                  type="tel"
                  id="telefono"
                  class="form-control"
                  v-model="formData.telefono"
                  placeholder="Ej: 2611234567"
                  maxlength="20"
                  required
                >
              </div>
            </div>

            <!-- Dirección -->
            <div class="mb-3">
              <label for="direccion" class="form-label">Dirección <span class="text-danger">*</span></label>
              <input
                type="text"
                id="direccion"
                class="form-control"
                v-model="formData.direccion"
                placeholder="Calle, número, piso, etc."
                maxlength="200"
                required
              >
            </div>

            <!-- Localidad -->
            <div class="mb-3">
              <label for="localidad" class="form-label">Localidad <span class="text-danger">*</span></label>
              <select
                id="localidad"
                class="form-select"
                v-model="formData.localidad"
                required

              >
                <option value="">Seleccionar localidad...</option>
                <option 
                  v-for="localidad in localidades" 
                  :key="localidad.id" 
                  :value="localidad.id"
                >
                  {{ localidad.nombre }}
                </option>
              </select>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close" :disabled="saving">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              {{ saving ? 'Guardando...' : (isEdit ? 'Actualizar' : 'Crear') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" v-if="show"></div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { ubicacionAPI } from '@/services/api'

interface Localidad {
  id: number
  nombre: string
}

interface PersonaFormData {
  id: number | null
  nombre: string
  apellido: string
  dni: string
  fecha_nacimiento: string
  telefono: string
  email: string
  direccion: string
  localidad: number | null
}

export default defineComponent({
  name: 'PersonaModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    personaData: {
      type: Object as PropType<PersonaFormData>,
      required: true
    }
  },
  emits: ['close', 'save'],
  data() {
    return {
      formData: {
        id: null,
        nombre: '',
        apellido: '',
        dni: '',
        fecha_nacimiento: '',
        telefono: '',
        email: '',
        direccion: '',
        localidad: null
      } as PersonaFormData,
      saving: false,
      errorMessage: null as string | null,
      localidades: [] as Localidad[]
    }
  },
  watch: {
    show: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.resetForm()
          this.loadLocalidades()
        }
      }
    },
    personaData: {
      immediate: true,
      deep: true,
      handler(newData) {
        if (newData) {
          this.formData = { ...newData }
        }
      }
    }
  },
  methods: {
    async loadLocalidades() {
      try {
        const response = await ubicacionAPI.getLocalidades()
        this.localidades = response.data
      } catch (err) {
      }
    },

    resetForm() {
      this.errorMessage = null
      this.saving = false
      if (!this.isEdit) {
        this.formData = {
          id: null,
          nombre: '',
          apellido: '',
          dni: '',
          fecha_nacimiento: '',
          telefono: '',
          email: '',
          direccion: '',
          localidad: null
        }
      }
    },
    
    async handleSubmit() {
      if (!this.formData.nombre.trim() || !this.formData.apellido.trim() || !this.formData.dni.trim() || !this.formData.fecha_nacimiento || !this.formData.telefono.trim() || !this.formData.email.trim() || !this.formData.direccion.trim() || !this.formData.localidad) {
        this.errorMessage = 'Todos los campos son obligatorios.'
        return
      }
      this.errorMessage = null
      this.saving = true
      this.$emit('save', this.formData, this.handleSaveResult)
    },

    handleSaveResult(success: boolean, errorMessage?: string) {
      this.saving = false
      if (!success && errorMessage) {
        this.errorMessage = errorMessage
      }
    },

    close() {
      this.$emit('close')
    }
  }
})
</script>

<style scoped>
.modal {
  background: rgba(0, 0, 0, 0.5);
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>