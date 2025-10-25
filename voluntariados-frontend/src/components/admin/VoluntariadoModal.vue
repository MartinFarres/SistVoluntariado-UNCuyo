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
          <button type="button" class="btn-close" @click="emitClose"></button>
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
                  v-model="localVoluntariadoData.nombre"
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
                    <label class="form-label">Fecha Inicio</label>
                    <input
                      type="date"
                      class="form-control date-input-convocatoria"
                      v-model="localVoluntariadoData.fecha_inicio_convocatoria"
                      :max="convocatoriaMaxInicio"
                    />
                    <small class="text-muted">Inicio del período de inscripción</small>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Fecha Fin</label>
                    <input
                      type="date"
                      class="form-control date-input-convocatoria"
                      v-model="localVoluntariadoData.fecha_fin_convocatoria"
                      :min="convocatoriaMinFin"
                      :max="cursadoMinInicio ? getDayBefore(cursadoMinInicio) : undefined"
                    />
                    <small class="text-muted">Cierre del período de inscripción</small>
                  </div>
                </div>
              </div>
              <!-- Timeline -->
              <div v-if="hasAnyDate" class="timeline-container mb-4">
                <div class="timeline-header">
                  <small class="text-muted">
                    <i class="bi bi-calendar-range me-1"></i>Línea de Tiempo
                  </small>
                </div>
                <div class="timeline">
                  <div
                    v-if="
                      localVoluntariadoData.fecha_inicio_convocatoria ||
                      localVoluntariadoData.fecha_fin_convocatoria
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
                      localVoluntariadoData.fecha_inicio_cursado ||
                      localVoluntariadoData.fecha_fin_cursado
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
                    <label class="form-label">Fecha Inicio</label>
                    <input
                      type="date"
                      class="form-control date-input-cursado"
                      v-model="localVoluntariadoData.fecha_inicio_cursado"
                      :min="cursadoMinInicio"
                      :max="localVoluntariadoData.fecha_fin_cursado || undefined"
                    />
                    <small class="text-muted">Inicio de actividades del voluntariado</small>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Fecha Fin</label>
                    <input
                      type="date"
                      class="form-control date-input-cursado"
                      v-model="localVoluntariadoData.fecha_fin_cursado"
                      :min="localVoluntariadoData.fecha_inicio_cursado || undefined"
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
                        localVoluntariadoData.descripcion
                          ? typeof localVoluntariadoData.descripcion === 'object'
                            ? localVoluntariadoData.descripcion.descripcion
                            : localVoluntariadoData.descripcion
                          : 'No asignada'
                      "
                      readonly
                    />
                    <button
                      class="btn btn-outline-secondary"
                      type="button"
                      @click="emitOpenDescripcionModal"
                    >
                      Crear
                    </button>
                  </div>
                </div>
                <!-- Organización -->
                <div class="col-md-6 mb-3">
                  <label class="form-label">Organización (opcional)</label>
                  <select class="form-control" v-model="localVoluntariadoData.organizacion">
                    <option :value="undefined">Sin organización</option>
                    <option v-for="org in organizacionesList" :key="org.id" :value="org.id">
                      {{ org.nombre }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-12 mb-3">
                  <label class="form-label">Ubicación en el mapa</label>
                  <GoogleMapSelector
                    :latitud="localVoluntariadoData.latitud"
                    :longitud="localVoluntariadoData.longitud"
                    :placeId="localVoluntariadoData.place_id"
                    @location-selected="onLocationSelected"
                  />
                  <small class="text-muted"
                    >Selecciona la ubicación en el mapa. Se actualizarán latitud, longitud y
                    place_id automáticamente.</small
                  >
                </div>
              </div>
              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label">Latitud</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="localVoluntariadoData.latitud"
                    readonly
                  />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Longitud</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="localVoluntariadoData.longitud"
                    readonly
                  />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Google Place ID</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="localVoluntariadoData.place_id"
                    readonly
                  />
                </div>
              </div>
            </div>
          </form>
        </div>
        <!-- Footer -->
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="emitClose">
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
<script setup lang="ts">
import { ref, computed, watch } from "vue";
// Calendar logic: restrict selectable dates
const convocatoriaMaxInicio = computed(() => {
  // fecha_inicio_convocatoria cannot be after fecha_fin_convocatoria
  return localVoluntariadoData.value.fecha_fin_convocatoria || undefined;
});
const convocatoriaMinFin = computed(() => {
  // fecha_fin_convocatoria cannot be before fecha_inicio_convocatoria
  return localVoluntariadoData.value.fecha_inicio_convocatoria || undefined;
});
const cursadoMinInicio = computed(() => {
  // fecha_inicio_cursado must be after fecha_fin_convocatoria
  return localVoluntariadoData.value.fecha_fin_convocatoria
    ? getDayAfter(localVoluntariadoData.value.fecha_fin_convocatoria)
    : undefined;
});
import GoogleMapSelector from "./GoogleMapSelector.vue";

interface VoluntariadoData {
  nombre?: string;
  descripcion?: string | { descripcion: string };
  fecha_inicio_convocatoria?: string;
  fecha_fin_convocatoria?: string;
  fecha_inicio_cursado?: string;
  fecha_fin_cursado?: string;
  organizacion?: number;
  latitud?: number | string;
  longitud?: number | string;
  place_id?: string;
}

const props = defineProps<{
  show: boolean;
  isEdit: boolean;
  voluntariadoData: VoluntariadoData;
  organizacionesList: Array<{ id: number; nombre: string }>;
}>();
const emit = defineEmits(["close", "save", "open-descripcion-modal"]);

const saving = ref(false);
const errorMessage = ref<string | null>(null);
const warningMessage = ref<string | null>(null);

const localVoluntariadoData = ref<VoluntariadoData>({ ...props.voluntariadoData });

// Only update localVoluntariadoData when modal opens
watch(
  () => props.show,
  (newVal) => {
    if (newVal) {
      errorMessage.value = null;
      warningMessage.value = null;
      saving.value = false;
      localVoluntariadoData.value = { ...props.voluntariadoData };
    }
  }
);

// When description changes, update only the descripcion field
watch(
  () => props.voluntariadoData.descripcion,
  (newDescripcion) => {
    localVoluntariadoData.value.descripcion = newDescripcion;
  }
);

watch(
  () => props.show,
  (newVal) => {
    if (newVal) {
      errorMessage.value = null;
      warningMessage.value = null;
      saving.value = false;
      localVoluntariadoData.value = { ...props.voluntariadoData };
    }
  }
);

// Watch for changes in voluntariadoData.descripcion and update localVoluntariadoData.descripcion
watch(
  () => props.voluntariadoData.descripcion,
  (newDescripcion) => {
    localVoluntariadoData.value.descripcion = newDescripcion;
  }
);

watch(
  () => [
    localVoluntariadoData.value.fecha_inicio_convocatoria,
    localVoluntariadoData.value.fecha_fin_convocatoria,
    localVoluntariadoData.value.fecha_inicio_cursado,
    localVoluntariadoData.value.fecha_fin_cursado,
  ],
  validateDates
);

function emitClose() {
  emit("close");
}
function emitOpenDescripcionModal() {
  emit("open-descripcion-modal");
}

function formatDate(dateString: string): string {
  if (!dateString) return "";
  const date = new Date(dateString + "T00:00:00");
  const options: Intl.DateTimeFormatOptions = {
    day: "2-digit",
    month: "short",
    year: "numeric",
  };
  return date.toLocaleDateString("es-ES", options);
}
function getDayAfter(dateString: string): string {
  const date = new Date(dateString);
  date.setDate(date.getDate() + 1);
  const result = date.toISOString().split("T")[0];
  return result || "";
}
function getDayBefore(dateString: string): string {
  const date = new Date(dateString);
  date.setDate(date.getDate() - 1);
  const result = date.toISOString().split("T")[0];
  return result || "";
}
function getDateRange(stage: "convocatoria" | "cursado"): string {
  const v = localVoluntariadoData.value;
  if (stage === "convocatoria") {
    const inicio = v.fecha_inicio_convocatoria || "";
    const fin = v.fecha_fin_convocatoria || "";
    if (inicio && fin) {
      return `${formatDate(inicio)} - ${formatDate(fin)}`;
    } else if (inicio) {
      return `Desde ${formatDate(inicio)}`;
    } else if (fin) {
      return `Hasta ${formatDate(fin)}`;
    }
  } else {
    const inicio = v.fecha_inicio_cursado || "";
    const fin = v.fecha_fin_cursado || "";
    if (inicio && fin) {
      return `${formatDate(inicio)} - ${formatDate(fin)}`;
    } else if (inicio) {
      return `Desde ${formatDate(inicio)}`;
    } else if (fin) {
      return `Hasta ${formatDate(fin)}`;
    }
  }
  return "";
}

function validateDates() {
  errorMessage.value = null;
  warningMessage.value = null;
  const {
    fecha_inicio_convocatoria,
    fecha_fin_convocatoria,
    fecha_inicio_cursado,
    fecha_fin_cursado,
  } = localVoluntariadoData.value;
  if (
    !fecha_inicio_convocatoria &&
    !fecha_fin_convocatoria &&
    !fecha_inicio_cursado &&
    !fecha_fin_cursado
  ) {
    return;
  }
  if (fecha_inicio_convocatoria && fecha_fin_convocatoria) {
    if (new Date(fecha_inicio_convocatoria) > new Date(fecha_fin_convocatoria)) {
      errorMessage.value =
        "La fecha de inicio de convocatoria debe ser anterior a la fecha de fin.";
      return;
    }
  }
  if (fecha_inicio_cursado && fecha_fin_cursado) {
    if (new Date(fecha_inicio_cursado) > new Date(fecha_fin_cursado)) {
      errorMessage.value = "La fecha de inicio de cursado debe ser anterior a la fecha de fin.";
      return;
    }
  }
  if (fecha_fin_convocatoria && fecha_inicio_cursado) {
    const finConv = new Date(fecha_fin_convocatoria);
    const inicioCurs = new Date(fecha_inicio_cursado);
    if (finConv >= inicioCurs) {
      errorMessage.value =
        "La convocatoria debe finalizar antes del inicio del cursado. Las etapas no deben superponerse.";
      return;
    }
    const daysDiff = Math.floor((inicioCurs.getTime() - finConv.getTime()) / (1000 * 60 * 60 * 24));
    if (daysDiff <= 3) {
      warningMessage.value =
        `Advertencia: Solo hay ${daysDiff} día(s) entre el fin de la convocatoria y el inicio del cursado. ` +
        "Se recomienda dejar más tiempo entre ambas etapas, pero puede continuar si lo desea.";
    }
  }
}

async function handleSubmit() {
  if (!localVoluntariadoData.value.nombre) {
    errorMessage.value = "El nombre es obligatorio.";
    return;
  }
  if (!localVoluntariadoData.value.descripcion) {
    errorMessage.value = "La Descripción es obligatoria.";
    return;
  }
  validateDates();
  if (errorMessage.value) {
    return;
  }
  saving.value = true;
  try {
    await emit("save", localVoluntariadoData.value);
  } catch (error) {
    errorMessage.value = (error as Error).message || "Error al guardar el voluntariado";
  } finally {
    saving.value = false;
  }
}

function onLocationSelected({
  latitud,
  longitud,
  place_id,
}: {
  latitud: number;
  longitud: number;
  place_id: string;
}) {
  localVoluntariadoData.value.latitud = latitud;
  localVoluntariadoData.value.longitud = longitud;
  localVoluntariadoData.value.place_id = place_id;
}

const hasAnyDate = computed(() => {
  const v = localVoluntariadoData.value;
  return !!(
    v.fecha_inicio_convocatoria ||
    v.fecha_fin_convocatoria ||
    v.fecha_inicio_cursado ||
    v.fecha_fin_cursado
  );
});
const showGap = computed(() => {
  const v = localVoluntariadoData.value;
  return !!(v.fecha_fin_convocatoria && v.fecha_inicio_cursado);
});
const gapDays = computed(() => {
  const v = localVoluntariadoData.value;
  if (!v.fecha_fin_convocatoria || !v.fecha_inicio_cursado) return 0;
  const finConv = new Date(v.fecha_fin_convocatoria);
  const inicioCurs = new Date(v.fecha_inicio_cursado);
  return Math.floor((inicioCurs.getTime() - finConv.getTime()) / (1000 * 60 * 60 * 24));
});
</script>

<style>
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
/* Add your styles here if needed */
</style>
