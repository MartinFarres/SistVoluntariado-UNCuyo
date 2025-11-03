<!-- src/components/landing/CancelConfirmationModal.vue -->
<template>
  <div
    v-if="show"
    class="modal fade show d-block"
    tabindex="-1"
    style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-exclamation-triangle-fill text-danger me-2"></i>
            Confirmar Cancelación
          </h5>
          <button type="button" class="btn-close" @click="$emit('cancel')"></button>
        </div>
        <div class="modal-body">
          <p>¿Estás seguro de que quieres cancelar tu inscripción a este voluntariado/turno?</p>
          <div class="voluntariado-info-box">
            <h6 class="mb-2">{{ voluntariadoTitle }}</h6>
            <p class="text-muted small mb-0">{{ organizationName }}</p>
          </div>
          <p class="text-danger small mt-3">
            <i class="bi bi-exclamation-circle-fill"></i> Esta acción no se puede deshacer.
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            @click="$emit('cancel')"
            :disabled="loading"
          >
            Volver
          </button>
          <button
            type="button"
            class="btn btn-danger"
            @click="$emit('confirm')"
            :disabled="loading"
          >
            <span v-if="loading">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Cancelando...
            </span>
            <span v-else>
              <i class="bi bi-trash me-1"></i>
              Sí, cancelar
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "CancelConfirmationModal",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    voluntariadoTitle: {
      type: String,
      required: true,
    },
    organizationName: {
      type: String,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["confirm", "cancel"],
});
</script>

<style scoped>
.voluntariado-info-box {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #dc3545;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background-color: #bb2d3b;
  border-color: #b02a37;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
