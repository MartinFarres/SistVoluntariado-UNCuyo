<!-- src/components/landing/OrganizationsSection.vue -->
<template>
  <section class="organizations-section">
    <div class="container">
      <h2 class="section-title text-center mb-3">{{ title }}</h2>
      <p class="section-subtitle text-center mb-5">{{ subtitle }}</p>

      <div class="organization-grid">
        <div
          v-for="(org, index) in organizations"
          :key="index"
          class="organization-card"
          @click="navigateToOrg(org.id)"
        >
          <div class="org-card-content">
            <div class="org-icon">
              <i class="bi bi-building"></i>
            </div>
            <h5 class="org-name">{{ org.name }}</h5>
            <div class="org-arrow">
              <i class="bi bi-arrow-right-circle"></i>
            </div>
          </div>
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
  id?: number;
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
  methods: {
    navigateToOrg(id?: number) {
      if (id) {
        this.$router.push(`/organizaciones/${id}`);
      }
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

.organization-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.organization-card {
  background: white;
  border-radius: 12px;
  padding: 2rem 1.5rem;
  border: 2px solid #e9ecef;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.organization-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--brand-start), var(--brand-accent));
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.organization-card:hover::before {
  transform: scaleX(1);
}

.organization-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: var(--brand-accent);
}

.org-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.org-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--brand-start), var(--brand-accent));
  border-radius: 50%;
  color: white;
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.organization-card:hover .org-icon {
  transform: scale(1.1) rotate(5deg);
}

.org-name {
  font-weight: 600;
  color: #343a40;
  text-align: center;
  margin: 0;
  font-size: 1.1rem;
  line-height: 1.4;
  min-height: 2.8rem;
  display: flex;
  align-items: center;
}

.org-arrow {
  color: var(--brand-accent);
  font-size: 1.5rem;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.organization-card:hover .org-arrow {
  opacity: 1;
  transform: translateX(0);
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

@media (max-width: 768px) {
  .organization-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .organization-card {
    padding: 1.5rem 1rem;
  }

  .org-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }

  .org-name {
    font-size: 1rem;
  }
}
</style>
