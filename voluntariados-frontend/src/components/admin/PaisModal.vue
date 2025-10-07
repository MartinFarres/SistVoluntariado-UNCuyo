<!-- src/components/admin/PaisModal.vue -->
<template>
  <div v-if="show" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-globe me-2"></i>
            {{ isEdit ? 'Edit Country' : 'New Country' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="countryName" class="form-label">Country Name *</label>
              <input 
                type="text" 
                class="form-control" 
                id="countryName"
                v-model="localData.nombre"
                required
                placeholder="Enter country name"
              >
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            Cancel
          </button>
          <button type="button" class="btn btn-primary" @click="handleSubmit">
            <i class="bi bi-check-lg me-1"></i>
            {{ isEdit ? 'Update' : 'Create' }}
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
  data() {
    return {
      localData: {
        id: null as number | null,
        nombre: ''
      }
    }
  },
  watch: {
    countryData: {
      immediate: true,
      handler(newVal) {
        this.localData = { ...newVal }
      }
    }
  },
  methods: {
    handleSubmit() {
      if (!this.localData.nombre.trim()) {
        alert('Country name is required')
        return
      }
      this.$emit('save', this.localData)
    }
  }
})
</script>