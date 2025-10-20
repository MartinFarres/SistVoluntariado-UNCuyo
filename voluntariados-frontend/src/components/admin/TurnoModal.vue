<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/TurnoModal.vue -->
<template>
  <div>
    <div
      class="modal fade"
      :class="{ show: show, 'd-block': show }"
      tabindex="-1"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-calendar-plus me-2"></i>
              {{ isEdit ? 'Editar Turno' : 'Crear Nuevo Turno' }}
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
                <label for="fecha" class="form-label">Fecha *</label>
                <input type="date" class="form-control" id="fecha" v-model="localTurno.fecha" required>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="hora_inicio" class="form-label">Hora Inicio *</label>
                  <input type="time" class="form-control" id="hora_inicio" v-model="localTurno.hora_inicio" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="hora_fin" class="form-label">Hora Fin *</label>
                  <input type="time" class="form-control" id="hora_fin" v-model="localTurno.hora_fin" required>
                </div>
              </div>

              <div class="mb-3">
                <label for="cupo" class="form-label">Cupo *</label>
                <input type="number" class="form-control" id="cupo" v-model.number="localTurno.cupo" required min="1">
              </div>

              <div class="mb-3">
                <label for="lugar" class="form-label">Lugar</label>
                <input type="text" class="form-control" id="lugar" v-model="localTurno.lugar" placeholder="e.g., Comedor Universitario">
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
                Guardar Turno
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="show"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

interface Turno {
  id?: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  cupo: number;
  lugar: string;
}

export default defineComponent({
  name: 'TurnoModal',
  props: {
    show: { type: Boolean, default: false },
    initialDate: { type: String, default: '' },
    turnoData: { type: Object as PropType<Turno | null>, default: null }
  },
  emits: ['close', 'save'],
  data() {
    return {
      localTurno: {} as Turno,
      saving: false,
      errorMessage: null as string | null,
    };
  },
  computed: {
    isEdit(): boolean {
      return !!(this.turnoData && this.turnoData.id);
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        if (this.isEdit && this.turnoData) {
          this.localTurno = { ...this.turnoData };
        } else {
          this.localTurno = {
            fecha: this.initialDate || new Date().toISOString().split('T')[0],
            hora_inicio: '',
            hora_fin: '',
            cupo: 1,
            lugar: '',
          };
        }
        this.errorMessage = null;
        this.saving = false;
      }
    },
  },
  methods: {
    handleClose() {
      this.$emit('close');
    },
    handleSubmit() {
      if (!this.localTurno.fecha || !this.localTurno.hora_inicio || !this.localTurno.hora_fin || this.localTurno.cupo <= 0) {
        this.errorMessage = 'Por favor, complete todos los campos obligatorios (Fecha, Hora Inicio, Hora Fin, Cupo).';
        return;
      }
      this.errorMessage = null;
      this.saving = true;
      this.$emit('save', this.localTurno);
    },
  },
});
</script>

<style scoped>
.modal.show { background: rgba(0, 0, 0, 0.5); }
</style>
