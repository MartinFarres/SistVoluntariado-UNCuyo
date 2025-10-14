<!-- src/components/landing/JoinConfirmationModal.vue -->
<template>
  <div 
    class="modal fade" 
    :class="{ show: show, 'd-block': show }"
    tabindex="-1" 
    @click.self="$emit('cancel')"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <!-- Success Animation -->
        <div v-if="showSuccess" class="success-animation">
          <div class="success-checkmark">
            <div class="check-icon">
              <span class="icon-line line-tip"></span>
              <span class="icon-line line-long"></span>
              <div class="icon-circle"></div>
              <div class="icon-fix"></div>
            </div>
          </div>
          <h3 class="success-title">¡Inscripción Exitosa!</h3>
          <p class="success-message">Te has unido al voluntariado correctamente</p>
        </div>

        <!-- Confirmation Content -->
        <template v-else>
          <div class="modal-header border-0">
            <h5 class="modal-title">
              <i class="bi bi-heart-fill text-danger me-2"></i>
              Confirmar Inscripción
            </h5>
            <button 
              type="button" 
              class="btn-close" 
              @click="$emit('cancel')"
              :disabled="loading"
            ></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">¿Estás seguro que deseas unirte a este voluntariado?</p>
            <div class="voluntariado-info-box">
              <h6 class="mb-2">{{ voluntariadoTitle }}</h6>
              <p class="text-muted small mb-0">{{ organizationName }}</p>
            </div>
          </div>
          <div class="modal-footer border-0">
            <button 
              type="button" 
              class="btn btn-secondary" 
              @click="$emit('cancel')"
              :disabled="loading"
            >
              Cancelar
            </button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="$emit('confirm')"
              :disabled="loading"
            >
              <span v-if="loading">
                <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                Procesando...
              </span>
              <span v-else>
                <i class="bi bi-check-circle me-2"></i>
                Confirmar
              </span>
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
  <div 
    v-if="show" 
    class="modal-backdrop fade"
    :class="{ show: show }"
  ></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'JoinConfirmationModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    voluntariadoTitle: {
      type: String,
      required: true
    },
    organizationName: {
      type: String,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    showSuccess: {
      type: Boolean,
      default: false
    }
  },
  emits: ['confirm', 'cancel']
})
</script>

<style scoped>
.modal {
  background: rgba(0, 0, 0, 0.5);
}

.modal.show {
  opacity: 1;
}

.modal-content {
  border-radius: 12px;
  border: none;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 1.5rem 1.5rem 0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
}

.modal-body {
  padding: 1.5rem;
}

.voluntariado-info-box {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #8B0000;
}

.modal-footer {
  padding: 0 1.5rem 1.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #8B0000, #DC143C);
  border: none;
  padding: 0.5rem 1.5rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(139, 0, 0, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  border-radius: 50px;
  padding: 0.5rem 1.5rem;
  font-weight: 600;
}

/* Success Animation */
.success-animation {
  padding: 3rem 2rem;
  text-align: center;
}

.success-checkmark {
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
}

.check-icon {
  width: 80px;
  height: 80px;
  position: relative;
  border-radius: 50%;
  box-sizing: content-box;
  border: 4px solid #4CAF50;
}

.check-icon::before {
  top: 3px;
  left: -2px;
  width: 30px;
  transform-origin: 100% 50%;
  border-radius: 100px 0 0 100px;
}

.check-icon::after {
  top: 0;
  left: 30px;
  width: 60px;
  transform-origin: 0 50%;
  border-radius: 0 100px 100px 0;
  animation: rotate-circle 4.25s ease-in;
}

.icon-line {
  height: 5px;
  background-color: #4CAF50;
  display: block;
  border-radius: 2px;
  position: absolute;
  z-index: 10;
}

.icon-line.line-tip {
  top: 46px;
  left: 14px;
  width: 25px;
  transform: rotate(45deg);
  animation: icon-line-tip 0.75s;
}

.icon-line.line-long {
  top: 38px;
  right: 8px;
  width: 47px;
  transform: rotate(-45deg);
  animation: icon-line-long 0.75s;
}

.icon-circle {
  top: -4px;
  left: -4px;
  z-index: 10;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  position: absolute;
  box-sizing: content-box;
  border: 4px solid rgba(76, 175, 80, 0.5);
}

.icon-fix {
  top: 8px;
  width: 5px;
  left: 26px;
  z-index: 1;
  height: 85px;
  position: absolute;
  transform: rotate(-45deg);
  background-color: white;
}

@keyframes rotate-circle {
  0% {
    transform: rotate(-45deg);
  }
  5% {
    transform: rotate(-45deg);
  }
  12% {
    transform: rotate(-405deg);
  }
  100% {
    transform: rotate(-405deg);
  }
}

@keyframes icon-line-tip {
  0% {
    width: 0;
    left: 1px;
    top: 19px;
  }
  54% {
    width: 0;
    left: 1px;
    top: 19px;
  }
  70% {
    width: 50px;
    left: -8px;
    top: 37px;
  }
  84% {
    width: 17px;
    left: 21px;
    top: 48px;
  }
  100% {
    width: 25px;
    left: 14px;
    top: 45px;
  }
}

@keyframes icon-line-long {
  0% {
    width: 0;
    right: 46px;
    top: 54px;
  }
  65% {
    width: 0;
    right: 46px;
    top: 54px;
  }
  84% {
    width: 55px;
    right: 0px;
    top: 35px;
  }
  100% {
    width: 47px;
    right: 8px;
    top: 38px;
  }
}

.success-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #4CAF50;
  margin-bottom: 0.5rem;
}

.success-message {
  color: #6c757d;
  font-size: 1rem;
}

.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-backdrop.show {
  opacity: 1;
}
</style>