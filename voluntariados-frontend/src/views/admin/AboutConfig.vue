<template>
  <div class="about-config-admin">
    <AdminLayout page-title="Configuración - About" :breadcrumbs="[{ label: 'About' }]">
      <div class="row py-3">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-body">
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
              </div>

              <div v-else-if="error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>

              <div v-if="successMessage" class="alert alert-success" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                {{ successMessage }}
              </div>

              <form v-else @submit.prevent="saveConfiguration">
                <div class="dynamic-content-header mb-4">
                  <h5 class="text-primary mb-2">
                    <i class="bi bi-file-text me-2"></i>
                    Contenido de la página "Sobre Nosotros"
                  </h5>
                  <div class="alert alert-info d-flex align-items-start">
                    <i class="bi bi-info-circle-fill me-3 fs-5"></i>
                    <div>
                      <strong>Configuración de contenido dinámico</strong>
                      <p class="mb-0 small">
                        Editá los valores, estadísticas, equipo e hitos que aparecen en la vista
                        About. Usá los botones "Cargar Ejemplo" para poblar las secciones con datos
                        de prueba.
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Mission & Vision -->
                <div class="config-section-card mb-4">
                  <div class="config-section-header" @click="toggleSection('missionVision')">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-flag me-2 text-primary"></i>
                      <h5 class="mb-0">Misión y Visión</h5>
                    </div>
                    <i
                      :class="[
                        'bi',
                        expandedSections.missionVision ? 'bi-chevron-up' : 'bi-chevron-down',
                      ]"
                    ></i>
                  </div>
                  <div v-show="expandedSections.missionVision" class="config-section-body">
                    <div class="d-flex justify-content-end mb-3">
                      <button
                        type="button"
                        class="btn btn-sm btn-outline-secondary me-2"
                        @click="confirmLoadExample('mission')"
                      >
                        <i class="bi bi-file-earmark-text me-1"></i> Cargar Ejemplo Misión
                      </button>
                      <button
                        type="button"
                        class="btn btn-sm btn-outline-secondary"
                        @click="confirmLoadExample('vision')"
                      >
                        <i class="bi bi-file-earmark-text me-1"></i> Cargar Ejemplo Visión
                      </button>
                    </div>
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Nuestra Misión</label>
                        <textarea class="form-control" v-model="mission" rows="4"></textarea>
                      </div>
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Nuestra Visión</label>
                        <textarea class="form-control" v-model="vision" rows="4"></textarea>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- What We Offer -->
                <div class="dynamic-field-card mb-4">
                  <div class="dynamic-field-header" @click="toggleSection('offers')">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-gift me-2 text-primary"></i>
                      <h6 class="mb-0">¿Qué Ofrecemos?</h6>
                    </div>
                    <i
                      :class="['bi', expandedSections.offers ? 'bi-chevron-up' : 'bi-chevron-down']"
                    ></i>
                  </div>
                  <div v-show="expandedSections.offers" class="dynamic-field-body">
                    <div class="d-flex justify-content-end mb-3">
                      <button
                        type="button"
                        class="btn btn-sm btn-outline-secondary me-2"
                        @click="confirmLoadExample('offers_students')"
                      >
                        <i class="bi bi-file-earmark-text me-1"></i> Cargar Ejemplo - Estudiantes
                      </button>
                      <button
                        type="button"
                        class="btn btn-sm btn-outline-secondary"
                        @click="confirmLoadExample('offers_organizations')"
                      >
                        <i class="bi bi-file-earmark-text me-1"></i> Cargar Ejemplo - Organizaciones
                      </button>
                    </div>
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Para Estudiantes (lista)</label>
                        <div v-for="(item, idx) in offersStudents" :key="idx" class="d-flex mb-2">
                          <input
                            type="text"
                            class="form-control me-2"
                            v-model="offersStudents[idx]"
                          />
                          <button
                            type="button"
                            class="btn btn-sm btn-danger"
                            @click="offersStudents.splice(idx, 1)"
                          >
                            <i class="bi bi-trash"></i>
                          </button>
                        </div>
                        <button
                          type="button"
                          class="btn btn-sm btn-success"
                          @click="offersStudents.push('')"
                        >
                          Agregar
                        </button>
                      </div>
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Para Organizaciones (lista)</label>
                        <div
                          v-for="(item, idx) in offersOrganizations"
                          :key="idx"
                          class="d-flex mb-2"
                        >
                          <input
                            type="text"
                            class="form-control me-2"
                            v-model="offersOrganizations[idx]"
                          />
                          <button
                            type="button"
                            class="btn btn-sm btn-danger"
                            @click="offersOrganizations.splice(idx, 1)"
                          >
                            <i class="bi bi-trash"></i>
                          </button>
                        </div>
                        <button
                          type="button"
                          class="btn btn-sm btn-success"
                          @click="offersOrganizations.push('')"
                        >
                          Agregar
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Values (Cards) -->
                <div class="dynamic-field-card mb-4">
                  <div class="dynamic-field-header" @click="toggleSection('values')">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-heart me-2 text-primary"></i>
                      <h6 class="mb-0">Valores (cards)</h6>
                    </div>
                    <i
                      :class="['bi', expandedSections.values ? 'bi-chevron-up' : 'bi-chevron-down']"
                    ></i>
                  </div>
                  <div v-show="expandedSections.values" class="dynamic-field-body">
                    <div class="d-flex justify-content-end mb-3">
                      <button
                        type="button"
                        class="btn btn-sm btn-outline-secondary me-2"
                        @click="confirmLoadExample('values')"
                      >
                        <i class="bi bi-file-earmark-text me-1"></i> Cargar Ejemplo
                      </button>
                      <button type="button" class="btn btn-sm btn-success" @click="addValue">
                        <i class="bi bi-plus-circle me-1"></i> Agregar
                      </button>
                    </div>
                    <div v-for="(val, idx) in values" :key="idx" class="form-item-card mb-3">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="mb-0">Valor {{ idx + 1 }}</h6>
                        <button
                          type="button"
                          class="btn btn-sm btn-danger"
                          @click="removeValue(idx)"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                      <div class="row">
                        <div class="col-md-3 mb-3">
                          <label class="form-label">Seleccionar Ícono</label>
                          <select class="form-select icon-select" v-model="val.icon">
                            <option
                              v-for="iconOption in availableIcons"
                              :key="iconOption.value"
                              :value="iconOption.value"
                            >
                              {{ iconOption.label }}
                            </option>
                          </select>
                          <div class="icon-preview">
                            <i :class="[val.icon, 'icon-preview-large']"></i>
                          </div>
                        </div>
                        <div class="col-md-9">
                          <div class="row">
                            <div class="col-12 mb-3">
                              <label class="form-label">Título</label>
                              <input type="text" class="form-control" v-model="val.title" />
                            </div>
                            <div class="col-12 mb-0">
                              <label class="form-label">Descripción</label>
                              <textarea
                                class="form-control"
                                v-model="val.description"
                                rows="4"
                              ></textarea>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-if="values.length === 0" class="alert alert-warning">
                      No hay valores. Usá "Cargar Ejemplo" o "Agregar".
                    </div>
                  </div>
                </div>

                <!-- Stats (base numbers for fixed metrics) -->
                <div class="dynamic-field-card mb-4">
                  <div class="dynamic-field-header" @click="toggleSection('stats')">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-bar-chart-line me-2 text-primary"></i>
                      <h6 class="mb-0">Estadísticas (bases)</h6>
                    </div>
                    <i
                      :class="['bi', expandedSections.stats ? 'bi-chevron-up' : 'bi-chevron-down']"
                    ></i>
                  </div>
                  <div v-show="expandedSections.stats" class="dynamic-field-body">
                    <div class="alert alert-info">
                      <strong>Nota:</strong> Las métricas mostradas en la página About son fijas y
                      no pueden modificarse (Voluntarios Activos, Organizaciones, Proyectos, Horas
                      de Voluntariado). Aquí podés configurar un número base que se sumará a cada
                      métrica para incluir datos históricos o importados de sistemas anteriores.
                    </div>

                    <div class="row g-3">
                      <div class="col-md-3">
                        <label class="form-label">Base Voluntarios</label>
                        <input
                          type="number"
                          class="form-control"
                          v-model.number="base_voluntarios"
                        />
                      </div>
                      <div class="col-md-3">
                        <label class="form-label">Base Organizaciones</label>
                        <input
                          type="number"
                          class="form-control"
                          v-model.number="base_organizaciones"
                        />
                      </div>
                      <div class="col-md-3">
                        <label class="form-label">Base Proyectos</label>
                        <input type="number" class="form-control" v-model.number="base_proyectos" />
                      </div>
                      <div class="col-md-3">
                        <label class="form-label">Base Horas</label>
                        <input
                          type="number"
                          step="0.01"
                          class="form-control"
                          v-model.number="base_horas"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Milestones -->
                <div class="dynamic-field-card mb-4">
                  <div class="dynamic-field-header" @click="toggleSection('milestones')">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-clock-history me-2 text-primary"></i>
                      <h6 class="mb-0">Hitos / Línea de Tiempo</h6>
                    </div>
                    <i
                      :class="[
                        'bi',
                        expandedSections.milestones ? 'bi-chevron-up' : 'bi-chevron-down',
                      ]"
                    ></i>
                  </div>
                  <div v-show="expandedSections.milestones" class="dynamic-field-body">
                    <div class="d-flex justify-content-end mb-3">
                      <button
                        type="button"
                        class="btn btn-sm btn-outline-secondary me-2"
                        @click="confirmLoadExample('milestones')"
                      >
                        <i class="bi bi-file-earmark-text me-1"></i> Cargar Ejemplo
                      </button>
                      <button type="button" class="btn btn-sm btn-success" @click="addMilestone">
                        <i class="bi bi-plus-circle me-1"></i> Agregar
                      </button>
                    </div>
                    <div v-for="(ms, idx) in milestones" :key="idx" class="form-item-card mb-3">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="mb-0">Hito {{ idx + 1 }}</h6>
                        <button
                          type="button"
                          class="btn btn-sm btn-danger"
                          @click="removeMilestone(idx)"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                      <div class="row">
                        <div class="col-md-3 mb-3">
                          <label class="form-label">Año</label>
                          <input type="text" class="form-control" v-model="ms.year" />
                        </div>
                        <div class="col-md-9 mb-0">
                          <label class="form-label">Título</label>
                          <input type="text" class="form-control" v-model="ms.title" />
                        </div>
                      </div>
                      <div class="mt-2">
                        <label class="form-label">Descripción</label>
                        <textarea class="form-control" v-model="ms.description" rows="2"></textarea>
                      </div>
                    </div>
                    <div v-if="milestones.length === 0" class="alert alert-warning">
                      No hay hitos. Usá "Cargar Ejemplo" o "Agregar".
                    </div>
                  </div>
                </div>

                <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                  <button type="button" class="btn btn-outline-secondary" @click="resetForm">
                    <i class="bi bi-arrow-clockwise me-1"></i> Resetear
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="saving">
                    <span
                      v-if="saving"
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                    ></span>
                    <i v-else class="bi bi-check-lg me-1"></i>
                    {{ saving ? "Guardando..." : "Guardar About" }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
    <!-- Confirmation modal for loading examples -->
    <ConfirmationModal
      :show="showExampleModal"
      title="Confirmar carga de ejemplo"
      :message="`¿Cargar ejemplo para ${exampleToLoad}? Se reemplazarán los datos actuales.`"
      type="warning"
      confirmText="Cargar"
      cancelText="Cancelar"
      @confirm="performLoadExample"
      @cancel="cancelLoadExample"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminLayout from "@/components/admin/AdminLayout.vue";
import ConfirmationModal from "@/components/admin/ConfirmationModal.vue";
import { landingConfigAPI } from "@/services/api";
import { useLandingConfig } from "@/composables/useLandingConfig";

export default defineComponent({
  name: "AboutConfigAdmin",
  components: { AdminLayout, ConfirmationModal },
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig();
    return { sharedLandingConfig: landingConfig, refreshLandingConfig: fetchLandingConfig };
  },
  data() {
    return {
      loading: true,
      saving: false,
      error: "",
      successMessage: "",
      // Mission / Vision and Offers
      mission: "",
      vision: "",
      offersStudents: [] as string[],
      offersOrganizations: [] as string[],
      // Confirmation modal for loading examples
      showExampleModal: false,
      exampleToLoad: "",
      // UI state for collapsible sections
      expandedSections: {
        missionVision: true,
        offers: true,
        values: true,
        stats: false,
        milestones: false,
      },
      values: [] as Array<{ icon: string; title: string; description: string }>,
      stats: [] as Array<{ number: string; label: string }>,

      milestones: [] as Array<{ year: string; title: string; description: string }>,
      // Base numbers for fixed metrics (admins can only change these)
      base_voluntarios: 0 as number,
      base_organizaciones: 0 as number,
      base_proyectos: 0 as number,
      base_horas: 0 as number,
      // Available icons for values
      availableIcons: [
        { label: "Corazón", value: "bi-heart" },
        { label: "Personas", value: "bi-people" },
        { label: "Bombilla", value: "bi-lightbulb" },
        { label: "Bandera", value: "bi-flag" },
      ],
    };
  },

  created() {
    // load current configuration when component is created
    // (uses admin endpoint)
    this.loadConfiguration();
  },

  methods: {
    addValue() {
      this.values.push({ icon: "bi-heart", title: "", description: "" });
    },
    removeValue(i: number) {
      this.values.splice(i, 1);
    },

    addStat() {
      this.stats.push({ number: "", label: "" });
    },
    removeStat(i: number) {
      this.stats.splice(i, 1);
    },

    addMilestone() {
      this.milestones.push({ year: "", title: "", description: "" });
    },
    removeMilestone(i: number) {
      this.milestones.splice(i, 1);
    },

    resetForm() {
      this.loadConfiguration();
      this.error = "";
      this.successMessage = "";
    },

    toggleSection(section: keyof typeof this.expandedSections) {
      this.expandedSections[section] = !this.expandedSections[section];
    },

    confirmLoadExample(type: string) {
      // store the type and open confirmation modal
      this.exampleToLoad = type;
      this.showExampleModal = true;
    },

    loadExample(type: string) {
      switch (type) {
        case "mission":
          this.mission =
            "Promover la participación activa de estudiantes universitarios en proyectos de voluntariado que generen un impacto positivo en la sociedad.";
          break;
        case "vision":
          this.vision =
            "Ser la plataforma líder en la región que conecta estudiantes universitarios con oportunidades de voluntariado.";
          break;
        case "offers_students":
          this.offersStudents = [
            "Desarrollo de habilidades blandas y técnicas",
            "Certificados de participación y reconocimiento",
            "Networking con profesionales y organizaciones",
            "Experiencia práctica en tu campo de estudio",
            "Acceso a capacitaciones y talleres",
          ];
          break;
        case "offers_organizations":
          this.offersOrganizations = [
            "Acceso a talento universitario comprometido",
            "Apoyo en proyectos sociales y comunitarios",
            "Visibilidad en la comunidad universitaria",
            "Alianzas estratégicas con la universidad",
            "Gestión simplificada de voluntarios",
          ];
          break;
        case "values":
          this.values = [
            { icon: "bi-heart", title: "Compromiso", description: "Compromiso con la comunidad." },
            { icon: "bi-people", title: "Inclusión", description: "Promovemos espacios diversos." },
            {
              icon: "bi-lightbulb",
              title: "Innovación",
              description: "Buscamos soluciones creativas.",
            },
          ];
          break;
        case "stats":
          this.stats = [
            { number: "500+", label: "Voluntarios Activos" },
            { number: "50+", label: "Organizaciones" },
            { number: "100+", label: "Proyectos" },
          ];
          break;
        case "milestones":
          this.milestones = [
            { year: "2018", title: "Fundación", description: "Inicio del programa" },
            { year: "2021", title: "Expansión", description: "Expansión regional" },
          ];
          break;
      }
    },

    async loadConfiguration() {
      this.loading = true;
      this.error = "";
      try {
        const response = await landingConfigAPI.getConfig();
        const cfg = response.data || {};
        this.mission = cfg.mission || "";
        this.vision = cfg.vision || "";
        this.offersStudents = cfg.offers_students || [];
        this.offersOrganizations = cfg.offers_organizations || [];
        this.values = cfg.values || [];
        this.stats = cfg.stats || [];
        this.milestones = cfg.milestones || [];
        // base numbers
        this.base_voluntarios = cfg.base_voluntarios ?? 0;
        this.base_organizaciones = cfg.base_organizaciones ?? 0;
        this.base_proyectos = cfg.base_proyectos ?? 0;
        this.base_horas = cfg.base_horas ?? 0;
      } catch (err: unknown) {
        console.error("Error loading landing config:", err);
        this.error = "Error al cargar la configuración";
      } finally {
        this.loading = false;
      }
    },

    // invoked when user confirms loading example
    performLoadExample() {
      if (this.exampleToLoad) {
        this.loadExample(this.exampleToLoad);
      }
      this.exampleToLoad = "";
      this.showExampleModal = false;
    },

    cancelLoadExample() {
      this.exampleToLoad = "";
      this.showExampleModal = false;
    },

    async saveConfiguration() {
      this.saving = true;
      this.error = "";
      this.successMessage = "";
      try {
        const data: Record<string, unknown> = {
          mission: this.mission,
          vision: this.vision,
          offers_students: this.offersStudents,
          offers_organizations: this.offersOrganizations,
          values: this.values,
          stats: this.stats,
          milestones: this.milestones,
          // base numbers for fixed metrics
          base_voluntarios: this.base_voluntarios,
          base_organizaciones: this.base_organizaciones,
          base_proyectos: this.base_proyectos,
          base_horas: this.base_horas,
        };

        const response = await landingConfigAPI.updateConfig(data);
        if (response.data) {
          this.successMessage = "About guardado correctamente";
          // Refresh shared config so AboutView and others pick it up
          await this.refreshLandingConfig();
          setTimeout(() => {
            this.successMessage = "";
          }, 4000);
        }
      } catch (err: unknown) {
        console.error("Error saving about config:", err);
        const e = err as { response?: { data?: { detail?: string } } };
        this.error = e.response?.data?.detail || "Error al guardar About";
      } finally {
        this.saving = false;
      }
    },
  },
});
</script>

