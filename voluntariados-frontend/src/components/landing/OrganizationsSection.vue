<!-- src/components/landing/OrganizationsSection.vue -->
<template>
  <section class="organizations-section">
    <div class="container">
      <h2 class="section-title text-center mb-3">{{ title }}</h2>
      <p class="section-subtitle text-center mb-5">{{ subtitle }}</p>

      <div class="organization-logos">
        <div
          v-for="(org, index) in organizations"
          :key="index"
          class="organization-logo"
          :title="org.name"
        >
          {{ org.name }}
        </div>
      </div>
      <div class="text-center mt-5">
        <router-link to="/organizaciones" class="btn btn-primary btn-lg">
          Ver todas las organizaciones
          <i class="bi bi-arrow-right ms-2"></i>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

interface Organization {
  name: string;
}

export default defineComponent({
  name: "OrganizationsSection",
  props: {
    title: {
      type: String,
      default: "Organizaciones Aliadas",
    },
    subtitle: {
      type: String,
      default: "Conocé las organizaciones con las que trabajamos para generar un impacto positivo.",
    },
    organizations: {
      type: Array as PropType<Organization[]>,
      default: () => [],
    },
  },
});
</script>

<style scoped>
.organizations-section {
  padding: 4rem 0;
  background-color: #f8f9fa;
}

.section-title {
  font-weight: 700;
  color: #343a40;
}

.section-subtitle {
  color: #6c757d;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.organization-logos {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 2rem;
}

.organization-logo {
  font-size: 1.2rem;
  font-weight: 600;
  color: #495057;
  padding: 1rem 1.5rem;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background-color: white;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
}

.organization-logo:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border-color: var(--brand-accent);
  color: var(--brand-accent);
}

.btn-primary {
  background-color: var(--brand-start);
  border-color: var(--brand-start);
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: var(--brand-accent);
  border-color: var(--brand-accent);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
</style>
