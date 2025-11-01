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
          <div
            v-if="errorMessage"
            class="alert alert-danger alert-dismissible fade show"
            role="alert"
          >
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>Error:</strong> {{ errorMessage }}
            <button type="button" class="btn-close" @click="errorMessage = null"></button>
          </div>
          <!-- Mensaje de advertencia -->
          <div
            v-if="warningMessage"
            class="alert alert-warning alert-dismissible fade show"
            role="alert"
          >
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>Advertencia:</strong> {{ warningMessage }}
            <button type="button" class="btn-close" @click="warningMessage = null"></button>
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
              <!-- Requiere convocatoria previa -->
              <div class="mb-3">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="requiereConvocatoria"
                    v-model="localVoluntariadoData.requiere_convocatoria"
                  />
                  <label class="form-check-label" for="requiereConvocatoria">
                    Requiere convocatoria previa para inscribirse a turnos
                  </label>
                </div>
                <small class="text-muted">
                  Si está marcado, los voluntarios deben estar aceptados en la convocatoria antes de
                  inscribirse a turnos.
                </small>
              </div>
              <!-- Fechas de convocatoria (solo visible si requiere_convocatoria es true) -->
              <div v-if="localVoluntariadoData.requiere_convocatoria" class="mb-3">
                <h6 class="text-primary mb-2">
                  <i class="bi bi-megaphone-fill me-2"></i>
                  Etapa de Convocatoria *
                </h6>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Fecha Inicio *</label>
                    <input
                      type="date"
                      class="form-control date-input-convocatoria"
                      v-model="localVoluntariadoData.fecha_inicio_convocatoria"
                      :max="convocatoriaMaxInicio"
                      required
                    />
                    <small class="text-muted">Inicio del período de inscripción</small>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Fecha Fin *</label>
                    <input
                      type="date"
                      class="form-control date-input-convocatoria"
                      v-model="localVoluntariadoData.fecha_fin_convocatoria"
                      :min="convocatoriaMinFin"
                      :max="cursadoMinInicio ? getDayBefore(cursadoMinInicio) : undefined"
                      required
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
                      localVoluntariadoData.requiere_convocatoria &&
                      (localVoluntariadoData.fecha_inicio_convocatoria ||
                        localVoluntariadoData.fecha_fin_convocatoria)
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
                  Etapa de Cursado *
                </h6>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Fecha Inicio *</label>
                    <input
                      type="date"
                      class="form-control date-input-cursado"
                      v-model="localVoluntariadoData.fecha_inicio_cursado"
                      :min="cursadoMinInicio"
                      :max="localVoluntariadoData.fecha_fin_cursado || undefined"
                      required
                    />
                    <small class="text-muted">Inicio de actividades del voluntariado</small>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Fecha Fin *</label>
                    <input
                      type="date"
                      class="form-control date-input-cursado"
                      v-model="localVoluntariadoData.fecha_fin_cursado"
                      :min="localVoluntariadoData.fecha_inicio_cursado || undefined"
                      required
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
                      Seleccionar
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
                  <!-- Google Places Autocomplete input -->
                  <div class="mb-2">
                    <div class="input-group">
                      <input
                        v-if="mapsReady"
                        ref="autocompleteInputRef"
                        type="text"
                        id="voluntariado-place-autocomplete"
                        class="form-control"
                        placeholder="Buscar dirección, lugar o copiar código Plus Code"
                      />
                      <input
                        v-else
                        type="text"
                        class="form-control"
                        disabled
                        :placeholder="
                          googleApiKey ? 'Cargando Autocomplete…' : 'Falta VITE_GOOGLE_MAPS_API_KEY'
                        "
                      />
                      <button
                        class="btn btn-outline-secondary"
                        type="button"
                        @click="showTooltipModal = true"
                        title="Ayuda para buscar ubicaciones"
                      >
                        <i class="bi bi-info-circle"></i>
                      </button>
                    </div>
                    <small class="text-muted"
                      >Usa el buscador para elegir un lugar. Luego puedes ajustar el pin en el mapa
                      si hace falta.</small
                    >
                  </div>
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

  <!-- Description selector modal: pick existing or create new -->
  <DescripcionSelectorModal
    :show="showDescripcionSelector"
    @close="showDescripcionSelector = false"
    @select="onDescripcionSelected"
  />

  <!-- Help modal for location search -->
  <LocationSearchHelpModal :show="showTooltipModal" @close="showTooltipModal = false" />
