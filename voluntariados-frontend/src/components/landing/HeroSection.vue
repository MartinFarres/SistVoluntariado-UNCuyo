<!-- src/components/landing/HeroSection.vue -->
<template>
  <section class="hero-section">
    <div class="hero-overlay"></div>
    <div class="container hero-content">
      <div class="row align-items-center min-vh-100">
        <div class="col-lg-8 mx-auto text-center">
          <h1 class="hero-title mb-4 animate-fade-in">
            {{ title }}
          </h1>
          <p class="hero-subtitle mb-5 animate-fade-in-delay">
            {{ subtitle }}
          </p>
          <div class="hero-actions animate-fade-in-delay-2">
            <router-link
              v-if="!isAuthenticated"
              to="/signup"
              class="btn btn-primary btn-lg me-3 mb-3"
            >
              <i class="bi bi-person-plus me-2"></i>
              {{ primaryButtonText }}
            </router-link>
            <router-link to="/voluntariados" class="btn btn-outline-light btn-lg mb-3">
              <i class="bi bi-search me-2"></i>
              {{ secondaryButtonText }}
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Scroll indicator -->
    <div class="scroll-indicator">
      <i class="bi bi-chevron-down"></i>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import authService from "@/services/authService";

export default defineComponent({
  name: "HeroSection",
  data() {
    return {
      isAuthenticated: false,
    };
  },
  props: {
    title: {
      type: String,
      default: "Convertite en el cambio que querés ver.",
    },
    subtitle: {
      type: String,
      default: "¡Sumáte a los voluntariados!",
    },
    primaryButtonText: {
      type: String,
      default: "Registrarme",
    },
    secondaryButtonText: {
      type: String,
      default: "Explorar Voluntariados",
    },
    backgroundImage: {
      type: String,
      default: "",
    },
  },
  mounted() {
    this.isAuthenticated = authService.isAuthenticated();
  },
});
</script>

<style scoped>
.hero-section {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--brand-start) 0%, var(--brand-end) 100%);
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120"><path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" fill="%23fff"/><path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" fill="%23fff"/><path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" fill="%23fff"/></svg>')
    no-repeat bottom;
  background-size: cover;
  opacity: 0.1;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  color: white;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  text-shadow: 2px 4px 8px rgba(0, 0, 0, 0.3);
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 300;
  text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-primary {
  background: white;
  color: var(--brand-accent);
  border: none;
  padding: 1rem 2.5rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  background: #f8f9fa;
  color: var(--brand-accent);
}

.btn-outline-light {
  border: 2px solid white;
  color: white;
  padding: 1rem 2.5rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background: white;
  color: var(--brand-accent);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  animation: bounce 2s infinite;
  color: white;
  font-size: 2rem;
  opacity: 0.7;
}

/* Animations */
@keyframes bounce {
  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateX(-50%) translateY(0);
  }
  40% {
    transform: translateX(-50%) translateY(-10px);
  }
  60% {
    transform: translateX(-50%) translateY(-5px);
  }
}

.animate-fade-in {
  animation: fadeIn 1s ease-in;
}

.animate-fade-in-delay {
  animation: fadeIn 1s ease-in 0.3s backwards;
}

.animate-fade-in-delay-2 {
  animation: fadeIn 1s ease-in 0.6s backwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .btn-lg {
    padding: 0.875rem 2rem;
    font-size: 1rem;
  }
}
</style>
