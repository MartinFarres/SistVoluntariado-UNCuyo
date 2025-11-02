<!-- src/components/admin/DescripcionSelectorModal.vue -->
<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <div class="modal fade" :class="{ show: show, 'd-block': show }" tabindex="-1" v-if="show">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-card-text me-2"></i>
            Seleccionar Descripción
          </h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>

        <div class="modal-body">
          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>

          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <button class="btn btn-sm btn-primary me-2" @click="openCreate">
                <i class="bi bi-plus-lg me-1"></i> Crear nueva descripción
              </button>
              <button class="btn btn-sm btn-outline-secondary" @click="fetchList">
                <i class="bi bi-arrow-clockwise"></i> Refrescar
              </button>
            </div>
            <div>
              <input
                v-model="filter"
                class="form-control form-control-sm"
                placeholder="Buscar resumen..."
              />
            </div>
          </div>

          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border" role="status"></div>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-hover description-table">
              <thead>
                <tr>
                  <th style="width: 60px" class="text-center">ID</th>
                  <th style="width: 80px" class="text-center">Logo</th>
                  <th style="width: 100px" class="text-center">Portada</th>
                  <th style="width: 200px">Resumen</th>
                  <th>Descripción</th>
                  <th style="width: 180px" class="text-end">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="desc in filteredList" :key="desc.id" class="description-row">
                  <td class="text-center align-middle">
                    <span class="badge bg-secondary">{{ desc.id }}</span>
                  </td>
                  <td class="text-center align-middle">
                    <div class="image-preview">
                      <img
                        v-if="desc.logo"
                        :src="desc.logo"
                        :alt="`Logo ${desc.id}`"
                        class="img-thumbnail logo-thumb"
                        @click="openImageModal(desc.logo, 'Logo')"
                      />
                      <span v-else class="text-muted small">
                        <i class="bi bi-image"></i>
                      </span>
                    </div>
                  </td>
                  <td class="text-center align-middle">
                    <div class="image-preview">
                      <img
                        v-if="desc.portada"
                        :src="desc.portada"
                        :alt="`Portada ${desc.id}`"
                        class="img-thumbnail portada-thumb"
                        @click="openImageModal(desc.portada, 'Portada')"
                      />
                      <span v-else class="text-muted small">
                        <i class="bi bi-image"></i>
                      </span>
                    </div>
                  </td>
                  <td class="align-middle">
                    <div class="resumen-cell">
                      <strong class="d-block mb-1">{{ truncate(desc.resumen, 80) }}</strong>
                    </div>
                  </td>
                  <td class="align-middle">
                    <small class="text-muted">{{
                      truncate(desc.descripcion || "Sin descripción", 120)
                    }}</small>
                  </td>
                  <td class="text-end align-middle">
                    <div class="btn-group" role="group">
                      <button
                        class="btn btn-sm btn-primary"
                        @click="select(desc)"
                        title="Seleccionar esta descripción"
                      >
                        <i class="bi bi-check-circle me-1"></i>
                        Seleccionar
                      </button>
                      <button
                        class="btn btn-sm btn-outline-secondary"
                        @click="preview(desc)"
                        title="Ver detalles"
                      >
                        <i class="bi bi-eye"></i>
                      </button>
                      <button
                        class="btn btn-sm btn-outline-warning"
                        @click.stop="openEdit(desc)"
                        title="Editar"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="!filteredList.length">
                  <td colspan="6" class="text-center text-muted py-4">
                    <i class="bi bi-inbox fs-2 d-block mb-2"></i>
                    <span>No se encontraron descripciones</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Image Modal for full-size preview -->
          <div
            v-if="showImageModal"
            class="modal fade show d-block"
            tabindex="-1"
            @click.self="closeImageModal"
          >
            <div class="modal-dialog modal-dialog-centered modal-lg">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">{{ imageModalTitle }}</h5>
                  <button type="button" class="btn-close" @click="closeImageModal"></button>
                </div>
                <div class="modal-body text-center">
                  <img :src="imageModalSrc" class="img-fluid rounded" :alt="imageModalTitle" />
                </div>
              </div>
            </div>
          </div>

          <!-- Details Preview Modal -->
          <div
            v-if="showDetailsModal"
            class="modal fade show d-block"
            tabindex="-1"
            @click.self="closeDetailsModal"
          >
            <div class="modal-dialog modal-dialog-centered modal-xl">
              <div class="modal-content">
                <div class="modal-header bg-gradient-primary">
                  <h5 class="modal-title text-white">
                    <i class="bi bi-eye me-2"></i>
                    Vista Previa de Descripción
                  </h5>
                  <button
                    type="button"
                    class="btn-close btn-close-white"
                    @click="closeDetailsModal"
                  ></button>
                </div>
                <div class="modal-body" v-if="selectedDesc">
                  <div class="row">
                    <!-- Images Section -->
                    <div class="col-md-4">
                      <div class="preview-images">
                        <div class="mb-3">
                          <label class="form-label fw-bold text-muted small"
                            >LOGO DEL VOLUNTARIADO</label
                          >
                          <div class="image-container">
                            <img
                              v-if="selectedDesc.logo"
                              :src="selectedDesc.logo"
                              alt="Logo"
                              class="img-fluid rounded shadow-sm"
                              @click="openImageModal(selectedDesc.logo, 'Logo')"
                              style="cursor: pointer"
                            />
                            <div v-else class="no-image-placeholder">
                              <i class="bi bi-image fs-1 text-muted"></i>
                              <p class="text-muted small mb-0">Sin logo</p>
                            </div>
                          </div>
                        </div>
                        <div>
                          <label class="form-label fw-bold text-muted small"
                            >IMAGEN DE PORTADA</label
                          >
                          <div class="image-container">
                            <img
                              v-if="selectedDesc.portada"
                              :src="selectedDesc.portada"
                              alt="Portada"
                              class="img-fluid rounded shadow-sm"
                              @click="openImageModal(selectedDesc.portada, 'Portada')"
                              style="cursor: pointer"
                            />
                            <div v-else class="no-image-placeholder">
                              <i class="bi bi-image fs-1 text-muted"></i>
                              <p class="text-muted small mb-0">Sin portada</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Content Section -->
                    <div class="col-md-8">
                      <div class="preview-content">
                        <div class="mb-4">
                          <label class="form-label fw-bold text-muted small">ID</label>
                          <div>
                            <span class="badge bg-secondary fs-6">{{ selectedDesc.id }}</span>
                          </div>
                        </div>

                        <div class="mb-4">
                          <label class="form-label fw-bold text-muted small">RESUMEN</label>
                          <div class="content-box">
                            <p class="mb-0">{{ selectedDesc.resumen || "Sin resumen" }}</p>
                          </div>
                        </div>

                        <div class="mb-3">
                          <label class="form-label fw-bold text-muted small"
                            >DESCRIPCIÓN DETALLADA</label
                          >
                          <div class="content-box">
                            <p class="mb-0 text-muted" style="white-space: pre-wrap">
                              {{ selectedDesc.descripcion || "Sin descripción detallada" }}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button class="btn btn-secondary" @click="closeDetailsModal">
                    <i class="bi bi-x-circle me-2"></i>
                    Cerrar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" @click="handleClose">Cerrar</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Create Modal (uses existing DescripcionModal component) -->
  <DescripcionModal :show="showCreate" @close="showCreate = false" @save="handleCreate" />
  <DescripcionModal
    :show="showEdit"
    :initial="editItem"
    @close="
      () => {
        showEdit = false;
        editItem = null;
      }
    "
    @save="handleEditSave"
  />
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import DescripcionModal from "./DescripcionModal.vue";
import { descripcionAPI } from "@/services/api";

