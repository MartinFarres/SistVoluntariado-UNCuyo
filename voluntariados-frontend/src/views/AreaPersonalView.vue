<template>
  <div class="area-personal-page">
    <AppNavBar />

    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <div v-else-if="error" class="container mt-4">
      <div class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        {{ error }}
      </div>
    </div>

    <div v-else class="container my-5">
      <div class="personal-header mb-5">
        <h1 class="display-5 fw-bold">Mi Área Personal</h1>
        <p class="lead">Gestiona tus voluntariados y sigue tu progreso.</p>
      </div>

      <!-- Próximos Voluntariados -->
      <section class="mb-5 content-section">
        <h2 class="section-title">
          <i class="bi bi-calendar-event me-2"></i>Mis Próximos Voluntariados
        </h2>
        <div v-if="proximosVoluntariados.length > 0" class="row g-4">
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
                  <span class="badge bg-primary card-badge">Próximo</span>
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
                        ><i class="bi bi-calendar-check text-primary"></i>
                        {{ formatDate(turno.fecha) }}</span
                      >
                      <span
                        ><i class="bi bi-clock text-primary"></i>
                        {{ formatTime(turno.hora_inicio) }} - {{ formatTime(turno.hora_fin) }}</span
                      >
                    </li>
                    <li v-if="voluntariado.turnos.length > 2" class="turno-item text-muted small">
                      Y {{ voluntariado.turnos.length - 2 }} más...
                    </li>
                  </ul>
                </div>
              </div>
            </router-link>
          </div>
        </div>
        <div v-else>
          <div class="alert alert-light text-center">
            No estás inscripto a próximos voluntariados.
            <router-link to="/voluntariados">¡Busca uno!</router-link>
          </div>
        </div>
      </section>

      <!-- Calendario -->
      <section class="mb-5 content-section">
        <h2 class="section-title"><i class="bi bi-calendar3 me-2"></i>Mi Calendario</h2>
        <div class="calendar-placeholder">
          <div class="card-body text-center">
            <div class="calendar-header">
              <span>Octubre 2025</span>
            </div>
            <div class="calendar-grid">
              <div class="day-name">Lu</div>
              <div class="day-name">Ma</div>
              <div class="day-name">Mi</div>
              <div class="day-name">Ju</div>
              <div class="day-name">Vi</div>
              <div class="day-name">Sa</div>
              <div class="day-name">Do</div>
              <div class="day empty"></div>
              <div class="day empty"></div>
              <div class="day">1</div>
              <div class="day">2</div>
              <div class="day">3</div>
              <div class="day">4</div>
              <div class="day">5</div>
              <div class="day">6</div>
              <div class="day">7</div>
              <div class="day">8</div>
              <div class="day">9</div>
              <div class="day event">10</div>
              <div class="day">11</div>
              <div class="day">12</div>
              <div class="day">13</div>
              <div class="day">14</div>
              <div class="day">15</div>
              <div class="day">16</div>
              <div class="day">17</div>
              <div class="day event">18</div>
              <div class="day">19</div>
              <div class="day">20</div>
              <div class="day event">21</div>
              <div class="day">22</div>
              <div class="day">23</div>
              <div class="day">24</div>
              <div class="day">25</div>
              <div class="day">26</div>
              <div class="day">27</div>
              <div class="day">28</div>
              <div class="day">29</div>
              <div class="day">30</div>
              <div class="day">31</div>
            </div>
            <p class="text-muted mt-3 small">Componente de Calendario (Próximamente)</p>
          </div>
        </div>
      </section>

      <!-- Voluntariados Completados -->
      <section class="content-section">
        <h2 class="section-title">
          <i class="bi bi-check2-circle me-2"></i>Mis Voluntariados Completados
        </h2>
        <div v-if="voluntariadosCompletados.length > 0">
          <ul class="list-group list-group-flush">
            <li
              v-for="voluntariado in voluntariadosCompletados"
              :key="voluntariado.id"
              class="list-group-item completado-item d-flex justify-content-between align-items-center flex-wrap"
            >
              <div>
                <h6 class="mb-1">{{ voluntariado.nombre }}</h6>
                <small class="text-muted"
                  >{{ voluntariado.organizacion_nombre }} &bull; Finalizado el:
                  {{ formatDate(voluntariado.fecha_fin) }}</small
                >
              </div>
              <button
                class="btn btn-outline-success btn-sm mt-2 mt-md-0"
                @click="descargarCertificado(voluntariado.id)"
              >
                <i class="bi bi-download me-2"></i>Descargar Certificado
              </button>
            </li>
          </ul>
        </div>
        <div v-else>
          <div class="alert alert-light text-center">Aún no has completado voluntariados.</div>
        </div>
      </section>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import {certificadoAPI, personaAPI} from "@/services/api";
import authService from "@/services/authService";

interface Turno {
  id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  lugar?: string;
}
interface Voluntariado {
  id: number;
  nombre: string;
  descripcion: string | { resumen: string; descripcion: string; portada: string | null };
  fecha_inicio: string;
  fecha_fin: string;
  organizacion_nombre: string;
  turnos: Turno[];
  estado: string;
}

export default defineComponent({
  name: "AreaPersonalView",
  components: {
    AppNavBar,
  },
  data() {
    return {
      loading: true,
      error: null as string | null,
      proximosVoluntariados: [] as Voluntariado[],
      voluntariadosCompletados: [] as Voluntariado[],
    };
  },
  async created() {
    await this.loadVoluntariados();
  },
  methods: {
    async loadVoluntariados() {
      this.loading = true;
      this.error = null;
      try {
        const user = authService.getStoredUser();
        if (user && user.persona) {
          const response = await personaAPI.getVoluntariadosVoluntario(user.persona);
          const voluntariados: Voluntariado[] = response.data;

          const hoy = new Date();
          hoy.setHours(0, 0, 0, 0);

          this.proximosVoluntariados = voluntariados.filter((v) => {
            if (!v.fecha_fin) return true;
            const fechaFin = new Date(v.fecha_fin);
            return fechaFin >= hoy;
          });

          this.voluntariadosCompletados = voluntariados.filter((v) => {
            if (!v.fecha_fin) return false;
            const fechaFin = new Date(v.fecha_fin);
            return fechaFin < hoy;
          });
        } else {
          this.error = "No se pudo obtener la información del voluntario.";
        }
      } catch (err: any) {
        console.error("Error loading voluntariados:", err);
        this.error = err.response?.data?.detail || "Error al cargar los voluntariados.";
      } finally {
        this.loading = false;
      }
    },
    getVoluntariadoDescription(voluntariado: Voluntariado): string {
      if (!voluntariado || !voluntariado.descripcion) {
        return "Sin descripción.";
      }
      let desc =
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
    formatDate(dateString: string): string {
      if (!dateString) return "Fecha no definida";
      const options: Intl.DateTimeFormatOptions = {
        year: "numeric",
        month: "short",
        day: "numeric",
      };
      return new Date(dateString).toLocaleDateString("es-AR", options);
    },
    formatTime(timeString: string): string {
      if (!timeString) return "";
      return timeString.substring(0, 5); // HH:MM
    },
    async descargarCertificado(voluntariadoId: number) {
      try {
        const response = await certificadoAPI.generarPorVoluntariado(voluntariadoId)
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `certificado_voluntariado_${voluntariadoId}.pdf`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
      } catch (error: any) {
        alert(error.response?.data?.detail || 'No se pudo generar el certificado.')
      }
    }

  },
});
</script>

<style scoped src="@/styles/areaPersonal.css"></style>
