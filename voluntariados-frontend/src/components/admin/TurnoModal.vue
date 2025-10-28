<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/TurnoModal.vue -->
<template>
  <div>
    <div
      class="modal fade"
      :class="{ show: show, 'd-block': show }"
      tabindex="-1"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-calendar-plus me-2"></i>
              {{ isEdit ? 'Editar Turno' : 'Crear Nuevo Turno' }}
            </h5>
            <button type="button" class="btn-close" @click="handleClose"></button>
          </div>
          <div class="modal-body compact">
            <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
              <i class="bi bi-exclamation-triangle-fill me-2"></i>
              {{ errorMessage }}
              <button type="button" class="btn-close" @click="errorMessage = null"></button>
            </div>

            <form @submit.prevent="handleSubmit">
              <!-- Fecha Section -->
              <div class="form-section compact">
                <h6 class="form-section-title">
                  <i class="bi bi-calendar3 me-2"></i>
                  Fecha del Turno
                </h6>
                <div class="mb-2">
                  <label for="fecha" class="form-label fw-semibold mb-1 small">Fecha *</label>
                  <input 
                    type="date" 
                    class="form-control form-control-sm" 
                    id="fecha" 
                    v-model="localTurno.fecha" 
                    :min="minDate"
                    :max="maxDate"
                    required
                  >
                  <small class="text-muted d-block mt-1" style="font-size: 0.75rem;">
                    <i class="bi bi-info-circle me-1"></i>
                    {{ dateRangeText }}
                  </small>
                </div>
              </div>

              <!-- Horario Section -->
              <div class="form-section compact">
                <h6 class="form-section-title">
                  <i class="bi bi-clock me-2"></i>
                  Horario
                </h6>
                <div class="row g-2">
                  <div class="col-md-6">
                    <label class="form-label fw-semibold mb-1 small">Hora Inicio *</label>
                    <div class="time-picker-wrapper">
                      <select 
                        class="form-select form-select-sm" 
                        v-model="horaInicioHour"
                        required
                      >
                        <option value="" disabled>HH</option>
                        <option v-for="h in hours" :key="h" :value="h">{{ h }}</option>
                      </select>
                      <span class="time-separator">:</span>
                      <select 
                        class="form-select form-select-sm" 
                        v-model="horaInicioMinute"
                        required
                      >
                        <option value="" disabled>MM</option>
                        <option v-for="m in minutes" :key="m" :value="m">{{ m }}</option>
                      </select>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label fw-semibold mb-1 small">Hora Fin *</label>
                    <div class="time-picker-wrapper">
                      <select 
                        class="form-select form-select-sm" 
                        v-model="horaFinHour"
                        required
                      >
                        <option value="" disabled>HH</option>
                        <option v-for="h in hours" :key="h" :value="h">{{ h }}</option>
                      </select>
                      <span class="time-separator">:</span>
                      <select 
                        class="form-select form-select-sm" 
                        v-model="horaFinMinute"
                        required
                      >
                        <option value="" disabled>MM</option>
                        <option v-for="m in minutes" :key="m" :value="m">{{ m }}</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div v-if="durationText" class="mt-1">
                  <small class="text-primary" style="font-size: 0.75rem;">
                    <i class="bi bi-stopwatch me-1"></i>
                    Duración: <strong>{{ durationText }}</strong>
                  </small>
                </div>
              </div>

              <!-- Detalles Section -->
              <div class="form-section compact">
                <h6 class="form-section-title">
                  <i class="bi bi-info-circle me-2"></i>
                  Detalles
                </h6>
                <div class="row g-2">
                  <div class="col-md-6">
                    <label for="cupo" class="form-label fw-semibold mb-1 small">Cupo *</label>
                    <input 
                      type="number" 
                      class="form-control form-control-sm" 
                      id="cupo" 
                      v-model.number="localTurno.cupo" 
                      required 
                      min="1"
                      placeholder="Ej: 20"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="lugar" class="form-label fw-semibold mb-1 small">Lugar</label>
                    <input 
                      type="text" 
                      class="form-control form-control-sm" 
                      id="lugar" 
                      v-model="localTurno.lugar" 
                      placeholder="Ej: Comedor Universitario"
                    >
                  </div>
                </div>
              </div>

              <!-- Creación Automática Section (only for new turnos) -->
              <div v-if="!isEdit" class="form-section compact">
                <div class="form-check form-switch mb-2">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    id="autoCreate" 
                    v-model="autoCreateEnabled"
                  >
                  <label class="form-check-label fw-semibold small" for="autoCreate">
                    <i class="bi bi-arrow-repeat me-2"></i>
                    Crear turnos automáticamente
                  </label>
                </div>

                <div v-if="autoCreateEnabled" class="auto-create-options">
                  <div class="alert alert-info mb-2 py-2">
                    <i class="bi bi-lightbulb me-2"></i>
                    <small style="font-size: 0.75rem;">Se crearán turnos con el mismo horario y configuración.</small>
                  </div>
                  
                  <div class="mb-2">
                    <label class="form-label fw-semibold mb-1 small">Intervalo *</label>
                    <select 
                      class="form-select form-select-sm" 
                      v-model="autoCreateInterval"
                      required
                    >
                      <option value="daily">Diario (cada día)</option>
                      <option value="weekly">Semanal (cada 7 días)</option>
                    </select>
                  </div>

                  <div class="auto-create-preview">
                    <div class="preview-header">
                      <i class="bi bi-eye me-2"></i>
                      <strong>Vista previa:</strong>
                    </div>
                    <div v-if="previewDates.length > 0" class="preview-list">
                      <div 
                        v-for="(date, idx) in previewDates.slice(0, 8)" 
                        :key="idx"
                        class="preview-item"
                      >
                        <i class="bi bi-calendar-check me-2"></i>
                        {{ formatPreviewDate(date) }}
                      </div>
                      <div v-if="previewDates.length > 8" class="preview-more">
                        <i class="bi bi-three-dots me-2"></i>
                        +{{ previewDates.length - 8 }} más...
                      </div>
                      <div class="preview-total">
                        <strong>Total: {{ previewDates.length }} turno(s)</strong>
                      </div>
                    </div>
                    <div v-else class="text-muted">
                      <i class="bi bi-exclamation-circle me-2"></i>
                      <small>No hay fechas válidas en el rango</small>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer compact">
            <button type="button" class="btn btn-secondary" @click="handleClose">
              <i class="bi bi-x-circle me-2"></i>
              Cancelar
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="handleSubmit"
              :disabled="saving || !isFormValid"
            >
              <span v-if="saving">
                <span class="spinner-border spinner-border-sm me-2"></span>
                Guardando...
              </span>
              <span v-else>
                <i class="bi bi-check-circle me-2"></i>
                {{ saveButtonText }}
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
import { formatDateShort, parseLocalDate } from '@/utils/dateUtils';

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
    turnoData: { type: Object as PropType<Turno | null>, default: null },
    fechaInicioCursado: { type: String as PropType<string | null>, default: null },
    fechaFinCursado: { type: String as PropType<string | null>, default: null },
  },
  emits: ['close', 'save'],
  data() {
    return {
      localTurno: {} as Turno,
      saving: false,
      errorMessage: null as string | null,
      // Time pickers
      horaInicioHour: '',
      horaInicioMinute: '',
      horaFinHour: '',
      horaFinMinute: '',
      hours: [] as string[],
      minutes: [] as string[],
      // Auto create
      autoCreateEnabled: false,
      autoCreateInterval: 'daily' as 'daily' | 'weekly',
    };
  },
  computed: {
    isEdit(): boolean {
      return !!(this.turnoData && this.turnoData.id);
    },
    minDate(): string {
      return this.fechaInicioCursado || '';
    },
    maxDate(): string {
      return this.fechaFinCursado || '';
    },
    dateRangeText(): string {
      if (!this.fechaInicioCursado || !this.fechaFinCursado) {
        return 'Seleccione una fecha';
      }
      return `Rango permitido: ${formatDateShort(this.fechaInicioCursado)} - ${formatDateShort(this.fechaFinCursado)}`;
    },
    durationText(): string {
      if (!this.horaInicioHour || !this.horaInicioMinute || !this.horaFinHour || !this.horaFinMinute) {
        return '';
      }
      const start = parseInt(this.horaInicioHour) * 60 + parseInt(this.horaInicioMinute);
      const end = parseInt(this.horaFinHour) * 60 + parseInt(this.horaFinMinute);
      const diff = end - start;
      if (diff <= 0) return 'Hora fin debe ser posterior a hora inicio';
      const hours = Math.floor(diff / 60);
      const mins = diff % 60;
      if (hours > 0 && mins > 0) return `${hours}h ${mins}min`;
      if (hours > 0) return `${hours}h`;
      return `${mins}min`;
    },
    previewDates(): string[] {
      if (!this.autoCreateEnabled || !this.localTurno.fecha) return [];
      
      const dates: string[] = [];
      const startDate = parseLocalDate(this.localTurno.fecha);
      const minDate = this.fechaInicioCursado ? parseLocalDate(this.fechaInicioCursado) : null;
      const maxDate = this.fechaFinCursado ? parseLocalDate(this.fechaFinCursado) : null;
      
      const increment = this.autoCreateInterval === 'daily' ? 1 : 7;
      let currentDate = new Date(startDate);
      
      // Generate dates within range
      while (true) {
        if (minDate && currentDate < minDate) {
          currentDate = new Date(currentDate.getTime() + increment * 24 * 60 * 60 * 1000);
          continue;
        }
        if (maxDate && currentDate > maxDate) break;
        
        const dateStr = this.formatDateString(currentDate);
        dates.push(dateStr);
        
        currentDate = new Date(currentDate.getTime() + increment * 24 * 60 * 60 * 1000);
        
        // Safety limit
        if (dates.length > 100) break;
      }
      
      return dates;
    },
    isFormValid(): boolean {
      if (!this.localTurno.fecha) return false;
      if (!this.horaInicioHour || !this.horaInicioMinute) return false;
      if (!this.horaFinHour || !this.horaFinMinute) return false;
      if (!this.localTurno.cupo || this.localTurno.cupo <= 0) return false;
      
      // Validate time range
      const start = parseInt(this.horaInicioHour) * 60 + parseInt(this.horaInicioMinute);
      const end = parseInt(this.horaFinHour) * 60 + parseInt(this.horaFinMinute);
      if (end <= start) return false;
      
      return true;
    },
    saveButtonText(): string {
      if (this.autoCreateEnabled && !this.isEdit) {
        return `Crear ${this.previewDates.length} Turno(s)`;
      }
      return this.isEdit ? 'Guardar Cambios' : 'Crear Turno';
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
    turnoData: {
      deep: true,
      immediate: true,
      handler() {
        if (this.show) this.initializeLocalTurno();
      }
    },
    horaInicioHour(val) {
      this.updateHoraInicio();
    },
    horaInicioMinute(val) {
      this.updateHoraInicio();
    },
    horaFinHour(val) {
      this.updateHoraFin();
    },
    horaFinMinute(val) {
      this.updateHoraFin();
    }
  },
  created() {
    // Generate hours (00-23)
    this.hours = Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'));
    // Generate minutes (00, 15, 30, 45)
    this.minutes = ['00', '15', '30', '45'];
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
        
        // Parse times for selects
        const [hh1, mm1] = this.localTurno.hora_inicio.split(':');
        this.horaInicioHour = hh1 || '';
        this.horaInicioMinute = mm1 || '';
        
        const [hh2, mm2] = this.localTurno.hora_fin.split(':');
        this.horaFinHour = hh2 || '';
        this.horaFinMinute = mm2 || '';
      } else {
        this.localTurno = {
          fecha: String(this.initialDate || today),
          hora_inicio: '',
          hora_fin: '',
          cupo: 20,
          lugar: '',
        };
        
        // Default times
        this.horaInicioHour = '09';
        this.horaInicioMinute = '00';
        this.horaFinHour = '12';
        this.horaFinMinute = '00';
        this.updateHoraInicio();
        this.updateHoraFin();
      }
      
      this.errorMessage = null;
      this.saving = false;
      this.autoCreateEnabled = false;
      this.autoCreateInterval = 'daily';
    },
    updateHoraInicio() {
      if (this.horaInicioHour && this.horaInicioMinute) {
        this.localTurno.hora_inicio = `${this.horaInicioHour}:${this.horaInicioMinute}`;
      }
    },
    updateHoraFin() {
      if (this.horaFinHour && this.horaFinMinute) {
        this.localTurno.hora_fin = `${this.horaFinHour}:${this.horaFinMinute}`;
      }
    },
    handleClose() {
      this.$emit('close');
    },
    handleSubmit() {
      if (!this.isFormValid) {
        this.errorMessage = 'Por favor, complete todos los campos obligatorios correctamente.';
        return;
      }
      
      this.errorMessage = null;
      this.saving = true;
      
      // If auto-create is enabled and not editing, emit multiple turnos
      if (this.autoCreateEnabled && !this.isEdit && this.previewDates.length > 0) {
        const turnos = this.previewDates.map(fecha => ({
          ...this.localTurno,
          fecha
        }));
        this.$emit('save', turnos);
      } else {
        this.$emit('save', this.localTurno);
      }
    },
    formatDateString(date: Date): string {
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, '0');
      const d = String(date.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    },
    formatPreviewDate(dateStr: string): string {
      return formatDateShort(dateStr);
    }
  },
});
</script>

