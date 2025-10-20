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
        <i class="bi bi-arrow-clockwise"></i> Reintentar
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
            <th v-for="column in columns" :key="column.key" :class="getAlignmentClass(column.align)">
              {{ column.label }}
            </th>
            <th v-if="showActions">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="item in pagedItems" 
            :key="item[itemKey]"
            :class="{ 'clickable-row': clickableRows }"
            @click="clickableRows ? $emit('row-click', item) : undefined"
          >
            <td v-for="column in columns" :key="column.key" :class="getAlignmentClass(column.align)">
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
                  @click.stop="$emit('edit', item)"
                  title="Edit"
                >
                  <i class="bi bi-pencil"></i>
                </button>
                <button 
                  v-if="showDelete"
                  class="btn btn-sm btn-outline-danger" 
                  @click.stop="$emit('delete', item)"
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
            {{ footerText || `${pageStartIndex}-${pageEndIndex} de ${items.length}` }}
          </small>
        </div>
        <div v-if="$slots.pagination">
          <slot name="pagination"></slot>
        </div>
        <div v-else class="d-flex align-items-center gap-2">
          <button class="btn btn-sm btn-outline-secondary" :disabled="currentPage === 1" @click="prevPage">
            <i class="bi bi-chevron-left"></i>
          </button>
          <span class="mx-2 small text-muted">Página {{ currentPage }} / {{ totalPages }}</span>
          <button class="btn btn-sm btn-outline-secondary" :disabled="currentPage === totalPages" @click="nextPage">
            <i class="bi bi-chevron-right"></i>
          </button>
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
  align?: 'left' | 'center' | 'right'
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
      default: 'Crear nuevo'
    },
    emptyText: {
      type: String,
      default: 'Vacío'
    },
    loadingText: {
      type: String,
      default: 'Cargando...'
    },
    footerText: {
      type: String,
      default: ''
    },
    showRetry: {
      type: Boolean,
      default: true
    },
    clickableRows: {
      type: Boolean,
      default: false
    },
    pageSize: {
      type: Number,
      default: 10
    }
  },
  emits: ['create', 'edit', 'delete', 'retry', 'row-click'],
  data() {
    return {
      currentPage: 1
    }
  },
  computed: {
    totalPages(): number {
      if (!this.items || this.items.length === 0) return 1
      return Math.ceil(this.items.length / this.pageSize)
    },
    pagedItems(): any[] {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return (this.items || []).slice(start, end)
    },
    pageStartIndex(): number {
      if (!this.items || this.items.length === 0) return 0
      return (this.currentPage - 1) * this.pageSize + 1
    },
    pageEndIndex(): number {
      if (!this.items || this.items.length === 0) return 0
      return Math.min(this.currentPage * this.pageSize, this.items.length)
    }
  },
  watch: {
    items() {
      // Clamp page when data changes
      if (this.currentPage > this.totalPages) this.currentPage = this.totalPages
      if (this.currentPage < 1) this.currentPage = 1
    }
  },
  methods: {
    getNestedValue(obj: any, path: string): any {
      return path.split('.').reduce((acc, part) => acc && acc[part], obj)
    },
    getAlignmentClass(align?: string): string {
      switch (align) {
        case 'center': return 'text-center'
        case 'right': return 'text-end'
        case 'left': 
        default: return 'text-start'
      }
    },
    goToPage(page: number) {
      const target = Math.min(Math.max(1, page), this.totalPages)
      this.currentPage = target
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage += 1
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage -= 1
    }
  }
})
</script>

<style>
/* Global styles for clickable rows - needed to override Bootstrap */
.table tbody tr.clickable-row {
  cursor: pointer !important;
  transition: all 0.15s ease-in-out !important;
}

.table tbody tr.clickable-row:hover {
  background-color: rgba(108, 117, 125, 0.10) !important; /* Neutral grey tint */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
}

.table tbody tr.clickable-row:hover td {
  background-color: rgba(108, 117, 125, 0.10) !important;
}

.table tbody tr.clickable-row:active {
  background-color: rgba(108, 117, 125, 0.15) !important;
}

.table tbody tr.clickable-row:active td {
  background-color: rgba(108, 117, 125, 0.15) !important;
}
</style>

<style scoped>
.card {
  border: 0;
  box-shadow: 0 0 2rem 0 rgba(136, 152, 170, 0.15);
  margin-top: calc(var(--bs-gutter-x) * .5);
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

/* Clickable row styles with maximum specificity */
.card .table-responsive .table.table-flush tbody tr.clickable-row {
  cursor: pointer !important;
  transition: all 0.15s ease-in-out !important;
}

.card .table-responsive .table.table-flush tbody tr.clickable-row:hover {
  background-color: rgba(108, 117, 125, 0.08) !important; /* Neutral grey tint */
  transform: scale(1.002) !important;
}

.card .table-responsive .table.table-flush tbody tr.clickable-row:hover td {
  background-color: rgba(108, 117, 125, 0.08) !important;
}

.card .table-responsive .table.table-flush tbody tr.clickable-row:active {
  background-color: rgba(108, 117, 125, 0.12) !important;
  transform: scale(1.001) !important;
}

.card .table-responsive .table.table-flush tbody tr.clickable-row:active td {
  background-color: rgba(108, 117, 125, 0.12) !important;
}
</style>