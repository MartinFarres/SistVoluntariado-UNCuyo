<template>
  <div class="admin-turnos-calendar">
    <div class="calendar-header d-flex justify-content-between align-items-center mb-3">
      <div class="d-flex align-items-center gap-2">
        <button class="btn btn-sm btn-outline-secondary" @click="prevMonth" :disabled="!canPrevMonth">
          <i class="bi bi-chevron-left"></i>
        </button>
        <h4 class="calendar-title text-capitalize mb-0">{{ monthName }}</h4>
        <button class="btn btn-sm btn-outline-secondary" @click="nextMonth" :disabled="!canNextMonth">
          <i class="bi bi-chevron-right"></i>
        </button>
      </div>
      <div>
        <small class="text-muted d-flex align-items-center gap-2">
          <span>
            <i class="bi bi-calendar-range me-1"></i>
            Rango permitido: {{ displayRange }}
          </span>
        </small>
        <div class="d-flex align-items-center gap-3 mt-1">
          <small class="text-muted">
            <span class="range-indicator in-range"></span> Disponible
          </small>
          <small class="text-muted">
            <span class="range-indicator out-of-range"></span> Fuera de rango
          </small>
        </div>
      </div>
    </div>

    <div class="calendar-grid">
      <div class="day-header" v-for="d in dayHeaders" :key="d">{{ d }}</div>

      <div
        v-for="(day, index) in calendarDays"
        :key="index"
        :class="getDayClasses(day)"
        :title="getDayTitle(day)"
        @click="onDayClick(day)"
      >
        <span class="day-number">
          {{ day.date.getDate() }}
          <i v-if="!isDateInRange(day.date) && day.isCurrentMonth" class="bi bi-lock-fill ms-1" style="font-size: 0.7rem;"></i>
        </span>

        <div v-if="day.turnos.length > 0" class="day-turnos-list">
          <div
            v-for="(t, idx) in day.turnos.slice(0,3)"
            :key="t.id || idx"
            class="turno-pill"
            @click.stop="onTurnoClick(t)"
          >
            <small>{{ formatTime(t.hora_inicio) }}–{{ formatTime(t.hora_fin) }}</small>
            <button 
              class="turno-delete-btn"
              @click.stop="onTurnoDelete(t)"
              title="Eliminar turno"
            >
              <i class="bi bi-x"></i>
            </button>
          </div>
          <div v-if="day.turnos.length > 3" class="more-pill">
            +{{ day.turnos.length - 3 }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'
import { formatDateShort, parseLocalDate } from '@/utils/dateUtils'

interface Turno {
  id?: number
  fecha: string
  hora_inicio: string
  hora_fin: string
  cupo: number
  lugar?: string
}

interface CalendarDay {
  date: Date
  dateString: string
  isCurrentMonth: boolean
  isToday: boolean
  turnos: Turno[]
}

export default defineComponent({
  name: 'AdminTurnosCalendarManagement',
  props: {
    voluntariadoId: { type: Number as PropType<number>, required: true },
    turnos: { type: Array as PropType<Turno[]>, default: () => [] },
    fechaInicioCursado: { type: String as PropType<string | null>, default: null },
    fechaFinCursado: { type: String as PropType<string | null>, default: null },
  },
  emits: ['day-click', 'turno-click', 'turno-delete'],
  data() {
    const now = new Date()
    return {
      currentMonth: now.getMonth(),
      currentYear: now.getFullYear(),
      dayHeaders: ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'] as string[],
    }
  },
  computed: {
    minDate(): Date | null {
      if (!this.fechaInicioCursado) return null
      return parseLocalDate(this.fechaInicioCursado)
    },
    maxDate(): Date | null {
      if (!this.fechaFinCursado) return null
      return parseLocalDate(this.fechaFinCursado)
    },
    monthName(): string {
      return new Date(this.currentYear, this.currentMonth)
        .toLocaleDateString('es-AR', { month: 'long', year: 'numeric' })
    },
    calendarDays(): CalendarDay[] {
      const firstDay = new Date(this.currentYear, this.currentMonth, 1)
      const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0)
      const startDay = firstDay.getDay()
      const daysInMonth = lastDay.getDate()
      const days: CalendarDay[] = []
      const today = new Date()
      today.setHours(0,0,0,0)

      // Previous month days
      const prevMonthLastDay = new Date(this.currentYear, this.currentMonth, 0).getDate()
      for (let i = startDay - 1; i >= 0; i--) {
        const date = new Date(this.currentYear, this.currentMonth - 1, prevMonthLastDay - i)
        days.push({
          date,
          dateString: this.formatDateString(date),
          isCurrentMonth: false,
          isToday: false,
          turnos: []
        })
      }

      // Current month days
      for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(this.currentYear, this.currentMonth, day)
        date.setHours(0,0,0,0)
        const dateString = this.formatDateString(date)
        const dayTurnos = (this.turnos || []).filter((t: Turno) => t.fecha === dateString)
        days.push({
          date,
          dateString,
          isCurrentMonth: true,
          isToday: date.getTime() === today.getTime(),
          turnos: dayTurnos
        })
      }

      // Next month days
      const remaining = 42 - days.length
      for (let i = 1; i <= remaining; i++) {
        const date = new Date(this.currentYear, this.currentMonth + 1, i)
        days.push({
          date,
          dateString: this.formatDateString(date),
          isCurrentMonth: false,
          isToday: false,
          turnos: []
        })
      }

      return days
    },
    displayRange(): string {
      if (!this.fechaInicioCursado || !this.fechaFinCursado) return 'Sin rango'
      return `${formatDateShort(this.fechaInicioCursado)} – ${formatDateShort(this.fechaFinCursado)}`
    },
    canPrevMonth(): boolean {
      if (!this.minDate) return true
      const prev = new Date(this.currentYear, this.currentMonth - 1, 1)
      return !(prev.getFullYear() < this.minDate.getFullYear() || 
               (prev.getFullYear() === this.minDate.getFullYear() && prev.getMonth() < this.minDate.getMonth()))
    },
    canNextMonth(): boolean {
      if (!this.maxDate) return true
      const next = new Date(this.currentYear, this.currentMonth + 1, 1)
      return !(next.getFullYear() > this.maxDate.getFullYear() || 
               (next.getFullYear() === this.maxDate.getFullYear() && next.getMonth() > this.maxDate.getMonth()))
    }
  },
  methods: {
    formatDateString(date: Date): string {
      const y = date.getFullYear()
      const m = String(date.getMonth() + 1).padStart(2,'0')
      const d = String(date.getDate()).padStart(2,'0')
      return `${y}-${m}-${d}`
    },
    formatTime(t: string | undefined): string {
      if (!t) return ''
      return t.substring(0,5)
    },
    prevMonth() {
      if (!this.canPrevMonth) return
      if (this.currentMonth === 0) {
        this.currentMonth = 11
        this.currentYear--
      } else {
        this.currentMonth--
      }
    },
    nextMonth() {
      if (!this.canNextMonth) return
      if (this.currentMonth === 11) {
        this.currentMonth = 0
        this.currentYear++
      } else {
        this.currentMonth++
      }
    },
    getDayClasses(day: CalendarDay): string[] {
      const classes = ['calendar-day']
      if (!day.isCurrentMonth) classes.push('other-month')
      if (day.isToday) classes.push('today')
      if (day.turnos.length > 0) classes.push('has-turnos')
      const inRange = this.isDateInRange(day.date)
      if (!inRange) classes.push('disabled', 'out-of-range')
      if (inRange && day.isCurrentMonth) classes.push('in-range')
      return classes
    },
    getDayTitle(day: CalendarDay): string {
      const inRange = this.isDateInRange(day.date)
      if (!inRange) {
        return 'Fecha fuera del rango permitido'
      }
      if (day.turnos.length > 0) {
        return `${day.turnos.length} turno(s) - Click para ver/editar`
      }
      if (day.isCurrentMonth) {
        return 'Click para crear un turno'
      }
      return ''
    },
    onDayClick(day: CalendarDay) {
      if (!this.isDateInRange(day.date)) {
        console.log('[Calendar] Day out of range, ignoring')
        return
      }
      this.$emit('day-click', day.dateString)
    },
    onTurnoClick(turno: Turno) {
      const turnoDate = parseLocalDate(turno.fecha)
      if (!this.isDateInRange(turnoDate)) {
        console.log('[Calendar] Turno out of range, ignoring')
        return
      }
      this.$emit('turno-click', turno)
    },
    onTurnoDelete(turno: Turno) {
      console.log('[Calendar] Turno delete requested:', turno.id)
      this.$emit('turno-delete', turno)
    },
    isDateInRange(date: Date): boolean {
      const d = new Date(date)
      d.setHours(0,0,0,0)
      
      if (this.minDate) {
        const min = new Date(this.minDate)
        min.setHours(0,0,0,0)
        if (d < min) return false
      }
      
      if (this.maxDate) {
        const max = new Date(this.maxDate)
        max.setHours(0,0,0,0)
        if (d > max) return false
      }
      
      return true
    }
  }
})
</script>

