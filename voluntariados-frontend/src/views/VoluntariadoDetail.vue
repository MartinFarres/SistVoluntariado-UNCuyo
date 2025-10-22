<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import VoluntariadoCard from "@/components/landing/VoluntariadoCard.vue";
import CTASection from "@/components/landing/CTASection.vue";
import JoinConfirmationModal from "@/components/landing/JoinConfirmationModal.vue";
import CancelConfirmationModal from "@/components/landing/CancelConfirmationModal.vue";
import { voluntariadoAPI, turnoAPI, organizacionAPI } from "@/services/api";
import authService from "@/services/authService";
import apiClient from "@/services/api";

interface Turno {
  id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  cupo: number;
  lugar?: string;
  voluntariado?: number | { id: number } | any;
}

interface Voluntariado {
  id: number;
  nombre: string;
  descripcion?: any;
  estado: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  turno?: number;
  gestionadores?: number[];
  organizacion?: number;
}

interface Organizacion {
  id: number;
  nombre: string;
  descripcion?: string;
  contacto_email?: string;
  localidad?: number;
  voluntariado?: number;
}

export default defineComponent({
  name: "VoluntariadoDetail",
  components: {
    AppNavBar,
    VoluntariadoCard,
    CTASection,
    JoinConfirmationModal,
    CancelConfirmationModal,
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      voluntariadoId: 0,

      voluntariadoData: null as Voluntariado | null,
      organizacion: null as Organizacion | null,

      allTurnos: [] as Turno[],

      allOrgVoluntariados: [] as any[],

      allSimilarVoluntariados: [] as any[],

      showAllTurnos: false,
      showAllOrgVoluntariados: false,
      showAllSimilar: false,

      isAuthenticated: false,

      // Join Modal state
      showJoinModal: false,
      joinLoading: false,
      joinSuccess: false,
      selectedTurnoId: null as number | null,

      // Cancel Modal state
      showCancelModal: false,
      cancelLoading: false,
      turnoToCancelId: null as number | null,

      // Enrollment state
      userInscripciones: [] as any[],
      isUserEnrolled: false,
      // ahora un arreglo reactivo de ids numéricos
      enrolledTurnoIds: [] as number[],

      // UI state
      isHovering: null as number | "main" | null,
    };
  },

  computed: {
    displayedTurnos(): Turno[] {
      return this.showAllTurnos ? this.allTurnos : this.allTurnos.slice(0, 2);
    },
    displayedOrgVoluntariados(): any[] {
      return this.showAllOrgVoluntariados
        ? this.allOrgVoluntariados
        : this.allOrgVoluntariados.slice(0, 2);
    },
    displayedSimilarVoluntariados(): any[] {
      return this.showAllSimilar
        ? this.allSimilarVoluntariados
        : this.allSimilarVoluntariados.slice(0, 3);
    },
  },

  async created() {
    this.voluntariadoId = parseInt(this.$route.params.id as string);
    this.isAuthenticated = authService.isAuthenticated();
    await this.loadVoluntariado();
  },

  methods: {
    async loadVoluntariado() {
      this.loading = true;
      this.error = null;

      try {
        const volRes = await voluntariadoAPI.getById(this.voluntariadoId);
        const volData: Voluntariado = volRes.data;
        this.voluntariadoData = volData;

        const [turnosRes, organizacionesRes, allVoluntariadosRes, inscripcionesRes] =
          await Promise.all([
            voluntariadoAPI.getTurnos(this.voluntariadoId), // BUGFIX: Fetch only shifts for this voluntariado
            organizacionAPI.getAll(),
            voluntariadoAPI.getAllActive(),
            this.isAuthenticated
              ? apiClient.get("/voluntariado/inscripciones/")
              : Promise.resolve({ data: [] }),
          ]);

        // guardar inscripciones primero
        this.userInscripciones = inscripcionesRes.data || [];

        // encontrar organización (si existe)
        if (volData.organizacion) {
          this.organizacion =
            organizacionesRes.data.find((o: any) => o.id === volData.organizacion) || null;
          if (this.organizacion) {
            await this.loadOrganizationVoluntariados(
              this.organizacion.id,
              allVoluntariadosRes.data
            );
          }
        }

        // BUGFIX: No longer need to filter, just map the data that is already correct from the API.
        this.allTurnos = (turnosRes.data as Turno[]).map((t: any) => ({
          ...t,
          id: Number(t.id),
          cupo: t.cupo != null ? Number(t.cupo) : t.cupo,
        }));

        // recalcular inscripciones ahora que allTurnos está disponible
        this.checkUserEnrollment();

        this.loadSimilarVoluntariados(allVoluntariadosRes.data);
      } catch (err: any) {
        console.error("Error loading voluntariado:", err);
        this.error = err.response?.data?.detail || "Error al cargar el voluntariado";
      } finally {
        this.loading = false;
      }
    },

    // NUEVO: extrae id numérico de distintos formatos que puede tener inscripcion.turno
    parseInscripcionTurnoId(turnoField: any): number | null {
      if (turnoField == null) return null;
      if (typeof turnoField === "number") return Number(turnoField);
      if (typeof turnoField === "object") {
        if ("id" in turnoField && turnoField.id != null) return Number(turnoField.id);
        if ("pk" in turnoField && turnoField.pk != null) return Number(turnoField.pk);
        if ("turno" in turnoField) return this.parseInscripcionTurnoId(turnoField.turno);
      }
      if (typeof turnoField === "string") {
        const m = turnoField.match(/(\d+)\/?$/);
        if (m) return Number(m[1]);
        const n = Number(turnoField);
        if (!isNaN(n)) return n;
      }
      return null;
    },

    checkUserEnrollment() {
      // Si no está autenticado o no hay inscripciones, limpiamos y salimos
      if (!this.isAuthenticated || !this.userInscripciones) {
        this.isUserEnrolled = false;
        this.enrolledTurnoIds = [];
        return;
      }

      // DEBUG: mostrar inscripciones recibidas
      // eslint-disable-next-line no-console
      console.debug("userInscripciones:", this.userInscripciones);

      const enrolledIdsSet = new Set<number>();

      for (const inscripcion of this.userInscripciones) {
        // Normalizar estado y filtrar solo inscripciones activas.
        // Aceptamos formas como "INS" (abreviada), "INSCRITO", y estados de asistencia "ASISTIO"
        const estado = (inscripcion.estado ?? "").toString().toUpperCase().trim();

        const isActive =
          estado.startsWith("INS") || // INS, INSCRITO, etc.
          estado.startsWith("ASI"); // ASISTIO, ASISTIÓ, etc.

        if (!isActive) continue;

        // Extraer id del turno de forma robusta
        const turnoVal = inscripcion.turno ?? inscripcion.turno_id ?? inscripcion.turnoId ?? null;
        const turnoId = this.parseInscripcionTurnoId(turnoVal);

        if (turnoId != null) {
          enrolledIdsSet.add(Number(turnoId));
        }
      }

      // Guardar como arreglo reactivo
      this.enrolledTurnoIds = Array.from(enrolledIdsSet);

      // DEBUG: mostrar ids extraídos
      // eslint-disable-next-line no-console
      console.debug("enrolledTurnoIds:", this.enrolledTurnoIds);

      // Mantener isUserEnrolled por compatibilidad (si está inscrito en algún turno del voluntariado)
      const voluntarioTurnoIdsInThisVol = this.enrolledTurnoIds.filter((tid) =>
        this.allTurnos.some((t) => Number(t.id) === Number(tid))
      );
      this.isUserEnrolled = voluntarioTurnoIdsInThisVol.length > 0;
    },

    async loadOrganizationVoluntariados(orgId: number, allVoluntariados: Voluntariado[]) {
      this.allOrgVoluntariados = allVoluntariados
        .filter((v) => v.organizacion === orgId && v.id !== this.voluntariadoId)
        .slice(0, 4)
        .map((v) => ({
          id: v!.id,
          title: v!.nombre,
          description: this.getDescriptionText(v!.descripcion) || "Sin descripción",
          isFree: true,
          tags: ["Tag 1", "Tag 2", "Tag 3"],
        }));
    },

    loadSimilarVoluntariados(allVoluntariados: Voluntariado[]) {
      if (!this.voluntariadoData) return;
      this.allSimilarVoluntariados = allVoluntariados
        .filter((v) => v.id !== this.voluntariadoId && v.estado === this.voluntariadoData?.estado)
        .slice(0, 6)
        .map((v) => ({
          id: v.id,
          title: v.nombre,
          description: this.getDescriptionText(v.descripcion) || "Sin descripción",
          isFree: true,
          tags: this.generateTags(v),
        }));
    },

    getDescriptionText(descripcion: any): string {
      if (!descripcion) return "Sin descripción disponible";
      if (typeof descripcion === "string") return descripcion;
      if (typeof descripcion === "object" && descripcion.descripcion) {
        return descripcion.descripcion;
      }
      if (typeof descripcion === "object" && descripcion.resumen) {
        return descripcion.resumen;
      }
      return "Sin descripción disponible";
    },

    generateTags(voluntariado: Voluntariado): string[] {
      const tags = [];
      if (voluntariado.estado) tags.push(voluntariado.estado);
      if (voluntariado.fecha_inicio) tags.push("Próximamente");
      tags.push("Tag " + ((voluntariado.id % 5) + 1));
      return tags.slice(0, 5);
    },

    generateSchedule(voluntariado: Voluntariado): Array<{ day: string; time: string }> {
      const schedule = [
        { day: "Lunes - Viernes", time: "08:00 - 23:00" },
        { day: "Sábado - Domingo", time: "15:00 - 20:00" },
      ];

      if (voluntariado.fecha_inicio && voluntariado.fecha_fin) {
        schedule.push({
          day: "Período",
          time: `${this.formatDate(voluntariado.fecha_inicio)} - ${this.formatDate(
            voluntariado.fecha_fin
          )}`,
        });
      }

      return schedule;
    },

    formatDate(dateString: string): string {
      const date = new Date(dateString);
      return date.toLocaleDateString("es-AR", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },

    formatTime(timeString: string): string {
      return timeString.substring(0, 5); // HH:MM
    },

    formatTurnoDate(turno: Turno): string {
      const date = new Date(turno.fecha);
      const dayName = date.toLocaleDateString("es-AR", { weekday: "long" });
      return dayName.charAt(0).toUpperCase() + dayName.slice(1);
    },

    formatTurnoFullDate(turno: Turno): string {
      const date = new Date(turno.fecha);
      return date.toLocaleDateString("es-AR", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },

    inscribirse() {
      if (!this.isAuthenticated) {
        this.$router.push({
          path: "/signup",
          query: { redirect: this.$route.fullPath },
        });
        return;
      }
      this.selectedTurnoId = null;
      this.showJoinModal = true;
    },

    enrollInTurno(turnoId: number) {
      if (!this.isAuthenticated) {
        this.$router.push({
          path: "/signup",
          query: { redirect: this.$route.fullPath },
        });
        return;
      }
      // marcar el turno seleccionado y abrir modal de confirmación
      this.selectedTurnoId = turnoId;
      this.showJoinModal = true;
    },

    handleJoinCancel() {
      this.showJoinModal = false;
      this.joinLoading = false;
      this.joinSuccess = false;
      this.selectedTurnoId = null;
    },

    async handleJoinConfirm() {
      this.joinLoading = true;
      this.error = null;

      const turnoIdToEnroll =
        this.selectedTurnoId || (this.voluntariadoData ? this.voluntariadoData.turno : null);

      if (!turnoIdToEnroll) {
        this.error = "No se ha especificado un turno para la inscripción.";
        this.joinLoading = false;
        alert(this.error);
        this.handleJoinCancel();
        return;
      }

      if (this.enrolledTurnoIds.includes(Number(turnoIdToEnroll))) {
        this.error = "Ya estás inscripto en este turno.";
        this.joinLoading = false;
        alert(this.error);
        this.handleJoinCancel();
        return;
      }

      try {
        await turnoAPI.inscribirse(turnoIdToEnroll);
        this.joinSuccess = true;

        setTimeout(() => {
          this.handleJoinCancel();
          // Reload all data to reflect new enrollment status
          this.loadVoluntariado();
        }, 3000);
      } catch (err: any) {
        console.error("Error enrolling in turno:", err);
        this.error = err.response?.data?.detail || "Error al inscribirse en el turno.";
        this.joinLoading = false;
        alert(this.error);
        this.handleJoinCancel();
      }
    },

    promptCancelEnrollment(turnoId: number | null) {
      if (turnoId && this.enrolledTurnoIds.includes(Number(turnoId))) {
        this.turnoToCancelId = turnoId;
        this.showCancelModal = true;
      }
    },

    handleCancelationModalClose() {
      this.showCancelModal = false;
      this.cancelLoading = false;
      this.turnoToCancelId = null;
    },

    async handleCancelConfirm() {
      if (!this.turnoToCancelId) return;

      this.cancelLoading = true;
      this.error = null;

      try {
        await turnoAPI.cancelarInscripcion(this.turnoToCancelId);
        this.handleCancelationModalClose();
        await this.loadVoluntariado();
      } catch (err: any) {
        console.error("Error cancelling enrollment:", err);
        this.error = err.response?.data?.detail || "Error al cancelar la inscripción.";
        alert(this.error); // Simple feedback for now
        this.handleCancelationModalClose();
      }
    },

    viewOrganization() {
      if (this.organizacion?.id) {
        this.$router.push(`/organizaciones/${this.organizacion.id}`);
      }
    },

    viewVoluntariado(id: number) {
      this.$router.push(`/voluntariados/${id}`);
      window.scrollTo(0, 0);
      this.voluntariadoId = id;
      this.loadVoluntariado();
    },

    // NUEVO/EXISTENTE: helper para obtener el id del voluntariado desde un turno de forma robusta
    getTurnoVoluntariadoId(turno: any): number | null {
      if (!turno) return null;
      if (typeof turno.voluntariado === "number") return Number(turno.voluntariado);
      if (turno.voluntariado && typeof turno.voluntariado === "object") {
        if ("id" in turno.voluntariado) return Number(turno.voluntariado.id);
        if ("voluntariado" in turno.voluntariado) return Number(turno.voluntariado.voluntariado);
      }
      if ("voluntariado_id" in turno) return Number(turno.voluntariado_id);
      if ("voluntariadoId" in turno) return Number(turno.voluntariadoId);
      return null;
    },
  },
});
</script>

<template>
  <div class="voluntariado-detail">
    <AppNavBar />

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-else-if="error" class="container mt-4">
      <div class="alert alert-warning" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
      </div>
    </div>

    <!-- Content -->
    <template v-else-if="voluntariadoData">
      <!-- Hero Section -->
      <section class="voluntariado-hero">
        <div class="hero-overlay"></div>
        <div class="container">
          <div class="row">
            <div class="col-lg-10 mx-auto">
              <div class="text-center mb-4">
                <h2
                  class="organization-name-hero"
                  @click="viewOrganization"
                  style="cursor: pointer"
                >
                  {{ organizacion?.nombre || "Organización" }}
                </h2>
              </div>

              <!-- Main Card -->
              <div class="voluntariado-card">
                <div class="row">
                  <!-- Image -->
                  <div class="col-md-4">
                    <div class="voluntariado-image">
                      <img
                        src="https://via.placeholder.com/600x400"
                        :alt="voluntariadoData.nombre"
                      />
                    </div>
                  </div>

                  <!-- Info -->
                  <div class="col-md-8">
                    <div class="voluntariado-info">
                      <div class="d-flex justify-content-between align-items-start mb-3">
                        <h1 class="voluntariado-title">{{ voluntariadoData.nombre }}</h1>
                        <!-- Eliminado el botón "Unirme" de la tarjeta principal para evitar confusión.
                             La inscripción se realiza desde cada turno en la lista de turnos abajo. -->
                      </div>

                      <!-- Tags -->
                      <div class="voluntariado-tags mb-3">
                        <span
                          v-for="(tag, index) in generateTags(voluntariadoData)"
                          :key="index"
                          class="badge bg-secondary me-2 mb-2"
                        >
                          {{ tag }}
                        </span>
                      </div>

                      <!-- Schedule -->
                      <div class="schedule-info">
                        <div
                          v-for="(schedule, index) in generateSchedule(voluntariadoData)"
                          :key="index"
                          class="schedule-item"
                        >
                          <strong>{{ schedule.day }}</strong>
                          <span>{{ schedule.time }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Description Section -->
      <section class="description-section py-5">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 mx-auto">
              <div class="description-content">
                <p
                  v-for="(paragraph, index) in getDescriptionText(
                    voluntariadoData.descripcion
                  ).split('\n\n')"
                  :key="index"
                  class="mb-4"
                >
                  {{ paragraph }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Turnos Section -->
      <section class="org-voluntariados-section py-5 bg-light" v-if="allTurnos.length > 0">
        <div class="container">
          <div class="section-header mb-4">
            <h2 class="section-title">Turnos Disponibles</h2>
            <p class="section-subtitle">
              Seleccioná el/los turno(s) que mejor se adapte(n) a tu disponibilidad
            </p>
          </div>

          <!-- Turnos Grid -->
          <div class="row g-3 mb-4">
            <div v-for="turno in displayedTurnos" :key="turno.id" class="col-md-6 col-lg-4">
              <div class="turno-card">
                <div class="turno-header">
                  <div>
                    <div class="turno-day">{{ formatTurnoDate(turno) }}</div>
                    <div class="turno-label">{{ turno.lugar || "Ubicación" }}</div>
                  </div>

                  <!-- Botón por turno -->
                  <div>
                    <button
                      v-if="!enrolledTurnoIds.includes(Number(turno.id))"
                      class="btn btn-sm btn-dark"
                      @click="enrollInTurno(turno.id)"
                    >
                      {{ isAuthenticated ? "Inscribirse" : "Registrarse" }}
                    </button>

                    <button
                      v-else
                      class="btn btn-sm"
                      :class="isHovering === turno.id ? 'btn-danger' : 'btn-success'"
                      @mouseenter="isHovering = turno.id"
                      @mouseleave="isHovering = null"
                      @click="promptCancelEnrollment(turno.id)"
                    >
                      <span v-if="isHovering === turno.id">
                        <i class="bi bi-x-circle"></i> Cancelar
                      </span>
                      <span v-else> <i class="bi bi-check-circle"></i> Inscrito </span>
                    </button>
                  </div>
                </div>
                <div class="turno-details">
                  <p class="turno-text">
                    {{ formatTurnoFullDate(turno) }}
                    {{ formatTime(turno.hora_inicio) }} - {{ formatTime(turno.hora_fin) }}
                  </p>
                  <p class="turno-text">
                    <i class="bi bi-people me-2"></i>
                    {{ turno.cupo }} cupos disponibles
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="text-center" v-if="!showAllTurnos && allTurnos.length > 2">
            <button class="btn btn-outline-secondary" @click="showAllTurnos = true">
              Ver más turnos
            </button>
          </div>
        </div>
      </section>

      <!-- Organization Voluntariados -->
      <section class="org-voluntariados-section py-5" v-if="allOrgVoluntariados.length > 0">
        <div class="container">
          <h2 class="section-title mb-4">Más de {{ organizacion?.nombre }}</h2>

          <div class="row g-4 mb-4">
            <div v-for="vol in displayedOrgVoluntariados" :key="vol.id" class="col-md-6">
              <div class="simple-card" @click="viewVoluntariado(vol.id)" style="cursor: pointer">
                <div class="card-image-placeholder">
                  <i class="bi bi-image"></i>
                </div>
                <div class="card-content">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <h4 class="card-title-small">{{ vol.title }}</h4>
                    <span v-if="vol.isFree" class="badge bg-success">FREE</span>
                  </div>
                  <p class="card-description-small">{{ vol.description }}</p>
                  <div class="card-tags">
                    <span v-for="(tag, idx) in vol.tags" :key="idx" class="tag-item">
                      <i class="bi bi-tag-fill me-1"></i>{{ tag }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
            class="text-center"
            v-if="!showAllOrgVoluntariados && allOrgVoluntariados.length > 2"
          >
            <button class="btn btn-outline-secondary" @click="showAllOrgVoluntariados = true">
              Ver más voluntariados de esta organización
            </button>
          </div>
        </div>
      </section>

      <!-- Voluntariados Similares Section -->
      <section
        class="similar-voluntariados-section py-5 bg-light"
        v-if="allSimilarVoluntariados.length > 0"
      >
        <div class="container">
          <h2 class="section-title mb-4">Voluntariados Similares</h2>

          <div class="row g-4 mb-4">
            <div
              v-for="vol in displayedSimilarVoluntariados"
              :key="vol.id"
              class="col-md-6 col-lg-4"
            >
              <div class="simple-card" @click="viewVoluntariado(vol.id)" style="cursor: pointer">
                <div class="card-image-placeholder">
                  <i class="bi bi-image"></i>
                </div>
                <div class="card-content">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <h4 class="card-title-small">{{ vol.title }}</h4>
                    <span v-if="vol.isFree" class="badge bg-success">FREE</span>
                  </div>
                  <p class="card-description-small">{{ vol.description }}</p>
                  <div class="card-tags">
                    <span v-for="(tag, idx) in vol.tags" :key="idx" class="tag-item">
                      <i class="bi bi-tag-fill me-1"></i>{{ tag }}
                    </span>
                  </div>
                  <button class="btn btn-sm btn-outline-primary mt-3 w-100">Leer más</button>
                </div>
              </div>
            </div>
          </div>

          <div class="text-center" v-if="!showAllSimilar && allSimilarVoluntariados.length > 3">
            <button class="btn btn-outline-secondary" @click="showAllSimilar = true">
              Ver más voluntariados similares
            </button>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <CTASection
        title="¡Inscríbete hoy y marca la diferencia!"
        primary-text="Registrarme como voluntario"
        primary-link="/signup"
        secondary-text="Soy Organización, quiero colaborar"
        secondary-link="/contact"
      />

      <JoinConfirmationModal
        :show="showJoinModal"
        :voluntariado-title="voluntariadoData.nombre"
        :organization-name="organizacion?.nombre || 'Organización'"
        :loading="joinLoading"
        :show-success="joinSuccess"
        @confirm="handleJoinConfirm"
        @cancel="handleJoinCancel"
      />

      <CancelConfirmationModal
        :show="showCancelModal"
        :voluntariado-title="voluntariadoData.nombre"
        :organization-name="organizacion?.nombre || 'Organización'"
        :loading="cancelLoading"
        @confirm="handleCancelConfirm"
        @cancel="handleCancelationModalClose"
      />
    </template>
  </div>
</template>

<style scoped src="./../styles/VoluntariadoDetail.css"></style>
