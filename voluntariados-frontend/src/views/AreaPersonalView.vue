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
      <h1 class="mb-4">Área Personal de Voluntario</h1>

      <!-- Carrusel de Próximos Voluntariados -->
      <section class="mb-5">
        <h2>Mis Próximos Voluntariados</h2>
        <div
          v-if="proximosVoluntariados.length > 0"
          id="proximosVoluntariadosCarousel"
          class="carousel slide"
          data-bs-ride="carousel"
        >
          <div class="carousel-inner">
            <div
              v-for="(chunk, index) in chunkedProximosVoluntariados"
              :key="index"
              class="carousel-item"
              :class="{ active: index === 0 }"
            >
              <div class="row">
                <div
                  class="col-12 col-md-4 mb-3"
                  v-for="voluntariado in chunk"
                  :key="voluntariado.id"
                >
                  <router-link :to="`/voluntariados/${voluntariado.id}`" class="card-link">
                    <div class="card voluntariado-card-carousel h-100">
                      <img
                        :src="getVoluntariadoImageUrl(voluntariado)"
                        class="card-img-top"
                        alt="Imagen del voluntariado"
                      />
                      <div class="card-body d-flex flex-column">
                        <h5 class="card-title">{{ voluntariado.nombre }}</h5>
                        <p class="card-text">
                          <small class="text-muted">{{ voluntariado.organizacion_nombre }}</small>
                        </p>
                        <p class="card-text flex-grow-1">
                          {{ getVoluntariadoDescription(voluntariado) }}
                        </p>
                        <ul class="list-unstyled mt-auto mb-0 turnos-list">
                          <li
                            v-for="turno in voluntariado.turnos"
                            :key="turno.id"
                            class="turno-item"
                          >
                            <div>
                              <i class="bi bi-calendar-check"></i>
                              {{ formatDate(turno.fecha) }} - {{ formatTime(turno.hora_inicio) }} a
                              {{ formatTime(turno.hora_fin) }}
                            </div>
                            <div v-if="turno.lugar" class="turno-location" :title="turno.lugar">
                              <i class="bi bi-geo-alt-fill"></i>
                              {{ turno.lugar }}
                            </div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          <button
            class="carousel-control-prev"
            type="button"
            data-bs-target="#proximosVoluntariadosCarousel"
            data-bs-slide="prev"
          >
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button
            class="carousel-control-next"
            type="button"
            data-bs-target="#proximosVoluntariadosCarousel"
            data-bs-slide="next"
          >
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
        <div v-else>
          <p>No estás inscripto a próximos voluntariados.</p>
        </div>
      </section>

      <!-- Calendario -->
      <section class="mb-5">
        <h2>Mi Calendario</h2>
        <div class="calendar-container">
          <!-- Aquí iría un componente de calendario. Por ahora un placeholder -->
          <p class="text-center p-5 bg-light rounded">Componente de Calendario Próximamente</p>
        </div>
      </section>

      <!-- Voluntariados Completados -->
      <section>
        <h2>Mis Voluntariados Completados</h2>
        <div v-if="voluntariadosCompletados.length > 0">
          <div
            v-for="voluntariado in voluntariadosCompletados"
            :key="voluntariado.id"
            class="card mb-3 completado-card"
          >
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-8">
                  <h5 class="card-title">{{ voluntariado.nombre }}</h5>
                  <p class="card-text mb-1">
                    <small class="text-muted"
                      >Finalizado el: {{ formatDate(voluntariado.fecha_fin) }}</small
                    >
                  </p>
                  <p class="card-text">
                    <small>{{ voluntariado.organizacion_nombre }}</small>
                  </p>
                </div>
                <div class="col-md-4 text-md-end">
                  <button class="btn btn-primary" @click="descargarCertificado(voluntariado.id)">
                    <i class="bi bi-download me-2"></i>Descargar Certificado
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <p>Aún no has completado voluntariados.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import { personaAPI } from "@/services/api";
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
      isMobile: window.innerWidth < 768,
    };
  },
  computed: {
    chunkedProximosVoluntariados() {
      const chunkSize = this.isMobile ? 1 : 3;
      const chunks = [];
      const voluntariados = this.proximosVoluntariados;
      if (!voluntariados) return [];
      for (let i = 0; i < voluntariados.length; i += chunkSize) {
        chunks.push(voluntariados.slice(i, i + chunkSize));
      }
      return chunks;
    },
  },
  async created() {
    window.addEventListener("resize", this.handleResize);
    await this.loadVoluntariados();
  },
  unmounted() {
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    handleResize() {
      this.isMobile = window.innerWidth < 768;
    },
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
            if (!v.fecha_fin) return true; // Si no tiene fecha de fin, lo consideramos próximo
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
      if (typeof voluntariado.descripcion === "object" && voluntariado.descripcion !== null) {
        return (
          voluntariado.descripcion.resumen ||
          voluntariado.descripcion.descripcion ||
          "Sin descripción."
        );
      }
      return voluntariado.descripcion;
    },
    getVoluntariadoImageUrl(voluntariado: Voluntariado): string {
      const defaultImg = "https://placehold.co/400x250/8B0000/white?text=Voluntariado";
      if (typeof voluntariado.descripcion === "object" && voluntariado.descripcion !== null) {
        return voluntariado.descripcion.portada || defaultImg;
      }
      return defaultImg;
    },
    formatDate(dateString: string): string {
      if (!dateString) return "Fecha no definida";
      const options: Intl.DateTimeFormatOptions = {
        year: "numeric",
        month: "long",
        day: "numeric",
      };
      return new Date(dateString).toLocaleDateString("es-AR", options);
    },
    formatTime(timeString: string): string {
      if (!timeString) return "";
      return timeString.substring(0, 5); // HH:MM
    },
    async descargarCertificado(voluntariadoId: number) {
      alert(
        `Funcionalidad para descargar certificado del voluntariado ID: ${voluntariadoId} no implementada aún.`
      );
      // try {
      //     const response = await certificadoAPI.download(certificadoId);
      //     const url = window.URL.createObjectURL(new Blob([response.data]));
      //     const link = document.createElement('a');
      //     link.href = url;
      //     link.setAttribute('download', `certificado-${certificadoId}.pdf`);
      //     document.body.appendChild(link);
      //     link.click();
      //     link.remove();
      // } catch (error) {
      //     console.error("Error al descargar el certificado:", error);
      //     this.error = "No se pudo descargar el certificado.";
      // }
    },
  },
});
</script>

<style scoped src="@/styles/areaPersonal.css"></style>
