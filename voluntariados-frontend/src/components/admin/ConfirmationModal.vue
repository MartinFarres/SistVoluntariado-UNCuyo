<!-- src/components/admin/ConfirmationModal.vue -->
<template>
  <div v-if="show" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i :class="iconClass" class="me-2"></i>
            {{ title }}
          </h5>
          <button type="button" class="btn-close" @click="handleCancel"></button>
        </div>
        <div class="modal-body">
          <div class="d-flex align-items-start">
            <div class="flex-shrink-0 me-3">
              <div :class="alertIconClass" class="rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px;">
                <i :class="alertIcon" class="fs-4"></i>
              </div>
            </div>
            <div class="flex-grow-1">
              <p class="mb-2 fw-bold">{{ message }}</p>
              <p v-if="description" class="mb-0 text-muted">{{ description }}</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleCancel">
            <i class="bi bi-x-lg me-1"></i>
            {{ cancelText }}
          </button>
          <button 
            type="button" 
            :class="confirmButtonClass"
            @click="handleConfirm"
            :disabled="processing"
          >
            <span v-if="processing">
              <span class="spinner-border spinner-border-sm me-2"></span>
              {{ processingText }}
            </span>
            <span v-else>
              <i :class="confirmIcon" class="me-1"></i>
              {{ confirmText }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ConfirmationModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: 'Confirmar acción'
    },
    message: {
      type: String,
      required: true
    },
    description: {
      type: String,
      default: ''
    },
    confirmText: {
      type: String,
      default: 'Eliminar'
    },
    cancelText: {
      type: String,
      default: 'Cancelar'
    },
    processingText: {
      type: String,
      default: 'Procesando...'
    },
    type: {
      type: String,
      default: 'danger', // danger, warning, info, success
      validator: (value: string) => ['danger', 'warning', 'info', 'success'].includes(value)
    },
    processing: {
      type: Boolean,
      default: false
    }
  },
  emits: ['confirm', 'cancel'],
  computed: {
    iconClass() {
      const icons = {
        danger: 'bi bi-exclamation-triangle-fill text-danger',
        warning: 'bi bi-exclamation-triangle-fill text-warning',
        info: 'bi bi-info-circle-fill text-info',
        success: 'bi bi-check-circle-fill text-success'
      }
      return icons[this.type as keyof typeof icons] || icons.danger
    },
    alertIconClass() {
      const classes = {
        danger: 'bg-danger-subtle text-danger',
        warning: 'bg-warning-subtle text-warning',
        info: 'bg-info-subtle text-info',
        success: 'bg-success-subtle text-success'
      }
      return classes[this.type as keyof typeof classes] || classes.danger
    },
    alertIcon() {
      const icons = {
        danger: 'bi bi-exclamation-triangle-fill',
        warning: 'bi bi-exclamation-triangle-fill',
        info: 'bi bi-info-circle-fill',
        success: 'bi bi-check-circle-fill'
      }
      return icons[this.type as keyof typeof icons] || icons.danger
    },
    confirmButtonClass() {
      const classes = {
        danger: 'btn btn-danger',
        warning: 'btn btn-warning',
        info: 'btn btn-info',
        success: 'btn btn-success'
      }
      return classes[this.type as keyof typeof classes] || classes.danger
    },
    confirmIcon() {
      const icons = {
        danger: 'bi bi-trash',
        warning: 'bi bi-exclamation-triangle',
        info: 'bi bi-info-circle',
        success: 'bi bi-check-lg'
      }
      return icons[this.type as keyof typeof icons] || icons.danger
    }
  },
  methods: {
    handleConfirm() {
      this.$emit('confirm')
    },
    handleCancel() {
      this.$emit('cancel')
    }
  }
})
</script>

<style scoped>
.modal {
  backdrop-filter: blur(2px);
}

.modal-content {
  border: 0;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.2);
}

.modal-header {
  border-bottom: 1px solid #e9ecef;
  padding: 1.25rem 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  border-top: 1px solid #e9ecef;
  padding: 1rem 1.5rem;
}

.btn-close:focus {
  box-shadow: none;
}
</style>