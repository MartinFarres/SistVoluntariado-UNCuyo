<!-- PersonaSetup.vue -->
<template>
  <div class="persona-setup">
    <div class="setup-form">
      <form @submit.prevent="submitForm">
        <div class="row">
          <!-- Left Column -->
          <div class="col-md-6">
            <h5 class="section-title mb-3">Información Personal</h5>

            <!-- Nombre -->
            <div class="mb-3">
              <label for="nombre" class="form-label">Nombre *</label>
              <input
                type="text"
                class="form-control"
                id="nombre"
                v-model="formData.nombre"
                :class="{ 'is-invalid': errors.nombre }"
                required
              />
              <div v-if="errors.nombre" class="invalid-feedback">
                {{ errors.nombre }}
              </div>
            </div>

            <!-- Apellido -->
            <div class="mb-3">
              <label for="apellido" class="form-label">Apellido *</label>
              <input
                type="text"
                class="form-control"
                id="apellido"
                v-model="formData.apellido"
                :class="{ 'is-invalid': errors.apellido }"
                required
              />
              <div v-if="errors.apellido" class="invalid-feedback">
                {{ errors.apellido }}
              </div>
            </div>

            <!-- DNI -->
            <div class="mb-3">
              <label for="dni" class="form-label">DNI *</label>
              <input
                type="text"
                class="form-control"
                id="dni"
                v-model="formData.dni"
                :class="{ 'is-invalid': errors.dni }"
                required
              />
              <div v-if="errors.dni" class="invalid-feedback">
                {{ errors.dni }}
              </div>
            </div>

            <!-- Fecha de Nacimiento -->
            <div class="mb-3">
              <label for="fecha_nacimiento" class="form-label">Fecha de Nacimiento *</label>
              <input
                type="date"
                class="form-control"
                id="fecha_nacimiento"
                v-model="formData.fecha_nacimiento"
                :class="{ 'is-invalid': errors.fecha_nacimiento }"
                required
              />
              <div v-if="errors.fecha_nacimiento" class="invalid-feedback">
                {{ errors.fecha_nacimiento }}
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="col-md-6">
            <h5 class="section-title mb-3">Información de Contacto</h5>

            <!-- Teléfono -->
            <div class="mb-3">
              <label for="telefono" class="form-label">Teléfono *</label>
              <input
                type="tel"
                class="form-control"
                id="telefono"
                v-model="formData.telefono"
                :class="{ 'is-invalid': errors.telefono }"
                required
              />
              <div v-if="errors.telefono" class="invalid-feedback">
                {{ errors.telefono }}
              </div>
            </div>

            <!-- Dirección -->
            <div class="mb-3">
              <label for="direccion" class="form-label">Dirección *</label>
              <input
                type="text"
                class="form-control"
                id="direccion"
                v-model="formData.direccion"
                :class="{ 'is-invalid': errors.direccion }"
                required
              />
              <div v-if="errors.direccion" class="invalid-feedback">
                {{ errors.direccion }}
              </div>
            </div>

            <!-- Localidad -->
            <div class="mb-3">
              <label for="localidad" class="form-label">Localidad *</label>
              <select
                class="form-select"
                id="localidad"
                v-model="formData.localidad"
                :class="{ 'is-invalid': errors.localidad }"
              >
                <option value="">Selecciona una localidad</option>
                <option v-for="localidad in localidades" :key="localidad.id" :value="localidad.id">
                  {{ getCompleteLocationName(localidad) }}
                </option>
              </select>
              <div v-if="errors.localidad" class="invalid-feedback">
                {{ errors.localidad }}
              </div>
            </div>
          </div>
        </div>

        <!-- Role-specific fields section -->
        <div class="row" v-if="userRole === 'VOL' || userRole === 'DELEG'">
          <div class="col-12">
            <h5 class="section-title mb-3 mt-4">Información Específica</h5>
          </div>
        </div>

        <!-- Voluntario specific fields -->
        <div v-if="userRole === 'VOL'" class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <div class="form-check mt-4">
                <input
                  class="form-check-input"
                  type="checkbox"
                  id="interno"
                  v-model="formData.interno"
                />
                <label class="form-check-label" for="interno">
                  Voluntario interno de la facultad
                </label>
              </div>
            </div>
          </div>
          <div class="col-12">
            <transition name="fade">
              <div v-if="formData.interno" class="voluntarios-internos-section">
                <h5 class="section-title mb-3 mt-4">Voluntarios Internos</h5>
                <div class="row">
                  <div class="col-md-4">
                    <div class="mb-3">
                      <label for="facultad" class="form-label">Facultad</label>
                      <select
                        class="form-select"
                        id="facultad"
                        v-model="formData.facultad"
                        @change="loadCarreras"
                      >
                        <option :value="null">Selecciona una facultad</option>
                        <option
                          v-for="facultad in facultades"
                          :key="facultad.id"
                          :value="facultad.id"
                        >
                          {{ facultad.nombre }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="mb-3">
                      <label for="carrera" class="form-label">Carrera</label>
                      <select
                        class="form-select"
                        id="carrera"
                        v-model="formData.carrera"
                        :disabled="!formData.facultad || carreras.length === 0"
                      >
                        <option :value="null">Selecciona una carrera</option>
                        <option v-for="carrera in carreras" :key="carrera.id" :value="carrera.id">
                          {{ carrera.nombre }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="mb-3">
                      <label for="condicion" class="form-label">Condición</label>
                      <select
                        class="form-select"
                        id="condicion"
                        v-model="formData.condicion"
                        required
                      >
                        <option value="">Seleccione una opción</option>
                        <option value="Estudiante">Estudiante</option>
                        <option value="Docente">Docente</option>
                        <option value="Egresado">Egresado</option>
                        <option value="Personal no docente">Personal no docente</option>
                        <option value="Intercambio">Intercambio</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else>
                <input type="hidden" v-model="formData.condicion" />
                <input type="hidden" v-model="formData.facultad" />
                <input type="hidden" v-model="formData.carrera" />
                <div class="mb-3">
                  <label class="form-label">Condición</label>
                  <input class="form-control" value="Externo" disabled />
                </div>
              </div>
            </transition>
          </div>
        </div>

        <!-- General error message -->
        <div v-if="generalError" class="alert alert-danger mb-3">
          {{ generalError }}
        </div>

        <!-- Submit button -->
        <div class="row">
          <div class="col-12 text-center">
            <button
              type="submit"
              :class="['btn', 'btn-lg', 'px-5', allFieldsComplete ? 'btn-primary' : 'btn-pending']"
              :disabled="submitting || !allFieldsComplete"
            >
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
              {{ submitting ? "Guardando..." : "Completar Configuración" }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { userAPI, ubicacionAPI, facultadAPI } from "@/services/api";

interface Localidad {
  id: number;
  nombre: string;
  departamento?: {
    id: number;
    nombre: string;
    provincia?: {
      id: number;
      nombre: string;
      pais?: { id: number; nombre: string };
    };
  };
}

export default defineComponent({
  name: "PersonaSetup",
  props: {
    userRole: {
      type: String,
      required: true,
      validator: (value: string) => ["VOL", "ADMIN", "DELEG"].includes(value),
    },
    userEmail: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      submitting: false as boolean,
      generalError: "" as string,
      errors: {} as Record<string, string>,
      localidades: [] as Localidad[],
      carreras: [] as Array<{ id: number; nombre: string }>,
      facultades: [] as Array<{ id: number; nombre: string }>,
      organizaciones: [] as Array<any>,
      formData: {
        nombre: "",
        apellido: "",
        dni: "",
        fecha_nacimiento: "",
        telefono: "",
        email: this.userEmail || "",
        direccion: "",
        localidad: null as number | null,
        interno: false,
        facultad: null as number | null,
        carrera: null as number | null,
        condicion: "",
        organizacion: null as number | null,
      },
    };
  },
  computed: {
    allFieldsComplete(): boolean {
      const required = [
        (this.formData.nombre || "").toString().trim(),
        (this.formData.apellido || "").toString().trim(),
        (this.formData.dni || "").toString().trim(),
        (this.formData.fecha_nacimiento || "").toString().trim(),
        (this.formData.telefono || "").toString().trim(),
        (this.formData.email || "").toString().trim(),
        (this.formData.direccion || "").toString().trim(),
        this.formData.localidad,
      ];
      if (this.userRole === "VOL") {
        required.push(this.formData.condicion);
      }
      return required.every((v) => v !== "" && v !== null && v !== undefined);
    },
  },
  async mounted() {
    await this.loadLocalidades();
    await this.loadFacultades();
    await this.loadOrganizaciones();
  },
  methods: {
    async loadFacultades() {
      try {
        const res = await facultadAPI.getFacultades();
        this.facultades = res.data;
      } catch (error) {
        console.error("Error loading facultades:", error);
      }
    },
    async loadLocalidades() {
      try {
        const [locRes, depRes, provRes, paisRes] = await Promise.all([
          ubicacionAPI.getLocalidades(),
          ubicacionAPI.getDepartamentos(),
          ubicacionAPI.getProvincias(),
          ubicacionAPI.getPaises(),
        ]);

        const paises = paisRes.data;
        const provincias = provRes.data;
        const departamentos = depRes.data;
        const localidades = locRes.data;

        this.localidades = localidades.map((localidad: any) => {
          const departamento = departamentos.find((d: any) => d.id === localidad.departamento);
          if (departamento) {
            const provincia = provincias.find((p: any) => p.id === departamento.provincia);
            if (provincia) {
              const pais = paises.find((pa: any) => pa.id === provincia.pais);
              departamento.provincia = { ...provincia, pais };
            }
            localidad.departamento = departamento;
          }
          return localidad;
        });
      } catch (error) {
        console.error("Error loading localidades:", error);
      }
    },
    async loadCarreras() {
      try {
        if (!this.formData.facultad) {
          this.carreras = [];
          this.formData.carrera = null;
          return;
        }
        const res = await facultadAPI.getCarreras();
        this.carreras = res.data.filter((c: any) => c.facultad === this.formData.facultad);
        if (!this.carreras.some((c: any) => c.id === this.formData.carrera)) {
          this.formData.carrera = null;
        }
      } catch (error) {
        console.error("Error loading carreras:", error);
        this.carreras = [];
      }
    },
    async loadOrganizaciones() {
      try {
        const { organizacionAPI } = await import("@/services/api");
        const res = await organizacionAPI.getAll();
        this.organizaciones = res.data;
      } catch (error) {
        console.error("Error loading organizaciones:", error);
      }
    },
    getCompleteLocationName(localidad: Localidad): string {
      const parts = [localidad.nombre];

      if (localidad.departamento) {
        parts.push(localidad.departamento.nombre);

        if (localidad.departamento.provincia) {
          parts.push(localidad.departamento.provincia.nombre);

          if (localidad.departamento.provincia.pais) {
            parts.push(localidad.departamento.provincia.pais.nombre);
          }
        }
      }

      return parts.join(", ");
    },
    async submitForm() {
      this.submitting = true;
      this.generalError = "";
      this.errors = {};

      try {
        const dataToSubmit: any = {
          nombre: this.formData.nombre,
          apellido: this.formData.apellido,
          dni: this.formData.dni,
          fecha_nacimiento: this.formData.fecha_nacimiento,
          telefono: this.formData.telefono,
          direccion: this.formData.direccion,
          localidad: this.formData.localidad,
        };

        if (this.userRole === "VOL") {
          dataToSubmit.carrera = this.formData.carrera;
          dataToSubmit.interno = this.formData.interno;
        } else if (this.userRole === "DELEG") {
          dataToSubmit.organizacion = this.formData.organizacion;
          // For Delegado the persona is usually already created by backend on user creation.
          // Try to detect existing persona and PATCH it instead of POSTing a new one.
          try {
            const meResp = await userAPI.getCurrentUser();
            console.log("Current user (me):", meResp.data);
            const personaId = meResp.data?.persona || null;

            // If backend already marked persona as settled_up, show message and stop
            if (meResp.data?.settled_up) {
              this.generalError =
                "La configuración de persona ya fue completada para este usuario.";
              this.submitting = false;
              return;
            }

            if (personaId) {
              // Prefer calling the user setup endpoint with PUT so backend selects the
              // correct subclass serializer and performs a partial update.
              try {
                const putResp = await userAPI.setupPersonaPut(dataToSubmit);
                console.log("setup_persona PUT response:", putResp.data);
                this.$emit("setup-complete");
                return;
              } catch (innerErr: any) {
                // Log server validation errors for debugging and fall back to POST
                const details = innerErr.response?.data;
                console.error("Error updating persona via setup_persona PUT:", details || innerErr);
                // Also dump the full response body for clarity
                try {
                  console.error("Full PUT response:", JSON.stringify(details));
                } catch (e) {
                  // ignore stringify errors
                }
                // If it's a server error (>=500) or non-JSON (HTML), stop and show a generic error instead of falling back
                const status = innerErr.response?.status;
                if (
                  (typeof details === "string" && details.startsWith("<!DOCTYPE html")) ||
                  (status && status >= 500)
                ) {
                  this.generalError =
                    "Ocurrió un error interno del servidor al actualizar la persona. Intente nuevamente más tarde.";
                  this.submitting = false;
                  return;
                }
                // If server returned a 'detail' message like 'User persona setup already completed', show it
                if (details?.detail) {
                  this.generalError = details.detail;
                  this.submitting = false;
                  return;
                }
                // If returned field errors, show them in the form and surface organizacion errors globally
                if (details && typeof details === "object" && !details.detail) {
                  this.errors = {};
                  Object.keys(details).forEach((field) => {
                    if (Array.isArray(details[field])) {
                      this.errors[field] = details[field][0];
                    }
                  });
                  // If organizacion specifically has errors, show them in generalError too
                  if (Array.isArray(details.organizacion) && details.organizacion.length) {
                    this.generalError = Array.isArray(details.organizacion)
                      ? details.organizacion.join("; ")
                      : String(details.organizacion);
                  }
                }
                // continue to fallback below
              }
            }
            // If no persona id, fall through to setupPersona (create)
          } catch (e: any) {
            // If fetching current user fails, fall back to setupPersona below, but log details
            console.error("Error checking current user persona:", e.response?.data || e);
          }
        }

        // Generic create path when persona does not exist yet
        await userAPI.setupPersona(dataToSubmit);

        this.$emit("setup-complete");
      } catch (error: any) {
        console.error("Error setting up persona:", error);
        // Dump full response body for debugging
        try {
          console.error("Full setup_persona response:", JSON.stringify(error.response?.data));
        } catch (e) {}

        if (error.response?.data) {
          const errorData = error.response.data;

          if (typeof errorData === "object" && !errorData.detail) {
            this.errors = {};
            Object.keys(errorData).forEach((field) => {
              if (Array.isArray(errorData[field])) {
                this.errors[field] = errorData[field][0];
              }
            });
            // surface organizacion errors at top level if present
            if (Array.isArray(errorData.organizacion) && errorData.organizacion.length) {
              this.generalError = errorData.organizacion.join("; ");
            }
          } else {
            this.generalError = errorData.detail || "Error al completar la configuración";
          }
        } else {
          this.generalError = "Error al completar la configuración";
        }
      } finally {
        this.submitting = false;
      }
    },
  },
});
</script>

<style scoped>
.persona-setup {
  background: transparent;
}

.setup-form {
  max-width: 100%;
  margin: 0 auto;
}

.section-title {
  color: var(--brand-end);
  font-weight: 600;
  border-bottom: 2px solid var(--brand-end);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.form-label {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-control,
.form-select {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
  border-color: var(--brand-start);
  box-shadow: 0 0 0 0.2rem rgba(95, 158, 160, 0.25);
}

.form-check-input:checked {
  background-color: var(--brand-start);
  border-color: var(--brand-start);
}

.form-check-input:focus {
  border-color: var(--brand-start);
  box-shadow: 0 0 0 0.25rem rgba(95, 158, 160, 0.25);
}

.alert-danger {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
  border-radius: 10px;
}

.invalid-feedback {
  display: block;
  font-size: 0.875rem;
  color: #dc3545;
  margin-top: 0.25rem;
}

.form-control.is-invalid,
.form-select.is-invalid {
  border-color: #dc3545;
}

@media (max-width: 768px) {
  .setup-form {
    padding: 0 1rem;
  }

  .section-title {
    font-size: 1.1rem;
  }
}
</style>
