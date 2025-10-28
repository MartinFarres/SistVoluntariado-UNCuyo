<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/components/admin/UserModal.vue -->
<template>
  <div class="modal fade" :class="{ show: show, 'd-block': show }" tabindex="-1" v-if="show">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ isEdit ? "Editar Usuario" : "Crear Nuevo Usuario" }}</h5>
          <button type="button" class="btn-close" @click="handleClose"></button>
        </div>
        <div class="modal-body">
          <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
            {{ errorMessage }}
            <button type="button" class="btn-close" @click="errorMessage = null"></button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label class="form-label">Email *</label>
              <input type="email" class="form-control" v-model="localData.email" required />
            </div>
            <div class="mb-3">
              <label class="form-label">
                Contraseña {{ isEdit ? "(dejar en blanco para mantener la actual)" : "*" }}
              </label>
              <input
                type="password"
                class="form-control"
                v-model="localData.password"
                :required="!isEdit"
                minlength="8"
                @input="checkPasswordStrength"
              />
              <small class="text-muted">Mínimo 8 caracteres</small>
              <div v-if="localData.password">
                <div class="progress mt-2" style="height: 6px">
                  <div
                    class="progress-bar"
                    :class="passwordStrengthClass"
                    :style="{ width: passwordStrength + '%' }"
                  ></div>
                </div>
                <small :class="passwordStrengthClassText">{{ passwordStrengthLabel }}</small>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Repetir contraseña *</label>
              <input
                type="password"
                class="form-control"
                v-model="repeatPassword"
                :required="!isEdit"
              />
              <small
                v-if="repeatPassword && localData.password !== repeatPassword"
                class="text-danger"
                >Las contraseñas no coinciden</small
              >
            </div>
            <div v-if="!isEdit" class="mb-3">
              <label class="form-label">Rol *</label>
              <select class="form-control" v-model="localData.role" required>
                <option value="VOL">Voluntario</option>
                <option value="DELEG">Delegado</option>
                <option value="ADMIN">Administrativo</option>
              </select>
            </div>
            <div v-if="localData.role === 'DELEG'" class="mb-3">
              <label class="form-label">Organización asociada *</label>
              <select class="form-select" v-model.number="localData.delegado_organizacion" required>
                <option :value="null">-- Seleccionar organización --</option>
                <option v-for="org in organizations" :key="org.id" :value="org.id">
                  {{ org.nombre }}
                </option>
              </select>
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
              {{ isEdit ? "Actualizar" : "Crear" }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" v-if="show"></div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";
import { organizacionAPI } from "@/services/api";

export default defineComponent({
  name: "UserModal",
  props: {
    show: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    userData: {
      type: Object as PropType<any>,
      required: true,
    },
  },
  emits: ["close", "save"],
  data() {
    return {
      localData: { ...this.userData },
      organizations: [] as Array<{ id: number; nombre: string }>,
      repeatPassword: "",
      passwordStrength: 0,
      passwordStrengthLabel: "",
      passwordStrengthClass: "",
      passwordStrengthClassText: "",
      saving: false,
      errorMessage: null as string | null,
    };
  },
  watch: {
    userData: {
      handler(newVal) {
        this.localData = { ...newVal };
      },
      deep: true,
    },
    show(newVal) {
      if (newVal) {
        this.errorMessage = null;
        this.saving = false;
        // Fetch organizations so the select is ready if role=DELEG
        this.fetchOrganizations();
      }
    },
  },
  methods: {
    async fetchOrganizations() {
      try {
        const resp = await organizacionAPI.getAll();
        this.organizations = resp.data || [];
      } catch (e) {
        // ignore errors, dropdown will be empty
        this.organizations = [];
      }
    },
    handleClose() {
      this.errorMessage = null;
      this.$emit("close");
    },
    handleSubmit() {
      this.errorMessage = null;
      if (!this.isEdit && this.localData.password !== this.repeatPassword) {
        this.errorMessage = "Las contraseñas no coinciden.";
        return;
      }
      // If the user is a Delegado, ensure an organization is selected (create or edit)
      if (this.localData.role === "DELEG") {
        const orgId = this.localData.delegado_organizacion;
        if (!orgId || orgId === null) {
          this.errorMessage = "Debe seleccionar una organización para el Delegado.";
          return;
        }
      }
      this.saving = true;
      this.$emit("save", this.localData, this.handleSaveResult);
    },
    handleSaveResult(success: boolean, errorMessage?: string) {
      this.saving = false;
      if (!success && errorMessage) {
        this.errorMessage = errorMessage;
      }
    },
    checkPasswordStrength() {
      const pwd = this.localData.password || "";
      let score = 0;
      if (pwd.length >= 8) score += 1;
      if (/[A-Z]/.test(pwd)) score += 1;
      if (/[a-z]/.test(pwd)) score += 1;
      if (/[0-9]/.test(pwd)) score += 1;
      if (/[^A-Za-z0-9]/.test(pwd)) score += 1;
      this.passwordStrength = score * 20;
      if (score <= 2) {
        this.passwordStrengthLabel = "Débil";
        this.passwordStrengthClass = "bg-danger";
        this.passwordStrengthClassText = "text-danger";
      } else if (score === 3 || score === 4) {
        this.passwordStrengthLabel = "Media";
        this.passwordStrengthClass = "bg-warning";
        this.passwordStrengthClassText = "text-warning";
      } else {
        this.passwordStrengthLabel = "Fuerte";
        this.passwordStrengthClass = "bg-success";
        this.passwordStrengthClassText = "text-success";
      }
    },
  },
});
</script>

<style scoped>
.modal.show {
  background: rgba(0, 0, 0, 0.5);
}
</style>
