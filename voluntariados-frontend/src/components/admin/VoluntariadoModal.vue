<!-- src/components/admin/VoluntariadoModal.vue -->
<template>
  <div class="modal fade" :class="{ show: show, 'd-block': show }" tabindex="-1" v-if="show">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-heart-fill text-danger me-2"></i>
            {{ isEdit ? "Editar Voluntariado" : "Crear Nuevo Voluntariado" }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <!-- Mensaje de error -->
          <div v-if="errorMessage" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ errorMessage }}
          </div>

          <!-- Mensaje de advertencia -->
          <div v-if="warningMessage" class="alert alert-warning">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ warningMessage }}
          </div>

          <!-- Formulario principal -->
          <form @submit.prevent="handleSubmit">
            <!-- Información básica -->
            <div class="mb-4">
              <h6 class="text-muted mb-3">Información Básica</h6>

              <div class="mb-3">
                <label class="form-label">Nombre *</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="voluntariadoData.nombre"
                  required
                />
              </div>

              <!-- Fechas de convocatoria -->
              <div class="mb-3">
                <h6 class="text-primary mb-2">
                  <i class="bi bi-megaphone-fill me-2"></i>
                  Etapa de Convocatoria
                </h6>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">
                      Fecha Inicio
                      <span
                        v-if="voluntariadoData.fecha_inicio_convocatoria"
                        class="badge bg-primary ms-1"
                      >
                        {{ formatDate(voluntariadoData.fecha_inicio_convocatoria) }}
                      </span>
                    </label>
                    <input
                      type="date"
                      class="form-control date-input-convocatoria"
                      v-model="voluntariadoData.fecha_inicio_convocatoria"
                      :max="voluntariadoData.fecha_fin_convocatoria || undefined"
                    />
                    <small class="text-muted">Inicio del período de inscripción</small>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">
                      Fecha Fin
                      <span
                        v-if="voluntariadoData.fecha_fin_convocatoria"
                        class="badge bg-primary ms-1"
                      >
                        {{ formatDate(voluntariadoData.fecha_fin_convocatoria) }}
                      </span>
                    </label>
                    <input
                      type="date"
                      class="form-control date-input-convocatoria"
                      v-model="voluntariadoData.fecha_fin_convocatoria"
                      :min="voluntariadoData.fecha_inicio_convocatoria || undefined"
                      :max="
                        voluntariadoData.fecha_inicio_cursado
                          ? getDayBefore(voluntariadoData.fecha_inicio_cursado)
                          : undefined
                      "
                    />
                    <small class="text-muted">Cierre del período de inscripción</small>
                  </div>
                </div>
              </div>

              <!-- Visual Timeline -->
              <div v-if="hasAnyDate" class="timeline-container mb-4">
                <div class="timeline-header">
                  <small class="text-muted"
                    ><i class="bi bi-calendar-range me-1"></i>Línea de Tiempo</small
                  >
                </div>
                <div class="timeline">
                  <div
                    v-if="
                      voluntariadoData.fecha_inicio_convocatoria ||
                      voluntariadoData.fecha_fin_convocatoria
                    "
                    class="timeline-stage convocatoria-stage"
                  >
                    <div class="stage-bar bg-primary"></div>
                    <div class="stage-label">
                      <small>Convocatoria</small>
                      <div v-if="getDateRange('convocatoria')" class="date-range">
                        {{ getDateRange("convocatoria") }}
                      </div>
                    </div>
                  </div>
                  <div v-if="showGap" class="timeline-gap">
                    <small class="text-muted">{{ gapDays }} día(s)</small>
                  </div>
                  <div
                    v-if="
                      voluntariadoData.fecha_inicio_cursado || voluntariadoData.fecha_fin_cursado
                    "
                    class="timeline-stage cursado-stage"
                  >
                    <div class="stage-bar bg-success"></div>
                    <div class="stage-label">
                      <small>Cursado</small>
                      <div v-if="getDateRange('cursado')" class="date-range">
                        {{ getDateRange("cursado") }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Fechas de cursado -->
              <div class="mb-3">
                <h6 class="text-success mb-2">
                  <i class="bi bi-book-fill me-2"></i>
                  Etapa de Cursado
                </h6>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">
                      Fecha Inicio
                      <span
                        v-if="voluntariadoData.fecha_inicio_cursado"
                        class="badge bg-success ms-1"
                      >
                        {{ formatDate(voluntariadoData.fecha_inicio_cursado) }}
                      </span>
                    </label>
                    <input
                      type="date"
                      class="form-control date-input-cursado"
                      v-model="voluntariadoData.fecha_inicio_cursado"
                      :min="
                        voluntariadoData.fecha_fin_convocatoria
                          ? getDayAfter(voluntariadoData.fecha_fin_convocatoria)
                          : undefined
                      "
                      :max="voluntariadoData.fecha_fin_cursado || undefined"
                    />
                    <small class="text-muted">Inicio de actividades del voluntariado</small>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">
                      Fecha Fin
                      <span v-if="voluntariadoData.fecha_fin_cursado" class="badge bg-success ms-1">
                        {{ formatDate(voluntariadoData.fecha_fin_cursado) }}
                      </span>
                    </label>
                    <input
                      type="date"
                      class="form-control date-input-cursado"
                      v-model="voluntariadoData.fecha_fin_cursado"
                      :min="voluntariadoData.fecha_inicio_cursado || undefined"
                    />
                    <small class="text-muted">Fin de actividades del voluntariado</small>
                  </div>
                </div>
              </div>
            </div>

            <!-- Información relacionada -->
            <div class="mb-4">
              <h6 class="text-muted mb-3">Información Relacionada</h6>
              <div class="row">
                <!-- Descripción -->
                <div class="col-md-6 mb-3">
                  <label class="form-label">Descripción *</label>
                  <div class="input-group">
                    <input
                      type="text"
                      class="form-control"
                      :value="
                        voluntariadoData.descripcion
                          ? voluntariadoData.descripcion.descripcion
                          : 'No asignada'
                      "
                      readonly
                    />
                    <button
                      class="btn btn-outline-secondary"
                      type="button"
                      @click="$emit('open-descripcion-modal')"
                    >
                      Crear
                    </button>
                  </div>
                </div>

                <!-- Organización -->
                <div class="col-md-6 mb-3">
                  <label class="form-label">Organización (opcional)</label>
                  <select
                    class="form-control"
                    v-model="voluntariadoData.organizacion"
                  >
                    <option :value="undefined">Sin organización</option>
                    <option
                      v-for="org in organizacionesList"
                      :key="org.id"
                      :value="org.id"
                    >
                      {{ org.nombre }}

                    </option>
                  </select>
                </div>
              </div>

              <!-- Gestión de turnos movida a una vista dedicada -->
            </div>
          </form>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            <i class="bi bi-x-circle me-2"></i> Cancelar
          </button>
          <button type="button" class="btn btn-primary" @click="handleSubmit" :disabled="saving">
            <span v-if="saving">
              <span class="spinner-border spinner-border-sm me-2"></span>Guardando...
            </span>
            <span v-else>
              <i class="bi bi-check-circle me-2"></i>{{ isEdit ? "Actualizar" : "Crear" }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal-backdrop fade show" v-if="show"></div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

export default defineComponent({
  name: "VoluntariadoModal",
  props: {
    show: { type: Boolean, default: false },
    isEdit: { type: Boolean, default: false },
    voluntariadoData: { type: Object as PropType<any>, required: true },
    organizacionesList: { type: Array as PropType<any[]>, default: () => [] }
  },
  emits: ["close", "save", "open-descripcion-modal"],
  data() {
    return {
      saving: false,
      errorMessage: null as string | null,
      warningMessage: null as string | null,
    };
  },
  computed: {
    hasAnyDate(): boolean {
      return !!(
        this.voluntariadoData.fecha_inicio_convocatoria ||
        this.voluntariadoData.fecha_fin_convocatoria ||
        this.voluntariadoData.fecha_inicio_cursado ||
        this.voluntariadoData.fecha_fin_cursado
      );
    },
    showGap(): boolean {
      return !!(
        this.voluntariadoData.fecha_fin_convocatoria && this.voluntariadoData.fecha_inicio_cursado
      );
    },
    gapDays(): number {
      if (
        !this.voluntariadoData.fecha_fin_convocatoria ||
        !this.voluntariadoData.fecha_inicio_cursado
      ) {
        return 0;
      }
      const finConv = new Date(this.voluntariadoData.fecha_fin_convocatoria);
      const inicioCurs = new Date(this.voluntariadoData.fecha_inicio_cursado);
      return Math.floor((inicioCurs.getTime() - finConv.getTime()) / (1000 * 60 * 60 * 24));
    },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.errorMessage = null;
        this.warningMessage = null;
        this.saving = false;
      }
    },
    // Watch date changes to validate and show warnings
    "voluntariadoData.fecha_inicio_convocatoria": "validateDates",
    "voluntariadoData.fecha_fin_convocatoria": "validateDates",
    "voluntariadoData.fecha_inicio_cursado": "validateDates",
    "voluntariadoData.fecha_fin_cursado": "validateDates",
  },
  methods: {
    formatDate(dateString: string): string {
      if (!dateString) return "";
      const date = new Date(dateString + "T00:00:00");
      const options: Intl.DateTimeFormatOptions = {
        day: "2-digit",
        month: "short",
        year: "numeric",
      };
      return date.toLocaleDateString("es-ES", options);
    },

    getDayAfter(dateString: string): string {
      const date = new Date(dateString);
      date.setDate(date.getDate() + 1);
      const result = date.toISOString().split("T")[0];
      return result || "";
    },

    getDayBefore(dateString: string): string {
      const date = new Date(dateString);
      date.setDate(date.getDate() - 1);
      const result = date.toISOString().split("T")[0];
      return result || "";
    },

    getDateRange(stage: "convocatoria" | "cursado"): string {
      if (stage === "convocatoria") {
        const inicio = this.voluntariadoData.fecha_inicio_convocatoria;
        const fin = this.voluntariadoData.fecha_fin_convocatoria;
        if (inicio && fin) {
          return `${this.formatDate(inicio)} - ${this.formatDate(fin)}`;
        } else if (inicio) {
          return `Desde ${this.formatDate(inicio)}`;
        } else if (fin) {
          return `Hasta ${this.formatDate(fin)}`;
        }
      } else {
        const inicio = this.voluntariadoData.fecha_inicio_cursado;
        const fin = this.voluntariadoData.fecha_fin_cursado;
        if (inicio && fin) {
          return `${this.formatDate(inicio)} - ${this.formatDate(fin)}`;
        } else if (inicio) {
          return `Desde ${this.formatDate(inicio)}`;
        } else if (fin) {
          return `Hasta ${this.formatDate(fin)}`;
        }
      }
      return "";
    },

    validateDates() {
      this.errorMessage = null;
      this.warningMessage = null;

      const {
        fecha_inicio_convocatoria,
        fecha_fin_convocatoria,
        fecha_inicio_cursado,
        fecha_fin_cursado,
      } = this.voluntariadoData;

      // Only validate if dates are provided
      if (
        !fecha_inicio_convocatoria &&
        !fecha_fin_convocatoria &&
        !fecha_inicio_cursado &&
        !fecha_fin_cursado
      ) {
        return;
      }

      // Validation 2: Start date before end date for convocatoria
      if (fecha_inicio_convocatoria && fecha_fin_convocatoria) {
        if (new Date(fecha_inicio_convocatoria) > new Date(fecha_fin_convocatoria)) {
          this.errorMessage =
            "La fecha de inicio de convocatoria debe ser anterior a la fecha de fin.";
          return;
        }
      }

      // Validation 2: Start date before end date for cursado
      if (fecha_inicio_cursado && fecha_fin_cursado) {
        if (new Date(fecha_inicio_cursado) > new Date(fecha_fin_cursado)) {
          this.errorMessage = "La fecha de inicio de cursado debe ser anterior a la fecha de fin.";
          return;
        }
      }

      // Validation 1: Convocatoria must be before cursado and should not overlap
      if (fecha_fin_convocatoria && fecha_inicio_cursado) {
        const finConv = new Date(fecha_fin_convocatoria);
        const inicioCurs = new Date(fecha_inicio_cursado);

        if (finConv >= inicioCurs) {
          this.errorMessage =
            "La convocatoria debe finalizar antes del inicio del cursado. Las etapas no deben superponerse.";
          return;
        }

        // Validation 3: Warning if stages are too close (3 days or less)
        const daysDiff = Math.floor(
          (inicioCurs.getTime() - finConv.getTime()) / (1000 * 60 * 60 * 24)
        );
        if (daysDiff <= 3) {
          this.warningMessage =
            `Advertencia: Solo hay ${daysDiff} día(s) entre el fin de la convocatoria y el inicio del cursado. ` +
            "Se recomienda dejar más tiempo entre ambas etapas, pero puede continuar si lo desea.";
        }
      }
    },

    async handleSubmit() {
      if (!this.voluntariadoData.nombre) {
        this.errorMessage = "El nombre es obligatorio.";
        return;
      }
      if (!this.voluntariadoData.descripcion) {
        this.errorMessage = "La Descripción es obligatoria.";
        return;
      }
      // Organización es ahora opcional, no se valida
      // Nota: No se validan fechas aquí; se derivan de los turnos cargados.

      // Validate dates before submitting
      this.validateDates();
      if (this.errorMessage) {
        return;
      }

      // If there's a warning but no error, user can still proceed
      this.saving = true;
      try {
        await this.$emit("save", this.voluntariadoData);
      } catch (error: any) {
        this.errorMessage = error.message || "Error al guardar el voluntariado";
      } finally {
        this.saving = false;
      }
    },
  },
});
</script>

