<template>
  <div class="area-personal-page">
    <AppNavBar />

    <!-- Hero Header -->
    <section class="page-header shared-hero">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto text-center">
            <h1 class="hero-title mb-4">Mi Área Personal</h1>
            <p class="hero-subtitle">
              Gestiona tus voluntariados y sigue tu progreso en tu camino solidario.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mt-4">
      <div class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        {{ error }}
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="container my-5 voluntariados-container">
      <!-- Statistics Cards -->
      <div class="stats-section mb-5">
        <div class="row g-4">
          <div class="col-lg-3 col-md-6">
            <div class="stat-card">
              <div class="stat-icon-wrapper upcoming">
                <i class="bi bi-calendar-event"></i>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ proximosVoluntariados.length }}</h3>
                <p class="stat-label">Próximos</p>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="stat-card">
              <div class="stat-icon-wrapper active">
                <i class="bi bi-heart-fill"></i>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ voluntariadosActivos.length }}</h3>
                <p class="stat-label">Activos</p>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="stat-card">
              <div class="stat-icon-wrapper completed">
                <i class="bi bi-check2-circle"></i>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ voluntariadosCompletados.length }}</h3>
                <p class="stat-label">Completados</p>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="stat-card">
              <div class="stat-icon-wrapper hours">
                <i class="bi bi-clock-history"></i>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ totalHorasFormatted }}</h3>
                <p class="stat-label">Horas Totales</p>
                <small
                  class="text-muted"
                  style="font-size: 0.7rem; display: block; margin-top: 0.25rem"
                >
                  Todos los voluntariados
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Mis Próximos Voluntariados -->
      <div class="table-with-arrow">
        <div class="pipeline-arrow-left">
          <div
            class="arrow-line"
            style="
              background: linear-gradient(180deg, var(--brand-start) 0%, var(--brand-mid) 100%);
            "
          ></div>
          <div class="arrow-head">
            <i class="bi bi-arrow-down-circle-fill" style="color: var(--brand-mid)"></i>
          </div>
        </div>
        <div class="section-content">
          <section class="content-section">
            <h2 class="section-title">
              <i class="bi bi-calendar-event me-2"></i>Mis Próximos Voluntariados
            </h2>
            <div v-if="proximosVoluntariados.length > 0">
              <div class="row g-4">
                <div
                  class="col-lg-4 col-md-6"
                  v-for="voluntariado in proximosVoluntariados"
                  :key="voluntariado.id"
                >
                  <router-link :to="`/voluntariados/${voluntariado.id}`" class="card-link">
                    <div class="card voluntariado-card h-100">
                      <div class="card-img-top-wrapper">
                        <img
                          :src="getVoluntariadoImageUrl(voluntariado)"
                          class="card-img-top"
                          alt="Imagen del voluntariado"
                        />
                        <div class="img-overlay"></div>
                        <span
                          v-if="voluntariado.source === 'convocatoria'"
                          class="badge bg-primary card-badge"
                          >Convocatoria</span
                        >
                        <span
                          v-else-if="voluntariado.source === 'preparacion'"
                          class="badge bg-warning text-dark card-badge"
                          >Preparación</span
                        >
                        <span v-else class="badge bg-brand card-badge">Próximo</span>
                      </div>
                      <div class="card-body d-flex flex-column">
                        <h5 class="card-title">{{ voluntariado.nombre }}</h5>
                        <p class="card-subtitle mb-2 text-muted">
                          {{ voluntariado.organizacion_nombre }}
                        </p>
                        <p class="card-text small flex-grow-1">
                          {{ getVoluntariadoDescription(voluntariado) }}
                        </p>
                        <ul class="list-unstyled mt-3 mb-0 turnos-list">
                          <li
                            v-for="turno in voluntariado.turnos.slice(0, 2)"
                            :key="turno.id"
                            class="turno-item"
                            :title="turno.lugar"
                          >
                            <span
                              ><i class="bi bi-calendar-check text-brand"></i>
                              {{ formatDateShort(turno.fecha) }}</span
                            >
                            <span
                              ><i class="bi bi-clock text-brand"></i>
                              {{ formatTime(turno.hora_inicio) }} -
                              {{ formatTime(turno.hora_fin) }}</span
                            >
                          </li>
                          <li
                            v-if="voluntariado.turnos.length > 2"
                            class="turno-item text-muted small"
                          >
                            Y {{ voluntariado.turnos.length - 2 }} más...
                          </li>
                        </ul>
                      </div>
                    </div>
                  </router-link>
                </div>
              </div>

              <!-- Load more buttons for proximos (if backend returns paginated results) -->
              <div class="mt-3">
                <div class="d-flex gap-2 justify-content-center">
                  <button
                    v-if="perStatus.convocatoria && perStatus.convocatoria.next"
                    @click.prevent="loadMoreStatus('convocatoria')"
                    class="btn btn-sm btn-outline-brand"
                    :disabled="perStatus.convocatoria.loading"
                  >
                    Cargar más Convocatoria
                  </button>
                  <button
                    v-if="perStatus.preparacion && perStatus.preparacion.next"
                    @click.prevent="loadMoreStatus('preparacion')"
                    class="btn btn-sm btn-outline-brand"
                    :disabled="perStatus.preparacion.loading"
                  >
                    Cargar más Preparación
                  </button>
                  <button
                    v-if="perStatus.upcoming && perStatus.upcoming.next"
                    @click.prevent="loadMoreStatus('upcoming')"
                    class="btn btn-sm btn-outline-brand"
                    :disabled="perStatus.upcoming.loading"
                  >
                    Cargar más Próximos
                  </button>
                </div>
              </div>
            </div>

            <div v-else>
              <div class="alert alert-light text-center py-4">
                <i class="bi bi-calendar-x display-4 text-muted d-block mb-3"></i>
                <p class="mb-2">No estás inscripto a próximos voluntariados.</p>
                <router-link to="/voluntariados" class="btn btn-brand btn-sm">
                  <i class="bi bi-search me-2"></i>¡Busca uno!
                </router-link>
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- Mi Calendario -->
      <div class="table-with-arrow">
        <div class="pipeline-arrow-left">
          <div
            class="arrow-line"
            style="
              background: linear-gradient(180deg, var(--brand-mid) 0%, var(--brand-accent) 100%);
            "
          ></div>
          <div class="arrow-head">
            <i class="bi bi-arrow-down-circle-fill" style="color: var(--brand-accent)"></i>
          </div>
        </div>
        <div class="section-content">
          <section class="content-section">
            <h2 class="section-title">
              <i class="bi bi-calendar3 me-2"></i>Mi Calendario de Turnos
            </h2>
            <div v-if="allTurnos.length > 0">
              <TurnosCalendar
                :turnos="allTurnos"
                :selected-date="selectedDate"
                @date-selected="handleDateSelected"
              />

              <!-- Selected Date Turnos Details -->
              <div v-if="selectedDateTurnos.length > 0" class="selected-date-details mt-4">
                <h5 class="mb-3">
                  <i class="bi bi-calendar-check me-2"></i>
                  Turnos para {{ selectedDate ? formatDateShort(selectedDate) : "" }}
                </h5>
                <div class="row g-3">
                  <div v-for="turno in selectedDateTurnos" :key="turno.id" class="col-md-6">
                    <div class="card turno-detail-card">
                      <div class="card-body">
                        <!-- Location Section -->
                        <div class="turno-location-section mb-3">
                          <h6 class="card-title mb-2">
                            <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                            Ubicación
                          </h6>
                          <div class="location-details">
                            <p v-if="turno.lugar" class="location-text mb-2">
                              {{ turno.lugar }}
                            </p>
                            <p v-else class="text-muted small mb-2"></p>
                            <a
                              :href="
                                getGoogleMapsUrl(getTurnoVoluntariado(turno.id), turno.lugar) ||
                                'https://www.google.com/maps'
                              "
                              target="_blank"
                              rel="noopener noreferrer"
                              class="btn btn-sm btn-outline-danger"
                            >
                              <i class="bi bi-geo-alt-fill me-1"></i>
                              Ver en Google Maps
                            </a>
                          </div>
                        </div>

                        <!-- Time Section -->
                        <div class="turno-time-section mb-3">
                          <p class="card-text mb-0">
                            <i class="bi bi-clock text-primary me-2"></i>
                            <strong>Horario:</strong> {{ formatTime(turno.hora_inicio) }} -
                            {{ formatTime(turno.hora_fin) }}
                          </p>
                        </div>

                        <!-- Voluntariado Link -->
                        <div class="turno-voluntariado-section">
                          <router-link
                            v-if="getTurnoVoluntariado(turno.id)"
                            :to="`/voluntariados/${getTurnoVoluntariado(turno.id)!.id}`"
                            class="btn btn-sm btn-outline-brand w-100"
                          >
                            <i class="bi bi-heart-fill me-1"></i>
                            Ver {{ getTurnoVoluntariadoName(turno.id) }}
                          </router-link>
                          <p v-else class="text-muted small mb-0">
                            Voluntariado: {{ getTurnoVoluntariadoName(turno.id) }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else>
              <div class="alert alert-light text-center py-4">
                <i class="bi bi-calendar2-x display-4 text-muted d-block mb-3"></i>
                <p class="mb-0">No tienes turnos programados en tus voluntariados.</p>
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- Voluntariados Activos -->
      <div class="table-with-arrow">
        <div class="pipeline-arrow-left">
          <div
            class="arrow-line"
            style="background: linear-gradient(180deg, var(--brand-accent) 0%, #198754 100%)"
          ></div>
          <div class="arrow-head">
            <i class="bi bi-arrow-down-circle-fill text-success"></i>
          </div>
        </div>
        <div class="section-content">
          <section class="content-section">
            <h2 class="section-title">
              <i class="bi bi-heart-fill me-2"></i>Mis Voluntariados Activos
            </h2>
            <div v-if="voluntariadosActivos.length > 0" class="row g-4">
              <div
                class="col-lg-6"
                v-for="voluntariado in voluntariadosActivos"
                :key="voluntariado.id"
              >
                <router-link :to="`/voluntariados/${voluntariado.id}`" class="card-link">
                  <div class="card voluntariado-active-card h-100">
                    <div class="card-body">
                      <div class="d-flex align-items-start mb-3">
                        <div class="icon-wrapper-active me-3">
                          <i class="bi bi-heart-fill text-white fs-4"></i>
                        </div>
                        <div class="flex-grow-1">
                          <h5 class="card-title mb-1">{{ voluntariado.nombre }}</h5>
                          <p class="card-subtitle text-muted mb-0">
                            {{ voluntariado.organizacion_nombre }}
                          </p>
                        </div>
                        <span class="badge bg-success">Activo</span>
                      </div>

                      <p class="card-text mb-3">
                        {{ getVoluntariadoDescription(voluntariado) }}
                      </p>

                      <div class="voluntariado-info mb-3">
                        <div class="info-item">
                          <i class="bi bi-calendar-range text-brand me-2"></i>
                          <small>
                            <strong>Inicio:</strong>
                            {{ formatDateShort(voluntariado.fecha_inicio_cursado || "") }}
                          </small>
                        </div>
                        <div class="info-item">
                          <i class="bi bi-calendar-check text-brand me-2"></i>
                          <small>
                            <strong>Fin:</strong>
                            {{ formatDateShort(voluntariado.fecha_fin_cursado || "") }}
                          </small>
                        </div>
                        <div
                          class="info-item"
                          v-if="voluntariado.turnos && voluntariado.turnos.length > 0"
                        >
                          <i class="bi bi-clock-history text-brand me-2"></i>
                          <small> <strong>Turnos:</strong> {{ voluntariado.turnos.length }} </small>
                        </div>
                        <button
                          v-if="userInscribedToVol(voluntariado)"
                          :disabled="(perVolHoras[voluntariado.id] ?? 0) <= 0"
                          type="button"
                          class="btn btn-outline-success btn-sm mt-2 mt-md-0"
                          @click.stop.prevent="descargarCertificado(voluntariado.id)"
                          :title="(perVolHoras[voluntariado.id] ?? 0) <= 0 ? 'No hay horas registradas' : ''"
                        >
                          <i class="bi bi-download me-2"></i>
                          <span v-if="(perVolHoras[voluntariado.id] ?? 0) > 0">Descargar Certificado Temporal</span>
                          <span v-else>Sin horas</span>
                          <small class="ms-2 text-muted">({{ perVolHoras[voluntariado.id] ?? 0 }} h)</small>
                        </button>
                      </div>

                      <div class="view-details-footer">
                        <span class="view-details-text">
                          <i class="bi bi-eye me-2"></i>Ver Detalles
                        </span>
                        <i class="bi bi-arrow-right"></i>
                      </div>
                    </div>
                  </div>
                </router-link>
              </div>
            </div>
            <div v-else>
              <div class="alert alert-light text-center py-4">
                <i class="bi bi-heart display-4 text-muted d-block mb-3"></i>
                <p class="mb-0">No tienes voluntariados activos en este momento.</p>
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- Voluntariados Completados -->
      <div class="table-with-arrow">
        <div class="pipeline-arrow-left">
          <div
            class="arrow-line"
            style="background: linear-gradient(180deg, #198754 0%, #212529 100%)"
          ></div>
          <div class="arrow-head">
            <i class="bi bi-arrow-down-circle-fill text-dark"></i>
          </div>
        </div>
        <div class="section-content">
          <section class="content-section">
            <h2 class="section-title">
              <i class="bi bi-check2-circle me-2"></i>Mis Voluntariados Completados
            </h2>
            <div v-if="voluntariadosCompletados.length > 0">
              <div class="list-group list-group-flush">
                <div
                  v-for="voluntariado in voluntariadosCompletados"
                  :key="voluntariado.id"
                  class="list-group-item completado-item d-flex justify-content-between align-items-center flex-wrap"
                >
                  <div class="d-flex align-items-center">
                    <div class="icon-wrapper-finished me-3">
                      <i class="bi bi-check-circle-fill text-success fs-5"></i>
                    </div>
                    <div>
                      <h6 class="mb-1">{{ voluntariado.nombre }}</h6>
                      <small class="text-muted">
                        {{ voluntariado.organizacion_nombre }} &bull; Finalizado el:
                        {{ formatDateShort(voluntariado.fecha_fin_cursado || "") }}
                      </small>
                    </div>
                  </div>
                  <button
                    v-if="userInscribedToVol(voluntariado)"
                    :disabled="(perVolHoras[voluntariado.id] ?? 0) <= 0"
                    type="button"
                    class="btn btn-outline-success btn-sm mt-2 mt-md-0"
                    @click.stop.prevent="descargarCertificado(voluntariado.id)"
                    :title="(perVolHoras[voluntariado.id] ?? 0) <= 0 ? 'No hay horas registradas' : ''"
                  >
                    <i class="bi bi-download me-2"></i>
                    <span v-if="(perVolHoras[voluntariado.id] ?? 0) > 0">Descargar Certificado</span>
                    <span v-else>Sin horas</span>
                    <small class="ms-2 text-muted">({{ perVolHoras[voluntariado.id] ?? 0 }} h)</small>
                  </button>
                </div>
              </div>
            </div>
            <div v-else>
              <div class="alert alert-light text-center py-4">
                <i class="bi bi-hourglass-bottom display-4 text-muted d-block mb-3"></i>
                <p class="mb-0">Aún no has completado voluntariados.</p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import TurnosCalendar from "@/components/TurnosCalendar.vue";
import apiClient, { certificadoAPI, voluntariadoAPI, userAPI, personaAPI } from "@/services/api";
import { formatHours, formatDateShort } from "@/utils/dateUtils";

interface Turno {
  id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  lugar?: string;
  cupo?: number;
  inscripciones_count?: number;
  is_full?: boolean;
}
type DescripcionResp =
  | string
  | { resumen?: string; descripcion?: string; portada?: string | null }
  | null;

interface VoluntariadoAPIResponse {
  id: number;
  nombre: string;
  descripcion: DescripcionResp;
  fecha_inicio_convocatoria?: string | null;
  fecha_fin_convocatoria?: string | null;
  fecha_inicio_cursado?: string | null;
  fecha_fin_cursado?: string | null;
  organizacion_nombre?: string;
  organizacion?: { nombre?: string };
  turnos?: Turno[];
  etapa?: string | null;
}
interface TurnoAPIResponse {
  id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  lugar?: string;
  cupo?: number;
  inscripciones_count?: number;
  is_full?: boolean;
}
interface Voluntariado {
  id: number;
  nombre: string;
  descripcion: string | { resumen?: string; descripcion?: string; portada?: string | null } | null;
  // Fechas provenientes del backend (cursado/convocatoria)
  fecha_inicio_convocatoria?: string | null;
  fecha_fin_convocatoria?: string | null;
  fecha_inicio_cursado?: string | null;
  fecha_fin_cursado?: string | null;
  // Nombre plano para evitar tocar el template en muchos lugares
  organizacion_nombre: string;
  // Para mantener compatibilidad con el template agregamos turnos en el fetch
  turnos: Turno[];
  // Etapa/estado calculado por el backend
  etapa?: string | null;
  // Source for UI (which mis-voluntariados endpoint returned it)
  source?: "upcoming" | "convocatoria" | "preparacion" | "active" | "finished";
}

export default defineComponent({
  name: "AreaPersonalView",
  components: {
    AppNavBar,
    TurnosCalendar,
  },
  data() {
    return {
      loading: true,
      error: null as string | null,
      proximosVoluntariados: [] as Voluntariado[],
      voluntariadosActivos: [] as Voluntariado[],
      voluntariadosCompletados: [] as Voluntariado[],
      // Pagination state per backend status endpoint
      perStatus: {
        upcoming: {
          items: [] as VoluntariadoAPIResponse[],
          next: null as string | null,
          loading: false,
        },
        convocatoria: {
          items: [] as VoluntariadoAPIResponse[],
          next: null as string | null,
          loading: false,
        },
        preparacion: {
          items: [] as VoluntariadoAPIResponse[],
          next: null as string | null,
          loading: false,
        },
        active: {
          items: [] as VoluntariadoAPIResponse[],
          next: null as string | null,
          loading: false,
        },
        finished: {
          items: [] as VoluntariadoAPIResponse[],
          next: null as string | null,
          loading: false,
        },
      } as Record<
        string,
        { items: VoluntariadoAPIResponse[]; next: string | null; loading: boolean }
      >,
      selectedDate: null as string | null,
      // Total horas retrieved from backend (Asistencia aggregation)
      totalHorasVoluntariado: 0,
      // Turnos the current user is inscribed to (used by the calendar)
      userInscribedTurnos: [] as Turno[],
      // Per-voluntariado horas for the current user
      perVolHoras: {} as Record<number, number>,
    };
  },
  async created() {
    await this.loadVoluntariados();
  },
  computed: {
    allTurnos(): Array<{
      id: number;
      fecha: string;
      hora_inicio: string;
      hora_fin: string;
      cupo: number;
      lugar?: string;
      inscripciones_count?: number;
      is_full?: boolean;
    }> {
      // Show ONLY the turnos the current user is inscribed to
      return (this.userInscribedTurnos || []).map((t) => ({
        ...t,
        cupo: typeof t.cupo === "number" ? t.cupo : 0,
      }));
    },
    selectedDateTurnos(): Array<{
      id: number;
      fecha: string;
      hora_inicio: string;
      hora_fin: string;
      cupo: number;
      lugar?: string;
      inscripciones_count?: number;
      is_full?: boolean;
    }> {
      if (!this.selectedDate) return [];
      return this.allTurnos.filter((turno) => turno.fecha === this.selectedDate);
    },
    totalHorasFormatted(): string {
      return formatHours(this.totalHorasVoluntariado);
    },
    // NOTE: totalHorasVoluntariado is provided by backend. See loadTotalHoras()
  },
  methods: {
    handleDateSelected(dateString: string) {
      this.selectedDate = dateString;
    },
    getTurnoVoluntariadoName(turnoId: number): string {
      // Check in upcoming voluntariados
      for (const vol of this.proximosVoluntariados) {
        if (vol.turnos && vol.turnos.some((t) => t.id === turnoId)) {
          return vol.nombre;
        }
      }
      // Check in active voluntariados
      for (const vol of this.voluntariadosActivos) {
        if (vol.turnos && vol.turnos.some((t) => t.id === turnoId)) {
          return vol.nombre;
        }
      }
      return "Desconocido";
    },
    getTurnoVoluntariado(turnoId: number): Voluntariado | null {
      // Check in upcoming voluntariados
      for (const vol of this.proximosVoluntariados) {
        if (vol.turnos && vol.turnos.some((t) => t.id === turnoId)) {
          return vol;
        }
      }
      // Check in active voluntariados
      for (const vol of this.voluntariadosActivos) {
        if (vol.turnos && vol.turnos.some((t) => t.id === turnoId)) {
          return vol;
        }
      }
      return null;
    },
    userInscribedToVol(voluntariado: Voluntariado): boolean {
      // Return true if any turno of the voluntariado is present in userInscribedTurnos
      if (!voluntariado || !Array.isArray(voluntariado.turnos) || voluntariado.turnos.length === 0) {
        return false;
      }
      const inscribedIds = new Set((this.userInscribedTurnos || []).map((t: Turno) => t.id));
      return voluntariado.turnos.some((t: Turno) => inscribedIds.has(t.id));
    },
    getGoogleMapsUrl(voluntariado: Voluntariado | null, lugar?: string): string | null {
      if (!voluntariado && !lugar) return null;
      const vol = voluntariado as any;
      if (vol && vol.place_id) {
        return `https://www.google.com/maps/search/?api=1&query=&query_place_id=${vol.place_id}`;
      } else if (vol && vol.latitud && vol.longitud) {
        return `https://www.google.com/maps/search/?api=1&query=${vol.latitud},${vol.longitud}`;
      } else if (lugar) {
        // Fallback: search by location text
        return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(lugar)}`;
      }
      return null;
    },
    async loadVoluntariados() {
      // Cargar listas ya filtradas por el backend usando los endpoints existentes
      this.loading = true;
      this.error = null;
      try {
        // Helper to fetch first page for a status endpoint
        const fetchFirst = async (key: string, fn: () => Promise<{ data: unknown }>) => {
          this.perStatus[key]!.loading = true;
          try {
            const res = await fn();
            const payload = res.data as unknown;
            if (payload && Array.isArray(payload)) {
              this.perStatus[key]!.items = payload as VoluntariadoAPIResponse[];
              this.perStatus[key]!.next = null;
            } else if (payload && typeof payload === "object" && "results" in (payload as object)) {
              const p = payload as { results?: VoluntariadoAPIResponse[]; next?: string | null };
              this.perStatus[key]!.items = p.results || [];
              this.perStatus[key]!.next = p.next || null;
            } else {
              this.perStatus[key]!.items = [];
              this.perStatus[key]!.next = null;
            }
          } finally {
            this.perStatus[key]!.loading = false;
          }
        };

        // Fetch initial pages in parallel
        await Promise.all([
          fetchFirst("upcoming", () => voluntariadoAPI.getMineUpcoming()),
          fetchFirst("convocatoria", () => voluntariadoAPI.getMineConvocatoria()),
          fetchFirst("preparacion", () => voluntariadoAPI.getMinePreparacion()),
          fetchFirst("active", () => voluntariadoAPI.getMineActive()),
          fetchFirst("finished", () => voluntariadoAPI.getMineFinished()),
        ]);

        // Map helper
        const mapToVol = (v: VoluntariadoAPIResponse, source?: string): Voluntariado => ({
          id: v.id,
          nombre: v.nombre,
          descripcion: v.descripcion,
          fecha_inicio_convocatoria: v.fecha_inicio_convocatoria ?? null,
          fecha_fin_convocatoria: v.fecha_fin_convocatoria ?? null,
          fecha_inicio_cursado: v.fecha_inicio_cursado ?? null,
          fecha_fin_cursado: v.fecha_fin_cursado ?? null,
          organizacion_nombre: v.organizacion_nombre || v.organizacion?.nombre || "",
          turnos: Array.isArray(v.turnos) ? v.turnos : [],
          etapa: v.etapa ?? null,
          source: (source as Voluntariado["source"]) || undefined,
        });

        // Build proximos: prefer convocatoria > preparacion > upcoming
        const seenIds = new Set<number>();
        const proximosList: Voluntariado[] = [];
        for (const v of this.perStatus.convocatoria!.items) {
          if (!v || seenIds.has(v.id)) continue;
          seenIds.add(v.id);
          proximosList.push(mapToVol(v, "convocatoria"));
        }
        for (const v of this.perStatus.preparacion!.items) {
          if (!v || seenIds.has(v.id)) continue;
          seenIds.add(v.id);
          proximosList.push(mapToVol(v, "preparacion"));
        }
        for (const v of this.perStatus.upcoming!.items) {
          if (!v || seenIds.has(v.id)) continue;
          seenIds.add(v.id);
          proximosList.push(mapToVol(v, "upcoming"));
        }

        this.proximosVoluntariados = proximosList;
        this.voluntariadosActivos = this.perStatus.active!.items.map((v) => mapToVol(v, "active"));
        this.voluntariadosCompletados = this.perStatus.finished!.items.map((v) =>
          mapToVol(v, "finished")
        );

        // Load total hours FIRST before loading turnos, to ensure we always have the correct total
        try {
          await this.loadTotalHoras();
        } catch (e) {
          console.error("Error loading total horas before turnos", e);
        }

        // Asegurar que los proximos/activos tengan sus turnos cargados (los endpoints de "mis" pueden no incluirlos)
        const idsParaTurnos = [
          ...this.proximosVoluntariados.map((v) => v.id),
          ...this.voluntariadosActivos.map((v) => v.id),
          ...this.voluntariadosCompletados.map((v) => v.id),
        ];
        if (idsParaTurnos.length > 0) {
          const turnosResponses = await Promise.all(
            idsParaTurnos.map((id) =>
              voluntariadoAPI.getTurnos(id).then((r) => ({ id, data: r.data }))
            )
          );
          const turnosMap: Record<number, Turno[]> = {};
          for (const { id, data } of turnosResponses) {
            const arr = (data || []) as TurnoAPIResponse[];
            turnosMap[id] = arr.map((t: TurnoAPIResponse) => ({
              id: t.id,
              fecha: t.fecha,
              hora_inicio: t.hora_inicio,
              hora_fin: t.hora_fin,
              lugar: t.lugar,
              cupo: typeof t.cupo === "number" ? t.cupo : 0,
              inscripciones_count: t.inscripciones_count,
              is_full: t.is_full,
            }));
          }
          // Insertar turnos en los objetos existentes para mantener el template sin cambios
          this.proximosVoluntariados = this.proximosVoluntariados.map((v) => ({
            ...v,
            turnos: turnosMap[v.id] || [],
          }));
          this.voluntariadosActivos = this.voluntariadosActivos.map((v) => ({
            ...v,
            turnos: turnosMap[v.id] || [],
          }));
          // Keep completed items in sync as well
          this.voluntariadosCompletados = this.voluntariadosCompletados.map((v) => ({
            ...v,
            turnos: turnosMap[v.id] || [],
          }));
          // Also ensure completed voluntariados receive their turnos so
          // userInscribedToVol() can detect inscriptions for finished items.
          this.voluntariadosCompletados = this.voluntariadosCompletados.map((v) => ({
            ...v,
            turnos: turnosMap[v.id] || [],
          }));
          // Load user's inscribed turnos for the calendar
          try {
            const userRes = await userAPI.getCurrentUser();
            const personaId = userRes.data?.persona;
            if (personaId) {
              const resp = await personaAPI.getVoluntariadosVoluntario(personaId);
              const volData = resp.data as VoluntariadoAPIResponse[];
              const inscribedTurnos: Turno[] = [];
              for (const v of volData || []) {
                if (Array.isArray(v.turnos)) {
                  for (const t of v.turnos) {
                    inscribedTurnos.push({
                      id: t.id,
                      fecha: t.fecha,
                      hora_inicio: t.hora_inicio,
                      hora_fin: t.hora_fin,
                      lugar: t.lugar,
                      cupo: typeof t.cupo === "number" ? t.cupo : 0,
                      inscripciones_count: t.inscripciones_count,
                      is_full: t.is_full,
                    });
                  }
                }
              }
              this.userInscribedTurnos = inscribedTurnos;
            } else {
              this.userInscribedTurnos = [];
            }
          } catch (e) {
            console.error("Error loading user inscribed turnos", e);
            this.userInscribedTurnos = [];
          }
          // After we've loaded inscribed turnos, fetch per-voluntariado horas for displayed lists
          try {
            await this.loadHorasForVoluntariados(idsParaTurnos);
          } catch (e) {
            console.error("Error loading horas per voluntariado", e);
          }
        }
      } catch (err) {
        console.error("Error loading voluntariados:", err);
        const errorResponse = err as { response?: { data?: { detail?: string } } };
        this.error = errorResponse.response?.data?.detail || "Error al cargar los voluntariados.";
      } finally {
        this.loading = false;
      }
    },
    async loadHorasForVoluntariados(ids: number[]) {
      // Fetch total_horas for each voluntariado for the current user in parallel
      const uniqueIds = Array.from(new Set(ids));
      const promises = uniqueIds.map((id) =>
        // Direct apiClient call to the new endpoint (namespaced under certificado)
        apiClient.get(`/certificado/generacion/horas-por-voluntariado/${id}/`).then((r) => ({ id, total: r.data?.total_horas ?? 0 })).catch((e) => {
          console.error("horas fetch failed for", id, e);
          return { id, total: 0 };
        })
      );
      const results = await Promise.all(promises);
      for (const res of results) {
        this.perVolHoras[res.id] = Number(res.total) || 0;
      }
    },
    getVoluntariadoDescription(voluntariado: Voluntariado): string {
      if (!voluntariado || !voluntariado.descripcion) {
        return "Sin descripción.";
      }
      const desc =
        typeof voluntariado.descripcion === "object" && voluntariado.descripcion !== null
          ? voluntariado.descripcion.resumen || voluntariado.descripcion.descripcion
          : voluntariado.descripcion;

      if (!desc) return "Sin descripción.";

      return desc.length > 100 ? desc.substring(0, 97) + "..." : desc;
    },
    getVoluntariadoImageUrl(voluntariado: Voluntariado): string {
      const defaultImg = "https://placehold.co/400x250/8B0000/FFFFFF?text=Voluntariado";
      if (typeof voluntariado.descripcion === "object" && voluntariado.descripcion !== null) {
        return voluntariado.descripcion.portada || defaultImg;
      }
      return defaultImg;
    },
    formatDateShort(dateString: string): string {
      if (!dateString) return "Fecha no definida";
      return formatDateShort(dateString);
    },
    formatTime(timeString: string): string {
      if (!timeString) return "";
      return timeString.substring(0, 5); // HH:MM
    },
    async descargarCertificado(voluntariadoId: number) {
      try {
        const response = await certificadoAPI.generarPorVoluntariado(voluntariadoId);
        const blob = new Blob([response.data], { type: "application/pdf" });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `certificado_voluntariado_${voluntariadoId}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        const err = error as { response?: { status?: number; data?: { detail?: string } } };
        const status = err.response?.status;
        const detail = err.response?.data?.detail;

        // Prefer server-provided message when available
        if (detail) {
          alert(detail);
          return;
        }

        // Fallback to status-based friendly messages when detail is missing
        if (status === 400) {
          alert("No hay horas registradas para este voluntariado.");
        } else if (status === 404) {
          alert("No estás inscripto a este voluntariado.");
        } else if (status === 403) {
          alert("No tienes permisos para generar este certificado.");
        } else {
          alert("No se pudo generar el certificado.");
        }
      }
    },
    // Pagination helpers: fetch next page for a given perStatus key and append results
    async fetchNext(key: string) {
      const nextUrl = this.perStatus[key]?.next;
      if (!nextUrl) return;
      this.perStatus[key]!.loading = true;
      try {
        const res = await apiClient.get(nextUrl);
        const payload = res.data as unknown;
        let newItems: VoluntariadoAPIResponse[] = [];
        if (payload && Array.isArray(payload)) {
          newItems = payload as VoluntariadoAPIResponse[];
        } else if (payload && typeof payload === "object" && "results" in (payload as object)) {
          newItems = (payload as { results?: VoluntariadoAPIResponse[] }).results || [];
        }
        const current = this.perStatus[key]!.items || [];
        this.perStatus[key]!.items = [...current, ...newItems];
        // update next
        if (payload && typeof payload === "object" && "next" in (payload as object)) {
          this.perStatus[key]!.next = (payload as { next?: string | null }).next || null;
        } else {
          this.perStatus[key]!.next = null;
        }
      } catch (e) {
        console.error("Error fetching next page:", e);
      } finally {
        this.perStatus[key]!.loading = false;
      }

      // Recompute aggregated lists and ensure turnos are present for new items
      await this.recomputeDerivedLists();
      try {
        const idsParaTurnos = [
          ...this.proximosVoluntariados.map((v) => v.id),
          ...this.voluntariadosActivos.map((v) => v.id),
          ...this.voluntariadosCompletados.map((v) => v.id),
        ];
        if (idsParaTurnos.length > 0) {
          const turnosResponses = await Promise.all(
            idsParaTurnos.map((id) =>
              voluntariadoAPI.getTurnos(id).then((r) => ({ id, data: r.data }))
            )
          );
          const turnosMap: Record<number, Turno[]> = {};
          for (const { id, data } of turnosResponses) {
            const arr = (data || []) as TurnoAPIResponse[];
            turnosMap[id] = arr.map((t: TurnoAPIResponse) => ({
              id: t.id,
              fecha: t.fecha,
              hora_inicio: t.hora_inicio,
              hora_fin: t.hora_fin,
              lugar: t.lugar,
              cupo: typeof t.cupo === "number" ? t.cupo : 0,
              inscripciones_count: t.inscripciones_count,
              is_full: t.is_full,
            }));
          }
          this.proximosVoluntariados = this.proximosVoluntariados.map((v) => ({
            ...v,
            turnos: turnosMap[v.id] || [],
          }));
          this.voluntariadosActivos = this.voluntariadosActivos.map((v) => ({
            ...v,
            turnos: turnosMap[v.id] || [],
          }));
          // Refresh total hours after pagination changed lists - MOVED to after turno fetching
          try {
            await this.loadTotalHoras();
          } catch (e) {
            console.error("Error loading total horas after pagination", e);
          }
          // Also refresh user's inscribed turnos after pagination
          try {
            const userRes = await userAPI.getCurrentUser();
            const personaId = userRes.data?.persona;
            if (personaId) {
              const resp = await personaAPI.getVoluntariadosVoluntario(personaId);
              const volData = resp.data as VoluntariadoAPIResponse[];
              const inscribedTurnos: Turno[] = [];
              for (const v of volData || []) {
                if (Array.isArray(v.turnos)) {
                  for (const t of v.turnos) {
                    inscribedTurnos.push({
                      id: t.id,
                      fecha: t.fecha,
                      hora_inicio: t.hora_inicio,
                      hora_fin: t.hora_fin,
                      lugar: t.lugar,
                      cupo: typeof t.cupo === "number" ? t.cupo : 0,
                      inscripciones_count: t.inscripciones_count,
                      is_full: t.is_full,
                    });
                  }
                }
              }
              this.userInscribedTurnos = inscribedTurnos;
            } else {
              this.userInscribedTurnos = [];
            }
          } catch (e) {
            console.error("Error loading user inscribed turnos after pagination", e);
            this.userInscribedTurnos = [];
          }
        }
      } catch (e) {
        console.error("Error fetching turnos after pagination", e);
      }
    },
    async loadMoreStatus(key: string) {
      await this.fetchNext(key);
    },
    async loadTotalHoras() {
      try {
        const userRes = await userAPI.getCurrentUser();
        const personaId = userRes.data?.persona;
        if (!personaId) {
          this.totalHorasVoluntariado = 0;
          return;
        }

        const resp = await apiClient.get(`/persona/voluntarios/${personaId}/horas/`);
        const total = resp.data?.total_horas ?? 0;
        this.totalHorasVoluntariado = Number(total) || 0;
        console.log(
          `[AreaPersonal] Total horas cargadas: ${this.totalHorasVoluntariado} (incluye todos los voluntariados activos y finalizados)`
        );
      } catch (err) {
        console.error("Error loading total horas:", err);
        this.totalHorasVoluntariado = 0;
      }
    },
    async recomputeDerivedLists() {
      // Rebuild proximos, activos and completados from perStatus
      const mapToVol = (v: VoluntariadoAPIResponse, source?: string): Voluntariado => ({
        id: v.id,
        nombre: v.nombre,
        descripcion: v.descripcion,
        fecha_inicio_convocatoria: v.fecha_inicio_convocatoria ?? null,
        fecha_fin_convocatoria: v.fecha_fin_convocatoria ?? null,
        fecha_inicio_cursado: v.fecha_inicio_cursado ?? null,
        fecha_fin_cursado: v.fecha_fin_cursado ?? null,
        organizacion_nombre: v.organizacion_nombre || v.organizacion?.nombre || "",
        turnos: Array.isArray(v.turnos) ? v.turnos : [],
        etapa: v.etapa ?? null,
        source: (source as Voluntariado["source"]) || undefined,
      });

      const seenIds = new Set<number>();
      const proximosList: Voluntariado[] = [];
      for (const v of this.perStatus.convocatoria!.items) {
        if (!v || seenIds.has(v.id)) continue;
        seenIds.add(v.id);
        proximosList.push(mapToVol(v, "convocatoria"));
      }
      for (const v of this.perStatus.preparacion!.items) {
        if (!v || seenIds.has(v.id)) continue;
        seenIds.add(v.id);
        proximosList.push(mapToVol(v, "preparacion"));
      }
      for (const v of this.perStatus.upcoming!.items) {
        if (!v || seenIds.has(v.id)) continue;
        seenIds.add(v.id);
        proximosList.push(mapToVol(v, "upcoming"));
      }

      this.proximosVoluntariados = proximosList;
      this.voluntariadosActivos = this.perStatus.active!.items.map((v) => mapToVol(v, "active"));
      this.voluntariadosCompletados = this.perStatus.finished!.items.map((v) =>
        mapToVol(v, "finished")
      );
    },
  },
});
</script>

