<!-- src/components/admin/PaisModal.vue -->
<template>
  <div v-if="show" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-globe me-2"></i>
            {{ isEdit ? 'Editar País' : 'Nuevo País' }}
          </h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
            {{ errorMessage }}
            <button type="button" class="btn-close" @click="errorMessage = null"></button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="countryName" class="form-label">Nombre *</label>
              <input
                type="text"
                class="form-control"
                id="countryName"
                v-model="localData.nombre"
                required
                placeholder="Ingrese el nombre del país"
              >
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleClose">
            Cancelar
          </button>
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
              <i class="bi bi-check-lg me-1"></i>
              {{ isEdit ? 'Actualizar' : 'Crear' }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

export default defineComponent({
  name: 'PaisModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    countryData: {
      type: Object as PropType<{ id: number | null; nombre: string }>,
      required: true
    }
  },
  emits: ['close', 'save'],
  data() {
    return {
      localData: {
        id: null as number | null,
        nombre: ''
      },
      saving: false,
      errorMessage: null as string | null
    }
  },
  watch: {
    countryData: {
      immediate: true,
      handler(newVal) {
        this.localData = { ...newVal }
      }
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
      if (!this.localData.nombre.trim()) {
        this.errorMessage = 'El nombre del país es requerido'
        return
      }
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