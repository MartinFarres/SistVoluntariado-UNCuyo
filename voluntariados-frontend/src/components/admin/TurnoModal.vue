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
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

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
    show: {
      immediate: true,
      handler(newVal) {
        console.log('[TurnoModal] show changed to:', newVal)
        if (newVal) this.initializeLocalTurno();
      }
    },
    // If parent updates turnoData while modal is open, refresh values
    turnoData: {
      deep: true,
      immediate: true,
      handler() {
        if (this.show) this.initializeLocalTurno();
      }
    }
  },
  methods: {
  normalizeTimeToInput(t: string | null | undefined) {
      if (!t) return '';
      if (typeof t === 'string') {
        const parts = t.split(':');
        if (parts.length >= 2) {
          const hh = (parts[0] || '').padStart(2, '0');
          const mm = (parts[1] || '').padStart(2, '0');
          return `${hh}:${mm}`;
        }
      }
      return '';
    },
    initializeLocalTurno() {
      const today = new Date().toISOString().split('T')[0];
      if (this.isEdit && this.turnoData) {
        this.localTurno = {
          id: this.turnoData.id,
          fecha: ((this.turnoData as any)?.fecha ?? today) as string,
          hora_inicio: this.normalizeTimeToInput((this.turnoData as any).hora_inicio),
          hora_fin: this.normalizeTimeToInput((this.turnoData as any).hora_fin),
          cupo: Number((this.turnoData as any).cupo) || 1,
          lugar: (this.turnoData as any).lugar || '',
        };
      } else {
        this.localTurno = {
          fecha: String(this.initialDate || today),
          hora_inicio: '',
          hora_fin: '',
          cupo: 1,
          lugar: '',
        };
      }
      this.errorMessage = null;
      this.saving = false;
    },
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