<!-- shared header CSS imported globally in main.ts -->

<style scoped>
/* Import theme variables */
@import "@/styles/theme.css";

.area-personal-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
}

/* Brand Color Utilities */
.text-brand {
  color: var(--brand-start) !important;
}

.bg-brand {
  background-color: var(--brand-start) !important;
}

.btn-brand {
  background: linear-gradient(90deg, var(--brand-start), var(--brand-end));
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.btn-brand:hover {
  background: linear-gradient(90deg, var(--brand-accent), var(--brand-mid));
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(95, 158, 160, 0.3);
  color: white;
}

.btn-outline-brand {
  border: 2px solid var(--brand-start);
  color: var(--brand-start);
  background: transparent;
  transition: all 0.3s ease;
}

.btn-outline-brand:hover {
  background: linear-gradient(90deg, var(--brand-start), var(--brand-end));
  border-color: var(--brand-start);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(95, 158, 160, 0.2);
}

/* Hero Header Customization */
.page-header.shared-hero {
  --shared-hero-bg: linear-gradient(135deg, var(--brand-start) 0%, var(--brand-end) 100%);
  --shared-hero-height: 280px;
}

/* Loading State */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* Container */
.voluntariados-container {
  position: relative;
}

/* Statistics Section */
.stats-section {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1rem;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  flex-shrink: 0;
}

.stat-icon-wrapper.upcoming {
  background: linear-gradient(135deg, var(--brand-start), var(--brand-mid));
  color: white;
}

.stat-icon-wrapper.active {
  background: linear-gradient(135deg, #198754, #28a745);
  color: white;
}

.stat-icon-wrapper.completed {
  background: linear-gradient(135deg, #0d6efd, #3d8bfd);
  color: white;
}

.stat-icon-wrapper.hours {
  background: linear-gradient(135deg, #fd7e14, #ff922b);
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #212529;
  margin: 0;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin: 0.25rem 0 0 0;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Pipeline Arrow System */
.table-with-arrow {
  display: flex;
  align-items: stretch;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.pipeline-arrow-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 40px;
  padding-top: 2rem;
  pointer-events: none;
  user-select: none;
}

.arrow-line {
  width: 4px;
  flex: 1;
  min-height: 80px;
  border-radius: 2px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.arrow-head {
  margin-top: -2px;
  font-size: 1.75rem;
  animation: bounce 2s ease-in-out infinite;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.15));
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(8px);
  }
}

.section-content {
  flex: 1;
}

/* Section Styles */
.content-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.3s ease;
}

.content-section:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #212529;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 3px solid #e9ecef;
  display: flex;
  align-items: center;
}

.section-title i {
  font-size: 1.5rem;
}

/* Voluntariado Cards */
.card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  transition: transform 0.3s ease;
}