<style scoped>
.about-config-admin {
  min-height: 100vh;
}

.card {
  border: none;
  border-radius: 0.5rem;
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-control,
.form-select {
  border-radius: 0.375rem;
  border: 1px solid #dee2e6;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus,
.form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.text-primary {
  color: #0d6efd !important;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.alert {
  border-radius: 0.375rem;
}

.border-top {
  border-top: 1px solid #dee2e6 !important;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* Dynamic Content Styles */
.dynamic-content-header .alert {
  background-color: #e7f3ff;
  border-color: #b3d9ff;
  color: #004085;
}

/* Configuration Section Card Styles */
.config-section-card {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.config-section-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.config-section-header {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s ease;
}

.config-section-header:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.config-section-header h5 {
  font-weight: 600;
  color: #495057;
  margin: 0;
  font-size: 1.1rem;
}

.config-section-header i.bi-chevron-up,
.config-section-header i.bi-chevron-down {
  font-size: 1.3rem;
  color: #6c757d;
  transition: transform 0.3s ease;
}

.config-section-body {
  padding: 1.75rem 1.5rem;
  animation: slideDown 0.3s ease;
}

/* Dynamic Field Card Styles */
.dynamic-field-card {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
}

.dynamic-field-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.dynamic-field-header {
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s ease;
}

.dynamic-field-header:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.dynamic-field-header h6 {
  font-weight: 600;
  color: #495057;
  margin: 0;
}

.dynamic-field-header i.bi-chevron-up,
.dynamic-field-header i.bi-chevron-down {
  font-size: 1.2rem;
  color: #6c757d;
  transition: transform 0.3s ease;
}

.dynamic-field-body {
  padding: 1.5rem 1.25rem;
  animation: slideDown 0.3s ease;
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

/* Form Item Card Styles */
.form-item-card {
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  transition: all 0.3s ease;
  position: relative;
}

.form-item-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #0d6efd;
}

.form-item-card h6 {
  font-weight: 600;
  color: #495057;
}

.form-item-card .btn-outline-danger {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

/* Button Styles */
.btn-outline-secondary {
  border-color: #6c757d;
  color: #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  border-color: #6c757d;
  color: white;
}

.btn-outline-primary {
  border: 2px solid #0d6efd;
  color: #0d6efd;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(13, 110, 253, 0.3);
}

/* Icon Selector Styles */
.icon-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.15s ease-in-out;
}

.icon-select:hover {
  border-color: #0d6efd;
}

.icon-select:focus {
  outline: none;
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Icon Preview Styles */
.icon-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 0.375rem;
  margin: 0.75rem 0;
  min-height: 100px;
  border: 2px dashed #dee2e6;
  transition: all 0.3s ease;
}

.icon-preview:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  border-color: #0d6efd;
}

.icon-preview-large {
  font-size: 3rem;
  color: #0d6efd;
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .config-section-header {
    padding: 1rem 1.25rem;
  }

  .config-section-body {
    padding: 1.25rem 1rem;
  }

  .dynamic-field-header {
    padding: 0.875rem 1rem;
  }

  .dynamic-field-body {
    padding: 1rem;
  }

  .form-item-card {
    padding: 1rem;
  }
}
</style>