const props = defineProps<{ show: boolean }>();
const emit = defineEmits<{
  (e: "close"): void;
  (e: "select", payload: any): void;
}>();

const loading = ref(false);
const error = ref<string | null>(null);
const list = ref<any[]>([]);
const filter = ref("");
const showCreate = ref(false);

// Edit modal state
const showEdit = ref(false);
const editItem = ref<any>(null);

// Image modal state
const showImageModal = ref(false);
const imageModalSrc = ref("");
const imageModalTitle = ref("");

// Details modal state
const showDetailsModal = ref(false);
const selectedDesc = ref<any>(null);

watch(
  () => props.show,
  (v) => {
    if (v) fetchList();
  }
);

async function fetchList() {
  loading.value = true;
  error.value = null;
  try {
    const res = await descripcionAPI.getAll();
    list.value = res.data || [];
  } catch (err: any) {
    console.error("Error fetching descriptions", err);
    error.value = err.response?.data?.detail || "Error al cargar descripciones";
  } finally {
    loading.value = false;
  }
}

const filteredList = computed(() => {
  const q = filter.value.trim().toLowerCase();
  if (!q) return list.value;
  return list.value.filter(
    (d) =>
      (d.resumen || "").toLowerCase().includes(q) || (d.descripcion || "").toLowerCase().includes(q)
  );
});

function truncate(text: string, max = 80) {
  if (!text) return "";
  return text.length > max ? text.slice(0, max) + "…" : text;
}

function handleClose() {
  emit("close");
}

function select(desc: any) {
  emit("select", desc);
}

function preview(desc: any) {
  selectedDesc.value = desc;
  showDetailsModal.value = true;
}

function closeDetailsModal() {
  showDetailsModal.value = false;
  selectedDesc.value = null;
}

function selectFromPreview() {
  if (selectedDesc.value) {
    emit("select", selectedDesc.value);
    closeDetailsModal();
    handleClose();
  }
}

function openImageModal(src: string, title: string) {
  imageModalSrc.value = src;
  imageModalTitle.value = title;
  showImageModal.value = true;
}

function closeImageModal() {
  showImageModal.value = false;
  imageModalSrc.value = "";
  imageModalTitle.value = "";
}

function openCreate() {
  showCreate.value = true;
}

function openEdit(desc: any) {
  editItem.value = desc;
  showEdit.value = true;
}

