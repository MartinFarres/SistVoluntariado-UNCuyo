<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/UserModal.vue -->
<template>
  <div
    class="modal fade"
    :class="{ show: show, 'd-block': show }"
    tabindex="-1"
    v-if="show"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ isEdit ? 'Editar Usuario' : 'Crear Nuevo Usuario' }}</h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
            {{ errorMessage }}
            <button type="button" class="btn-close" @click="errorMessage = null"></button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label class="form-label">Email *</label>
              <input
                type="email"
                class="form-control"
                v-model="localData.email"
                required
              >
            </div>
            <div class="mb-3">
              <label class="form-label">
                Contraseña {{ isEdit ? '(dejar en blanco para mantener la actual)' : '*' }}
              </label>
              <input
                type="password"
                class="form-control"
                v-model="localData.password"
                :required="!isEdit"
                minlength="8"
              >
              <small class="text-muted">Mínimo 8 caracteres</small>
            </div>
            <div class="mb-3">
              <label class="form-label">Rol *</label>
              <select class="form-control" v-model="localData.role" required>
                <option value="VOL">Voluntario</option>
                <option value="DELEG">Delegado</option>
                <option value="ADMIN">Administrativo</option>
              </select>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleClose">Cancelar</button>
          <button
            type="button"
            class="btn btn-primary"
            @click="handleSubmit"
            :disabled="saving"
          >
            <span v-if="saving">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Guardando...
            </span>
            <span v-else>
              {{ isEdit ? 'Actualizar' : 'Crear' }}
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
  name: 'UserModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    userData: {
      type: Object as PropType<any>,
      required: true
    }
  },
  emits: ['close', 'save'],
  data() {
    return {
      localData: { ...this.userData },
      saving: false,
      errorMessage: null as string | null
    }
  },
  watch: {
    userData: {
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
      this.errorMessage = null
      this.$emit('close')
    },
    handleSubmit() {
      this.errorMessage = null
      this.saving = true
      this.$emit('save', this.localData, this.handleSaveResult)
    },
    handleSaveResult(success: boolean, errorMessage?: string) {
      this.saving = false
      if (!success && errorMessage) {
        this.errorMessage = errorMessage
      }
    }
  }
})
</script>

<style scoped>
.modal.show {
  background: rgba(0, 0, 0, 0.5);
}
</style>