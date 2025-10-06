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
          <h5 class="modal-title">{{ isEdit ? 'Edit User' : 'Create New User' }}</h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
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
                Password {{ isEdit ? '(leave blank to keep current)' : '*' }}
              </label>
              <input 
                type="password" 
                class="form-control" 
                v-model="localData.password" 
                :required="!isEdit"
                minlength="8"
              >
              <small class="text-muted">Minimum 8 characters</small>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Role *</label>
              <select class="form-control" v-model="localData.role" required>
                <option value="VOL">Voluntario</option>
                <option value="DELEG">Delegado</option>
                <option value="ADMIN">Administrativo</option>
              </select>
            </div>
            
            <div class="mb-3 form-check">
              <input 
                type="checkbox" 
                class="form-check-input" 
                id="isActive"
                v-model="localData.is_active"
              >
              <label class="form-check-label" for="isActive">
                Active
              </label>
            </div>
            
            <div class="mb-3 form-check">
              <input 
                type="checkbox" 
                class="form-check-input" 
                id="isStaff"
                v-model="localData.is_staff"
              >
              <label class="form-check-label" for="isStaff">
                Staff Member
              </label>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleClose">Cancel</button>
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
      this.$emit('close')
    },
    async handleSubmit() {
      this.errorMessage = null
      this.saving = true
      
      try {
        await this.$emit('save', this.localData)
      } catch (error: any) {
        this.errorMessage = error.message || 'Failed to save user'
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
</style>