</template>
<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from "vue";
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
import DescripcionSelectorModal from "./DescripcionSelectorModal.vue";
import LocationSearchHelpModal from "./LocationSearchHelpModal.vue";

interface Descripcion {
  id?: number;
  resumen?: string;
  descripcion?: string;
  logo?: string | null;
  portada?: string | null;
}

interface VoluntariadoData {
  nombre?: string;
  descripcion?: string | { descripcion: string } | Descripcion;
  fecha_inicio_convocatoria?: string;
  fecha_fin_convocatoria?: string;
  fecha_inicio_cursado?: string;
  fecha_fin_cursado?: string;
  organizacion?: number;
  latitud?: number | string;
  longitud?: number | string;
  place_id?: string;
  requiere_convocatoria?: boolean;
}

const props = defineProps<{
  show: boolean;
  isEdit: boolean;
  voluntariadoData: VoluntariadoData;
  organizacionesList: Array<{ id: number; nombre: string }>;
}>();
const emit = defineEmits(["close", "save"]);

const saving = ref(false);
const errorMessage = ref<string | null>(null);
const warningMessage = ref<string | null>(null);

const localVoluntariadoData = ref<VoluntariadoData>({ ...props.voluntariadoData });

const showDescripcionSelector = ref(false);
const googleApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string | undefined;
const mapsReady = ref(false);
const autocompleteInputRef = ref<HTMLInputElement | null>(null);
const showTooltipModal = ref(false);

