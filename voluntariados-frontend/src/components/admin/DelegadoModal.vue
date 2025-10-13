<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/DelegadoModal.vue -->
<template>
  <div class="modal fade show d-block align-items-center justify-content-center" tabindex="-1" v-if="show" @click.self="close" style="display: flex; min-height: 100vh;">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-person-gear me-2"></i>
            {{ isEdit ? 'Editar' : 'Crear' }} Delegado
          </h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        
        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
              {{ errorMessage }}
              <button type="button" class="btn-close" @click="errorMessage = null"></button>
            </div>
            
            <!-- Reuse Persona fields -->
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="nombre" class="form-label">Nombre <span class="text-danger">*</span></label>
                <input type="text" id="nombre" class="form-control" v-model="formData.nombre" required maxlength="100" />
              </div>
              <div class="col-md-6 mb-3">
                <label for="apellido" class="form-label">Apellido <span class="text-danger">*</span></label>
                <input type="text" id="apellido" class="form-control" v-model="formData.apellido" required maxlength="100" />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="dni" class="form-label">DNI <span class="text-danger">*</span></label>
                <input type="text" id="dni" class="form-control" v-model="formData.dni" required maxlength="20" />
              </div>
              <div class="col-md-6 mb-3">
                <label for="fecha_nacimiento" class="form-label">Fecha de Nacimiento <span class="text-danger">*</span></label>
                <input type="date" id="fecha_nacimiento" class="form-control" v-model="formData.fecha_nacimiento" required />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="email" class="form-label">Email <span class="text-danger">*</span></label>
                <input type="email" id="email" class="form-control" v-model="formData.email" required maxlength="254" />
              </div>
              <div class="col-md-6 mb-3">
                <label for="telefono" class="form-label">Teléfono <span class="text-danger">*</span></label>
                <input type="tel" id="telefono" class="form-control" v-model="formData.telefono" required maxlength="20" />
              </div>
            </div>

            <div class="mb-3">
              <label for="direccion" class="form-label">Dirección <span class="text-danger">*</span></label>
              <input type="text" id="direccion" class="form-control" v-model="formData.direccion" required maxlength="200" />
            </div>

            <div class="mb-3">
              <label for="localidad" class="form-label">Localidad <span class="text-danger">*</span></label>
              <select id="localidad" class="form-select" v-model="formData.localidad" required>
                <option :value="null">Seleccionar localidad...</option>
                <option v-for="loc in localidades" :key="loc.id" :value="loc.id">{{ loc.nombre }}</option>
              </select>
            </div>

            <!-- Extra field: Organizacion -->
            <div class="mb-3">
              <label for="organizacion" class="form-label">Organización</label>
              <select id="organizacion" class="form-select" v-model="formData.organizacion">
                <option :value="null">Seleccionar organización...</option>
                <option v-for="org in organizaciones" :key="org.id" :value="org.id">{{ org.nombre }}</option>
              </select>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close" :disabled="saving">Cancelar</button>
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
import { ubicacionAPI, organizacionAPI } from '@/services/api'

interface Localidad { id: number; nombre: string }
interface Organizacion { id: number; nombre: string }

interface DelegadoFormData {
  id: number | null
  nombre: string
  apellido: string
  dni: string
  fecha_nacimiento: string
  telefono: string
  email: string
  direccion: string
  localidad: number | null
  organizacion: number | null
}

export default defineComponent({
  name: 'DelegadoModal',
  props: {
    show: { type: Boolean, required: true },
    isEdit: { type: Boolean, default: false },
    delegadoData: { type: Object as PropType<DelegadoFormData>, required: true }
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
        localidad: null,
        organizacion: null
      } as DelegadoFormData,
      saving: false,
      errorMessage: null as string | null,
      localidades: [] as Localidad[],
      organizaciones: [] as Organizacion[]
    }
  },
  watch: {
    show: { immediate: true, handler(newVal) { if (newVal) { this.resetForm(); this.loadOptions() } } },
    delegadoData: { immediate: true, deep: true, handler(newData) { if (newData) { this.formData = { ...newData } } } }
  },
  methods: {
    async loadOptions() {
      try {
        const [locRes, orgRes] = await Promise.all([
          ubicacionAPI.getLocalidades(),
          organizacionAPI.getAll()
        ])
        this.localidades = locRes.data
        this.organizaciones = orgRes.data
      } catch (err) {
      }
    },
    resetForm() {
      this.errorMessage = null
      this.saving = false
      if (!this.isEdit) {
        this.formData = { id: null, nombre: '', apellido: '', dni: '', fecha_nacimiento: '', telefono: '', email: '', direccion: '', localidad: null, organizacion: null }
      }
    },
    async handleSubmit() {
        if (!this.formData.nombre.trim() || !this.formData.apellido.trim() || !this.formData.dni.trim() || !this.formData.fecha_nacimiento || !this.formData.telefono.trim() || !this.formData.email.trim()) {
        	this.errorMessage = 'Todos los campos de persona son obligatorios.'
        	return
        }

        if (!this.formData.direccion.trim()) {
            this.errorMessage = 'La direccion es obligatoria.'
            return
        }

        if (!this.formData.localidad) {
            this.errorMessage = 'La localidad es obligatoria.'
            return
        }

        if (this.formData.organizacion === null) {
            this.errorMessage = 'La organización es obligatoria.'
            return
        }

    	this.errorMessage = null
    	this.saving = true
    	this.$emit('save', this.formData, this.handleSaveResult)
    },
    handleSaveResult(success: boolean, errorMessage?: string) {
      this.saving = false
      if (!success && errorMessage) this.errorMessage = errorMessage
    },
    close() { this.$emit('close') }
  }
})
</script>

<style scoped>
.modal { background: rgba(0, 0, 0, 0.5); }
.spinner-border-sm { width: 1rem; height: 1rem; }
</style>