.card-link:hover {
  transform: translateY(-5px);
}

.voluntariado-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.voluntariado-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.card-img-top-wrapper {
  position: relative;
  overflow: hidden;
  height: 200px;
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.card-link:hover .card-img-top {
  transform: scale(1.05);
}

.img-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.3) 100%);
}

.card-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  font-size: 0.75rem;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #212529;
  margin-bottom: 0.5rem;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #6c757d;
}

.turnos-list {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 0.75rem;
}

.turno-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.turno-item:last-child {
  border-bottom: none;
}

.turno-item i {
  margin-right: 0.25rem;
}

/* Icon Wrappers */
.icon-wrapper-finished {
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(25, 135, 84, 0.1);
  border-radius: 0.75rem;
  flex-shrink: 0;
}

.icon-wrapper-active {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(95, 158, 160, 0.1);
  border-radius: 0.75rem;
  flex-shrink: 0;
}

/* Active Voluntariado Cards */
.voluntariado-active-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-left: 4px solid #198754;
  background: white;
}

.card-link:hover .voluntariado-active-card {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
  border-left-width: 6px;
}

.voluntariado-active-card .card-body {
  padding: 1.5rem;
}

.voluntariado-active-card .card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #212529;
  transition: color 0.3s ease;
}

.card-link:hover .voluntariado-active-card .card-title {
  color: #198754;
}

