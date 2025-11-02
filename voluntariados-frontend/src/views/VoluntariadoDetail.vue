<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import VoluntariadoCard from "@/components/landing/VoluntariadoCard.vue";
import CTASection from "@/components/landing/CTASection.vue";
import JoinConfirmationModal from "@/components/landing/JoinConfirmationModal.vue";
import CancelConfirmationModal from "@/components/landing/CancelConfirmationModal.vue";
import TurnosCalendar from "@/components/TurnosCalendar.vue";
import GoogleMapViewer from "@/components/GoogleMapViewer.vue";
import { voluntariadoAPI, turnoAPI, organizacionAPI } from "@/services/api";
import authService from "@/services/authService";
import apiClient from "@/services/api";
import { parseLocalDate, formatDateShort, formatDateLong, getWeekdayName } from "@/utils/dateUtils";
import { getGoogleMapsDirectionsUrl, formatCoordinates } from "@/utils/mapsUtils";

interface Turno {
  id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  cupo: number;
  lugar?: string;
  voluntariado?: number | { id: number } | any;
  inscripciones_count?: number;
  is_full?: boolean;
}

interface Voluntariado {
  id: number;
  nombre: string;
  descripcion?: any;
  // Computed from turnos (if provided by some endpoints)
  fecha_inicio?: string;
  fecha_fin?: string;
  // Explicit convocatoria and cursado date ranges from backend serializer
  fecha_inicio_convocatoria?: string;
  fecha_fin_convocatoria?: string;
  fecha_inicio_cursado?: string;
  fecha_fin_cursado?: string;
  etapa?: string;
  turno?: number;
  requiere_convocatoria?: boolean;
  // Can arrive as nested object from API serializer or an id depending on endpoint
  organizacion?: number | Record<string, any> | null;
  // Location fields
  latitud?: number | null;
  longitud?: number | null;
  place_id?: string | null;
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
    TurnosCalendar,
    GoogleMapViewer,
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

      showAllTurnos: false,
      showAllOrgVoluntariados: false,

      isAuthenticated: false,
      userRole: null as string | null,

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

      // Convocatoria state
      userConvocatoriaInscripcion: null as any | null,
      hasAcceptedConvocatoria: false,

      // Convocatoria modal state
      showCancelConvocatoriaModal: false,
      cancelConvocatoriaLoading: false,
      showConvocatoriaSuccess: false,

      // UI state
      isHovering: null as number | "main" | null,

