<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script lang="ts">
import { defineComponent, type PropType } from "vue";

interface Turno {
  id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  cupo: number;
  lugar?: string;
  inscripciones_count?: number;
  is_full?: boolean;
}

interface CalendarDay {
  date: Date;
  dateString: string;
  isCurrentMonth: boolean;
  isToday: boolean;
  turnos: Turno[];
}

export default defineComponent({
  name: "TurnosCalendar",
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
    return {
      currentMonth: new Date().getMonth(),
      currentYear: new Date().getFullYear(),
    };
  },
  computed: {
    calendarDays(): CalendarDay[] {
      const firstDay = new Date(this.currentYear, this.currentMonth, 1);
      const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0);
      const startDay = firstDay.getDay(); // 0 = Sunday
      const daysInMonth = lastDay.getDate();

      const days: CalendarDay[] = [];
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      // Previous month days
      const prevMonthLastDay = new Date(this.currentYear, this.currentMonth, 0).getDate();
      for (let i = startDay - 1; i >= 0; i--) {
        const date = new Date(this.currentYear, this.currentMonth - 1, prevMonthLastDay - i);
        days.push({
          date,
          dateString: this.formatDateString(date),
          isCurrentMonth: false,
          isToday: false,
          turnos: [],
        });
      }

      // Current month days
      for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(this.currentYear, this.currentMonth, day);
        const dateString = this.formatDateString(date);
        const dayTurnos = this.turnos.filter((t: Turno) => t.fecha === dateString);

        days.push({
          date,
          dateString,
          isCurrentMonth: true,
          isToday: date.getTime() === today.getTime(),
          turnos: dayTurnos,
        });
      }

      // Next month days to fill the grid
      const remainingDays = 42 - days.length; // 6 rows * 7 days
      for (let day = 1; day <= remainingDays; day++) {
        const date = new Date(this.currentYear, this.currentMonth + 1, day);
        days.push({
          date,
          dateString: this.formatDateString(date),
          isCurrentMonth: false,
          isToday: false,
          turnos: [],
        });
      }

      return days;
    },
    monthName(): string {
      return new Date(this.currentYear, this.currentMonth).toLocaleDateString("es-AR", {
        month: "long",
        year: "numeric",
      });
    },
  },
  methods: {
    formatDateString(date: Date): string {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
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
    selectDate(day: CalendarDay) {
      if (day.turnos.length > 0) {
        this.$emit("date-selected", day.dateString);
      }
    },
    getDayClasses(day: CalendarDay): string[] {
      const classes = ["calendar-day"];
      if (!day.isCurrentMonth) classes.push("other-month");
      if (day.isToday) classes.push("today");
      if (day.turnos.length > 0) {
        classes.push("has-turnos");
        // Check if all turnos on this day are full
        const allFull = day.turnos.every((t) => t.is_full);
        if (allFull) classes.push("all-full");
      }
      if (day.dateString === this.selectedDate) classes.push("selected");
      return classes;
    },
    getAvailableTurnosCount(day: CalendarDay): number {
      return day.turnos.filter((t) => !t.is_full).length;
    },
  },
});
</script>

<template>
  <div class="turnos-calendar">
    <div class="calendar-header">
      <button class="btn btn-sm btn-outline-secondary" @click="prevMonth">
        <i class="bi bi-chevron-left"></i>
      </button>
      <h4 class="calendar-title text-capitalize">{{ monthName }}</h4>
      <button class="btn btn-sm btn-outline-secondary" @click="nextMonth">
        <i class="bi bi-chevron-right"></i>
      </button>
    </div>

    <div class="calendar-grid">
      <!-- Day headers -->
      <div class="day-header" v-for="day in ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']" :key="day">
        {{ day }}
      </div>

      <!-- Calendar days -->
      <div
        v-for="(day, index) in calendarDays"
        :key="index"
        :class="getDayClasses(day)"
        @click="selectDate(day)"
      >
        <span class="day-number">{{ day.date.getDate() }}</span>
        <span v-if="day.turnos.length > 0" class="turnos-indicator">
          {{ getAvailableTurnosCount(day) || day.turnos.length }}
        </span>
      </div>
    </div>

    <div class="calendar-legend mt-3">
      <small class="text-muted">
        <span class="legend-item">
          <span class="legend-dot has-turnos"></span>
          Turnos disponibles
        </span>
        <span class="legend-item ms-3">
          <span class="legend-dot all-full"></span>
          Todos completos
        </span>
        <span class="legend-item ms-3">
          <span class="legend-dot today"></span>
          Hoy
        </span>
      </small>
    </div>
  </div>
</template>

<style scoped>
.turnos-calendar {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.calendar-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.day-header {
  text-align: center;
  font-weight: 600;
  font-size: 0.875rem;
  color: #6c757d;
  padding: 0.5rem;
  text-transform: uppercase;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: default;
  position: relative;
  transition: all 0.2s ease;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
}

.calendar-day.other-month {
  opacity: 0.3;
  background: transparent;
}

.calendar-day.today {
  background: #e7f3ff;
  border-color: #0d6efd;
  font-weight: 600;
}

.calendar-day.has-turnos {
  cursor: pointer;
  background: #d1e7dd;
  border-color: #198754;
}

.calendar-day.has-turnos:hover {
  background: #b8ddc8;
  transform: scale(1.05);
}

.calendar-day.all-full {
  background: #f8d7da;
  border-color: #dc3545;
  cursor: default;
}

.calendar-day.all-full:hover {
  background: #f8d7da;
  transform: none;
}

.calendar-day.all-full .turnos-indicator {
  background: #dc3545;
}

.calendar-day.selected {
  background: #0d6efd;
  color: white;
  border-color: #0d6efd;
}

.calendar-day.selected .turnos-indicator {
  background: white;
  color: #0d6efd;
}

.day-number {
  font-size: 0.875rem;
  line-height: 1;
}

.turnos-indicator {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #198754;
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.calendar-legend {
  display: flex;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.legend-dot.has-turnos {
  background: #d1e7dd;
  border: 1px solid #198754;
}

.legend-dot.all-full {
  background: #f8d7da;
  border: 1px solid #dc3545;
}

.legend-dot.today {
  background: #e7f3ff;
  border: 1px solid #0d6efd;
}

@media (max-width: 768px) {
  .turnos-calendar {
    padding: 1rem;
  }

  .calendar-title {
    font-size: 1rem;
  }

  .day-header {
    font-size: 0.75rem;
    padding: 0.25rem;
  }

  .calendar-day {
    padding: 0.25rem;
  }

  .day-number {
    font-size: 0.75rem;
  }

  .turnos-indicator {
    width: 14px;
    height: 14px;
    font-size: 0.5rem;
    top: 2px;
    right: 2px;
  }
}
</style>