<style scoped>
.modal.show {
  background: rgba(0, 0, 0, 0.5);
}
.modal-lg {
  max-width: 900px;
}
.table-sm th,
.table-sm td {
  padding: 0.5rem;
}

/* Date input styling */
.date-input-convocatoria:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.date-input-cursado:focus {
  border-color: #198754;
  box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25);
}

/* Timeline container */
.timeline-container {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid #dee2e6;
}

.timeline-header {
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.timeline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-height: 60px;
}

.timeline-stage {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stage-bar {
  height: 30px;
  border-radius: 0.25rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stage-bar:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.stage-label {
  text-align: center;
  font-weight: 600;
  color: #495057;
}

.stage-label small {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.date-range {
  font-size: 0.7rem;
  color: #6c757d;
  font-weight: normal;
  margin-top: 0.25rem;
}

.timeline-gap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 0.5rem;
  position: relative;
}

.timeline-gap::before {
  content: "→";
  font-size: 1.5rem;
  color: #6c757d;
  display: block;
}

.timeline-gap small {
  position: absolute;
  bottom: -20px;
  white-space: nowrap;
  background: #fff;
  padding: 0.1rem 0.3rem;
  border-radius: 0.25rem;
  font-size: 0.65rem;
  border: 1px solid #dee2e6;
}

/* Badge styling */
.badge {
  font-weight: 500;
  padding: 0.25rem 0.5rem;
  font-size: 0.7rem;
}

/* Helper text */
small.text-muted {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.75rem;
}

/* Section headers */
h6.text-primary,
h6.text-success {
  font-weight: 600;
  display: flex;
  align-items: center;
  padding: 0.5rem;
  background: rgba(13, 110, 253, 0.05);
  border-radius: 0.25rem;
  margin-bottom: 1rem;
}

h6.text-success {
  background: rgba(25, 135, 84, 0.05);
}

h6 i {
  font-size: 1.1rem;
}
</style>
