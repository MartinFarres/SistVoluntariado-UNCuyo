<template>
  <div
    class="modal fade"
    :class="{ show: show, 'd-block': show }"
    tabindex="-1"
    v-if="show"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-person-badge text-primary me-2"></i>
            {{ isEdit ? 'Editar Autoridad' : 'Crear Nueva Autoridad' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <!-- Mensaje de error -->
          <div v-if="errorMessage" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ errorMessage }}
          </div>

          <!-- Formulario principal -->
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label class="form-label">Nombre *</label>
              <input
                type="text"
                class="form-control"
                v-model="autoridadData.nombre"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Apellido *</label>
              <input
                type="text"
                class="form-control"
                v-model="autoridadData.apellido"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Cargo *</label>
              <input
                type="text"
                class="form-control"
                v-model="autoridadData.cargo"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Entidad Encargada *</label>
              <input
                type="text"
                class="form-control"
                v-model="autoridadData.entidad_encargada"
                required
              />
            </div>

            <!-- Vista previa de firma y carga -->
            <div class="mb-3">
              <label class="form-label">Firma (opcional)</label>

              <div v-if="autoridadData.firma" class="mb-2 text-center">
                <img
                  :src="autoridadData.firma"
                  alt="Firma actual"
                  class="img-thumbnail"
                  style="max-height: 120px; object-fit: contain;"
                />
                <div class="text-muted small mt-1">
                  Firma actual — si subís una nueva, se reemplazará
                </div>
              </div>

              <!-- Input de archivo -->
              <input
                type="file"
                class="form-control"
                @change="onFileChange"
                accept="image/*"
              />
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            <i class="bi bi-x-circle me-2"></i> Cancelar
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="handleSubmit"
            :disabled="saving"
          >
            <span v-if="saving">
              <span class="spinner-border spinner-border-sm me-2"></span>Guardando...
            </span>
            <span v-else>
              <i class="bi bi-check-circle me-2"></i>{{ isEdit ? 'Actualizar' : 'Crear' }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal-backdrop fade show" v-if="show"></div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'AutoridadModal',
  props: {
    show: { type: Boolean, default: false },
    isEdit: { type: Boolean, default: false },
    autoridadData: { type: Object as PropType<any>, required: true }
  },
  emits: ['close', 'save'],
  data() {
    return {
      saving: false,
      errorMessage: null as string | null,
      newFile: null as File | null
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.errorMessage = null
        this.saving = false
        this.newFile = null
      }
    }
  },
  methods: {
    async handleSubmit() {
      if (!this.autoridadData.nombre) {
        this.errorMessage = 'El nombre es obligatorio.'
        return
      }
      if (!this.autoridadData.apellido) {
        this.errorMessage = 'El apellido es obligatorio.'
        return
      }
      if (!this.autoridadData.cargo) {
        this.errorMessage = 'El cargo es obligatorio.'
        return
      }
      if (!this.autoridadData.entidad_encargada) {
        this.errorMessage = 'La entidad encargada es obligatoria.'
        return
      }

      const formData = new FormData()
      formData.append('nombre', this.autoridadData.nombre)
      formData.append('apellido', this.autoridadData.apellido)
      formData.append('cargo', this.autoridadData.cargo)
      formData.append('entidad_encargada', this.autoridadData.entidad_encargada)

      if (this.newFile) {
        formData.append('firma', this.newFile)
      }

      this.errorMessage = null
      this.saving = true
      try {
        await this.$emit('save', formData)
      } catch (error: any) {
        this.errorMessage = error.message || 'Error al guardar la autoridad'
      } finally {
        this.saving = false
      }
    },
    onFileChange(event: Event) {
      const file = (event.target as HTMLInputElement).files?.[0]
      if (file) {
        this.newFile = file
      } else {
        this.newFile = null
      }
    }
  }
})
</script>

<style scoped>
.modal.show {
  background: rgba(0, 0, 0, 0.5);
}
.img-thumbnail {
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 4px;
}
</style>
