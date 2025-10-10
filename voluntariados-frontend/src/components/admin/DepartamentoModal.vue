<!-- src/components/admin/DepartamentoModal.vue -->
<template>
  <div v-if="show" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-building me-2"></i>
            {{ isEdit ? 'Editar Departamento' : 'Nuevo Departamento' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="departamentoName" class="form-label">Nombre *</label>
              <input 
                type="text" 
                class="form-control" 
                id="departamentoName"
                v-model="localData.nombre"
                required
                placeholder="Ingrese el nombre del departamento"
              >
            </div>
            <div class="mb-3">
              <label for="provincia" class="form-label">Provincia *</label>
              <select 
                class="form-control" 
                id="provincia"
                v-model="localData.provincia"
                required
              >
                <option :value="null">Debe seleccionar una provincia</option>
                <option v-for="provincia in provincias" :key="provincia.id" :value="provincia.id">
                  {{ provincia.nombre }}
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

interface Provincia {
  id: number
  nombre: string
}

export default defineComponent({
  name: 'DepartamentoModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    departamentoData: {
      type: Object as PropType<{ id: number | null; nombre: string; provincia: number | null }>,
      required: true
    },
    provincias: {
      type: Array as PropType<Provincia[]>,
      required: true
    }
  },
  data() {
    return {
      localData: {
        id: null as number | null,
        nombre: '',
        provincia: null as number | null
      }
    }
  },
  watch: {
    departamentoData: {
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
      if (!this.localData.provincia) {
        alert('Debe seleccionar una provincia')
        return
      }
      this.$emit('save', this.localData)
    }
  }
})
</script>