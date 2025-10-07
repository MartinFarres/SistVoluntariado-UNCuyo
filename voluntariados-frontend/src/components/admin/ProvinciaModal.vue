<!-- src/components/admin/ProvinciaModal.vue -->
<template>
  <div v-if="show" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-geo-alt me-2"></i>
            {{ isEdit ? 'Editar Provincia' : 'Nueva Provincia' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="provinciaName" class="form-label">Nombre *</label>
              <input 
                type="text" 
                class="form-control" 
                id="provinciaName"
                v-model="localData.nombre"
                required
                placeholder="Ingrese el nombre de la provincia"
              >
            </div>
            <div class="mb-3">
              <label for="pais" class="form-label">País *</label>
              <select 
                class="form-control" 
                id="pais"
                v-model="localData.pais"
                required
              >
                <option :value="null" disabled>Debe seleccionar un país</option>
                <option v-for="pais in paises" :key="pais.id" :value="pais.id">
                  {{ pais.nombre }}
                </option>
              </select>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            Cancelar
          </button>
          <button type="button" class="btn btn-primary" @click="handleSubmit">
            <i class="bi bi-check-lg me-1"></i>
            {{ isEdit ? 'Actualizar' : 'Crear' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

interface Pais {
  id: number
  nombre: string
}

export default defineComponent({
  name: 'ProvinciaModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    provinciaData: {
      type: Object as PropType<{ id: number | null; nombre: string; pais: number | null }>,
      required: true
    },
    paises: {
      type: Array as PropType<Pais[]>,
      required: true
    }
  },
  data() {
    return {
      localData: {
        id: null as number | null,
        nombre: '',
        pais: null as number | null,
      }
    }
  },
  watch: {
    provinciaData: {
      immediate: true,
      handler(newVal) {
        this.localData = { ...newVal }
      }
    }
  },
  methods: {
    handleSubmit() {
      if (!this.localData.nombre.trim()) {
        alert('El nombre es requerido')
        return
      }
      if (!this.localData.pais) {
        alert('Debe seleccionar un país')
        return
      }
      this.$emit('save', this.localData)
    }
  }
})
</script>