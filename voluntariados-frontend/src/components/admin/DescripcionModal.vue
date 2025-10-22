<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/DescripcionModal.vue -->
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
            <i class="bi bi-card-text me-2"></i>
            Crear Nueva Descripción
          </h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ errorMessage }}
          </div>

          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="resumen" class="form-label">Resumen *</label>
              <textarea class="form-control" id="resumen" v-model="localDescripcion.resumen" rows="3" required></textarea>
              <small class="text-muted">Un resumen corto que se mostrará en las listas.</small>
            </div>

            <div class="mb-3">
              <label for="descripcion-detallada" class="form-label">Descripción Detallada</label>
              <textarea class="form-control" id="descripcion-detallada" v-model="localDescripcion.descripcion" rows="5"></textarea>
            </div>

            <div class="mb-3">
              <label for="logo" class="form-label">Logo (Opcional)</label>
              <input type="file" class="form-control" id="logo" @change="handleFileChange($event, 'logo')" accept="image/*">
            </div>

            <div class="mb-3">
              <label for="portada" class="form-label">Portada (Opcional)</label>
              <input type="file" class="form-control" id="portada" @change="handleFileChange($event, 'portada')" accept="image/*">
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleClose">
            <i class="bi bi-x-circle me-2"></i>
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
              <i class="bi bi-check-circle me-2"></i>
              Guardar Descripción
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" v-if="show"></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'DescripcionModal',
  props: {
    show: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['close', 'save'],
  data() {
    return {
      localDescripcion: {
        resumen: '',
        descripcion: '',
        logo: null as File | null,
        portada: null as File | null,
      },
      saving: false,
      errorMessage: null as string | null,
    };
  },
  watch: {
    show(newVal) {
      if (newVal) {
        // Reset form when modal is shown
        this.localDescripcion = {
          resumen: '',
          descripcion: '',
          logo: null,
          portada: null,
        };
        this.errorMessage = null;
        this.saving = false;
      }
    },
  },
  methods: {
    handleClose() {
      this.$emit('close');
    },
    handleFileChange(event: Event, field: 'logo' | 'portada') {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        this.localDescripcion[field] = target.files[0];
      }
    },
    handleSubmit() {
      if (!this.localDescripcion.resumen.trim()) {
        this.errorMessage = 'El resumen es un campo obligatorio.';
        return;
      }
      this.errorMessage = null;

      // For file uploads, we must use FormData
      const formData = new FormData();
      formData.append('resumen', this.localDescripcion.resumen);
      formData.append('descripcion', this.localDescripcion.descripcion);
      if (this.localDescripcion.logo) {
        formData.append('logo', this.localDescripcion.logo);
      }
      if (this.localDescripcion.portada) {
        formData.append('portada', this.localDescripcion.portada);
      }

      this.$emit('save', formData);
    },
  },
});
</script>

<style scoped>
.modal.show {
  background: rgba(0, 0, 0, 0.5);
}
</style>
