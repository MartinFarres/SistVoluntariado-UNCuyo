<template>
  <AdminLayout
    page-title="Administración de Encabezados"
    :breadcrumbs="[{ label: 'Encabezados' }]"
  >
    <template #header-actions>
      <button class="btn btn-light" @click="openCreateModal">
        <i class="bi bi-plus"></i> Nuevo Encabezado
      </button>
    </template>



    <div class="row">
      <div class="col">
        <AdminTable
          title="Encabezados"
          :columns="columns"
          :items="encabezados"
          :loading="loading"
          :error="error"
          :footer-text="`Mostrando ${encabezados.length} encabezado(s)`"
          empty-text="No se encontraron encabezados. ¡Crea el primero!"
          :showCreateButton= "false"
          @create="openCreateModal"
          @edit="editEncabezado"
          @delete="confirmDelete"
          @retry="fetchEncabezados"
        >
          <!-- Imagen 1 -->
          <template #cell-imagen_1="{ item }">
            <div v-if="item.imagen_1">
              <img :src="item.imagen_1" alt="Logo 1" style="height: 40px; object-fit: contain;">
            </div>
            <div v-else class="text-muted">Sin imagen</div>
          </template>

          <!-- Imagen 2 -->
          <template #cell-imagen_2="{ item }">
            <div v-if="item.imagen_2">
              <img :src="item.imagen_2" alt="Logo 2" style="height: 40px; object-fit: contain;">
            </div>
            <div v-else class="text-muted">Sin imagen</div>
          </template>

          <!-- Imagen 3 -->
          <template #cell-imagen_3="{ item }">
            <div v-if="item.imagen_3">
              <img :src="item.imagen_3" alt="Logo 3" style="height: 40px; object-fit: contain;">
            </div>
            <div v-else class="text-muted">Sin imagen</div>
          </template>

          <!-- Imagen 4 -->
          <template #cell-imagen_4="{ item }">
            <div v-if="item.imagen_4">
              <img :src="item.imagen_4" alt="Logo 4" style="height: 40px; object-fit: contain;">
            </div>
            <div v-else class="text-muted">Sin imagen</div>
          </template>
        </AdminTable>
        <div class="d-flex w-100 justify-content-end">
          <button
            class="btn btn-sm btn-primary"
            @click="openCreateModal"
            :disabled="encabezados.length > 0"
          >
            <i class="bi bi-plus"></i> Nuevo Encabezado
          </button>
        </div>
      </div>
    </div>


    <!-- Modal -->
    <EncabezadoModal
      v-if="showEncabezadoModal"
      :show="showEncabezadoModal"
      :is-edit="isEditMode"
      :encabezado-data="formData"
      @close="closeModal"
      @save="saveEncabezado"
    />
  </AdminLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminTable, { type TableColumn } from '@/components/admin/AdminTable.vue'
import EncabezadoModal from '@/components/admin/EncabezadoModal.vue'
import { encabezadoAPI } from '@/services/api'

const createInitialFormData = () => ({
  id: null,
  imagen_1: null as File | null,
  imagen_2: null as File | null,
  imagen_3: null as File | null,
  imagen_4: null as File | null
})

export default defineComponent({
  name: 'AdminEncabezados',
  components: {
    AdminLayout,
    AdminTable,
    EncabezadoModal
  },
  data() {
    return {
      loading: false,
      error: null as string | null,
      encabezados: [] as any[],
      showEncabezadoModal: false,
      isEditMode: false,
      formData: createInitialFormData(),
      columns: [
        { key: 'imagen_1', label: 'Logo 1' },
        { key: 'imagen_2', label: 'Logo 2' },
        { key: 'imagen_3', label: 'Logo 3' },
        { key: 'imagen_4', label: 'Logo 4' }
      ] as TableColumn[]
    }
  },
  mounted() {
    this.fetchEncabezados()
  },
  methods: {
    async fetchEncabezados() {
      this.loading = true
      this.error = null
      try {
        const response = await encabezadoAPI.getAll()
        this.encabezados = response.data
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Error al cargar encabezados'
      } finally {
        this.loading = false
      }
    },
    openCreateModal() {
      this.formData = createInitialFormData()
      this.isEditMode = false
      this.showEncabezadoModal = true
    },
    editEncabezado(encabezado: any) {
      this.formData = { ...encabezado }
      this.isEditMode = true
      this.showEncabezadoModal = true
    },
    async saveEncabezado(files: Record<number, File>) {
      try {
        const form = new FormData()
        if (files[1] instanceof File) form.append('imagen_1', files[1])
        if (files[2] instanceof File) form.append('imagen_2', files[2])
        if (files[3] instanceof File) form.append('imagen_3', files[3])
        if (files[4] instanceof File) form.append('imagen_4', files[4])

        if (this.isEditMode && this.formData.id) {
          await encabezadoAPI.update(this.formData.id, form)
        } else {
          await encabezadoAPI.create(form)
        }

        this.closeModal()
        await this.fetchEncabezados()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al guardar el encabezado')
      }
    },
    confirmDelete(encabezado: any) {
      if (confirm(`¿Estás seguro de que quieres eliminar este encabezado?`)) {
        this.deleteEncabezado(encabezado.id)
      }
    },
    async deleteEncabezado(id: number) {
      try {
        await encabezadoAPI.delete(id)
        await this.fetchEncabezados()
      } catch (err: any) {
        alert(err.response?.data?.detail || 'Error al eliminar el encabezado')
      }
    },
    closeModal() {
      this.showEncabezadoModal = false
      this.isEditMode = false
    }
  }
})
</script>

<style scoped>
img {
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f8f9fa;
}
</style>
