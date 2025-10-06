<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/AdminTable.vue -->
<template>
  <div class="card shadow">
    <!-- Card header -->
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0">{{ title }}</h3>
        </div>
        
      </div>
      
      <!-- Filters Slot -->
      <div v-if="$slots.filters" class="row mt-3">
        <slot name="filters"></slot>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-muted mt-3">{{ loadingText }}</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger m-4">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
      <button 
        v-if="showRetry" 
        @click="$emit('retry')" 
        class="btn btn-sm btn-outline-danger ms-3"
      >
        <i class="bi bi-arrow-clockwise"></i> Retry
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="items.length === 0" class="text-center py-5">
      <i class="bi bi-inbox fs-1 text-muted d-block mb-3"></i>
      <h5 class="text-muted">{{ emptyText }}</h5>
      <button 
        v-if="showCreateButton" 
        @click="$emit('create')" 
        class="btn btn-primary mt-3"
      >
        <i class="bi bi-plus"></i> {{ createButtonText }}
      </button>
    </div>

    <!-- Table -->
    <div v-else class="table-responsive">
      <table class="table align-items-center table-flush">
        <thead class="thead-light">
          <tr>
            <th v-for="column in columns" :key="column.key">
              {{ column.label }}
            </th>
            <th v-if="showActions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item[itemKey]">
            <td v-for="column in columns" :key="column.key">
              <!-- Custom cell content via slot -->
              <slot 
                :name="`cell-${column.key}`" 
                :item="item" 
                :value="getNestedValue(item, column.key)"
              >
                <!-- Default cell rendering -->
                {{ getNestedValue(item, column.key) }}
              </slot>
            </td>
            <td v-if="showActions">
              <slot name="actions" :item="item">
                <!-- Default actions -->
                <button 
                  v-if="showEdit"
                  class="btn btn-sm btn-outline-primary me-1" 
                  @click="$emit('edit', item)"
                  title="Edit"
                >
                  <i class="bi bi-pencil"></i>
                </button>
                <button 
                  v-if="showDelete"
                  class="btn btn-sm btn-outline-danger" 
                  @click="$emit('delete', item)"
                  title="Delete"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Footer / Pagination -->
    <div v-if="items.length > 0" class="card-footer py-4">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <small class="text-muted">
            {{ footerText }}
          </small>
        </div>
        <div v-if="$slots.pagination">
          <slot name="pagination"></slot>
        </div>
        <div class="col text-end" v-if="showCreateButton">
            <button class="btn btn-sm btn-primary" @click="$emit('create')">
              <i class="bi bi-plus"></i> {{ createButtonText }}
            </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

export interface TableColumn {
  key: string
  label: string
  sortable?: boolean
}

export default defineComponent({
  name: 'AdminTable',
  props: {
    title: {
      type: String,
      required: true
    },
    columns: {
      type: Array as PropType<TableColumn[]>,
      required: true
    },
    items: {
      type: Array as PropType<any[]>,
      default: () => []
    },
    itemKey: {
      type: String,
      default: 'id'
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: undefined,
    },
    showActions: {
      type: Boolean,
      default: true
    },
    showEdit: {
      type: Boolean,
      default: true
    },
    showDelete: {
      type: Boolean,
      default: true
    },
    showCreateButton: {
      type: Boolean,
      default: true
    },
    createButtonText: {
      type: String,
      default: 'Create New'
    },
    emptyText: {
      type: String,
      default: 'No items found'
    },
    loadingText: {
      type: String,
      default: 'Loading...'
    },
    footerText: {
      type: String,
      default: ''
    },
    showRetry: {
      type: Boolean,
      default: true
    }
  },
  emits: ['create', 'edit', 'delete', 'retry'],
  methods: {
    getNestedValue(obj: any, path: string): any {
      return path.split('.').reduce((acc, part) => acc && acc[part], obj)
    }
  }
})
</script>

<style scoped>
.card {
  border: 0;
  box-shadow: 0 0 2rem 0 rgba(136, 152, 170, 0.15);
}

.table thead th {
  padding: 0.75rem 1rem;
  text-transform: uppercase;
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 1px;
  border-bottom: 1px solid #e9ecef;
}

.table-flush tbody tr:first-child td {
  border-top: 0;
}

.card-footer {
  background-color: transparent;
  border-top: 1px solid #e9ecef;
}
</style>