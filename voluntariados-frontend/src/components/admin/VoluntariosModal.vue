<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/VoluntariosModal.vue -->
<template>
  <div class="modal fade show d-block align-items-center justify-content-center" tabindex="-1" v-if="show" @click.self="close" style="display: flex; min-height: 100vh;">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-person me-2"></i>
            {{ isEdit ? 'Editar' : 'Crear' }} Voluntario
          </h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
              {{ errorMessage }}
              <button type="button" class="btn-close" @click="errorMessage = null"></button>
            </div>

            <!-- Persona fields -->
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="nombre" class="form-label">Nombre <span class="text-danger">*</span></label>
                <input type="text" id="nombre" class="form-control" v-model="formData.nombre" required maxlength="120" />
              </div>
              <div class="col-md-6 mb-3">
                <label for="apellido" class="form-label">Apellido <span class="text-danger">*</span></label>
                <input type="text" id="apellido" class="form-control" v-model="formData.apellido" required maxlength="120" />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="dni" class="form-label">DNI</label>
                <input type="text" id="dni" class="form-control" v-model="formData.dni" maxlength="20" />
              </div>
              <div class="col-md-6 mb-3">
                <label for="fecha_nacimiento" class="form-label">Fecha de Nacimiento</label>
                <input type="date" id="fecha_nacimiento" class="form-control" v-model="formData.fecha_nacimiento" />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" id="email" class="form-control" v-model="formData.email" maxlength="254" />
              </div>
              <div class="col-md-6 mb-3">
                <label for="telefono" class="form-label">Teléfono</label>
                <input type="tel" id="telefono" class="form-control" v-model="formData.telefono" maxlength="30" />
              </div>
            </div>

            <div class="mb-3">
              <label for="direccion" class="form-label">Dirección</label>
              <input type="text" id="direccion" class="form-control" v-model="formData.direccion" maxlength="255" />
            </div>

            <div class="mb-3">
              <label for="localidad" class="form-label">Localidad</label>
              <select id="localidad" class="form-select" v-model="formData.localidad">
                <option :value="null">Seleccionar localidad...</option>
                <option v-for="loc in localidades" :key="loc.id" :value="loc.id">{{ loc.nombre }}</option>
              </select>
            </div>

            <!-- Voluntario specific fields -->
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="carrera" class="form-label">Carrera</label>
                <select id="carrera" class="form-select" v-model="formData.carrera">
                  <option :value="null">Seleccionar carrera...</option>
                  <option v-for="c in carreras" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                </select>
              </div>
              <div class="col-md-6 mb-3 d-flex align-items-center">
                <div class="form-check mt-3">
                  <input class="form-check-input" type="checkbox" id="interno" v-model="formData.interno">
                  <label class="form-check-label" for="interno">Voluntario interno</label>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <label for="observaciones" class="form-label">Observaciones</label>
              <textarea id="observaciones" class="form-control" v-model="formData.observaciones" rows="3" maxlength="2000" />
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
import { ubicacionAPI, facultadAPI } from '@/services/api'

interface Localidad { id: number; nombre: string }
interface Carrera { id: number; nombre: string }

interface VoluntarioFormData {
  id: number | null
  nombre: string
  apellido: string
  dni: string
  fecha_nacimiento: string
  telefono: string
  email: string
  direccion: string
  localidad: number | null
  interno: boolean
  observaciones: string
  carrera: number | null
}

export default defineComponent({
  name: 'VoluntariosModal',
  props: {
    show: { type: Boolean, required: true },
    isEdit: { type: Boolean, default: false },
    voluntarioData: { type: Object as PropType<VoluntarioFormData>, required: true }
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
        interno: false,
        observaciones: '',
        carrera: null
      } as VoluntarioFormData,
      saving: false,
      errorMessage: null as string | null,
      localidades: [] as Localidad[],
      carreras: [] as Carrera[]
    }
  },
  watch: {
    show: { immediate: true, handler(newVal) { if (newVal) { this.resetForm(); this.loadOptions() } } },
    voluntarioData: { immediate: true, deep: true, handler(newData) { if (newData) { this.formData = { ...newData } } } }
  },
  methods: {
    async loadOptions() {
      try {
        const [locRes, carRes] = await Promise.all([
          ubicacionAPI.getLocalidades(),
          facultadAPI.getCarreras()
        ])
        this.localidades = locRes.data
        this.carreras = carRes.data
      } catch (err) {
        // swallow
      }
    },
    resetForm() {
      this.errorMessage = null
      this.saving = false
      if (!this.isEdit) {
        this.formData = { id: null, nombre: '', apellido: '', dni: '', fecha_nacimiento: '', telefono: '', email: '', direccion: '', localidad: null, interno: false, observaciones: '', carrera: null }
      }
    },
    async handleSubmit() {
      // Basic minimal validation (nombre y apellido obligatorios)
      if (!this.formData.nombre.trim() || !this.formData.apellido.trim()) {
        this.errorMessage = 'Nombre y apellido son obligatorios.'
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
