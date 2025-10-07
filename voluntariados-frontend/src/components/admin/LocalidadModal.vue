<!-- src/components/admin/LocalidadModal.vue -->
<template>
  <div v-if="show" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-pin-map me-2"></i>
            {{ isEdit ? 'Editar Localidad' : 'Nueva Localidad' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="localidadName" class="form-label">Nombre *</label>
              <input 
                type="text" 
                class="form-control" 
                id="localidadName"
                v-model="localData.nombre"
                required
                placeholder="Ingrese el nombre de la localidad"
              >
            </div>
            <div class="mb-3">
              <label for="codigoPostal" class="form-label">Código Postal *</label>
              <input 
                type="text" 
                class="form-control" 
                id="codigoPostal"
                v-model="localData.codigo_postal"
                required
                placeholder="Ingrese el código postal"
              >
            </div>
            <div class="mb-3">
              <label for="departamento" class="form-label">Departamento *</label>
              <select 
                class="form-control" 
                id="departamento"
                v-model="localData.departamento"
                required
              >
                <option :value="null">Debe seleccionar un departamento</option>
                <option v-for="departamento in departamentos" :key="departamento.id" :value="departamento.id">
                  {{ departamento.nombre }}
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

interface Departamento {
  id: number
  nombre: string
}

export default defineComponent({
  name: 'LocalidadModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    localidadData: {
      type: Object as PropType<{ id: number | null; nombre: string; codigo_postal: string; departamento: number | null }>,
      required: true
    },
    departamentos: {
      type: Array as PropType<Departamento[]>,
      required: true
    }
  },
  data() {
    return {
      localData: {
        id: null as number | null,
        nombre: '',
        codigo_postal: '',
        departamento: null as number | null
      }
    }
  },
  watch: {
    localidadData: {
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
      if (!this.localData.codigo_postal.trim()) {
        alert('El código postal es requerido')
        return
      }
      if (!this.localData.departamento) {
        alert('Debe seleccionar un departamento')
        return
      }
      this.$emit('save', this.localData)
    }
  }
})
</script>