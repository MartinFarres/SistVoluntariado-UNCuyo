<!-- src/components/admin/VoluntariadoModal.vue -->
<template>
  <div
    class="modal fade"
    :class="{ show: show, 'd-block': show }"
    tabindex="-1"
    v-if="show"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-heart-fill text-danger me-2"></i>
            {{ isEdit ? 'Editar Voluntariado' : 'Crear Nuevo Voluntariado' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <!-- Mensaje de error -->
          <div v-if="errorMessage" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ errorMessage }}
          </div>

          <!-- Formulario principal -->
          <form @submit.prevent="handleSubmit">
            <!-- Información básica -->
            <div class="mb-4">
              <h6 class="text-muted mb-3">Información Básica</h6>

              <div class="mb-3">
                <label class="form-label">Nombre *</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="voluntariadoData.nombre"
                  required
                />
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Fecha de Inicio</label>
                  <input
                    type="date"
                    class="form-control"
                    v-model="voluntariadoData.fecha_inicio"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Fecha de Fin</label>
                  <input
                    type="date"
                    class="form-control"
                    v-model="voluntariadoData.fecha_fin"
                    :min="voluntariadoData.fecha_inicio"
                  />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Estado *</label>
                <select
                  class="form-control"
                  v-model="voluntariadoData.estado"
                  required
                >
                  <option value="DRAFT">Borrador</option>
                  <option value="ACTIVE">Activo</option>
                  <option value="CLOSED">Cerrado</option>
                </select>
              </div>
            </div>

            <!-- Información relacionada -->
            <div class="mb-4">
              <h6 class="text-muted mb-3">Información Relacionada</h6>
              <div class="row">
                <!-- Descripción -->
                <div class="col-md-6 mb-3">
                  <label class="form-label">Descripción *</label>
                  <div class="input-group">
                    <input
                      type="text"
                      class="form-control"
                      :value="voluntariadoData.descripcion ? voluntariadoData.descripcion.descripcion : 'No asignada'"
                      readonly
                    />
                    <button
                      class="btn btn-outline-secondary"
                      type="button"
                      @click="$emit('open-descripcion-modal')"
                    >
                      Crear
                    </button>
                  </div>
                </div>

                <!-- Manager -->
                <div class="col-md-6 mb-3">
                  <label class="form-label">Manager *</label>
                  <select
                    class="form-control"
                    v-model="voluntariadoData.gestionadores"
                    required
                  >
                    <option :value="null">Seleccione un manager</option>
                    <option
                      v-for="gestor in gestionadoresList"
                      :key="gestor.id"
                      :value="gestor.id"
                    >
                      {{ gestor.nombre }} {{ gestor.apellido }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Tabla de Turnos usando AdminTable -->
              <div class="mt-4">
                <AdminTable
                  title="Turnos"
                  :columns="turnosColumns"
                  :items="voluntariadoData.turnos"
                  empty-text="No hay turnos asignados"
                  create-button-text="Crear Turno"
                  @edit="editTurno"
                  @delete="deleteTurno"
                  @create="$emit('open-turno-modal')"
                >
                </AdminTable>
              </div>
            </div>
          </form>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            <i class="bi bi-x-circle me-2"></i> Cancelar
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="handleSubmit"
            :disabled="saving"
          >
            <span v-if="saving">
              <span class="spinner-border spinner-border-sm me-2"></span>Guardando...
            </span>
            <span v-else>
              <i class="bi bi-check-circle me-2"></i>{{ isEdit ? 'Actualizar' : 'Crear' }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal-backdrop fade show" v-if="show"></div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import {turnoAPI} from "@/services/api.ts";

export default defineComponent({
  name: 'VoluntariadoModal',
  components: { AdminTable },
  props: {
    show: { type: Boolean, default: false },
    isEdit: { type: Boolean, default: false },
    voluntariadoData: { type: Object as PropType<any>, required: true },
    gestionadoresList: { type: Array as PropType<any[]>, default: () => [] }
  },
  emits: ['close', 'save', 'open-turno-modal', 'open-descripcion-modal'],
  data() {
    return {
      saving: false,
      errorMessage: null as string | null,
      turnosColumns: [
        { key: 'fecha', label: 'Fecha' },
        { key: 'hora_inicio', label: 'Hora Inicio' },
        { key: 'hora_fin', label: 'Hora Fin' },
        { key: 'cupo', label: 'Cupo' },
        { key: 'lugar', label: 'Lugar' }
      ]
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.errorMessage = null
        this.saving = false
      }
    }
  },
  methods: {
    async handleSubmit() {
      if (!this.voluntariadoData.nombre) {
        this.errorMessage = 'El nombre es obligatorio.'
        return
      }
      if (!this.voluntariadoData.descripcion) {
        this.errorMessage = 'La Descripción es obligatoria.'
        return
      }
      if (!this.voluntariadoData.gestionadores) {
        this.errorMessage = 'El Manager es obligatorio.'
        return
      }

      this.errorMessage = null
      this.saving = true
      try {
        await this.$emit('save', this.voluntariadoData)
      } catch (error: any) {
        this.errorMessage = error.message || 'Error al guardar el voluntariado'
      } finally {
        this.saving = false
      }
    },

    editTurno(turno: any) {
    // Abrir modal de turno con datos de turno seleccionado
      this.$emit('open-turno-modal', turno);
    },
    async deleteTurno(turno: any) {
      if (!confirm(`¿Eliminar el turno del ${turno.fecha}?`)) return;
      try {

        await turnoAPI.delete(turno.id);
        this.voluntariadoData.turnos = this.voluntariadoData.turnos.filter(t => t.id !== turno.id);
      } catch (err) {
        console.error('Error al eliminar turno:', err);
        alert('No se pudo eliminar el turno.');
      }
    }

  }
})
</script>

<style scoped>
.modal.show {
  background: rgba(0, 0, 0, 0.5);
}
.modal-lg {
  max-width: 900px;
}
.table-sm th,
.table-sm td {
  padding: 0.5rem;
}
</style>