<style scoped>
.admin-turnos-calendar {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.range-indicator {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 4px;
  vertical-align: middle;
}

.range-indicator.in-range {
  background: #c8e6c9;
  border: 1px solid #4caf50;
}

.range-indicator.out-of-range {
  background: #fff5f5;
  border: 1px solid #ffc9c9;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 6px;
}

.day-header {
  text-align: center;
  font-weight: 600;
  padding: 0.5rem;
  color: #6c757d;
  font-size: 0.875rem;
}

.calendar-day {
  min-height: 90px;
  border-radius: 6px;
  padding: 0.5rem;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  cursor: pointer;
  transition: all 0.2s ease;
}

.calendar-day:hover:not(.disabled):not(.other-month) {
  background: #e9ecef;
  border-color: #0d6efd;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.calendar-day.other-month {
  opacity: 0.4;
  background: transparent;
  cursor: default;
}

.calendar-day.other-month.out-of-range {
  opacity: 0.25;
  background: transparent !important;
}

.calendar-day.today {
  background: #e7f3ff;
  border-color: #0d6efd;
  font-weight: 600;
}

.calendar-day.today.in-range {
  background: #e7f9f0;
  border-color: #0d6efd;
  box-shadow: 0 0 0 2px rgba(13, 110, 253, 0.15);
}

.calendar-day.today.out-of-range {
  background: #ffe7e7 !important;
  border-color: #ff6b6b !important;
}

.calendar-day.has-turnos {
  background: #fff;
}

.calendar-day.disabled {
  cursor: not-allowed;
}

.calendar-day.out-of-range {
  background: #fff5f5 !important;
  border-color: #ffc9c9 !important;
  color: #a0a0a0;
  position: relative;
  overflow: hidden;
}

.calendar-day.out-of-range::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    rgba(255, 201, 201, 0.1) 10px,
    rgba(255, 201, 201, 0.1) 20px
  );
  pointer-events: none;
}

