<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- src/views/SignUp.vue -->
<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-7 col-md-9">
          <div class="card auth-card border-0 shadow-lg">
            <div class="card-header bg-transparent text-center pb-3">
              <div class="text-center mt-4 mb-3">
                <i class="bi bi-heart-fill text-danger" style="font-size: 3rem"></i>
              </div>
              <h2 class="mb-0 auth-heading">Crear Cuenta</h2>
            </div>
            <div class="card-body px-5 py-4">
              <!-- Error Alert -->
              <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
                <button type="button" class="btn-close" @click="error = null"></button>
              </div>

              <form @submit.prevent="handleRegister">
                <div class="form-group mb-3">
                  <label class="form-label">Email</label>
                  <div class="input-group input-group-merge">
                    <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                    <input
                      type="email"
                      class="form-control"
                      placeholder="nombre@ejemplo.com"
                      v-model="formData.email"
                      required
                      :disabled="loading"
                    />
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label class="form-label">Contraseña</label>
                      <div class="input-group input-group-merge">
                        <span class="input-group-text">
                          <i class="bi bi-lock"></i>
                        </span>
                        <input
                          :type="showPassword ? 'text' : 'password'"
                          class="form-control"
                          placeholder="Contraseña"
                          v-model="formData.password"
                          required
                          minlength="8"
                          :disabled="loading"
                          @input="validatePassword"
                        />
                      </div>
                      <small class="text-muted">Mínimo 8 caracteres</small>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label class="form-label">Confirmar Contraseña</label>
                      <div class="input-group input-group-merge">
                        <span class="input-group-text">
                          <i class="bi bi-lock-fill"></i>
                        </span>
                        <input
                          :type="showPassword ? 'text' : 'password'"
                          class="form-control"
                          placeholder="Contraseña"
                          v-model="confirmPassword"
                          required
                          :disabled="loading"
                          @input="validatePassword"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div class="form-check mb-3 small">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    @click="showPassword = !showPassword"
                    :disabled="loading"
                    id="showPwd"
                  />
                  <label class="form-check-label" for="showPwd">Mostrar contraseña</label>
                </div>

                <!-- Password strength indicator -->
                <div v-if="formData.password" class="mb-3">
                  <small class="text-muted">Seguridad de contraseña</small>
                  <div class="progress" style="height: 5px">
                    <div
                      class="progress-bar"
                      :class="passwordStrengthClass"
                      :style="{ width: passwordStrength + '%' }"
                    ></div>
                  </div>
                  <small :class="passwordStrengthTextClass">{{ passwordStrengthText }}</small>
                </div>

                <!-- Password match indicator -->
                <div v-if="confirmPassword" class="mb-3">
                  <small :class="passwordsMatch ? 'text-success' : 'text-danger'">
                    <i
                      class="bi"
                      :class="passwordsMatch ? 'bi-check-circle-fill' : 'bi-x-circle-fill'"
                    ></i>
                    {{
                      passwordsMatch ? "Las contraseñas coinciden" : "Las contraseñas no coinciden"
                    }}
                  </small>
                </div>

                <div class="form-group mb-3">
                  <div class="text-center">
                    <button
                      type="submit"
                      class="btn btn-primary w-100"
                      :disabled="loading || !passwordsMatch"
                    >
                      <span v-if="loading">
                        <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                        Creando cuenta...
                      </span>
                      <span v-else>
                        <i class="bi bi-person-plus me-2"></i>
                        Crear Cuenta
                      </span>
                    </button>
                  </div>
                </div>
              </form>
            </div>
            <div class="card-footer bg-transparent">
              <div class="text-center">
                <small class="text-muted">
                  ¿Ya tienes una cuenta?
                  <router-link to="/signin" class="text-primary fw-bold">Inicia Sesión</router-link>
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AuthService from "@/services/authService";

export default defineComponent({
  name: "SignUp",
  data() {
    return {
      formData: {
        email: "",
        password: "",
        role: "VOL" as "VOL" | "DELEG",
      },
      confirmPassword: "",
      showPassword: false,
      loading: false,
      error: null as string | null,
    };
  },
  computed: {
    passwordsMatch(): boolean {
      if (!this.confirmPassword) return false;
      return this.formData.password === this.confirmPassword;
    },
    passwordStrength(): number {
      const password = this.formData.password;
      if (!password) return 0;
      let strength = 0;
      if (password.length >= 8) strength += 25;
      if (password.length >= 12) strength += 25;
      if (/[a-z]/.test(password)) strength += 12.5;
      if (/[A-Z]/.test(password)) strength += 12.5;
      if (/[0-9]/.test(password)) strength += 12.5;
      if (/[^a-zA-Z0-9]/.test(password)) strength += 12.5;
      return Math.min(strength, 100);
    },
    passwordStrengthText(): string {
      const s = this.passwordStrength;
      if (s === 0) return "";
      if (s < 40) return "Débil";
      if (s < 70) return "Media";
      return "Fuerte";
    },
    passwordStrengthClass(): string {
      const s = this.passwordStrength;
      if (s < 40) return "bg-danger";
      if (s < 70) return "bg-warning";
      return "bg-success";
    },
    passwordStrengthTextClass(): string {
      const s = this.passwordStrength;
      if (s < 40) return "text-danger";
      if (s < 70) return "text-warning";
      return "text-success";
    },
  },
  mounted() {
    if (AuthService.isAuthenticated()) {
      this.$router.push("/admin/dashboard");
    }
  },
  methods: {
    validatePassword() {
      // Trigger computed updates
    },
    async handleRegister() {
      this.error = null;
      if (!this.passwordsMatch) {
        this.error = "Las contraseñas no coinciden";
        return;
      }
      // Terms removed – no validation needed
      this.loading = true;
      try {
        await AuthService.register(this.formData);
        await AuthService.login({
          email: this.formData.email,
          password: this.formData.password,
        });
        this.$router.push("/setup");
      } catch (err: any) {
        this.error = err.message || "Error al registrarse. Intenta nuevamente.";
      } finally {
        this.loading = false;
      }
    },
  },
});
</script>

<style scoped>
/* SignUp relies on shared auth.css & theme.css */
</style>
