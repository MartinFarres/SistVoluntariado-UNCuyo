<!-- src/components/admin/OrganizacionModal.vue -->
<template>
  <div
    v-if="show"
    class="modal fade show d-block align-items-center justify-content-center"
    tabindex="-1"
    style="background-color: rgba(0, 0, 0, 0.5); display: flex; min-height: 100vh"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-building me-2"></i>
            {{ isEdit ? "Editar Organización" : "Nueva Organización" }}
          </h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
            {{ errorMessage }}
            <button type="button" class="btn-close" @click="errorMessage = null"></button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="row">
              <!-- Nombre -->
              <div class="col-md-6 mb-3">
                <label for="organizationName" class="form-label">Nombre *</label>
                <input
                  type="text"
                  class="form-control"
                  id="organizationName"
                  v-model="localData.nombre"
                  required
                  placeholder="Ingrese el nombre de la organización"
                  maxlength="200"
                />
              </div>

              <!-- Estado -->
              <div class="col-md-6 mb-3">
                <label for="organizationStatus" class="form-label">Estado</label>
                <select class="form-select" id="organizationStatus" v-model="localData.activo">
                  <option :value="true">Activo</option>
                  <option :value="false">Inactivo</option>
                </select>
              </div>
            </div>

            <div class="row">
              <!-- Email de contacto -->
              <div class="col-md-6 mb-3">
                <label for="contactEmail" class="form-label">Email de contacto</label>
                <input
                  type="email"
                  class="form-control"
                  id="contactEmail"
                  v-model="localData.contacto_email"
                  placeholder="contacto@organizacion.com"
                  maxlength="254"
                />
              </div>

              <!-- Localidad -->
              <div class="col-md-6 mb-3">
                <label for="localidad" class="form-label">Localidad</label>
                <select class="form-select" id="localidad" v-model="localData.localidad">
                  <option value="">Seleccionar localidad...</option>
                  <option
                    v-for="localidad in localidades"
                    :key="localidad.id"
                    :value="localidad.id"
                  >
                    {{ localidad.nombre }}
                  </option>
                </select>
              </div>
            </div>

            <div class="row">
              <!-- Slogan -->
              <div class="col-md-6 mb-3">
                <label for="slogan" class="form-label">Slogan (opcional)</label>
                <input
                  id="slogan"
                  type="text"
                  class="form-control"
                  v-model="localData.slogan"
                  maxlength="255"
                  placeholder="Frase breve o slogan"
                />
              </div>

              <!-- URL -->
              <div class="col-md-6 mb-3">
                <label for="orgUrl" class="form-label">Sitio web (opcional)</label>
                <input
                  id="orgUrl"
                  type="url"
                  class="form-control"
                  v-model="localData.url"
                  placeholder="https://www.organizacion.org"
                />
              </div>
            </div>

            <!-- Descripción -->
            <div class="mb-3">
              <label for="description" class="form-label">Descripción</label>
              <textarea
                class="form-control"
                id="description"
                v-model="localData.descripcion"
                rows="3"
                placeholder="Descripción de la organización..."
              ></textarea>
            </div>

            <div class="row">
              <!-- Logo -->
              <div class="col-md-6 mb-3">
                <label class="form-label">Logo (opcional)</label>
                <input type="file" accept="image/*" class="form-control" @change="onLogoChange" />
                <div v-if="logoPreview" class="mt-2">
                  <img
                    :src="logoPreview"
                    alt="Logo preview"
                    class="img-thumbnail"
                    style="max-width: 120px; max-height: 120px"
                  />
                </div>
              </div>

              <!-- Banner -->
              <div class="col-md-6 mb-3">
                <label class="form-label">Banner / Portada (opcional)</label>
                <input type="file" accept="image/*" class="form-control" @change="onBannerChange" />
                <div v-if="bannerPreview" class="mt-2">
                  <img
                    :src="bannerPreview"
                    alt="Banner preview"
                    class="img-thumbnail"
                    style="max-width: 240px; max-height: 120px"
                  />
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleClose">Cancelar</button>
          <button type="button" class="btn btn-primary" @click="handleSubmit" :disabled="saving">
            <span v-if="saving">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Guardando...
            </span>
            <span v-else>
              <i class="bi bi-check-lg me-1"></i>
              {{ isEdit ? "Actualizar" : "Crear" }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";
import { ubicacionAPI } from "@/services/api";

interface Localidad {
  id: number;
  nombre: string;
}

interface OrganizacionFormData {
  id: number | null;
  nombre: string;
  activo: boolean;
  descripcion: string;
  contacto_email: string;
  localidad: number | null;
  direccion?: string | null;
  logo?: string | null;
  banner?: string | null;
  slogan?: string | null;
  url?: string | null;
}

export default defineComponent({
  name: "OrganizacionModal",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    organizationData: {
      type: Object as PropType<OrganizacionFormData>,
      required: true,
    },
  },
  emits: ["close", "save"],
  data() {
    return {
      localData: {
        id: null as number | null,
        nombre: "",
        activo: true,
        descripcion: "",
        contacto_email: "",
        localidad: null as number | null,
        // existing preview urls
        logo: null as string | null,
        banner: null as string | null,
        slogan: null as string | null,
        url: null as string | null,
      } as OrganizacionFormData,
      saving: false,
      errorMessage: null as string | null,
      localidades: [] as Localidad[],
      logoFile: null as File | null,
      bannerFile: null as File | null,
      logoPreview: null as string | null,
      bannerPreview: null as string | null,
    };
  },
  watch: {
    organizationData: {
      immediate: true,
      handler(newVal) {
        this.localData = { ...newVal };
        // keep previews if present (handle either object or primitive)
        const nv: any = newVal as any;
        this.logoPreview = nv?.logo || null;
        this.bannerPreview = nv?.banner || null;
        this.localData.slogan = nv?.slogan || null;
        this.localData.url = nv?.url || null;
      },
    },
    show(newVal) {
      if (newVal) {
        this.errorMessage = null;
        this.saving = false;
        this.loadLocalidades();
      }
    },
  },
  methods: {
    onLogoChange(e: Event) {
      const input = e.target as HTMLInputElement;
      if (input.files && input.files[0]) {
        this.logoFile = input.files[0];
        this.logoPreview = URL.createObjectURL(this.logoFile);
      } else {
        this.logoFile = null;
        this.logoPreview = null;
      }
    },

    onBannerChange(e: Event) {
      const input = e.target as HTMLInputElement;
      if (input.files && input.files[0]) {
        this.bannerFile = input.files[0];
        this.bannerPreview = URL.createObjectURL(this.bannerFile);
      } else {
        this.bannerFile = null;
        this.bannerPreview = null;
      }
    },
    async loadLocalidades() {
      try {
        const response = await ubicacionAPI.getLocalidades();
        this.localidades = response.data;
      } catch (err) {
        console.error("Error loading localidades:", err);
      }
    },

    handleClose() {
      this.errorMessage = null;
      this.$emit("close");
    },

    handleSubmit() {
      if (!this.localData.nombre.trim()) {
        this.errorMessage = "El nombre de la organización es requerido";
        return;
      }

      this.errorMessage = null;
      this.saving = true;

      // Prepare data for API - convert empty strings to null
      // If files were selected, build FormData
      if (this.logoFile || this.bannerFile) {
        const formData = new FormData();
        if (this.localData.id) formData.append("id", String(this.localData.id));
        formData.append("nombre", this.localData.nombre);
        formData.append("activo", String(this.localData.activo));
        if (this.localData.descripcion) formData.append("descripcion", this.localData.descripcion);
        if (this.localData.contacto_email)
          formData.append("contacto_email", this.localData.contacto_email);
        if (this.localData.localidad)
          formData.append("localidad", String(this.localData.localidad));
        if (this.localData.direccion) formData.append("direccion", this.localData.direccion);
        if (this.logoFile) formData.append("logo", this.logoFile);
        if (this.bannerFile) formData.append("banner", this.bannerFile);

        this.$emit("save", formData, this.handleSaveResult);
      } else {
        // When no new files are selected, don't send the existing logo/banner URLs
        // as part of the JSON payload — DRF ImageField expects files for write and
        // sending the URL string can cause validation errors. Omitting these
        // fields leaves the server-stored images intact.
        // copy and remove logo/banner so they are not sent as string URLs
        const rest = { ...(this.localData as Record<string, unknown>) } as Record<string, unknown>;
        delete rest["logo"];
        delete rest["banner"];

        const dataToSave = {
          ...rest,
          descripcion: this.localData.descripcion || null,
          contacto_email: this.localData.contacto_email || null,
          localidad: this.localData.localidad || null,
        };
        this.$emit("save", dataToSave, this.handleSaveResult);
      }
    },

    handleSaveResult(success: boolean, errorMessage?: string) {
      this.saving = false;
      if (!success && errorMessage) {
        this.errorMessage = errorMessage;
      }
    },
  },
});
</script>
