<template>
  <div class="modal fade" :class="{ 'show': show, 'd-block': show }" tabindex="-1" @click.self="close">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ isEdit ? 'Editar' : 'Nueva' }} Carrera</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="carrera-nombre" class="form-label">Nombre</label>
              <input
                id="carrera-nombre"
                v-model="localCarreraData.nombre"
                class="form-control"
                type="text"
                placeholder="Nombre de la carrera"
                required
              >
            </div>
            <div class="mb-3">
              <label for="carrera-facultad" class="form-label">Facultad</label>
              <select
                id="carrera-facultad"
                v-model="localCarreraData.facultad"
                class="form-control"
                required
              >
                <option value="" disabled>Seleccione una facultad</option>
                <option v-for="fac in facultades" :key="fac.id" :value="fac.id">
                  {{ fac.nombre }}
                </option>
              </select>
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

export default defineComponent({
  name: 'CarreraModal',
  props: {
    show: { type: Boolean, required: true },
    isEdit: { type: Boolean, default: false },
    carreraData: { type: Object as PropType<any>, required: true },
    facultades: { type: Array as PropType<any[]>, required: true }
  },
  emits: ['close', 'save'],
  data() {
    return {
      localCarreraData: { ...this.carreraData },
      loading: false,
      error: null as string | null,
    };
  },
  watch: {
    carreraData: {
      handler(newData) {
        this.localCarreraData = { ...newData };
        this.error = null;
      },
      deep: true,
    },
    show(newVal) {
      if (!newVal) {
        this.loading = false;
        this.error = null;
      }
    },
  },
  methods: {
    close() {
      if (!this.loading) this.$emit('close');
    },
    submitForm() {
      if (!this.localCarreraData.nombre.trim()) {
        this.error = 'El nombre es obligatorio.';
        return;
      }
      if (!this.localCarreraData.facultad) {
        this.error = 'Debe seleccionar una facultad.';
        return;
      }
      this.loading = true;
      this.error = null;
      this.$emit('save', this.localCarreraData);
    },
  },
});
</script>