<style scoped>
.modal.show { 
  background: rgba(0, 0, 0, 0.5); 
}

.modal-body.compact {
  padding: 1rem 1.25rem;
  max-height: 70vh;
  overflow-y: auto;
  font-size: 0.875rem;
}

.modal-content {
  border: none;
  border-radius: 8px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.modal-title {
  font-size: 1.1rem;
}

.form-section {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 0.75rem;
  margin-bottom: 0.75rem;
}

.form-section.compact {
  padding: 0.6rem 0.75rem;
  margin-bottom: 0.6rem;
}

.form-section-title {
  color: #495057;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid #dee2e6;
}

.time-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.time-picker-wrapper select {
  flex: 1;
  font-size: 0.875rem;
}

.time-separator {
  font-size: 1rem;
  font-weight: bold;
  color: #6c757d;
}

.form-control, .form-select {
  border-radius: 6px;
  border: 1px solid #dee2e6;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.form-control-sm, .form-select-sm {
  padding: 0.4rem 0.65rem;
  font-size: 0.875rem;
}

.form-control:focus, .form-select:focus {
  border-color: var(--brand-mid, #4682B4);
  box-shadow: 0 0 0 0.2rem rgba(70, 130, 180, 0.15);
}

.form-label {
  font-size: 0.875rem;
}

.form-check-input {
  width: 2.5rem;
  height: 1.25rem;
  cursor: pointer;
}

.form-check-input:checked {
  background-color: var(--brand-mid, #4682B4);
  border-color: var(--brand-mid, #4682B4);
}

.form-check-label {
  cursor: pointer;
  font-size: 0.875rem;
}

.auto-create-options {
  background: white;
  border: 2px solid var(--brand-mid, #4682B4);
  border-radius: 6px;
  padding: 0.75rem;
  margin-top: 0.5rem;
}

.auto-create-preview {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 0.75rem;
  margin-top: 0.5rem;
}

.preview-header {
  font-size: 0.8rem;
  color: #495057;
  margin-bottom: 0.5rem;
}

.preview-list {
  max-height: 180px;
  overflow-y: auto;
}

.preview-item {
  background: white;
  padding: 0.35rem 0.6rem;
  border-radius: 4px;
  margin-bottom: 0.35rem;
  border-left: 2px solid var(--brand-mid, #4682B4);
  font-size: 0.8rem;
}

.preview-more {
  text-align: center;
  padding: 0.35rem;
  color: #6c757d;
  font-style: italic;
  font-size: 0.8rem;
}

.preview-total {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #dee2e6;
  text-align: center;
  color: var(--brand-mid, #4682B4);
  font-size: 0.875rem;
}

.alert {
  border-radius: 6px;
  border: none;
  font-size: 0.875rem;
}

.alert-info {
  background: rgba(135, 206, 235, 0.15);
  color: var(--brand-accent, #008080);
}

.alert-danger {
  background: #f8d7da;
  color: #842029;
}

.btn {
  font-size: 0.875rem;
}

.modal-footer.compact {
  border-top: 1px solid #dee2e6;
  padding: 0.75rem 1.25rem;
}

.text-primary {
  color: var(--brand-mid, #4682B4) !important;
}

/* Custom scrollbar for preview list and modal body */
.preview-list::-webkit-scrollbar,
.modal-body.compact::-webkit-scrollbar {
  width: 6px;
}

.preview-list::-webkit-scrollbar-track,
.modal-body.compact::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.preview-list::-webkit-scrollbar-thumb,
.modal-body.compact::-webkit-scrollbar-thumb {
  background: var(--brand-start, #5F9EA0);
  border-radius: 3px;
}

.preview-list::-webkit-scrollbar-thumb:hover,
.modal-body.compact::-webkit-scrollbar-thumb:hover {
  background: var(--brand-accent, #008080);
}
</style>
