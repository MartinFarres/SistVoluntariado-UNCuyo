<template>
  <div class="d-flex flex-column align-items-center justify-content-center vh-100 text-center bg-light px-3">
    <div class="mb-4">
      <i class="bi bi-wifi-off error-icon" style="font-size: 5rem;"></i>
    </div>

    <h2 class="fw-bold mb-3 error-title">Ups... algo salió mal 😔</h2>

    <p class="text-muted mb-4" style="max-width: 480px;">
      No pudimos conectar con el servidor o se produjo un error inesperado.
      Por favor, verificá tu conexión o intentá nuevamente en unos momentos.
    </p>

    <div class="d-flex gap-3">
      <button class="btn btn-primary themed-primary" @click="recargar">
        <i class="bi bi-arrow-clockwise me-2"></i> Reintentar
      </button>

      <button class="btn btn-outline-secondary themed-outline" @click="volverInicio">
        <i class="bi bi-house-door me-2"></i> Ir al inicio
      </button>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: "ErrorPage",
  methods: {
    recargar() {
      // Prefer navigating back to the previous page first. If that doesn't leave
      // the error view within a short timeout, fallback to reloading the page.
      try {
        if (this.$router && typeof this.$router.back === 'function') {
          this.$router.back()
          setTimeout(() => {
            // If we're still on the error route, reload as a fallback
            if (this.$route && this.$route.name === 'ErrorPage') {
              window.location.reload()
            }
          }, 700)
          return
        }
      } catch (e) {
        // ignore and fallback
      }

      // If router.back isn't available, try history.back(). If that doesn't
      // navigate away quickly, reload as a final fallback.
      if (window.history.length > 1) {
        window.history.back()
        setTimeout(() => window.location.reload(), 700)
      } else {
        window.location.reload()
      }
    },
    volverInicio() {
      this.$router.push("/")
    }
  }
}
</script>

<style scoped>
.vh-100 {
  height: 100vh;
}
.bi {
  animation: float 3s ease-in-out infinite;
}

/* Theme-based styling using CSS variables from src/styles/theme.css */
.error-icon {
  color: var(--brand-heart);
}

.error-title {
  color: var(--brand-mid);
}

.themed-primary {
  background: linear-gradient(90deg, var(--brand-start), var(--brand-end));
  border: none;
  box-shadow: 0 4px 10px var(--brand-accent-shadow);
}

.themed-outline {
  border-color: var(--brand-mid);
  color: var(--brand-mid);
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>
