<!-- src/components/admin/OrganizacionModal.vue -->
<template>
  <div v-if="show" class="modal fade show d-block align-items-center justify-content-center" tabindex="-1" style="background-color: rgba(0,0,0,0.5); display: flex; min-height: 100vh;">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-building me-2"></i>
            {{ isEdit ? 'Editar Organización' : 'Nueva Organización' }}
          </h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
            {{ errorMessage }}
            <button type="button" class="btn-close" @click="errorMessage = null"></button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="row">
              <!-- Nombre -->
              <div class="col-md-6 mb-3">
                <label for="organizationName" class="form-label">Nombre *</label>
                <input
                  type="text"
                  class="form-control"
                  id="organizationName"
                  v-model="localData.nombre"
                  required
                  placeholder="Ingrese el nombre de la organización"
                  maxlength="200"
                >
              </div>
              
              <!-- Estado -->
              <div class="col-md-6 mb-3">
                <label for="organizationStatus" class="form-label">Estado</label>
                <select
                  class="form-select"
                  id="organizationStatus"
                  v-model="localData.activo"
                >
                  <option :value="true">Activo</option>
                  <option :value="false">Inactivo</option>
                </select>
              </div>
            </div>

            <div class="row">
              <!-- Email de contacto -->
              <div class="col-md-6 mb-3">
                <label for="contactEmail" class="form-label">Email de contacto</label>
                <input
                  type="email"
                  class="form-control"
                  id="contactEmail"
                  v-model="localData.contacto_email"
                  placeholder="contacto@organizacion.com"
                  maxlength="254"
                >
              </div>

              <!-- Localidad -->
              <div class="col-md-6 mb-3">
                <label for="localidad" class="form-label">Localidad</label>
                <select
                  class="form-select"
                  id="localidad"
                  v-model="localData.localidad"
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

            <!-- Descripción -->
            <div class="mb-3">
              <label for="description" class="form-label">Descripción</label>
              <textarea
                class="form-control"
                id="description"
                v-model="localData.descripcion"
                rows="3"
                placeholder="Descripción de la organización..."
              ></textarea>
            </div>

          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleClose">
            Cancelar
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="handleSubmit"
            :disabled="saving"
          >
            <span v-if="saving">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Guardando...
            </span>
            <span v-else>
              <i class="bi bi-check-lg me-1"></i>
              {{ isEdit ? 'Actualizar' : 'Crear' }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { ubicacionAPI } from '@/services/api'

interface Localidad {
  id: number
  nombre: string
}



interface OrganizacionFormData {
  id: number | null
  nombre: string
  activo: boolean
  descripcion: string
  contacto_email: string
  localidad: number | null
}

export default defineComponent({
  name: 'OrganizacionModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    organizationData: {
      type: Object as PropType<OrganizacionFormData>,
      required: true
    }
  },
  emits: ['close', 'save'],
  data() {
    return {
      localData: {
        id: null as number | null,
        nombre: '',
        activo: true,
        descripcion: '',
        contacto_email: '',
        localidad: null as number | null,
      } as OrganizacionFormData,
      saving: false,
      errorMessage: null as string | null,
      localidades: [] as Localidad[],
    }
  },
  watch: {
    organizationData: {
      immediate: true,
      handler(newVal) {
        this.localData = { ...newVal }
      }
    },
    show(newVal) {
      if (newVal) {
        this.errorMessage = null
        this.saving = false
        this.loadLocalidades()
      }
    }
  },
  methods: {
    async loadLocalidades() {
      try {
        const response = await ubicacionAPI.getLocalidades()
        this.localidades = response.data
      } catch (err) {
        console.error('Error loading localidades:', err)
      }
    },


    handleClose() {
      this.errorMessage = null
      this.$emit('close')
    },
    
    handleSubmit() {
      if (!this.localData.nombre.trim()) {
        this.errorMessage = 'El nombre de la organización es requerido'
        return
      }
      
      this.errorMessage = null
      this.saving = true
      
      // Prepare data for API - convert empty strings to null
      const dataToSave = {
        ...this.localData,
        descripcion: this.localData.descripcion || null,
        contacto_email: this.localData.contacto_email || null,
        localidad: this.localData.localidad || null,
      }
      
      this.$emit('save', dataToSave, this.handleSaveResult)
    },
    
    handleSaveResult(success: boolean, errorMessage?: string) {
      this.saving = false
      if (!success && errorMessage) {
        this.errorMessage = errorMessage
      }
    }
  }
})
</script>