.voluntariado-active-card .card-subtitle {
  font-size: 0.9rem;
}

.icon-wrapper-active {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #198754, #28a745);
  border-radius: 12px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.card-link:hover .icon-wrapper-active {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 4px 12px rgba(25, 135, 84, 0.4);
}

.view-details-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 2px solid #e9ecef;
  color: #198754;
  font-weight: 600;
  transition: all 0.3s ease;
}

.card-link:hover .view-details-footer {
  color: #198754;
  border-top-color: #198754;
}

.view-details-text {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
}

.card-link:hover .view-details-footer i.bi-arrow-right {
  transform: translateX(5px);
}

.view-details-footer i {
  transition: transform 0.3s ease;
}

.voluntariado-info {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 0.75rem;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 0.25rem 0;
}

.info-item i {
  font-size: 1rem;
}

.info-item small {
  color: #495057;
}

/* Completed Items */
.completado-item {
  padding: 1.25rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  transition: all 0.2s ease;
  background: white;
}

.completado-item:hover {
  background: #f8f9fa;
  border-color: #198754;
  transform: translateX(5px);
}

.completado-item h6 {
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.25rem;
}

/* Turno Detail Cards */
.turno-detail-card {
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  transition: all 0.2s ease;
  border-left: 3px solid var(--brand-start);
}

