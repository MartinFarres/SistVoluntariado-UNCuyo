<!-- ProfileView.vue -->
<script lang="ts">
import { defineComponent } from "vue";
import AppNavBar from "@/components/Navbar.vue";
import { userAPI, personaAPI, facultadAPI, ubicacionAPI } from "@/services/api";
import authService from "@/services/authService";

interface User {
  id: number;
  email: string;
  role: "VOL" | "DELEG" | "ADMIN";
  is_active: boolean;
  persona: number | null;
}

interface Localidad {
  id: number;
  nombre: string;
  departamento?: {
    id: number;
    nombre: string;
    provincia?: {
      id: number;
      nombre: string;
      pais?: { id: number; nombre: string };
    };
  };
}

interface PersonaBase {
  id: number;
  nombre: string;
  apellido: string;
  dni: string;
  fecha_nacimiento: string;
  telefono: string;
  email: string;
  direccion: string;
  localidad: number | Localidad;
}

interface Voluntario extends PersonaBase {
  carrera?: number | { id: number; nombre: string };
  interno: boolean;
}

interface Delegado extends PersonaBase {
  organizacion?: number | { id: number; nombre: string };
}

interface Administrador extends PersonaBase {
  // Admins have the base persona fields only
}

export default defineComponent({
  name: "ProfileView",
  components: {
    AppNavBar,
  },
  data() {
    return {
      loading: true,
      error: null as string | null,
      user: null as User | null,
      persona: null as Voluntario | Delegado | Administrador | null,
      localidades: [] as Localidad[],
      carreras: [] as Array<{ id: number; nombre: string }>,
      organizaciones: [] as Array<{ id: number; nombre: string }>,
      editMode: false,
      saving: false,
      editForm: {
        nombre: "",
        apellido: "",
        dni: "",
        fecha_nacimiento: "",
        telefono: "",
        direccion: "",
        localidad: null as number | null,
        carrera: null as number | null,
        interno: false,
      },
      errors: {} as Record<string, string>,
    };
  },
  computed: {
    roleDisplay(): string {
      const roles: Record<string, string> = {
        ADMIN: "Administrador",
        DELEG: "Delegado",
        VOL: "Voluntario",
      };
      return this.user ? (roles[this.user.role] || "") : "";
    },
    isVoluntario(): boolean {
      return this.user?.role === "VOL";
    },
    isDelegado(): boolean {
      return this.user?.role === "DELEG";
    },
    isAdmin(): boolean {
      return this.user?.role === "ADMIN";
    },
    fullName(): string {
      return this.persona
        ? `${this.persona.nombre} ${this.persona.apellido}`
        : "";
    },
    locationName(): string {
      if (!this.persona) return "";
      
      const localidad = this.localidades.find(
        (l) => l.id === (typeof this.persona!.localidad === 'number' ? this.persona!.localidad : this.persona!.localidad.id)
      );
      
      if (localidad) {
        return this.getCompleteLocationName(localidad);
      }
      
      return "";
    },
    carreraName(): string {
      if (!this.isVoluntario || !this.persona) return "";
      const voluntario = this.persona as Voluntario;
      
      if (!voluntario.carrera) return "No especificada";
      
      if (typeof voluntario.carrera === 'number') {
        const carrera = this.carreras.find(c => c.id === voluntario.carrera);
        return carrera?.nombre || "No especificada";
      }
      
      return voluntario.carrera.nombre || "No especificada";
    },
    organizacionName(): string {
      if (!this.isDelegado || !this.persona) return "";
      const delegado = this.persona as Delegado;
      
      if (!delegado.organizacion) return "No especificada";
      
      if (typeof delegado.organizacion === 'number') {
        const org = this.organizaciones.find(o => o.id === delegado.organizacion);
        return org?.nombre || "No especificada";
      }
      
      return delegado.organizacion.nombre || "No especificada";
    },
    age(): number | null {
      if (!this.persona?.fecha_nacimiento) return null;
      
      const birthDate = new Date(this.persona.fecha_nacimiento);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      
      return age;
    },
  },
  async mounted() {
    await this.loadProfileData();
  },
  methods: {
    async loadProfileData() {
      this.loading = true;
      this.error = null;

      try {
        // Get current user
        this.user = await authService.getCurrentUser();

        if (!this.user.persona) {
          this.error = "No hay información de persona asociada";
          return;
        }

        // Load auxiliary data
        await Promise.all([
          this.loadLocalidades(),
          this.loadCarreras(),
          this.loadOrganizaciones(),
        ]);

        // Load persona data based on role
        if (this.user.role === "VOL") {
          const response = await personaAPI.getVoluntarioById(this.user.persona);
          this.persona = response.data;
        } else if (this.user.role === "DELEG") {
          const response = await personaAPI.getDelegadoById(this.user.persona);
          this.persona = response.data;
        } else if (this.user.role === "ADMIN") {
          const response = await personaAPI.getAdministradorById(this.user.persona);
          this.persona = response.data;
        }

        // Initialize edit form with current data
        this.initializeEditForm();
      } catch (err: any) {
        console.error("Error loading profile:", err);
        this.error =
          err.response?.data?.detail || "Error al cargar el perfil";
      } finally {
        this.loading = false;
      }
    },

    initializeEditForm() {
      if (!this.persona) return;

      this.editForm.nombre = this.persona.nombre;
      this.editForm.apellido = this.persona.apellido;
      this.editForm.dni = this.persona.dni;
      this.editForm.fecha_nacimiento = this.persona.fecha_nacimiento;
      this.editForm.telefono = this.persona.telefono;
      this.editForm.direccion = this.persona.direccion;
      this.editForm.localidad = typeof this.persona.localidad === 'number' 
        ? this.persona.localidad 
        : this.persona.localidad.id;

      if (this.isVoluntario && this.persona) {
        const voluntario = this.persona as Voluntario;
        this.editForm.carrera = typeof voluntario.carrera === 'number'
          ? voluntario.carrera
          : voluntario.carrera?.id || null;
        this.editForm.interno = voluntario.interno;
      }
    },

    enableEditMode() {
      this.editMode = true;
      this.initializeEditForm();
    },

    cancelEdit() {
      this.editMode = false;
      this.errors = {};
      this.initializeEditForm();
    },

    async saveProfile() {
      this.saving = true;
      this.errors = {};

      try {
        const dataToUpdate: any = {
          nombre: this.editForm.nombre,
          apellido: this.editForm.apellido,
          dni: this.editForm.dni,
          fecha_nacimiento: this.editForm.fecha_nacimiento,
          telefono: this.editForm.telefono,
          direccion: this.editForm.direccion,
          localidad: this.editForm.localidad,
        };

        // Add role-specific fields
        if (this.isVoluntario) {
          dataToUpdate.carrera = this.editForm.carrera;
          dataToUpdate.interno = this.editForm.interno;
        }

        // Update based on role
        if (this.user?.role === "VOL" && this.user.persona) {
          await personaAPI.updateVoluntario(this.user.persona, dataToUpdate);
        } else if (this.user?.role === "DELEG" && this.user.persona) {
          await personaAPI.updateDelegado(this.user.persona, dataToUpdate);
        } else if (this.user?.role === "ADMIN" && this.user.persona) {
          await personaAPI.updateAdministrador(this.user.persona, dataToUpdate);
        }

        // Reload profile data
        await this.loadProfileData();
        
        this.editMode = false;
      } catch (err: any) {
        console.error("Error updating profile:", err);
        
        if (err.response?.data) {
          const errorData = err.response.data;
          
          // Handle field-specific errors
          if (typeof errorData === "object" && !errorData.detail) {
            this.errors = {};
            Object.keys(errorData).forEach((field) => {
              if (Array.isArray(errorData[field])) {
                this.errors[field] = errorData[field][0];
              }
            });
          } else {
            this.error = errorData.detail || "Error al actualizar el perfil";
          }
        } else {
          this.error = "Error al actualizar el perfil";
        }
      } finally {
        this.saving = false;
      }
    },

    async loadLocalidades() {
      try {
        const [locRes, depRes, provRes, paisRes] = await Promise.all([
          ubicacionAPI.getLocalidades(),
          ubicacionAPI.getDepartamentos(),
          ubicacionAPI.getProvincias(),
          ubicacionAPI.getPaises(),
        ]);

        const paises = paisRes.data;
        const provincias = provRes.data;
        const departamentos = depRes.data;
        const localidades = locRes.data;

        this.localidades = localidades.map((localidad: any) => {
          const departamento = departamentos.find(
            (d: any) => d.id === localidad.departamento
          );
          if (departamento) {
            const provincia = provincias.find(
              (p: any) => p.id === departamento.provincia
            );
            if (provincia) {
              const pais = paises.find((pa: any) => pa.id === provincia.pais);
              departamento.provincia = { ...provincia, pais };
            }
            localidad.departamento = departamento;
          }
          return localidad;
        });
      } catch (error) {
        console.error("Error loading localidades:", error);
      }
    },

    async loadCarreras() {
      try {
        const res = await facultadAPI.getCarreras();
        this.carreras = res.data;
      } catch (error) {
        console.error("Error loading carreras:", error);
      }
    },

    async loadOrganizaciones() {
      try {
        const { organizacionAPI } = await import("@/services/api");
        const res = await organizacionAPI.getAll();
        this.organizaciones = res.data;
      } catch (error) {
        console.error("Error loading organizaciones:", error);
      }
    },

    getCompleteLocationName(localidad: Localidad): string {
      const parts = [localidad.nombre];

      if (localidad.departamento) {
        parts.push(localidad.departamento.nombre);

        if (localidad.departamento.provincia) {
          parts.push(localidad.departamento.provincia.nombre);

          if (localidad.departamento.provincia.pais) {
            parts.push(localidad.departamento.provincia.pais.nombre);
          }
        }
      }

      return parts.join(", ");
    },

    formatDate(dateString: string): string {
      const date = new Date(dateString);
      return date.toLocaleDateString("es-AR", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
  },
});
</script>

<template>
  <div class="profile">
    <AppNavBar />

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mt-5">
      <div class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
      </div>
    </div>

    <!-- Profile Content -->
    <div v-else-if="persona" class="profile-content">
      <!-- Hero Section -->
      <section class="profile-hero">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-md-3 text-center">
              <div class="profile-avatar">
                <i class="bi bi-person-circle"></i>
              </div>
            </div>
            <div class="col-md-9">
              <div class="d-flex justify-content-between align-items-start flex-wrap">
                <div>
                  <h1 class="profile-name">{{ fullName }}</h1>
                  <p class="profile-role">
                    <i class="bi bi-award me-2"></i>
                    {{ roleDisplay }}
                  </p>
                  <p class="profile-email">
                    <i class="bi bi-envelope me-2"></i>
                    {{ persona.email }}
                  </p>
                </div>
                <div class="mt-3 mt-md-0">
                  <button
                    v-if="!editMode"
                    @click="enableEditMode"
                    class="btn btn-light btn-lg"
                  >
                    <i class="bi bi-pencil-square me-2"></i>
                    Editar Perfil
                  </button>
                  <div v-else class="d-flex gap-2">
                    <button
                      @click="saveProfile"
                      :disabled="saving"
                      class="btn btn-success btn-lg"
                    >
                      <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                      <i v-else class="bi bi-check-circle me-2"></i>
                      {{ saving ? 'Guardando...' : 'Guardar' }}
                    </button>
                    <button
                      @click="cancelEdit"
                      :disabled="saving"
                      class="btn btn-light btn-lg"
                    >
                      <i class="bi bi-x-circle me-2"></i>
                      Cancelar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Profile Details -->
      <section class="profile-details py-5">
        <div class="container">
          <h2 class="section-title text-center mb-5">
            {{ editMode ? 'Editar Información Personal' : 'Información Personal' }}
          </h2>

          <!-- View Mode -->
          <div v-if="!editMode" class="row g-4">
            <!-- Personal Information Card -->
            <div class="col-lg-6">
              <div class="info-card">
                <div class="info-card-header">
                  <i class="bi bi-person-lines-fill me-2"></i>
                  <h3>Datos Personales</h3>
                </div>
                <div class="info-card-body">
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-card-text me-2"></i>
                      DNI:
                    </span>
                    <span class="info-value">{{ persona.dni }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-calendar-event me-2"></i>
                      Fecha de Nacimiento:
                    </span>
                    <span class="info-value">{{ formatDate(persona.fecha_nacimiento) }}</span>
                  </div>
                  <div v-if="age" class="info-item">
                    <span class="info-label">
                      <i class="bi bi-hourglass-split me-2"></i>
                      Edad:
                    </span>
                    <span class="info-value">{{ age }} años</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-telephone me-2"></i>
                      Teléfono:
                    </span>
                    <span class="info-value">{{ persona.telefono }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Contact & Location Card -->
            <div class="col-lg-6">
              <div class="info-card">
                <div class="info-card-header">
                  <i class="bi bi-geo-alt-fill me-2"></i>
                  <h3>Ubicación</h3>
                </div>
                <div class="info-card-body">
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-house-door me-2"></i>
                      Dirección:
                    </span>
                    <span class="info-value">{{ persona.direccion }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-pin-map me-2"></i>
                      Localidad:
                    </span>
                    <span class="info-value">{{ locationName }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Role-Specific Information -->
            <!-- Voluntario Card -->
            <div v-if="isVoluntario" class="col-lg-12">
              <div class="info-card special-card">
                <div class="info-card-header">
                  <i class="bi bi-mortarboard-fill me-2"></i>
                  <h3>Información de Voluntario</h3>
                </div>
                <div class="info-card-body">
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-book me-2"></i>
                      Carrera:
                    </span>
                    <span class="info-value">{{ carreraName }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-building me-2"></i>
                      Tipo:
                    </span>
                    <span class="info-value">
                      {{ (persona as Voluntario).interno ? 'Voluntario Interno' : 'Voluntario Externo' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Delegado Card -->
            <div v-if="isDelegado" class="col-lg-12">
              <div class="info-card special-card">
                <div class="info-card-header">
                  <i class="bi bi-briefcase-fill me-2"></i>
                  <h3>Información de Delegado</h3>
                </div>
                <div class="info-card-body">
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-building me-2"></i>
                      Organización:
                    </span>
                    <span class="info-value">{{ organizacionName }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Admin Card -->
            <div v-if="isAdmin" class="col-lg-12">
              <div class="info-card special-card admin-card">
                <div class="info-card-header">
                  <i class="bi bi-shield-fill-check me-2"></i>
                  <h3>Información de Administrador</h3>
                </div>
                <div class="info-card-body">
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-key me-2"></i>
                      Permisos:
                    </span>
                    <span class="info-value">Acceso completo al sistema</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">
                      <i class="bi bi-speedometer2 me-2"></i>
                      Panel:
                    </span>
                    <span class="info-value">
                      <router-link to="/admin/dashboard" class="text-decoration-none">
                        Ir al Panel de Administración
                        <i class="bi bi-arrow-right ms-1"></i>
                      </router-link>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Edit Mode -->
          <div v-else class="row g-4">
            <div class="col-12">
              <div class="edit-card">
                <form @submit.prevent="saveProfile">
                  <div class="row g-4">
                    <!-- Personal Information Section -->
                    <div class="col-12">
                      <h4 class="edit-section-title">
                        <i class="bi bi-person-lines-fill me-2"></i>
                        Datos Personales
                      </h4>
                    </div>

                    <div class="col-md-6">
                      <label for="nombre" class="form-label">Nombre *</label>
                      <input
                        type="text"
                        class="form-control"
                        id="nombre"
                        v-model="editForm.nombre"
                        :class="{ 'is-invalid': errors.nombre }"
                        required
                      />
                      <div v-if="errors.nombre" class="invalid-feedback">
                        {{ errors.nombre }}
                      </div>
                    </div>

                    <div class="col-md-6">
                      <label for="apellido" class="form-label">Apellido *</label>
                      <input
                        type="text"
                        class="form-control"
                        id="apellido"
                        v-model="editForm.apellido"
                        :class="{ 'is-invalid': errors.apellido }"
                        required
                      />
                      <div v-if="errors.apellido" class="invalid-feedback">
                        {{ errors.apellido }}
                      </div>
                    </div>

                    <div class="col-md-6">
                      <label for="dni" class="form-label">DNI *</label>
                      <input
                        type="text"
                        class="form-control"
                        id="dni"
                        v-model="editForm.dni"
                        :class="{ 'is-invalid': errors.dni }"
                        required
                      />
                      <div v-if="errors.dni" class="invalid-feedback">
                        {{ errors.dni }}
                      </div>
                    </div>

                    <div class="col-md-6">
                      <label for="fecha_nacimiento" class="form-label">Fecha de Nacimiento *</label>
                      <input
                        type="date"
                        class="form-control"
                        id="fecha_nacimiento"
                        v-model="editForm.fecha_nacimiento"
                        :class="{ 'is-invalid': errors.fecha_nacimiento }"
                        required
                      />
                      <div v-if="errors.fecha_nacimiento" class="invalid-feedback">
                        {{ errors.fecha_nacimiento }}
                      </div>
                    </div>

                    <div class="col-md-6">
                      <label for="telefono" class="form-label">Teléfono *</label>
                      <input
                        type="tel"
                        class="form-control"
                        id="telefono"
                        v-model="editForm.telefono"
                        :class="{ 'is-invalid': errors.telefono }"
                        required
                      />
                      <div v-if="errors.telefono" class="invalid-feedback">
                        {{ errors.telefono }}
                      </div>
                    </div>

                    <!-- Location Section -->
                    <div class="col-12 mt-4">
                      <h4 class="edit-section-title">
                        <i class="bi bi-geo-alt-fill me-2"></i>
                        Ubicación
                      </h4>
                    </div>

                    <div class="col-md-6">
                      <label for="direccion" class="form-label">Dirección *</label>
                      <input
                        type="text"
                        class="form-control"
                        id="direccion"
                        v-model="editForm.direccion"
                        :class="{ 'is-invalid': errors.direccion }"
                        required
                      />
                      <div v-if="errors.direccion" class="invalid-feedback">
                        {{ errors.direccion }}
                      </div>
                    </div>

                    <div class="col-md-6">
                      <label for="localidad" class="form-label">Localidad *</label>
                      <select
                        class="form-select"
                        id="localidad"
                        v-model="editForm.localidad"
                        :class="{ 'is-invalid': errors.localidad }"
                        required
                      >
                        <option value="">Selecciona una localidad</option>
                        <option
                          v-for="localidad in localidades"
                          :key="localidad.id"
                          :value="localidad.id"
                        >
                          {{ getCompleteLocationName(localidad) }}
                        </option>
                      </select>
                      <div v-if="errors.localidad" class="invalid-feedback">
                        {{ errors.localidad }}
                      </div>
                    </div>

                    <!-- Voluntario Specific Fields -->
                    <template v-if="isVoluntario">
                      <div class="col-12 mt-4">
                        <h4 class="edit-section-title">
                          <i class="bi bi-mortarboard-fill me-2"></i>
                          Información de Voluntario
                        </h4>
                      </div>

                      <div class="col-md-6">
                        <label for="carrera" class="form-label">Carrera</label>
                        <select
                          class="form-select"
                          id="carrera"
                          v-model="editForm.carrera"
                          :class="{ 'is-invalid': errors.carrera }"
                        >
                          <option :value="null">Selecciona una carrera</option>
                          <option
                            v-for="carrera in carreras"
                            :key="carrera.id"
                            :value="carrera.id"
                          >
                            {{ carrera.nombre }}
                          </option>
                        </select>
                        <div v-if="errors.carrera" class="invalid-feedback">
                          {{ errors.carrera }}
                        </div>
                      </div>

                      <div class="col-md-6">
                        <div class="form-check mt-4">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            id="interno"
                            v-model="editForm.interno"
                          />
                          <label class="form-check-label" for="interno">
                            Voluntario interno de la facultad
                          </label>
                        </div>
                      </div>
                    </template>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.profile {
  overflow-x: hidden;
  min-height: 100vh;
  background: #f8f9fa;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 240px;
}

/* Hero Section */
.profile-hero {
  background: linear-gradient(135deg, #8b0000 0%, #dc143c 100%);
  color: white;
  padding: 2rem 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.profile-avatar {
  font-size: 5rem;
  color: white;
  margin-bottom: 0.5rem;
}

.profile-avatar i {
  display: block;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.profile-name {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-role {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0.25rem;
  opacity: 0.95;
}

.profile-email {
  font-size: 0.95rem;
  opacity: 0.9;
  margin-bottom: 0;
}

/* Section Title */
.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  position: relative;
  padding-bottom: 0.5rem;
}

.section-title::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #8b0000, #dc143c);
  border-radius: 2px;
}

/* Reduce vertical padding for details section overriding py-5 */
.profile-details {
  padding-top: 2rem !important;
  padding-bottom: 2rem !important;
}

/* Info Cards */
.info-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  height: 100%;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.info-card-header {
  background: linear-gradient(135deg, #8b0000, #dc143c);
  color: white;
  padding: 1rem;
  display: flex;
  align-items: center;
}

.info-card-header i {
  font-size: 1.5rem;
}

.info-card-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.info-card-body {
  padding: 1.25rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: start;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e9ecef;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 600;
  color: #495057;
  display: flex;
  align-items: center;
  flex: 0 0 auto;
  margin-right: 1rem;
}

.info-label i {
  color: #dc143c;
}

.info-value {
  color: #6c757d;
  text-align: right;
  flex: 1;
  word-wrap: break-word;
}

/* Special Cards */
.special-card .info-card-header {
  background: linear-gradient(135deg, #0d6efd, #0a58ca);
}

.admin-card .info-card-header {
  background: linear-gradient(135deg, #198754, #146c43);
}

/* Links */
.info-value a {
  color: #dc143c;
  font-weight: 600;
  transition: all 0.2s ease;
}

.info-value a:hover {
  color: #8b0000;
}

/* Edit Card */
.edit-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.edit-section-title {
  color: #dc143c;
  font-weight: 600;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.25rem;
  border-bottom: 2px solid #dc143c;
}

.form-label {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-control,
.form-select {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
  border-color: #8b0000;
  box-shadow: 0 0 0 0.2rem rgba(139, 0, 0, 0.25);
}

.form-check-input:checked {
  background-color: #8b0000;
  border-color: #8b0000;
}

.form-check-input:focus {
  border-color: #8b0000;
  box-shadow: 0 0 0 0.25rem rgba(139, 0, 0, 0.25);
}

.form-check-label {
  font-weight: 500;
  color: #495057;
}

.invalid-feedback {
  display: block;
  font-size: 0.875rem;
  color: #dc3545;
  margin-top: 0.25rem;
}

.form-control.is-invalid,
.form-select.is-invalid {
  border-color: #dc3545;
}

.btn-light {
  background: white;
  border: 2px solid white;
  color: #dc143c;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-light:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
}

.btn-success {
  background: linear-gradient(135deg, #198754, #146c43);
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-success:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(25, 135, 84, 0.3);
}

.btn-success:disabled,
.btn-light:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Make large buttons more compact within this view */
.btn-lg {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .profile-hero {
    padding: 1.5rem 0;
  }

  .profile-avatar {
    font-size: 3.5rem;
  }

  .profile-name {
    font-size: 1.5rem;
  }

  .profile-role {
    font-size: 1rem;
  }

  .profile-email {
    font-size: 0.9rem;
  }

  .section-title {
    font-size: 1.6rem;
  }

  .info-item {
    flex-direction: column;
    align-items: start;
  }

  .info-value {
    text-align: left;
    margin-top: 0.5rem;
  }

  .info-card-header h3 {
    font-size: 1.1rem;
  }
}
</style>