.calendar-day.out-of-range .day-number {
  color: #c0c0c0;
  position: relative;
  z-index: 1;
}

.calendar-day.out-of-range:hover {
  background: #fff5f5 !important;
  border-color: #ffc9c9 !important;
  transform: none !important;
  box-shadow: none !important;
}

.calendar-day.in-range {
  border-color: #c8e6c9;
  background: #f1f8f4;
}

.calendar-day.in-range:hover {
  border-color: #4caf50;
  background: #e8f5e9;
}

.calendar-day.in-range.has-turnos {
  background: #fff;
  border-color: #81c784;
}

.day-number {
  font-size: 0.875rem;
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.day-turnos-list {
  margin-top: 6px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.turno-pill {
  background: #198754;
  color: white;
  padding: 3px 6px;
  border-radius: 12px;
  font-size: 0.7rem;
  cursor: pointer;
  transition: background 0.2s ease;
  position: relative;
  display: flex;
  align-items: center;
  gap: 4px;
}

.turno-pill:hover {
  background: #157347;
  transform: scale(1.05);
  padding-right: 24px;
}

.turno-pill small {
  font-size: 0.7rem;
}

.turno-delete-btn {
  position: absolute;
  right: 2px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(220, 53, 69, 0.9);
  border: none;
  color: white;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  padding: 0;
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.75rem;
  line-height: 1;
  transition: all 0.2s ease;
}

.turno-delete-btn:hover {
  background: #dc3545;
  transform: translateY(-50%) scale(1.1);
}

.turno-pill:hover .turno-delete-btn {
  display: flex;
}

.more-pill {
  background: #6c757d;
  color: white;
  padding: 3px 6px;
  border-radius: 12px;
  font-size: 0.7rem;
}

@media (max-width: 768px) {
  .calendar-day {
    min-height: 70px;
    padding: 0.25rem;
  }
  
  .day-number {
    font-size: 0.75rem;
  }
  
  /* Show delete button on mobile without hover */
  .turno-delete-btn {
    display: flex;
    opacity: 0.7;
  }
  
  .turno-pill {
    padding-right: 24px;
  }
}
</style>