async function handleCreate(payload: { id: number | null; formData: FormData }) {
  try {
    // Forward to API — backend expects multipart when files present; axios will handle headers
    const res = await descripcionAPI.create(payload.formData as any);
    const created = res.data;
    // add to list and select
    list.value.unshift(created);
    showCreate.value = false;
    emit("select", created);
    emit("close");
  } catch (err) {
    console.error("Error creating descripcion", err);
    alert("Error al crear la descripción");
  }
}

async function handleEditSave(payload: { id: number | null; formData: FormData }) {
  try {
    if (!payload.id) {
      // fallback to create if no id
      const res = await descripcionAPI.create(payload.formData as any);
      const created = res.data;
      // replace or add
      list.value.unshift(created);
      emit("select", created);
    } else {
      const res = await descripcionAPI.update(Number(payload.id), payload.formData as any);
      const updated = res.data;
      // update the item in the list
      const idx = list.value.findIndex((d) => d.id === updated.id);
      if (idx !== -1) {
        list.value.splice(idx, 1, updated);
      } else {
        // if not present, add to top
        list.value.unshift(updated);
      }
      // optionally select updated
      emit("select", updated);
    }

    showEdit.value = false;
    editItem.value = null;
    emit("close");
  } catch (err: any) {
    console.error("Error updating descripcion", err);
    alert(err.response?.data?.detail || "Error al actualizar la descripción");
  }
}
</script>

<style scoped>
/* Table styling */
.description-table {
  margin-bottom: 0;
  border-collapse: separate;
  border-spacing: 0;
}

.description-table thead th {
  /* Softer header: neutral background to avoid heavy brand colors */
  background-color: #f8f9fa;
  color: #343a40;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  padding: 1rem 0.75rem;
  border: none;
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid #e9ecef;
}

.description-table thead th:first-child {
  border-top-left-radius: 0.5rem;
}

.description-table thead th:last-child {
  border-top-right-radius: 0.5rem;
}

.description-row {
  transition: all 0.2s ease;
  cursor: pointer;
}

.description-row:hover {
  background-color: #f8f9fa;
  transform: scale(1.005);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.description-row td {
  padding: 1rem 0.75rem;
  vertical-align: middle;
  border-bottom: 1px solid #e9ecef;
}

/* Image thumbnails */
.image-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60px;
}

.logo-thumb,
.portada-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #dee2e6;
  border-radius: 0.375rem;
}

.logo-thumb:hover,
.portada-thumb:hover {
  transform: scale(1.08);
  border-color: #adb5bd; /* subtle neutral accent on hover */
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  z-index: 5;
}

.portada-thumb {
  width: 90px;
  height: 60px;
}

/* Resumen cell */
.resumen-cell strong {
  color: #495057;
  font-size: 0.95rem;
  line-height: 1.4;
}

/* Badge styling */
.badge {
  font-weight: 600;
  font-size: 0.85rem;
  padding: 0.35rem 0.65rem;
}

/* Button group */
.btn-group .btn {
  transition: all 0.2s ease;
}

.btn-primary {
  /* Neutral primary for lists and small actions */
  background-color: #ffffff;
  color: #212529;
  border: 1px solid #dee2e6;
  box-shadow: none !important;
  text-shadow: none !important;
}

.btn-primary:hover {
  background-color: #f1f3f5;
  color: #212529;
  transform: translateY(-1px);
  box-shadow: none !important;
}

/* Empty state */
.description-table tbody tr td i.bi-inbox {
  color: #adb5bd;
}

/* Responsive table */
.table-responsive {
  max-height: 500px;
  overflow-y: auto;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.table-responsive::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.table-responsive::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-responsive::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.table-responsive::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Image modal overlay: the backdrop opacity is handled in shared CSS */

/* Action buttons hover */
.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
  transform: translateY(-1px);
}

/* Details Preview Modal */
.bg-gradient-primary {
  background-color: var(--brand-end);
}

.preview-images .image-container {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #dee2e6;
  transition: all 0.3s ease;
}


.preview-images .image-container img {
  max-height: 200px;
  transition: transform 0.3s ease;
}

.preview-images .image-container img:hover {
  transform: scale(1.05);
}

.no-image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.preview-content .content-box {
  background: #f8f9fa;
  border-left: 4px solid #adb5bd; /* neutral accent */
  padding: 1rem;
  border-radius: 0.375rem;
  min-height: 60px;
}

/* Make the details preview header follow the global modal theme instead of brand gradient */
.bg-gradient-primary {
  background-color: rgb(228, 228, 228) !important;
}
.bg-gradient-primary .modal-title {
  color: #343a40 !important;
}

.preview-content .content-box p {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #495057;
}

.form-label.fw-bold {
  color: var(--brand-accent);
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}

/* Search input styling */
.form-control-sm {
  border-radius: 0.375rem;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
}

.form-control-sm:focus {
  border-color: var(--brand-end);
  box-shadow: 0 0 0 0.2rem rgba(135, 206, 235, 0.15);
}

/* Button styling improvements */
.btn {
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(108, 117, 125, 0.2);
}

.btn-close-white {
  filter: brightness(0) invert(1);
}
</style>