.turno-detail-card:hover {
  background: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.turno-detail-card .card-body {
  padding: 1.25rem;
}

.turno-detail-card .card-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.5rem;
}

.turno-location-section,
.turno-time-section,
.turno-voluntariado-section {
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e9ecef;
}

.turno-voluntariado-section {
  border-bottom: none;
  padding-bottom: 0;
}

.location-details {
  padding-left: 1.75rem;
}

.location-text {
  font-size: 0.95rem;
  color: #495057;
  font-weight: 500;
}

.turno-time-section .card-text {
  font-size: 0.9rem;
  color: #495057;
}

.selected-date-details h5 {
  font-weight: 600;
  color: #212529;
}

/* Alert Customization */
.alert-light {
  border: 2px dashed #dee2e6;
  background: #f8f9fa;
}

/* Responsive Design */
@media (max-width: 768px) {
  .stats-section {
    margin-bottom: 2rem !important;
  }

  .stat-card {
    padding: 1.25rem;
  }

  .stat-icon-wrapper {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }

  .stat-number {
    font-size: 1.75rem;
  }

  .stat-label {
    font-size: 0.8rem;
  }

  .table-with-arrow {
    gap: 1rem;
  }

  .pipeline-arrow-left {
    min-width: 30px;
  }

  .arrow-line {
    width: 3px;
    min-height: 60px;
  }

  .arrow-head {
    font-size: 1.5rem;
  }

  .content-section {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .page-header.shared-hero {
    --shared-hero-height: 220px;
  }

  .hero-title {
    font-size: 2.5rem !important;
  }

  .hero-subtitle {
    font-size: 1rem !important;
  }

  .turno-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .completado-item {
    flex-direction: column;
    align-items: flex-start !important;
  }

  .completado-item .btn {
    margin-top: 1rem !important;
    width: 100%;
  }
}

@media (max-width: 576px) {
  .content-section {
    padding: 1rem;
  }

  .section-title {
    font-size: 1.25rem;
  }
}
</style>
