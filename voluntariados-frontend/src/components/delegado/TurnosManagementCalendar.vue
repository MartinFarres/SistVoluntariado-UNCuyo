<template>
  <div class="turnos-management-calendar">
    <div class="calendar-header d-flex justify-content-between align-items-center mb-3">
      <div class="d-flex gap-2">
        <button class="btn btn-sm btn-outline-secondary" @click="prevMonth" type="button">
          <i class="bi bi-chevron-left"></i>
        </button>
        <button class="btn btn-sm btn-outline-secondary" @click="nextMonth" type="button">
          <i class="bi bi-chevron-right"></i>
        </button>
      </div>
      <h5 class="mb-0 text-capitalize">{{ monthName }}</h5>
      <div></div>
    </div>

    <div class="calendar-grid mb-2">
      <div class="day-header" v-for="day in ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']" :key="day">
        {{ day }}
      </div>

      <div
        v-for="(day, idx) in calendarDays"
        :key="idx"
        :class="dayClasses(day)"
        @click="onDayClick(day)"
          role="button"
          :aria-disabled="day.turnos.length === 0"
      >
        <span class="day-number">{{ day.date.getDate() }}</span>

        <span v-if="day.turnos.length > 0" class="turnos-indicator">
          {{ day.turnos.length }}
        </span>

        <!-- Show 'Próximamente' only when the day actually has turnos that are blocked -->
        <small v-if="day.isProximamente && day.turnos.length > 0" class="d-block mt-1 text-muted proximamente-label">Próximamente</small>
        <small v-else-if="day.needsFollowUp" class="d-block mt-1 text-warning followup-label">Asistencia pendiente</small>
      </div>
    </div>

    <div class="calendar-legend mt-3">
      <small class="text-muted d-flex gap-3 flex-wrap">
        <span class="legend-item"><span class="legend-dot has-turnos"></span> Turnos</span>
        <span class="legend-item"><span class="legend-dot proximamente"></span> Próximamente (bloqueado)</span>
        <span class="legend-item"><span class="legend-dot followup"></span> Asistencia pendiente</span>
      </small>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

interface Turno {
  id: number;
  fecha: string; // YYYY-MM-DD
  hora_inicio?: string; // HH:MM:SS
  hora_fin?: string; // HH:MM:SS
  // optional asistencia flags if backend provides
  asistencia_completa?: boolean;
  asistencia?: { completa?: boolean } | null;
}

interface CalendarDay {
  date: Date;
  dateString: string;
  isCurrentMonth: boolean;
  isToday: boolean;
  turnos: Turno[];
  isProximamente: boolean;
  needsFollowUp: boolean;
}