function ensureGoogleMapsScript(): Promise<void> {
  return new Promise((resolve, reject) => {
    const g = (globalThis as unknown as { google?: typeof google }).google;
    if (g && g.maps && g.maps.places) return resolve();
    if (!googleApiKey) {
      // Without API key we can't load the script; leave mapsReady false
      return reject(new Error("Missing Google Maps API key"));
    }
    const existing = document.querySelector(
      'script[src^="https://maps.googleapis.com/maps/api/js"]'
    ) as HTMLScriptElement | null;
    if (existing) {
      existing.addEventListener("load", () => resolve());
      existing.addEventListener("error", () => reject(new Error("Google Maps failed to load")));
      return;
    }
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${googleApiKey}&libraries=places&loading=async`;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Google Maps failed to load"));
    document.head.appendChild(script);
  });
}

function onDescripcionSelected(desc: Descripcion) {
  localVoluntariadoData.value.descripcion = desc;
  showDescripcionSelector.value = false;
}

// Only update localVoluntariadoData when modal opens
watch(
  () => props.show,
  (newVal) => {
    if (newVal) {
      errorMessage.value = null;
      warningMessage.value = null;
      saving.value = false;
      localVoluntariadoData.value = { ...props.voluntariadoData };
      ensureGoogleMapsScript()
        .then(() => {
          mapsReady.value = true;
        })
        .catch(() => {
          mapsReady.value = false;
        });
    }
  }
);

watch(
  () => mapsReady.value,
  async (ready) => {
    if (ready) {
      // Wait for the v-if to render the input
      await nextTick();

      if (autocompleteInputRef.value) {
        // Initialize Google Places Autocomplete on our input
        const g = (globalThis as unknown as { google?: typeof google }).google;
        if (g?.maps?.places) {
          const autocomplete = new g.maps.places.Autocomplete(autocompleteInputRef.value, {
            fields: ["geometry", "place_id", "formatted_address", "name"],
            componentRestrictions: { country: "ar" },
          });

          autocomplete.addListener("place_changed", () => {
            const place = autocomplete.getPlace();

            if (place && place.geometry && place.geometry.location) {
              const location = place.geometry.location;
              let lat: number;
              let lng: number;

              if (typeof location.lat === "function") {
                lat = location.lat();
                lng = location.lng();
              } else {
                lat = location.lat as unknown as number;
                lng = location.lng as unknown as number;
              }

              const placeId = place.place_id || "";

              localVoluntariadoData.value.latitud = lat;
              localVoluntariadoData.value.longitud = lng;
              localVoluntariadoData.value.place_id = placeId;
            }
          });
        }
      }
    }
  }
);

onMounted(() => {
  if (props.show) {
    ensureGoogleMapsScript()
      .then(() => {
        mapsReady.value = true;
      })
      .catch(() => {
        mapsReady.value = false;
      });
  }
});

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

// Clear convocatoria dates when requiere_convocatoria is set to false
watch(
  () => localVoluntariadoData.value.requiere_convocatoria,
  (newValue) => {
    if (!newValue) {
      // Clear convocatoria dates when checkbox is unchecked
      localVoluntariadoData.value.fecha_inicio_convocatoria = undefined;
      localVoluntariadoData.value.fecha_fin_convocatoria = undefined;
    }
  }
);

function emitClose() {
  emit("close");
}
function emitOpenDescripcionModal() {
  // Open the local selector modal so admin can pick or create a description
  showDescripcionSelector.value = true;
}

function scrollToTop() {
  // Scroll modal body to top to show error messages
  const modalBody = document.querySelector(".modal-body");
  if (modalBody) {
    modalBody.scrollTop = 0;
  }
}

function isRecord(val: unknown): val is Record<string, unknown> {
  return typeof val === "object" && val !== null;
}
function hasStringDetail(val: unknown): val is { detail: string } {
  return isRecord(val) && typeof (val as Record<string, unknown>).detail === "string";
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
    requiere_convocatoria,
  } = localVoluntariadoData.value;

  // Get today's date for comparison (without time)
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Validate convocatoria dates if required
  if (requiere_convocatoria) {
    if (fecha_inicio_convocatoria && fecha_fin_convocatoria) {
      const inicioConv = new Date(fecha_inicio_convocatoria);
      const finConv = new Date(fecha_fin_convocatoria);

      // Check if start is before end
      if (inicioConv > finConv) {
        errorMessage.value =
          "La fecha de inicio de convocatoria debe ser anterior a la fecha de fin.";
        return;
      }

      // Warn if convocatoria dates are in the past
      if (finConv < today) {
        warningMessage.value = "Advertencia: Las fechas de convocatoria están en el pasado.";
      }
    } else if (fecha_inicio_convocatoria || fecha_fin_convocatoria) {
      // One date is set but not the other
      errorMessage.value =
        "Debe especificar tanto la fecha de inicio como la de fin de convocatoria.";
      return;
    }
  }

  // Validate cursado dates
  if (fecha_inicio_cursado && fecha_fin_cursado) {
    const inicioCurs = new Date(fecha_inicio_cursado);
    const finCurs = new Date(fecha_fin_cursado);

    // Check if start is before end
    if (inicioCurs > finCurs) {
      errorMessage.value = "La fecha de inicio de cursado debe ser anterior a la fecha de fin.";
      return;
    }

    // Check minimum duration (at least 1 day)
    const durationDays = Math.floor(
      (finCurs.getTime() - inicioCurs.getTime()) / (1000 * 60 * 60 * 24)
    );
    if (durationDays < 1) {
      errorMessage.value = "El período de cursado debe tener al menos 1 día de duración.";
      return;
    }

    // Warn if cursado dates are in the past
    if (finCurs < today && !warningMessage.value) {
      warningMessage.value = "Advertencia: Las fechas de cursado están en el pasado.";
    }
  } else if (fecha_inicio_cursado || fecha_fin_cursado) {
    // One date is set but not the other
    errorMessage.value = "Debe especificar tanto la fecha de inicio como la de fin de cursado.";
    return;
  }

  // Validate overlap between convocatoria and cursado if requiere_convocatoria is true
  if (requiere_convocatoria && fecha_fin_convocatoria && fecha_inicio_cursado) {
    const finConv = new Date(fecha_fin_convocatoria);
    const inicioCurs = new Date(fecha_inicio_cursado);

    // Check for overlap or immediate adjacency
    if (finConv >= inicioCurs) {
      errorMessage.value =
        "La convocatoria debe finalizar antes del inicio del cursado. Las etapas no deben superponerse.";
      return;
    }

    // Calculate gap between stages
    const daysDiff = Math.floor((inicioCurs.getTime() - finConv.getTime()) / (1000 * 60 * 60 * 24));

    // Warn if gap is too short
    if (daysDiff <= 3 && !warningMessage.value) {
      warningMessage.value =
        `Advertencia: Solo hay ${daysDiff} día(s) entre el fin de la convocatoria y el inicio del cursado. ` +
        "Se recomienda dejar más tiempo entre ambas etapas para la preparación.";
    }
  }
}

async function handleSubmit() {
  // Clear previous messages
  errorMessage.value = null;
  warningMessage.value = null;

  // Validate required fields
  if (!localVoluntariadoData.value.nombre || !localVoluntariadoData.value.nombre.trim()) {
    errorMessage.value = "El nombre es obligatorio.";
    scrollToTop();
    return;
  }

  if (!localVoluntariadoData.value.descripcion) {
    errorMessage.value = "La Descripción es obligatoria.";
    scrollToTop();
    return;
  }

  // Validate convocatoria dates if required
  if (localVoluntariadoData.value.requiere_convocatoria) {
    if (
      !localVoluntariadoData.value.fecha_inicio_convocatoria ||
      !localVoluntariadoData.value.fecha_fin_convocatoria
    ) {
      errorMessage.value =
        "Si requiere convocatoria, debe especificar las fechas de inicio y fin de convocatoria.";
      scrollToTop();
      return;
    }
  }

  // Validate cursado dates
  if (
    !localVoluntariadoData.value.fecha_inicio_cursado ||
    !localVoluntariadoData.value.fecha_fin_cursado
  ) {
    errorMessage.value = "Las fechas de inicio y fin de cursado son obligatorias.";
    scrollToTop();
    return;
  }

  // Validate date ranges and overlaps
  validateDates();
  if (errorMessage.value) {
    scrollToTop();
    return;
  }

  saving.value = true;
  try {
    await emit("save", localVoluntariadoData.value);
  } catch (error) {
    const err = error as { response?: { data?: unknown }; message?: string };
    if (err.response && typeof err.response.data !== "undefined") {
      // Handle backend validation errors
      const backendErrors = err.response.data;
      if (typeof backendErrors === "string") {
        errorMessage.value = backendErrors;
      } else if (hasStringDetail(backendErrors)) {
        errorMessage.value = backendErrors.detail;
      } else {
        // Format multiple field errors
        let errorMessages = "";
        if (isRecord(backendErrors)) {
          errorMessages = Object.entries(backendErrors)
            .map(([field, messages]) => {
              const msgArray = Array.isArray(messages) ? messages : [messages];
              const strMsgs = msgArray.map((m) => String(m));
              return `${field}: ${strMsgs.join(", ")}`;
            })
            .join("\n");
        }
        errorMessage.value = errorMessages || "Error al guardar el voluntariado";
      }
    } else {
      errorMessage.value = err.message || "Error al guardar el voluntariado";
    }
    scrollToTop();
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
  return !!(v.requiere_convocatoria && v.fecha_fin_convocatoria && v.fecha_inicio_cursado);
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

/* Alert styling */
.alert {
  white-space: pre-line;
  animation: slideDown 0.3s ease-out;
  margin-bottom: 1rem;
}

.alert-danger {
  border-left: 4px solid #dc3545;
}

.alert-warning {
  border-left: 4px solid #ffc107;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
/* Ensure Google Places suggestions appear above the Bootstrap modal/backdrop */
.pac-container {
  z-index: 2000 !important; /* modal ~1055, backdrop ~1050 */
}
/* Add your styles here if needed */
</style>
