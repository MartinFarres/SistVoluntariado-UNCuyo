<!-- eslint-disable @typescript-eslint/no-explicit-any -->
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
            {{ isEdit ? 'Edit Voluntariado' : 'Create New Voluntariado' }}
          </h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ errorMessage }}
          </div>
          
          <form @submit.prevent="handleSubmit">
            <!-- Basic Information -->
            <div class="mb-4">
              <h6 class="text-muted mb-3">
                <i class="bi bi-info-circle me-2"></i>
                Basic Information
              </h6>
              
              <div class="mb-3">
                <label class="form-label">Name *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="localData.nombre" 
                  required
                  placeholder="e.g., Community Garden Project"
                >
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Start Date</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    v-model="localData.fecha_inicio"
                  >
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">End Date</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    v-model="localData.fecha_fin"
                    :min="localData.fecha_inicio"
                  >
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Status *</label>
                <select class="form-control" v-model="localData.estado" required>
                  <option value="DRAFT">Borrador (Draft)</option>
                  <option value="ACTIVE">Activo (Active)</option>
                  <option value="CLOSED">Cerrado (Closed)</option>
                </select>
                <small class="text-muted">
                  <i class="bi bi-lightbulb me-1"></i>
                  Draft: Hidden from volunteers | Active: Visible & accepting applications | Closed: No new applications
                </small>
              </div>
            </div>

            <!-- Related Information -->
            <div class="mb-4">
              <h6 class="text-muted mb-3">
                <i class="bi bi-link-45deg me-2"></i>
                Related Information
              </h6>
              
              <div class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i>
                <small>
                  <strong>Note:</strong> You'll need to create Turnos, Descriptions, and assign Managers separately. 
                  These fields link to existing records.
                </small>
              </div>

              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label">Turno ID</label>
                  <input 
                    type="number" 
                    class="form-control" 
                    v-model.number="localData.turno"
                    placeholder="Leave empty for now"
                  >
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Description ID</label>
                  <input 
                    type="number" 
                    class="form-control" 
                    v-model.number="localData.descripcion"
                    placeholder="Leave empty for now"
                  >
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Manager ID</label>
                  <input 
                    type="number" 
                    class="form-control" 
                    v-model.number="localData.gestionadores"
                    placeholder="Leave empty for now"
                  >
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleClose">
            <i class="bi bi-x-circle me-2"></i>
            Cancel
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="handleSubmit"
            :disabled="saving"
          >
            <span v-if="saving">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Saving...
            </span>
            <span v-else>
              <i class="bi bi-check-circle me-2"></i>
              {{ isEdit ? 'Update' : 'Create' }}
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

export default defineComponent({
  name: 'VoluntariadoModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    voluntariadoData: {
      type: Object as PropType<any>,
      required: true
    }
  },
  emits: ['close', 'save'],
  data() {
    return {
      localData: { ...this.voluntariadoData },
      saving: false,
      errorMessage: null as string | null
    }
  },
  watch: {
    voluntariadoData: {
      handler(newVal) {
        this.localData = { ...newVal }
      },
      deep: true
    },
    show(newVal) {
      if (newVal) {
        this.errorMessage = null
        this.saving = false
      }
    }
  },
  methods: {
    handleClose() {
      this.$emit('close')
    },
    async handleSubmit() {
      // Validate dates
      if (this.localData.fecha_inicio && this.localData.fecha_fin) {
        if (new Date(this.localData.fecha_inicio) > new Date(this.localData.fecha_fin)) {
          this.errorMessage = 'End date must be after start date'
          return
        }
      }

      // Validate required fields
      if (!this.localData.nombre || !this.localData.nombre.trim()) {
        this.errorMessage = 'Name is required'
        return
      }

      this.errorMessage = null
      this.saving = true
      
      try {
        await this.$emit('save', this.localData)
      } catch (error: any) {
        this.errorMessage = error.message || 'Failed to save voluntariado'
        this.saving = false
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
  max-width: 800px;
}
</style>