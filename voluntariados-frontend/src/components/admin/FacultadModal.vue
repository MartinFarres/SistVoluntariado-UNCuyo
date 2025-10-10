<template>
  <div class="modal fade" :class="{ 'show': show, 'd-block': show }" tabindex="-1" @click.self="close">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ isEdit ? 'Editar' : 'Nueva' }} Facultad</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="facultad-nombre" class="form-label">Nombre</label>
              <input
                id="facultad-nombre"
                v-model="localFacultadData.nombre"
                class="form-control"
                type="text"
                placeholder="Nombre de la facultad"
                required
              >
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" v-model="localFacultadData.activa" id="facultad-activa">
              <label class="form-check-label" for="facultad-activa">
                Activa
              </label>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="close">Cancelar</button>
          <button type="button" class="btn btn-primary" @click="submitForm" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <div v-if="show" class="modal-backdrop fade show"></div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

interface FacultadData {
  id: number | null;
  nombre: string;
  activa: boolean;
}

export default defineComponent({
  name: 'FacultadModal',
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    facultadData: {
      type: Object as PropType<FacultadData>,
      required: true,
    },
  },
  emits: ['close', 'save'],
  data() {
    return {
      localFacultadData: { ...this.facultadData },
      loading: false,
      error: null as string | null,
    };
  },
  watch: {
    facultadData: {
      handler(newData) {
        this.localFacultadData = { ...newData };
        this.error = null;
      },
      deep: true,
    },
  },
  methods: {
    close() {
      if (!this.loading) {
        this.$emit('close');
      }
    },
    async submitForm() {
      if (!this.localFacultadData.nombre) {
        this.error = 'El nombre es obligatorio.';
        return;
      }
      this.loading = true;
      this.error = null;
      try {
        await this.$emit('save', this.localFacultadData);
      } catch (e: any) {
        this.error = e.message || 'Ocurrió un error al guardar la facultad.';
        this.loading = false;
      }
    },
  },
});
</script>

<style scoped>
.modal.d-block {
  display: block;
}
</style>