      // Calendar state
      selectedCalendarDate: null as string | null,
    };
  },

  computed: {
    displayedTurnos(): Turno[] {
      let turnos = this.allTurnos;

      // Filter by selected date if calendar date is selected
      if (this.selectedCalendarDate) {
        turnos = turnos.filter((t) => t.fecha === this.selectedCalendarDate);
      }

      return this.showAllTurnos ? turnos : turnos.slice(0, 2);
    },
    canJoinTurnos(): boolean {
      // Only VOL users can join turnos
      if (!this.isVoluntarioUser) {
        return false;
      }

      // If voluntariado doesn't require convocatoria, users can join directly during Activo stage
      if (this.voluntariadoData?.requiere_convocatoria === false) {
        return this.voluntariadoData?.etapa === "Activo";
      }

      // For voluntariados that require convocatoria:
      // Cannot join turnos during Convocatoria stage
      if (this.voluntariadoData?.etapa === "Convocatoria") {
        return false;
      }

      // During Activo stage, must have accepted convocatoria inscription
      if (this.voluntariadoData?.etapa === "Activo") {
        return this.hasAcceptedConvocatoria;
      }

      // For other stages (Preparación, etc.), default to false
      return false;
    },
    turnoBlockedReason(): string | null {
      if (!this.isAuthenticated) {
        return null; // Will show "Registrarse" button
      }

      // Block ADMIN and DELEGADO roles
      if (!this.isVoluntarioUser) {
        return "Solo los usuarios con rol de Voluntario pueden inscribirse a turnos.";
      }

      // If voluntariado doesn't require convocatoria, no blocking during Activo stage
      if (this.voluntariadoData?.requiere_convocatoria === false) {
        if (this.voluntariadoData?.etapa === "Activo") {
          return null; // Can join freely
        }
        return "Los turnos estarán disponibles cuando el voluntariado esté activo.";
      }

      // For voluntariados that require convocatoria:
      if (this.voluntariadoData?.etapa === "Convocatoria") {
        // Check if user is already enrolled in convocatoria
        if (this.isEnrolledInConvocatoria) {
          return "Ya estás inscripto en la convocatoria. Los turnos estarán disponibles cuando el voluntariado esté activo. Por favor, espera a que finalice la etapa de convocatoria.";
        }
        return "Los turnos estarán disponibles cuando el voluntariado esté activo. Actualmente en etapa de convocatoria. Puedes inscribirte a la convocatoria.";
      }

      if (this.voluntariadoData?.etapa === "Activo" && !this.hasAcceptedConvocatoria) {
        return "Debes tener una inscripción aceptada en la convocatoria para unirte a turnos";
      }

      return null;
    },
    isEnrolledInConvocatoria(): boolean {
      if (!this.userConvocatoriaInscripcion) {
        return false;
      }
      const estado = (this.userConvocatoriaInscripcion.estado ?? "")
        .toString()
        .toUpperCase()
        .trim();
      // Consider enrolled if state is not CANCELADO (CAN) or empty
      // Backend uses abbreviated codes: INS, CAN, ACE, REJ
      const isEnrolled = estado !== "CANCELADO" && estado !== "CAN" && estado !== "";

      return isEnrolled;
    },
    convocatoriaButtonText(): string {
      if (!this.isEnrolledInConvocatoria) {
        return "Inscribirse a Convocatoria";
      }
      const estado = (this.userConvocatoriaInscripcion?.estado ?? "")
        .toString()
        .toUpperCase()
        .trim();
      // Backend uses abbreviated codes: INS, CAN, ACE, REJ
      if (estado === "ACEPTADO" || estado === "ACE") {
        return "Cancelar Inscripción (Aceptado)";
      }
      if (estado === "RECHAZADO" || estado === "REJ") {
        return "Cancelar Inscripción (Rechazado)";
      }
      if (estado === "INSCRITO" || estado === "INS") {
        return "Cancelar Inscripción";
      }
      return "Cancelar Inscripción";
    },
    displayedOrgVoluntariados(): any[] {
      return this.showAllOrgVoluntariados
        ? this.allOrgVoluntariados
        : this.allOrgVoluntariados.slice(0, 2);
    },
    turnosSubtitle(): string {
      if (!this.voluntariadoData?.etapa) {
        return "Seleccioná entre los turnos disponibles para participar en este voluntariado.";
      }

      // If voluntariado doesn't require convocatoria, simplify the message
      if (this.voluntariadoData.requiere_convocatoria === false) {
        if (this.voluntariadoData.etapa === "Activo") {
          return "Seleccioná entre los turnos disponibles para participar en este voluntariado.";
        }
        return "Los turnos estarán disponibles cuando el voluntariado esté activo.";
      }

      // For voluntariados that require convocatoria:
      if (this.voluntariadoData.etapa === "Convocatoria") {
        return "Los turnos aún no están habilitados para inscripción. Podés ver los horarios disponibles mientras esperás que finalice la convocatoria.";
      }

      if (this.voluntariadoData.etapa === "Activo") {
        if (this.hasAcceptedConvocatoria) {
          return "¡Tu inscripción fue aceptada! Seleccioná los turnos en los que deseas participar.";
        } else {
          return "Los turnos ya no están disponibles para inscripción. Solo los voluntarios con inscripción aceptada pueden unirse.";
        }
      }

      if (this.voluntariadoData.etapa === "Preparación") {
        return "Los turnos estarán disponibles cuando el voluntariado esté activo.";
      }

      return "Seleccioná entre los turnos disponibles para participar en este voluntariado.";
    },
    hasValidLocation(): boolean {
      return !!(
        this.voluntariadoData?.latitud &&
        this.voluntariadoData?.longitud &&
        !isNaN(this.voluntariadoData.latitud) &&
        !isNaN(this.voluntariadoData.longitud)
      );
    },
    isVoluntarioUser(): boolean {
      return (this.userRole || "").toString().toUpperCase() === "VOL";
    },
  },

  async created() {
    this.voluntariadoId = parseInt(this.$route.params.id as string);
    this.isAuthenticated = authService.isAuthenticated();
    // If authenticated, attempt to load current user to determine role
    if (this.isAuthenticated) {
      try {
        const user = await authService.getCurrentUser();
        this.userRole = user?.role || null;
      } catch (err) {
        console.debug("Could not load current user role:", err);
        this.userRole = null;
      }
    }

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

        const [
          turnosRes,
          organizacionesRes,
          allVoluntariadosRes,
          inscripcionesRes,
          convocatoriaRes,
        ] = await Promise.all([
          voluntariadoAPI.getTurnos(this.voluntariadoId), // BUGFIX: Fetch only shifts for this voluntariado
          organizacionAPI.getAll(),
          voluntariadoAPI.getAllActive(),
          this.isAuthenticated
            ? apiClient.get("/voluntariado/inscripciones/")
            : Promise.resolve({ data: [] }),
          this.isAuthenticated
            ? apiClient.get("/voluntariado/inscripciones-convocatoria/")
            : Promise.resolve({ data: [] }),
        ]);

        // guardar inscripciones primero
        this.userInscripciones = inscripcionesRes.data || [];

        // Check convocatoria inscription status
        this.checkConvocatoriaStatus(convocatoriaRes.data || []);

        // encontrar organización (si existe)
        if (volData.organizacion) {
          if (typeof volData.organizacion === "object") {
            this.organizacion = volData.organizacion as any;
          } else {
            this.organizacion =
              organizacionesRes.data.find((o: any) => o.id === volData.organizacion) || null;
          }
          if (this.organizacion) {
            await this.loadOrganizationVoluntariados(
              (this.organizacion as any).id,
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
      if (!this.isAuthenticated || !this.userInscripciones || this.userRole != "VOL") {
        this.isUserEnrolled = false;
        this.enrolledTurnoIds = [];
        return;
      }

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

      // Mantener isUserEnrolled por compatibilidad (si está inscrito en algún turno del voluntariado)
      const voluntarioTurnoIdsInThisVol = this.enrolledTurnoIds.filter((tid) =>
        this.allTurnos.some((t) => Number(t.id) === Number(tid))
      );
      this.isUserEnrolled = voluntarioTurnoIdsInThisVol.length > 0;
    },

    checkConvocatoriaStatus(convocatoriaInscripciones: any[]) {
      // Find inscription for this specific voluntariado
      const inscription = convocatoriaInscripciones.find((insc: any) => {
        const volId =
          typeof insc.voluntariado === "object" ? insc.voluntariado?.id : insc.voluntariado;
        return Number(volId) === Number(this.voluntariadoId);
      });

      this.userConvocatoriaInscripcion = inscription || null;

      // Check if user has an accepted convocatoria inscription
      if (inscription) {
        const estado = (inscription.estado ?? "").toString().toUpperCase().trim();
        this.hasAcceptedConvocatoria = estado === "ACE" || estado === "ACEPTADO";
      } else {
        this.hasAcceptedConvocatoria = false;
        console.debug("No convocatoria inscription found for voluntariado:", this.voluntariadoId);
      }

      // eslint-disable-next-line no-console
      console.debug("Convocatoria status:", {
        inscription,
        estado: inscription?.estado,
        hasAcceptedConvocatoria: this.hasAcceptedConvocatoria,
        isEnrolled: this.isEnrolledInConvocatoria,
      });
    },

    async loadOrganizationVoluntariados(orgId: number, allVoluntariados: Voluntariado[]) {
      this.allOrgVoluntariados = allVoluntariados
        .filter((v) => v.organizacion === orgId && v.id !== this.voluntariadoId)
        .slice(0, 4)
        .map((v) => {
          let resumen = "";
          if (v.descripcion && typeof v.descripcion === "object" && v.descripcion.resumen) {
            resumen = v.descripcion.resumen;
          } else if (
            v.descripcion &&
            typeof v.descripcion === "object" &&
            v.descripcion.descripcion
          ) {
            resumen = v.descripcion.descripcion;
          } else if (typeof v.descripcion === "string") {
            resumen = v.descripcion;
          }
          return {
            id: v.id,
            title: v.nombre,
            description: resumen || "Sin descripción",
            isFree: true,
            tags: ["Tag 1", "Tag 2", "Tag 3"],
          };
        });
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
      if (voluntariado.etapa) tags.push(voluntariado.etapa as string);
      if (voluntariado.fecha_inicio) tags.push("Próximamente");
      tags.push("Tag " + ((voluntariado.id % 5) + 1));
      return tags.slice(0, 5);
    },

    // Información de etapa: etiqueta, descripción y estilo visual
    getStageInfo(etapa?: string): { label: string; description: string; badgeClass: string } {
      const stage = (etapa || "").toString();
      switch (stage) {
        case "Proximamente":
          return {
            label: "Próximamente",
            description: "Antes del inicio de la convocatoria.",
            badgeClass: "bg-secondary",
          };
        case "Convocatoria":
          return {
            label: "Convocatoria",
            description: "Período de postulación abierto para inscribirse al voluntariado.",
            badgeClass: "bg-primary",
          };
        case "Preparación":
          return {
            label: "Preparación",
            description: "Convocatoria cerrada. Organizándose el cursado y actividades.",
            badgeClass: "bg-warning text-dark",
          };
        case "Activo":
          return {
            label: "Activo",
            description: "El voluntariado está en curso y se realizan actividades.",
            badgeClass: "bg-success",
          };
        case "Finalizado":
          return {
            label: "Finalizado",
            description: "El voluntariado ya finalizó.",
            badgeClass: "bg-dark",
          };
        default:
          return {
            label: stage || "Sin etapa",
            description: "Etapa no disponible.",
            badgeClass: "bg-secondary",
          };
      }
    },

    generateSchedule(voluntariado: Voluntariado): Array<{ day: string; time: string }> {
      const schedule: Array<{ day: string; time: string }> = [];

      // Rango de Convocatoria
      if (voluntariado.fecha_inicio_convocatoria && voluntariado.fecha_fin_convocatoria) {
        schedule.push({
          day: "Convocatoria",
          time: `${this.formatDate(voluntariado.fecha_inicio_convocatoria)} - ${this.formatDate(
            voluntariado.fecha_fin_convocatoria
          )}`,
        });
      }

      // Rango de Cursado
      if (voluntariado.fecha_inicio_cursado && voluntariado.fecha_fin_cursado) {
        schedule.push({
          day: "Acción",
          time: `${this.formatDate(voluntariado.fecha_inicio_cursado)} - ${this.formatDate(
            voluntariado.fecha_fin_cursado
          )}`,
        });
      }

      return schedule;
    },

    formatDate(dateString: string): string {
      return formatDateShort(dateString);
    },

    formatTime(timeString: string): string {
      return timeString.substring(0, 5); // HH:MM
    },

    formatTurnoDate(turno: Turno): string {
      return getWeekdayName(turno.fecha as unknown as string);
    },

    formatTurnoFullDate(turno: Turno): string {
      return formatDateShort(turno.fecha as unknown as string);
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

    async handleConvocatoriaAction() {
      if (!this.isAuthenticated) {
        this.$router.push("/register");
        return;
      }

      if (this.isEnrolledInConvocatoria) {
        // Show cancel confirmation modal
        this.showCancelConvocatoriaModal = true;
      } else {
        // Join convocatoria directly
        await this.joinConvocatoria();
      }
    },

    async joinConvocatoria() {
      try {
        await apiClient.post("/voluntariado/inscripciones-convocatoria/inscribirse/", {
          voluntariado_id: this.voluntariadoId,
        });

        // Show success modal (stays open until user closes it)
        this.showConvocatoriaSuccess = true;
      } catch (err: any) {
        console.error("Error joining convocatoria:", err);
        this.error = err.response?.data?.detail || "Error al inscribirse en la convocatoria.";
        alert(this.error);
      }
    },

    handleConvocatoriaSuccessClose() {
      this.showConvocatoriaSuccess = false;
      // Reload data after user closes the success modal
      this.loadVoluntariado();
    },

    handleCancelConvocatoriaModalClose() {
      this.showCancelConvocatoriaModal = false;
      this.cancelConvocatoriaLoading = false;
    },

    async handleCancelConvocatoriaConfirm() {
      if (!this.userConvocatoriaInscripcion?.id) return;

      this.cancelConvocatoriaLoading = true;
      this.error = null;

      try {
        await apiClient.post(
          `/voluntariado/inscripciones-convocatoria/${this.userConvocatoriaInscripcion.id}/cancelar/`
        );
        this.handleCancelConvocatoriaModalClose();
        await this.loadVoluntariado();
      } catch (err: any) {
        console.error("Error cancelling convocatoria:", err);
        this.error =
          err.response?.data?.detail || "Error al cancelar la inscripción a la convocatoria.";
        alert(this.error);
        this.handleCancelConvocatoriaModalClose();
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

    handleDateSelected(dateString: string | null) {
      if (this.selectedCalendarDate === dateString) {
        // Toggle off if clicking the same date
        this.selectedCalendarDate = null;
      } else {
        this.selectedCalendarDate = dateString;
        // Scroll to turnos list
        this.$nextTick(() => {
          const turnosList = document.getElementById("turnos-list");
          if (turnosList) {
            turnosList.scrollIntoView({ behavior: "smooth", block: "start" });
          } else {
            // Fallback to section if header doesn't exist yet
            const turnosSection = document.querySelector(".org-voluntariados-section");
            if (turnosSection) {
              turnosSection.scrollIntoView({ behavior: "smooth", block: "start" });
            }
          }
        });
      }
    },

    formatSelectedDate(dateString: string): string {
      return formatDateLong(dateString);
    },

    // Maps utility functions
    formatCoordinates(lat: number, lng: number): string {
      return formatCoordinates(lat, lng);
    },

    getGoogleMapsDirectionsUrl(lat: number, lng: number, label?: string): string {
      return getGoogleMapsDirectionsUrl(lat, lng, label);
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
      <section
        class="voluntariado-hero"
        :style="
          voluntariadoData?.descripcion?.portada
            ? {
                backgroundImage: `url(${voluntariadoData.descripcion.portada})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
              }
            : {}
        "
      >
        <div class="hero-overlay"></div>
        <div class="container">
          <div class="row">
            <div class="col-lg-10 mx-auto">
              <!-- Main Card -->
              <div class="voluntariado-card">
                <div class="row">
                  <!-- Image -->
                  <div class="col-md-4">
                    <div class="voluntariado-image">
                      <img
                        :src="
                          voluntariadoData.descripcion?.logo ||
                          voluntariadoData.descripcion?.portada ||
                          'https://via.placeholder.com/600x400'
                        "
                        :alt="voluntariadoData.nombre"
                        style="max-width: 100%; height: auto; object-fit: contain"
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

                      <!-- Organización -->
                      <div
                        class="mb-2 text-muted d-flex align-items-center gap-2"
                        v-if="organizacion?.nombre"
                      >
                        <i class="bi bi-building"></i>
                        <button
                          class="btn btn-link p-0 text-decoration-none"
                          @click="viewOrganization"
                        >
                          {{ organizacion.nombre }}
                        </button>
                      </div>

                      <!-- Etapa del Voluntariado -->
                      <div class="stage-info mb-3" v-if="voluntariadoData?.etapa">
                        <span
                          class="badge"
                          :class="getStageInfo(voluntariadoData?.etapa).badgeClass"
                        >
                          {{ getStageInfo(voluntariadoData?.etapa).label }}
                        </span>
                        <small class="text-muted ms-2">
                          {{ getStageInfo(voluntariadoData?.etapa).description }}
                        </small>
                      </div>

                      <!-- Convocatoria Button (shown during Convocatoria stage, or during Activo if user is enrolled) -->
                      <!-- Only show if voluntariado requires convocatoria -->
                      <div
                        v-if="
                          voluntariadoData &&
                          voluntariadoData.requiere_convocatoria !== false &&
                          (voluntariadoData.etapa === 'Convocatoria' ||
                            (voluntariadoData.etapa === 'Activo' && isEnrolledInConvocatoria))
                        "
                        class="mb-3"
                      >
                        <template v-if="isVoluntarioUser">
                          <button
                            class="btn"
                            :class="isEnrolledInConvocatoria ? 'btn-danger' : 'btn-primary'"
                            :disabled="!isAuthenticated"
                            @click="handleConvocatoriaAction"
                          >
                            <i
                              class="bi me-2"
                              :class="isEnrolledInConvocatoria ? 'bi-x-circle' : 'bi-pencil-square'"
                            ></i>
                            {{ convocatoriaButtonText }}
                          </button>
                        </template>

                        <template v-else-if="!isAuthenticated">
                          <button class="btn btn-outline-secondary" disabled>
                            <i class="bi bi-person-plus me-2"></i>
                            Registrarse
                          </button>
                        </template>
                        <!-- Authenticated non-VOL users won't see convocatoria actions -->
                      </div>

                      <!-- Descripción breve dentro de la tarjeta -->
                      <div class="description-preview mb-3">
                        <p
                          v-for="(paragraph, index) in getDescriptionText(
                            voluntariadoData.descripcion
                          )
                            .split('\n\n')
                            .slice(0, 2)"
                          :key="index"
                          class="mb-2"
                        >
                          {{ paragraph }}
                        </p>
                      </div>

                      <!-- Rango de fechas de Convocatoria y Cursado -->
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

      <!-- Location Section -->
      <section class="location-section py-5" v-if="hasValidLocation">
        <div class="container">
          <div class="section-header mb-4">
            <h2 class="section-title">
              <i class="bi bi-geo-alt-fill me-2"></i>
              Ubicación
            </h2>
          </div>

          <div class="row">
            <div class="col-lg-10 mx-auto">
              <div class="location-card">
                <GoogleMapViewer
                  :latitud="voluntariadoData.latitud"
                  :longitud="voluntariadoData.longitud"
                  :place_id="voluntariadoData.place_id"
                  :title="voluntariadoData.nombre"
                  :zoom="16"
                />

                <!-- Location Info -->
                <div class="location-info mt-3 text-center">
                  <div class="row g-3">
                    <div class="col-md-4">
                      <div class="location-detail">
                        <i class="bi bi-geo-alt text-primary mb-2 d-block fs-4"></i>
                        <h6 class="mb-1">Coordenadas</h6>
                        <small class="text-muted">
                          {{
                            formatCoordinates(voluntariadoData.latitud!, voluntariadoData.longitud!)
                          }}
                        </small>
                      </div>
                    </div>
                    <div class="col-md-4" v-if="voluntariadoData.place_id">
                      <div class="location-detail">
                        <i class="bi bi-pin-map text-success mb-2 d-block fs-4"></i>
                        <h6 class="mb-1">Lugar verificado</h6>
                        <small class="text-muted">Ubicación confirmada en Google Maps</small>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="location-detail">
                        <a
                          :href="getGoogleMapsDirectionsUrl(voluntariadoData.latitud!, voluntariadoData.longitud!)"
                          target="_blank"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="bi bi-signpost-2 me-1"></i>
                          Cómo llegar
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Turnos Section -->
      <section
        class="org-voluntariados-section py-5 bg-light"
        id="turnos-section"
        v-if="allTurnos.length > 0"
      >
        <div class="container">
          <div class="section-header mb-4">
            <h2 class="section-title">Turnos Disponibles</h2>
            <p class="section-subtitle">
              {{ turnosSubtitle }}
            </p>
          </div>

          <!-- Calendar View -->
          <div class="row mb-4">
            <div class="col-lg-8 mx-auto">
              <TurnosCalendar
                :turnos="allTurnos"
                :selected-date="selectedCalendarDate"
                @date-selected="handleDateSelected"
              />
              <div v-if="selectedCalendarDate" class="text-center mt-3">
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="selectedCalendarDate = null"
                >
                  <i class="bi bi-x-circle me-1"></i>
                  Mostrar todos los turnos
                </button>
              </div>
            </div>
          </div>

          <!-- Selected Date Header -->
          <div v-if="selectedCalendarDate" class="selected-date-header mb-4" id="turnos-list">
            <h3 class="text-center">
              <i class="bi bi-calendar-check me-2"></i>
              Turnos disponibles para el día: {{ formatSelectedDate(selectedCalendarDate) }}
            </h3>
          </div>

          <!-- Blocked Turnos Alert -->
          <div
            v-if="turnoBlockedReason && isAuthenticated"
            class="alert alert-warning mb-4"
            role="alert"
          >
            <div class="d-flex align-items-center">
              <i class="bi bi-exclamation-triangle-fill me-3" style="font-size: 1.5rem"></i>
              <div>
                <strong>Inscripción a turnos no disponible</strong>
                <p class="mb-0 mt-1">{{ turnoBlockedReason }}</p>
              </div>
            </div>
          </div>

          <!-- Turnos Grid -->
          <div class="row g-3 mb-4">
            <div v-for="turno in displayedTurnos" :key="turno.id" class="col-md-6 col-lg-4">
              <div
                class="turno-card"
                :class="{
                  'turno-full': turno.is_full,
                  'turno-enrolled': enrolledTurnoIds.includes(Number(turno.id)),
                }"
              >
                <!-- Card Header with Day and Status Badge -->
                <div class="turno-header">
                  <div class="turno-day-section">
                    <div class="turno-day">{{ formatTurnoDate(turno) }}</div>
                    <div class="turno-date-full">{{ formatTurnoFullDate(turno) }}</div>
                  </div>

                  <!-- Status Badge -->
                  <div class="turno-status-badge">
                    <span
                      v-if="enrolledTurnoIds.includes(Number(turno.id))"
                      class="badge bg-success"
                    >
                      <i class="bi bi-check-circle-fill"></i> Inscrito
                    </span>
                    <span v-else-if="turno.is_full" class="badge bg-secondary">
                      <i class="bi bi-dash-circle"></i> Completo
                    </span>
                    <span v-else-if="!canJoinTurnos" class="badge bg-warning text-dark">
                      <i class="bi bi-lock-fill"></i> Bloqueado
                    </span>
                    <span v-else class="badge bg-primary">
                      <i class="bi bi-calendar-check"></i> Disponible
                    </span>
                  </div>
                </div>

                <!-- Card Body with Details -->
                <div class="turno-body">
                  <div class="turno-info-row">
                    <i class="bi bi-clock-fill text-primary"></i>
                    <span
                      >{{ formatTime(turno.hora_inicio) }} - {{ formatTime(turno.hora_fin) }}</span
                    >
                  </div>

                  <div class="turno-info-row">
                    <i class="bi bi-people-fill text-success"></i>
                    <span v-if="turno.inscripciones_count !== undefined">
                      <strong>{{ turno.inscripciones_count }}/{{ turno.cupo }}</strong> inscriptos
                    </span>
                    <span v-else>
                      <strong>{{ turno.cupo }}</strong> cupos disponibles
                    </span>
                  </div>
                </div>

                <!-- Card Footer with Action Button -->
                <div class="turno-footer">
                  <!-- Already enrolled -->
                  <button
                    v-if="enrolledTurnoIds.includes(Number(turno.id))"
                    class="btn btn-sm w-100"
                    :class="isHovering === turno.id ? 'btn-danger' : 'btn-outline-success'"
                    @mouseenter="isHovering = turno.id"
                    @mouseleave="isHovering = null"
                    @click="promptCancelEnrollment(turno.id)"
                  >
                    <span v-if="isHovering === turno.id">
                      <i class="bi bi-x-circle"></i> Cancelar Inscripción
                    </span>
                    <span v-else> <i class="bi bi-check-circle"></i> Inscrito en este turno </span>
                  </button>

                  <!-- Turno is full -->
                  <button v-else-if="turno.is_full" class="btn btn-sm btn-secondary w-100" disabled>
                    <i class="bi bi-dash-circle"></i> Turno Completo
                  </button>

                  <!-- Cannot join - stage restriction or no convocatoria acceptance -->
                  <!-- If user not authenticated show blocked register button -->
                  <button
                    v-else-if="!isAuthenticated"
                    class="btn btn-sm btn-outline-secondary w-100"
                    disabled
                  >
                    <i class="bi bi-person-plus"></i> Registrarse
                  </button>

                  <!-- Authenticated but not a Voluntario: do not allow joining -->
                  <button
                    v-else-if="!isVoluntarioUser"
                    class="btn btn-sm btn-warning w-100"
                    disabled
                  >
                    <i class="bi bi-lock"></i> No disponible
                  </button>

                  <!-- Cannot join because of stage/convocatoria rules -->
                  <button
                    v-else-if="!canJoinTurnos"
                    class="btn btn-sm btn-warning w-100"
                    disabled
                    :title="turnoBlockedReason || ''"
                  >
                    <i class="bi bi-lock"></i> No Disponible
                  </button>

                  <!-- Available to join for authenticated VOL users -->
                  <button
                    v-else
                    class="btn btn-sm btn-primary w-100"
                    @click="enrollInTurno(turno.id)"
                  >
                    <i class="bi bi-plus-circle"></i>
                    Inscribirse
                  </button>
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

      <!-- CTA Section -->
      <CTASection
        title="¡Inscríbete hoy y marca la diferencia!"
        primary-text="Registrarme como voluntario"
        primary-link="/signup"
        secondary-text="Soy Organización, quiero colaborar"
        secondary-link="/about#contact"
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

      <!-- Convocatoria Cancel Confirmation Modal -->
      <CancelConfirmationModal
        :show="showCancelConvocatoriaModal"
        :voluntariado-title="voluntariadoData.nombre"
        :organization-name="organizacion?.nombre || 'Organización'"
        :loading="cancelConvocatoriaLoading"
        @confirm="handleCancelConvocatoriaConfirm"
        @cancel="handleCancelConvocatoriaModalClose"
      />

      <!-- Convocatoria Success Modal -->
      <div
        v-if="showConvocatoriaSuccess"
        class="modal fade show d-block"
        tabindex="-1"
        style="background-color: rgba(0, 0, 0, 0.5)"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header border-0">
              <h5 class="modal-title">
                <i class="bi bi-check-circle-fill text-success me-2"></i>
                ¡Inscripción Exitosa!
              </h5>
              <button
                type="button"
                class="btn-close"
                @click="handleConvocatoriaSuccessClose"
              ></button>
            </div>
            <div class="modal-body">
              <div class="success-checkmark mb-3">
                <div class="check-icon">
                  <span class="icon-line line-tip"></span>
                  <span class="icon-line line-long"></span>
                  <div class="icon-circle"></div>
                  <div class="icon-fix"></div>
                </div>
              </div>
              <p class="text-center mb-3">
                Te has inscripto en el voluntariado exitosamente. Al finalizar la convocatoria
                podrás inscribirte a los turnos.
              </p>
            </div>
            <div class="modal-footer border-0">
              <button
                type="button"
                class="btn btn-primary w-100"
                @click="handleConvocatoriaSuccessClose"
              >
                Aceptar
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped src="./../styles/VoluntariadoDetail.css"></style>
