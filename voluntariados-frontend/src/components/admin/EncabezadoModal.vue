<template>
  <div
    class="modal fade"
    :class="{ show: show, 'd-block': show }"
    tabindex="-1"
    v-if="show"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-image text-primary me-2"></i>
            {{ isEdit ? 'Editar Encabezado del Certificado' : 'Nuevo Encabezado del Certificado' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ errorMessage }}
          </div>

          <form @submit.prevent="handleSubmit">
            <div class="row">
              <div v-for="i in 4" :key="i" class="col-md-6 mb-4">
                <label class="form-label">Imagen {{ i }}</label>

                <!-- Vista previa -->
                <div v-if="encabezadoData[`imagen_${i}`]" class="mb-2 text-center">
                  <img
                    :src="encabezadoData[`imagen_${i}`]"
                    alt="Imagen actual"
                    class="img-thumbnail"
                    style="max-height: 120px; object-fit: contain;"
                  />
                  <div class="text-muted small mt-1">
                    Imagen actual — si subís una nueva, se reemplazará
                  </div>
                </div>

                <!-- Input de archivo -->
                <input
                  type="file"
                  class="form-control"
                  accept="image/png,image/jpeg"
                  @change="onFileChange($event, i)"
                />
              </div>
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
              <i class="bi bi-check-circle me-2"></i>{{ isEdit ? 'Actualizar' : 'Guardar' }}
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
  name: 'EncabezadoModal',
  props: {
    show: { type: Boolean, default: false },
    encabezadoData: { type: Object as PropType<any>, required: true },
    isEdit: { type: Boolean, default: false }
  },
  emits: ['close', 'save'],
  data() {
    return {
      saving: false,
      errorMessage: null as string | null,
      newFiles: {} as Record<number, File>
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.errorMessage = null
        this.saving = false
        this.newFiles = {}
      }
    }
  },
  methods: {
    async handleSubmit() {
      if (![1, 2, 3, 4].some(i => this.newFiles[i])) {
        this.errorMessage = 'Debes seleccionar al menos una imagen para actualizar.'
        return
      }

      this.errorMessage = null
      this.saving = true
      try {
        await this.$emit('save', this.newFiles)  // 👈 Emitimos archivos crudos
      } catch (error: any) {
        this.errorMessage = error.message || 'Error al guardar el encabezado'
      } finally {
        this.saving = false
      }
    },
    onFileChange(event: Event, index: number) {
      const file = (event.target as HTMLInputElement).files?.[0]
      if (file) {
        this.newFiles[index] = file
      } else {
        delete this.newFiles[index]
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