export default defineComponent({
  name: "TurnosManagementCalendar",
  props: {
    turnos: {
      type: Array as PropType<Turno[]>,
      required: true,
    },
    selectedDate: {
      type: String as PropType<string | null>,
      default: null,
    },
  },
  emits: ["date-selected"],
  data() {
    const now = new Date();
    return {
      currentMonth: now.getMonth(),
      currentYear: now.getFullYear(),
    };
  },
  computed: {
    monthName(): string {
      return new Date(this.currentYear, this.currentMonth).toLocaleDateString("es-AR", {
        month: "long",
        year: "numeric",
      });
    },
    calendarDays(): CalendarDay[] {
      const firstDay = new Date(this.currentYear, this.currentMonth, 1);
      const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0);
      const startDay = firstDay.getDay();
      const daysInMonth = lastDay.getDate();

      const days: CalendarDay[] = [];
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      // Prev month fill
      const prevMonthLastDay = new Date(this.currentYear, this.currentMonth, 0).getDate();
      for (let i = startDay - 1; i >= 0; i--) {
        const date = new Date(this.currentYear, this.currentMonth - 1, prevMonthLastDay - i);
        days.push({
          date,
          dateString: this.formatDateString(date),
          isCurrentMonth: false,
          isToday: false,
          turnos: [],
          isProximamente: false,
          needsFollowUp: false,
        });
      }

      // Current month days
      for (let d = 1; d <= daysInMonth; d++) {
        const date = new Date(this.currentYear, this.currentMonth, d);
        const dateString = this.formatDateString(date);
        const dayTurnos = this.turnos.filter((t: Turno) => t.fecha === dateString);
        const isToday = date.getTime() === today.getTime();
        const isProximamente = date.getTime() > today.getTime();

        // Determine if at least one turno on this date (today or past) has asistencia incomplete
        // Mark the cell as needing follow-up if any turno for that date is not marked as completed
        // Note: future turnos are ignored here.
        const needsFollowUp = dayTurnos.some((t) => {
          try {
            const turnoDate = new Date(t.fecha);
            turnoDate.setHours(0, 0, 0, 0);
            // ignore future turnos
            if (turnoDate.getTime() > today.getTime()) return false;
            const asistenciaCompleted = this.isAsistenciaCompleted(t);
            return !asistenciaCompleted;
          } catch {
            return false;
          }
        });

        days.push({
          date,
          dateString,
          isCurrentMonth: true,
          isToday,
          turnos: dayTurnos,
          isProximamente,
          needsFollowUp,
        });
      }

      // Next month fill to 6 rows
      const remaining = 42 - days.length;
      for (let i = 1; i <= remaining; i++) {
        const date = new Date(this.currentYear, this.currentMonth + 1, i);
        days.push({
          date,
          dateString: this.formatDateString(date),
          isCurrentMonth: false,
          isToday: false,
          turnos: [],
          isProximamente: false,
          needsFollowUp: false,
        });
      }

      return days;
    },
  },
  methods: {
    formatDateString(date: Date): string {
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, "0");
      const d = String(date.getDate()).padStart(2, "0");
      return `${y}-${m}-${d}`;
    },
    prevMonth() {
      if (this.currentMonth === 0) {
        this.currentMonth = 11;
        this.currentYear--;
      } else {
        this.currentMonth--;
      }
    },
    nextMonth() {
      if (this.currentMonth === 11) {
        this.currentMonth = 0;
        this.currentYear++;
      } else {
        this.currentMonth++;
      }
    },
    onDayClick(day: CalendarDay) {
      // blocked only when there are no turnos
      if (day.turnos.length === 0) return;
      // Allow selecting future (Próximamente) days — the UI will show them but actions remain blocked
      this.$emit("date-selected", day.dateString);
    },
    dayClasses(day: CalendarDay) {
      const classes = ["calendar-day"];
      if (!day.isCurrentMonth) classes.push("other-month");
      if (day.isToday) classes.push("today");
      if (day.turnos.length > 0) classes.push("has-turnos");
  // only mark proximamente visually when there are turnos on that day
  if (day.isProximamente && day.turnos.length > 0) classes.push("proximamente");
      if (day.needsFollowUp) classes.push("needs-followup");
      if (day.dateString === this.selectedDate) classes.push("selected");
      return classes;
    },
    // Determine if a turno is finished (by fecha + hora_fin if available)
    isTurnoFinished(turno: Turno): boolean {
      try {
        const now = new Date();
        // Build end datetime if hora_fin present
        if (turno.hora_fin) {
          const dt = new Date(`${turno.fecha}T${turno.hora_fin}`);
          if (!isNaN(dt.getTime())) {
            return dt.getTime() < now.getTime();
          }
        }
        // fallback: compare date only
        const turnoDate = new Date(turno.fecha);
        turnoDate.setHours(23, 59, 59, 999);
        return turnoDate.getTime() < now.getTime();
      } catch {
        return false;
      }
    },
    // Heuristic to detect asistencia completed flag in turno object
    isAsistenciaCompleted(turno: Turno): boolean {
      if (turno == null) return false;
      if ((turno as any).asistencia_completa === true) return true;
      if ((turno as any).asistencia_completa === false) return false;
      // Prefer canonical backend field if provided. Fallback to legacy shapes.
    if (turno && typeof (turno as any).asistencia_completa !== 'undefined') {
      return !!(turno as any).asistencia_completa
    }
    // Legacy fallback: nested asistencia object
    if (turno && (turno as any).asistencia) {
      const a = (turno as any).asistencia
      return !!(a.completa || a.presente)
    }
    // Legacy numeric fallback: compare counts
    if (turno && (turno as any).asistencias_registradas != null && typeof (turno as any).inscripciones_count !== 'undefined') {
      return (turno as any).asistencias_registradas >= (turno as any).inscripciones_count
    }
      // other possible keys
      if ((turno as any).asistenciaCompleted !== undefined) return !!(turno as any).asistenciaCompleted;
      return false;
    },
  },
});
</script>

<style scoped>
.turnos-management-calendar {
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  box-sizing: border-box;
}

.calendar-header { padding: 0.25rem 0; }

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-auto-rows: minmax(64px, 1fr);
  gap: 6px;
  width: 100%;
  height: calc(100% - 86px); /* leave room for header & legend */
}

.day-header {
  text-align: center;
  font-weight: 700;
  font-size: 0.8rem;
  color: #6c757d;
  padding: 0.35rem;
}

.calendar-day {
  min-height: 64px;
  padding: 0.5rem;
  border-radius: 6px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: default;
  position: relative;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
  box-sizing: border-box;
}

.calendar-day.other-month { opacity: 0.35; background: transparent; }

.calendar-day.today { background: #eef7ff; border-color: #0d6efd; font-weight: 600; }

.calendar-day.has-turnos { cursor: pointer; background: #e9f7ef; border-color: #198754; }

.calendar-day.has-turnos:hover { transform: translateY(-3px); box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

.calendar-day.proximamente {
  /* Use neutral/grey styling for proximamente (blocked) to match design */
  background: #f5f5f6; /* light grey */
  border-color: #dee2e6; /* neutral grey border */
  color: #6c757d;
  cursor: default;
}

/* If a proximamente day has turnos, make it clickable (cursor pointer) */
.calendar-day.proximamente.has-turnos {
  cursor: pointer;
}

.calendar-day.needs-followup {
  background: #fff8db; /* light yellow */
  border-color: #ffca2c;
}

.calendar-day.selected {
  background: #0d6efd;
  color: white;
  border-color: #0d6efd;
}

.day-number { font-size: 0.9rem; }

.turnos-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #198754;
  color: #fff;
  width: 20px;
  height: 20px;
  font-size: 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: 700;
}

.proximamente-label { font-size: 0.675rem; color: #856404; }
.followup-label { font-size: 0.675rem; color: #856404; }

.calendar-legend .legend-dot {
  width: 12px;
  height: 12px;
  display: inline-block;
  border-radius: 50%;
  margin-right: 6px;
}
.legend-dot.has-turnos { background: #e9f7ef; border: 1px solid #198754; }
.legend-dot.proximamente { background: #f5f5f6; border: 1px solid #dee2e6; }
.legend-dot.followup { background: #fff8db; border: 1px solid #ffca2c; }

@media (max-width: 767px) {
  .calendar-grid { grid-auto-rows: minmax(52px, auto); height: auto; }
  .turnos-indicator { width: 16px; height: 16px; font-size: 0.55rem; top: 6px; right: 6px; }
}
</style>